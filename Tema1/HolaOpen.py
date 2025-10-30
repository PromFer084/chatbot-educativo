from langchain_openai import ChatOpenAI  #importamos la clase

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

pregunta = "¿Cuando llego el hombre a la luna?"

print("Pregunta: ", pregunta)

respuesta = llm.invoke(pregunta)

print("Respuesta del modelo: ", respuesta.content)
