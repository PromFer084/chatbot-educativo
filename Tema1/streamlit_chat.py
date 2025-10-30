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














# import os
# from langchain_openai import ChatOpenAI
# from langchain.schema import AIMessage, HumanMessage, SystemMessage
# import streamlit as st
# from langchain.prompts import PromptTemplate

# # ============================================================================
# # CONFIGURACIÓN INICIAL
# # ============================================================================

# st.set_page_config(
#     page_title="Chatbot Escolar - Colegio Pio XII",
#     page_icon="🤖",
#     layout="centered",
#     initial_sidebar_state="expanded"
# )

# # ============================================================================
# # FUNCIONES AUXILIARES
# # ============================================================================

# def inicializar_sesion():
#     """Inicializa el estado de la sesión con valores por defecto"""
#     if "mensajes" not in st.session_state:
#         st.session_state.mensajes = [
#             SystemMessage(content=(
#                 "Eres FerChus, un asistente educativo del Colegio Pio XII en Despeñaderos, Córdoba. "
#                 "Eres amigable, paciente y ayudas con dudas escolares de todas las materias. "
#                 "Respondes de forma clara, didáctica y motivadora."
#             ))
#         ]
#     if "contador_mensajes" not in st.session_state:
#         st.session_state.contador_mensajes = 0


# def obtener_historial_formateado(max_mensajes=10):
#     """
#     Formatea el historial de mensajes para el prompt.
#     Limita a los últimos N mensajes para no exceder tokens.
#     """
#     mensajes_recientes = st.session_state.mensajes[-max_mensajes:]
#     historial = []
    
#     for msg in mensajes_recientes:
#         if isinstance(msg, SystemMessage):
#             continue
#         elif isinstance(msg, HumanMessage):
#             historial.append(f"Estudiante: {msg.content}")
#         elif isinstance(msg, AIMessage):
#             historial.append(f"FerChus: {msg.content}")
    
#     return "\n".join(historial) if historial else "No hay conversación previa."


# def limpiar_conversacion():
#     """Reinicia la conversación manteniendo solo el mensaje de sistema"""
#     mensaje_sistema = st.session_state.mensajes[0]
#     st.session_state.mensajes = [mensaje_sistema]
#     st.session_state.contador_mensajes = 0


# def validar_api_key():
#     """Verifica que la API key de OpenAI esté configurada"""
#     if not os.getenv("OPENAI_API_KEY"):
#         st.error("⚠️ **Error:** No se encontró OPENAI_API_KEY en las variables de entorno")
#         st.info("💡 Configura tu API key antes de usar el chatbot")
#         st.code("export OPENAI_API_KEY='tu-api-key-aqui'", language="bash")
#         st.stop()

# # ============================================================================
# # INTERFAZ PRINCIPAL
# # ============================================================================

# # ============================================================================
# # INICIALIZACIÓN TEMPRANA (antes del sidebar)
# # ============================================================================

# inicializar_sesion()

# # Título y descripción
# st.title("🤖 Chat Educativo - Colegio Pio XII")
# st.markdown("**Despeñaderos, Córdoba** | Asistente: *FerChus* 📚")
# st.divider()

# # ============================================================================
# # SIDEBAR - CONFIGURACIÓN
# # ============================================================================

# with st.sidebar:
#     st.header("⚙️ Configuración")
    
#     # Botón de reset (siempre en la parte superior)
#     if st.button("🧹 Nueva conversación", key="reset_btn", use_container_width=True):
#         limpiar_conversacion()
#         st.rerun()
    
#     st.divider()
    
#     # Configuración del modelo
#     temperature = st.slider(
#         "💡 Creatividad",
#         min_value=0.0,
#         max_value=1.0,
#         value=0.7,
#         step=0.1,
#         help="Mayor valor = respuestas más creativas"
#     )
    
#     model_name = st.selectbox(
#         "🤖 Modelo",
#         options=["gpt-4o-mini", "gpt-4o"],
#         index=0,
#         help="gpt-4o-mini es más rápido y económico"
#     )
    
#     st.divider()
    
#     # Estadísticas
#     st.caption("📊 **Estadísticas**")
#     num_mensajes = len([m for m in st.session_state.mensajes if not isinstance(m, SystemMessage)])
#     st.caption(f"💬 Mensajes: {num_mensajes // 2}")

# # ============================================================================
# # VALIDACIÓN Y CONFIGURACIÓN DEL MODELO
# # ============================================================================

# validar_api_key()

# # Crear prompt template optimizado
# prompt_template = PromptTemplate(
#     input_variables=["mensaje", "historial"],
#     template="""Eres FerChus, un asistente educativo amigable del Colegio Pio XII.

# Contexto de la conversación:
# {historial}

# Pregunta del estudiante: {mensaje}

# Responde de manera clara, didáctica y motivadora. Si es un tema complejo, usa ejemplos."""
# )

# # Crear modelo y cadena
# try:
#     chat_model = ChatOpenAI(model=model_name, temperature=temperature)
#     cadena = prompt_template | chat_model
# except Exception as e:
#     st.error(f"❌ Error al inicializar el modelo: {str(e)}")
#     st.stop()

# # ============================================================================
# # MOSTRAR HISTORIAL
# # ============================================================================

# for msg in st.session_state.mensajes:
#     if isinstance(msg, SystemMessage):
#         continue
    
#     role = "assistant" if isinstance(msg, AIMessage) else "user"
#     avatar = "🤖" if role == "assistant" else "👤"
    
#     with st.chat_message(role, avatar=avatar):
#         st.markdown(msg.content)

# # ============================================================================
# # INPUT Y RESPUESTA
# # ============================================================================

# pregunta = st.chat_input("💬 Escribe tu consulta aquí...")

# if pregunta:
#     # Mostrar mensaje del usuario
#     with st.chat_message("user", avatar="👤"):
#         st.markdown(pregunta)
    
#     # Agregar al historial
#     st.session_state.mensajes.append(HumanMessage(content=pregunta))
    
#     # Generar respuesta
#     try:
#         with st.chat_message("assistant", avatar="🤖"):
#             response_placeholder = st.empty()
#             full_response = ""
            
#             # Obtener historial formateado (fijo en 10 mensajes)
#             historial_formateado = obtener_historial_formateado(10)
            
#             # Streaming de respuesta
#             with st.spinner("FerChus está pensando..."):
#                 for chunk in cadena.stream({
#                     "mensaje": pregunta,
#                     "historial": historial_formateado
#                 }):
#                     full_response += chunk.content
#                     response_placeholder.markdown(full_response + "▌")
            
#             # Mostrar respuesta final
#             response_placeholder.markdown(full_response)
        
#         # Agregar respuesta al historial
#         st.session_state.mensajes.append(AIMessage(content=full_response))
#         st.session_state.contador_mensajes += 1
        
#         # Limitar historial automáticamente (mantener últimos 20 mensajes + sistema)
#         if len(st.session_state.mensajes) > 21:
#             mensaje_sistema = st.session_state.mensajes[0]
#             st.session_state.mensajes = [mensaje_sistema] + st.session_state.mensajes[-20:]
    
#     except Exception as e:
#         st.error(f"❌ **Error al generar respuesta:** {str(e)}")
#         st.info("💡 Verifica tu conexión y configuración de API key")
#         # Remover el último mensaje del usuario si hubo error
#         st.session_state.mensajes.pop()

# # ============================================================================
# # FOOTER
# # ============================================================================

# st.divider()
# st.caption("🏫 Colegio Pio XII - Despeñaderos")