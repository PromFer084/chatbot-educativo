from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
import streamlit as st #le asignamos un alias es streamlit
from langchain.prompts import PromptTemplate
import streamlit as st


# #Conf la pagina de la app
st.set_page_config(page_title="Chatbot Educativo ", page_icon="🤖") 
st.title("🤖 Chat para el COLEGIO PIO XII - Despeñaderos-")
st.markdown("Este es un *chatbot escolar* . ¡Arranquemos!") #añadimos descripcion txt

#agregamos una barra para configurar TEMPERATURA Y LLM A ELEGIR
with st.sidebar:
    st.header("Configuración")
    temperature = st.slider("Creatividad", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Modelo", ["gpt-4", "gpt-4o-mini", "gpt-5"])

#configuramos y definimos el modelo
    chat_model = ChatOpenAI(model=model_name, temperature=temperature)


#Memoria, implementacion
#1-comprobar si hay mensajes
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

 #  Botón para limpiar historial
if st.button("🧹 Nueva conversación"):
    st.session_state.mensajes = ""
    st.success("Historial limpiado correctamente ✅")
    st.rerun()

#creamos el template
prompt_template = PromptTemplate(
    input_variables=["mensaje", "historial"],
    template="""
Eres un asistente útil, amigable y profesional llamado ChatBoti. 
Tu objetivo es ayudar al usuario de forma clara, empática y precisa, 
manteniendo coherencia con el contexto previo.

Historial de conversación:
{historial}

Usuario: {mensaje}

ChatBot Pro:"""
)

#cremos la cadena
cadena = prompt_template|chat_model

#si hay mensajes previos, los mostramos en la interfaz
for msg in st.session_state.mensajes:
    rol = "assistant" if isinstance(msg, AIMessage) else "user" if isinstance(msg, HumanMessage) else "system"
    with st.chat_message(rol):
        st.markdown(msg.content)

#cuadro de entrada de txt de usuario
pregunta = st.chat_input("Escribe tu mensaje: ")

# if pregunta:
#     #mostramos el mensaje por pantalla
#     with st.chat_message("user"):
#         st.markdown(pregunta)
    #almacenamos en la memoria
    # st.session_state.mensajes.append(HumanMessage(content=pregunta))

    #generar la respuesta usando el llm
    # respuesta = chat_model.invoke(st.session_state.mensajes)

    #mostrar la rta en la interfaz
    
    # with st.chat_message("assistant"):
    #     st.markdown(respuesta.content)

    # #lo añado a la memoria
    # st.session_state.mensajes.append(respuesta) 

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)
    
    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty() #contenedor vacio
            full_response = ""
 
            # ¡Aquí está la magia del streaming!
            for chunk in cadena.stream({"mensaje": pregunta, "historial": st.session_state.mensajes}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")  # El cursor parpadeante
            
            response_placeholder.markdown(full_response)
        
        # No olvides almacenar los mensajes
        st.session_state.mensajes.append(HumanMessage(content=pregunta))
        st.session_state.mensajes.append(AIMessage(content=full_response))
        
    except Exception as e:
        # ¿Qué tipo de errores podrían ocurrir aquí?
        st.error(f"Error al generar respuesta: {str(e)}")
        st.info("Verifica que tu API Key de OpenAI esté configurada correctamente.")

# FOOTER
st.divider()
st.caption("🏫 Colegio Pio XII - Despeñaderos")       
