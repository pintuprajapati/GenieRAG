QnA_prompt = [
    ("system", "You are an helpful assistant for question-answering tasks who understands user question and context and provide response accordingly"),
    ("human", "Use the following pieces of retrieved context to answer the question. \n\
    If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. \n\
    Question: {question} \n\
    Context: {context} \n \
    Answer:")
]