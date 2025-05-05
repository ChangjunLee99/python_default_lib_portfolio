# RAG (Retrieval-Augmented Generation) 애플리케이션

이 애플리케이션은 Flask 기반의 RAG 시스템을 구현한 웹 서비스입니다. 벡터 데이터베이스(ChromaDB)를 활용하여 문서를 저장하고 검색할 수 있는 기능을 제공합니다.

## 주요 기능

### 1. 문서 관리
- **파일 업로드**: 다양한 형식의 문서를 시스템에 업로드할 수 있습니다.
- **PDF 추가**: 로컬 디렉토리에서 PDF 파일을 추가할 수 있습니다.
- **문서 직접 추가**: 텍스트 문서를 직접 시스템에 추가할 수 있습니다.

### 2. 벡터 데이터베이스 관리
- **데이터 검색**: 저장된 문서에서 관련 내용을 검색할 수 있습니다.
- **데이터 삭제**: 특정 ID의 데이터를 삭제할 수 있습니다.
- **전체 데이터 삭제**: 벡터 데이터베이스의 모든 데이터를 삭제할 수 있습니다.

### 3. RAG 검색
- **RAG 기반 검색**: Retrieval-Augmented Generation을 활용한 고급 검색 기능을 제공합니다.

## API 엔드포인트

### POST /api/insertFile
- 파일을 시스템에 업로드합니다.
- **요청 파라미터**:
  - `file`: 업로드할 파일 (multipart/form-data)

### POST /api/searchVDB
- 벡터 데이터베이스에서 검색을 수행합니다.
- **요청 파라미터**:
  - `name`: 검색할 컬렉션 이름
  - `query`: 검색 쿼리
  - `k`: 반환할 결과 수
  - `fetch_k`: 검색할 결과 수

### POST /api/delete_from_VDB
- 벡터 데이터베이스에서 특정 ID의 데이터를 삭제합니다.
- **요청 파라미터**:
  - `name`: 컬렉션 이름
  - `ids`: 삭제할 데이터의 ID 배열

### POST /api/truncateVDB
- 벡터 데이터베이스의 모든 데이터를 삭제합니다.
- **요청 파라미터**:
  - `name`: 삭제할 컬렉션 이름

### POST /api/addPDF
- 로컬 디렉토리에서 PDF 파일을 추가합니다.
- **요청 파라미터**:
  - `name`: 컬렉션 이름
  - `path`: PDF 파일 경로

### POST /api/addDocuments
- 문서를 직접 시스템에 추가합니다.
- **요청 파라미터**:
  - `name`: 컬렉션 이름
  - `documents`: 추가할 문서 배열

### POST /api/searchRAG
- RAG를 사용하여 검색을 수행합니다.
- **요청 파라미터**:
  - `name`: 검색할 컬렉션 이름
  - `query`: 검색 쿼리
  - `k`: 반환할 결과 수
  - `fetch_k`: 검색할 결과 수

## 실행 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 애플리케이션 실행:
```bash
python app.py
```

기본적으로 애플리케이션은 5000번 포트에서 실행됩니다. 포트를 변경하려면 환경 변수 `PORT`를 설정하거나 코드를 수정하세요.

## 환경 설정

- `PORT`: 서버 포트 번호 (기본값: 5000)
- 기타 설정은 `lib/util.py`에서 확인할 수 있습니다.

## 의존성

- Flask
- ChromaDB
- SQLite3
- 기타 필요한 패키지는 `requirements.txt`에 명시되어 있습니다. 