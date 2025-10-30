from langchain_google_genai import ChatGoogleGenerativeAI  #importamos la clase

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

pregunta = "¿Cuando llego el hombre a la luna?"

print("Pregunta: ", pregunta)

respuesta = llm.invoke(pregunta)

print("Respuesta del modelo: ", respuesta.content)
