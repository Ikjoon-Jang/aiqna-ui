from rag_query import generate_answer

question = "현재 적용되어 있는 rule을 알려주세요"
answer = generate_answer(question)

print("질문:")
print(question)
print("🧠 GPT 응답:")
print(answer)
