import streamlit as st
from Interpretador import predict_class, get_response, intents
import nltk
from nltk.stem import WordNetLemmatizer
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


nltk.download('wordnet')
nltk.download('punkt')


# Configuración de la aplicación Streamlit
st.set_page_config(
    page_title="Asistente Virtual para Estudiantes",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Agregar estilos CSS personalizados
st.markdown("""
    <style>
    .stApp {
        background-image: url('https://img.freepik.com/vector-gratis/fondo-tecnologia-blanca-futurista_23-2148390336.jpg?w=996&t=st=1724449086~exp=1724449686~hmac=347eda688c8cd9414aead2ee0e28690f75afb804fc20779edbdfefada20df4eb'); 
        background-size: cover;
        background-position: center;
    }
    .stTitle {
        color: black;
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton > button {
        background-color: transparent !important; /* Color celeste */
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        box-shadow: none !important
    }
    .stButton > button:hover {
        background-color: #00A2CC; /* Un tono más oscuro de celeste para el hover */
    }

    /* Estilos para los mensajes del chat */
    div[data-testid="stMarkdownContainer"] {
        background-color: rgba(255, 255, 255, 0.7) !important; /* Fondo blanco traslúcido */
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        color: black !important;
    }

    /* Estilos para el cuadro de entrada de texto */
    textarea {
        background-color: rgba(255, 255, 255, 0.7) !important; /* Fondo blanco traslúcido */
        color: black !important; /* Texto negro */
        border: 1px solid #ccc !important; /* Borde gris */
        padding: 10px !important; /* Espaciado interno */
        border-radius: 5px !important; /* Bordes redondeados */
        width: 100% !important; /* Ocupa todo el ancho disponible */
        box-shadow: none !important; /* Eliminar sombras */
    }

    /* Estilo para el placeholder del cuadro de entrada */
    textarea::placeholder {
        color: #666 !important; /* Color del placeholder */
    }

    /* Alinear el cuadro de entrada correctamente */
    div[data-testid="stChatInput"] {
        padding: 10px !important;
        display: flex;
        justify-content: center;
    }

    /* Asegurar que el contenedor del cuadro de entrada no tenga márgenes adicionales */
    div[data-testid="stChatInput"] > div {
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Título centrado y personalizado
st.markdown('<div class="stTitle">Asistente Virtual para Estudiantes</div>', unsafe_allow_html=True)

# Inicializar el estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

# Mostrar los mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Mostrar el mensaje inicial del asistente
if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Hola, ¿cómo puedo ayudarte?")
        st.session_state.messages.append({"role": "assistant", "content": "Hola, ¿cómo puedo ayudarte?"})
        st.session_state.first_message = False

# Capturar el mensaje del usuario y la respuesta del asistente
if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    # Ocultar los botones de feedback al ingresar una nueva consulta###

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Implementación del algoritmo de AI
    insts = predict_class(prompt)
    res = get_response(insts, intents)

    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role": "assistant", "content": res})

    # Hacer visible los botones de feedback solo después de la respuesta###
    st.session_state.feedback_visible = True

    # Dividir la pantalla en 20 columnas para los botones solo si feedback_visible es True
    if st.session_state.feedback_visible:  # Solo mostrar si es visible
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20 = st.columns(
                20)

            # Colocar el botón de feedback positivo en la columna 19
            with col19:
                if st.button("👍", key="good"):
                    st.session_state.feedback_visible = False  # Ocultar botones después de recibir el feedback

            # Colocar el botón de feedback negativo en la columna 20
            with col20:
                if st.button("👎", key="bad"):
                    st.session_state.feedback_visible = False  # Ocultar botones después de recibir el feedback
