from langchain_openai import ChatOpenAI  #importamos la clase
from langchain.prompts import PromptTemplate
#from langchain.chains import LLMChain

chat = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="Saluda al usuario con su nombre.\nNombre del usuario: {nombre}\nAsistente: "
)


chain = plantilla | chat

resultado = chain.invoke({"nombre":"Fernando"})
print(resultado.content)

