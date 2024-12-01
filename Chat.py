import streamlit as st
import unicode
import pandas as pd
from Interpretador import predict_class, get_response, intents
from unidecode import unidecode  # Agregar para eliminar tildes

# Definir la ruta del archivo CSV donde se guardará la conversación
CSV_FILE = "chat_history.csv"

# Intentar cargar el archivo CSV si existe, de lo contrario, crear uno vacío
try:
    chat_history_df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    chat_history_df = pd.DataFrame(columns=["ChatID", "Role", "Content"])

# Función para obtener el texto del botón en la barra lateral
def get_button_label(chat_df, chat_id):
    first_message = chat_df[(chat_df["ChatID"] == chat_id) & (chat_df["Role"] == "User")].iloc[0]["Content"]
    return f"Chat {chat_id[0:7]}: {' '.join(first_message.split()[:5])}..."

# Función para agregar la conversación al CSV
def add_chat_to_csv(chat_id, role, content):
    global chat_history_df
    new_chat = pd.DataFrame({"ChatID": [chat_id], "Role": [role], "Content": [content]})
    chat_history_df = pd.concat([chat_history_df, new_chat], ignore_index=True)
    chat_history_df.to_csv(CSV_FILE, index=False)

# Configuración de la aplicación Streamlit
st.set_page_config(
    page_title="Asistente Virtual para Estudiantes",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inicializar el estado de la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []  # Almacena los mensajes del chat
if "chat_id" not in st.session_state:
    st.session_state.chat_id = 1  # ID único de la conversación

# Estilos CSS personalizados
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
        background-color: transparent !important;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
        box-shadow: none !important
    }
    .stButton > button:hover {
        background-color: #00A2CC;
    }

    div[data-testid="stMarkdownContainer"] {
        background-color: rgba(255, 255, 255, 0.7) !important; 
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
        color: black !important;
    }

    textarea {
        background-color: rgba(255, 255, 255, 0.7) !important; 
        color: black !important; 
        border: 1px solid #ccc !important; 
        padding: 10px !important;
        border-radius: 5px !important;
        width: 100% !important; 
        box-shadow: none !important;
    }

    textarea::placeholder {
        color: #666 !important; 
    }

    div[data-testid="stChatInput"] {
        padding: 10px !important;
        display: flex;
        justify-content: center;
    }

    div[data-testid="stChatInput"] > div {
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# Título centrado
st.markdown('<div class="stTitle">Asistente Virtual para Estudiantes</div>', unsafe_allow_html=True)

# Mostrar los mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Mostrar el mensaje inicial del asistente si es el primer mensaje
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        google_drive_link = "https://drive.google.com/drive/folders/1hzw7Sjbi0A36a--Zefc09eGi0FZUAk-a?usp=sharing"
        google_drive_link2 = "https://drive.google.com/file/d/1CsFCI-KTZ5e2a_pyZm7sdJJ7xhT7L2zU/view?usp=sharing"
        google_drive_link3 = "https://drive.google.com/file/d/1q5-3pkY6aJt59xCVECmVMpLiGTMfvHDC/view?usp=sharing"
        # Inserción correcta de los enlaces
        st.markdown(
            f"1. **Syllabus** [aquí]({google_drive_link})\n 2. **Información general** (Perfil de egreso, etc)\n 3. **Malla** [aquí]({google_drive_link2})\n 4. **Acerca de Eliminar Asignaturas** [aquí]({google_drive_link3})\n 5. **Fechas registraduría** (Según el mes)\n 6. **Otras opciones** (por ejemplo, preguntas frecuentes, ayuda, certificado médico, etc .)")
        st.markdown("Hola, ¿cómo puedo ayudarte?")

# Capturar el mensaje del usuario y la respuesta del asistente
if prompt := st.chat_input("¿Cómo puedo ayudarte?"):
    prompt = unidecode(prompt)  # Eliminar tildes antes de procesar la entrada
    with st.chat_message("user"):
        st.markdown(prompt)

    # Implementación del algoritmo de AI
    insts = predict_class(prompt)
    res = get_response(insts, intents)

    with st.chat_message("assistant"):
        st.markdown(res)

    # Guardar el chat en el archivo CSV
    add_chat_to_csv(st.session_state.chat_id, "User", prompt)
    add_chat_to_csv(st.session_state.chat_id, "Assistant", res)

    # Guardar el mensaje en la sesión para mostrar en la UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": res})

    # Incrementar el ID del chat para futuras interacciones
    st.session_state.chat_id += 1

    # Hacer visible los botones de feedback solo después de la respuesta
    st.session_state.feedback_visible = True

    # Dividir la pantalla en 20 columnas para los botones solo si feedback_visible es True
    if st.session_state.feedback_visible:
        with st.container():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15, col16, col17, col18, col19, col20 = st.columns(20)

            # Colocar el botón de feedback positivo en la columna 19
            with col19:
                if st.button("👍", key="good"):
                    st.session_state.feedback_visible = False  # Ocultar botones después de recibir el feedback
                    add_chat_to_csv(st.session_state.chat_id, "Feedback", "like")

            # Colocar el botón de feedback negativo en la columna 20
            with col20:
                result = st.button("👎", key="bad")  # Usamos el resultado del botón
                if result:  # Si el botón fue presionado
                    st.session_state.feedback_visible = False  # Ocultar los botones después de recibir el feedback
                    print("Feedback negativo recibido: Guardando...")  # Depuración adicional
                    add_chat_to_csv(st.session_state.chat_id, "Feedback", "dislike")  # Guardar el feedback en el archivo CSV
                    st.success("¡Gracias por tu feedback! Estamos trabajando para mejorar.")
