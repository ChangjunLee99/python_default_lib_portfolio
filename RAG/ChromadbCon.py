import sys;from os import path
tt = path.dirname( path.dirname( path.abspath(__file__) ) )
if not tt in sys.path : sys.path.append(tt)

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#import chromadb
#from langchain.vectorstores import Chroma
from RAG.ChromaEx import * # 유사도 확인을 위해 수정
#from langchain_community.embeddings.sentence_transformer import HuggingFaceEmbeddings # SentenceTransformerEmbeddings
from transformers import AutoTokenizer
from langchain_huggingface import HuggingFaceEmbeddings
from lib.util import *

class ChromadbCon:
    def __init__(self, util:Util, sentence_transformer, tokenizer):
        self.m_util : Util = util
        self.DB_PATH = None
        if self.m_util.get("DB_PATH")  != None:
            self.DB_PATH = self.m_util.getValueStr("DB_PATH")
        else:
            self.DB_PATH = self.m_util.getNowDir() + self.m_util.getDirSep() + "DB" 
        self.m_vdb :Chroma= None
        self.m_vdb_dict : dict[str,Chroma] = {}
        self.m_sentence_transformer = sentence_transformer
        self.m_tokenizer = tokenizer

    def makeDB(self,name : str='default'):
        '''DB 생성'''
        return Chroma(
            collection_name = 'name',
            embedding_function=self.m_sentence_transformer,
            persist_directory=self.DB_PATH + self.m_util.getDirSep()+"test",
            collection_metadata = {'hnsw:space': 'cosine'}
        )
    def loadDB(self,name : str='default'):
        '''DB 로드'''
        if name not in self.m_vdb_dict.keys():
            self.m_vdb_dict[name] = self.makeDB(name)
    
    def getDB(self,name : str='default'):
        '''DB 가져오기'''
        if name not in self.m_vdb_dict.keys():
            self.m_vdb_dict[name] = self.makeDB(name)
        return self.m_vdb_dict[name]

    def persist(self,name : str=None):
        '''현재 프로세서가 사용하는 DB 저장'''
        for now_name in self.m_vdb_dict.keys():
            if name != None and now_name != name:
                pass
            else:
                self.m_vdb_dict[now_name].persist()

    def add_texts(self, name,texts,metadatas):
        for i in range(3):  
            try:
                self.m_vdb_dict[name].add_texts(texts,metadatas)
                return True
            except:
                self.m_util.logErr("chromadbCon::add_texts add_texts failed")
        return False
        

    def add_Documents(self, name,documents):
        tlist = []
        metalist = []
        for document in documents: 
            
            tlist.append(document.page_content)
            tokensize = self.getTokenSizeFromST(document.page_content)
            
            if tokensize > self.getMaxTokenSizeFromST():
                self.m_util.logErr("최대 토큰 수 초과, tokenSize:",tokensize)
            metalist.append(document.metadata)
        
        tsize = len(tlist)
        ret = self.add_texts(name,tlist,metalist)
        if ret == False:
            return 0
        self.m_util.logErr("chromadbCon::add_Documents adding document data Done")

        return tsize
    
    def add_PDF_From_Local_Dir(self, name, path):
        '''로컬 경로의 PDF 문서 입력'''
        if self.m_vdb == None:
            self.m_vdb = self.makeDB()
        if self.m_util.isFile(path) != True:
            print(f"add_PDF_From_Local_Dir file doesn't Exist! {path}")
            return
        
        loader = PyMuPDFLoader(path)
        data = loader.load()
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=512,
            #chunk_size=256,
            chunk_overlap=200,
            encoding_name='cl100k_base'
        )
        documents = text_splitter.split_documents(data)
        tlist = []
        metalist = []
        for document in documents: 
            tlist.append(document.page_content)
            tokensize = self.getTokenSizeFromST(document.page_content)
            if tokensize > self.getMaxTokenSizeFromST():
                print("최대 토큰 수 초과, tokenSize:",tokensize)
            metalist.append(document.metadata)
        tsize = len(tlist)
        ret = self.add_texts(name,tlist,metalist)
        if ret == False:
            return 0
        self.m_util.logErr("chromadbCon::add_PDF_From_Local_Dir adding document data Done")
        return tsize
    
    def getMaxTokenSizeFromST(self):
        return 512

    def getTokenSizeFromST(self, sentence):
        '''SBERT에서 제공하는 토큰화를 활용하여 문장의 토큰 기준 크기를 반환함'''
        try:
            input_ids = self.m_tokenizer.encode(sentence)
            tokens = self.m_tokenizer.tokenize(self.m_temp_tokenizer.decode(input_ids))
            return len(tokens)
        except:
            return 0
        
    def query(self, name, query, k : int= 2, fetch_k : int = 10):
        '''DB에서 검색'''
        nowDB = self.getDB(name)
        for i in range(3):
            try:
                res= nowDB.max_marginal_relevance_search(query, k, fetch_k=fetch_k)
                return res
            except:
                self.m_util.logErr("R2_LANGCHAIN_RAG_P::query Error While Searching Failed" + str(i+1))
        return None


    def delete_data(self, name, ids):
        '''데이터 삭제'''
        nowDB = self.getDB(name)
        try:
            nowDB._collection.delete(ids=ids)
            return True
        except Exception as e:
            self.m_util.logErr(f"ChromadbCon::delete_data 오류 발생: {str(e)}")
            return False

    def delete_all_data(self, name):
        '''모든 데이터 삭제'''
        nowDB = self.getDB(name)
        try:
            nowDB._collection.delete()
            return True
        except Exception as e:
            self.m_util.logErr(f"ChromadbCon::delete_all_data 오류 발생: {str(e)}")
            return False

if __name__ == "__main__":
    util = Util()
    util.parsesys()
    temp_Model = HuggingFaceEmbeddings(model_name="jhgan/ko-sroberta-multitask")
    temp_tokenizer = AutoTokenizer.from_pretrained('jhgan/ko-sroberta-multitask')
    con = ChromadbCon(util,temp_Model, temp_tokenizer)