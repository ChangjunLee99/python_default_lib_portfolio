#pip install google-generativeai

import google.generativeai as genai

import pyperclip

GOOGLE_API_KEY=""
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
print(model.count_tokens("why is sky blue?"))
#{query}
# 여러 턴
#문서 이름 : KINX2023036771
#질문에 대한 답변, 탐색 된 문장, 원본 목차 이름, 원본 목차 내용을 자연스러운 하나의 문장으로 순서대로 설명해줘.
try:
    while True:
        query = input("Query: ")
        insertText = f'''너는 레시피 키워드 추출기야. 
        너의 역할은 사용자가 입력한 문장에서 주어진 키워드 리스트 중 가장 어울리는 키워드들을 선택해주는거야.
        키워드와 키워드를 분리하는건 |이 문자로 분리해줘. 해당되는 내용이 없을 경우 빈 문자열을 작성해줘.
        키워드 리스트 안에 있는 문자들 중에서만 골라야해.
        키워드 리스트:"김치","고추","매콤한","고기","돼지고기","소고기","간편한","정성스러운","감자","양배추","치커리"
        질문:"김치에 돼지고기 넣는 음식 이름이 뭐였지?"
        '''
        messages = [{'role':'user', 'parts': [str(insertText)]}]
        response = model.generate_content(messages)
        for i in range(3):
            try:
                text = response.text
                break
            except:
                print(f"error {i}")
        try:
            pyperclip.copy(text)
        except:
            pass
        print(response.text)

except KeyboardInterrupt:
    print("\nExiting...")
# messages.append(response.candidates[0].content)
# messages.append({'role':'user', 'parts': ['초끈이론에 대해서 알려줘']})
# response = model.generate_content(messages)

# response = model.generate_content("중세시대 배경에서 의사의 삶에 대해 작성해줘.")


# 특정 형태 생성
# https://ai.google.dev/gemini-api/docs/api-overview?hl=ko
# model = genai.GenerativeModel('gemini-1.5-flash',
#                               generation_config={"response_mime_type": "application/json"})

# prompt = """
#   List 5 popular cookie recipes.

#   Using this JSON schema:

#     Recipe = {"recipe_name": str}

#   Return a `list[Recipe]`
#   """

# response = model.generate_content(prompt)
# print(response.text)