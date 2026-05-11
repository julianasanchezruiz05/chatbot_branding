import streamlit as st
import time

# Configuración inicial de la página web (Título, ícono y diseño centrado)
st.set_page_config(page_title="Chatbot | Juliana Branding", page_icon="✨", layout="centered")

# Utilizamos CSS para darle un aspecto moderno, limpio y profesional a la interfaz.
st.markdown("""
    <style>
    /* Fondo general más suave */
    .stApp {
        background-color: #FDFEFE;
    }
    /* Estilos del encabezado principal */
    .main-header {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        color: #2C3E50;
        margin-bottom: 0px;
    }
    /* Estilo del subtítulo */
    .subtitle {
        text-align: center;
        color: #7F8C8D;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    /* Mejorando el diseño de los botones para que parezcan opciones de chat */
    div[data-testid="stButton"] button {
        border-radius: 20px;
        border: 1.5px solid #E5E7E9;
        background-color: #ffffff;
        color: #2C3E50;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    /* Efecto Hover en botones: color de marca sutil */
    div[data-testid="stButton"] button:hover {
        border-color: #9B59B6;
        color: #9B59B6;
        box-shadow: 0 4px 10px rgba(155, 89, 182, 0.15);
        transform: translateY(-2px);
    }
    /* Estilizando el input del chat */
    div[data-testid="stChatInput"] {
        border-radius: 25px !important;
    }
    </style>
""", unsafe_allow_html=True)

# En la web, necesitamos guardar el estado para saber en qué paso vamos
if "step" not in st.session_state:
    st.session_state.step = 0 # Inicia en el paso 0

if "data" not in st.session_state:
    st.session_state.data = {} # Diccionario para guardar respuestas del usuario

if "messages" not in st.session_state:
    # Mensaje inicial de bienvenida
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! ✨ **BIENVENIDO AL CHATBOT DE JULIANA BRANDING**.\n\nEstoy aquí para ayudarte a impulsar tu proyecto de internet. Para empezar, **¿cómo te llamas?**"}
    ]

st.markdown("<h1 class='main-header'>✨ Juliana Branding</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Tu asistente virtual de diseño y estrategia</p>", unsafe_allow_html=True)

# Renderiza todos los mensajes previos guardados en la sesión
for msg in st.session_state.messages:
    avatar = "👩‍🎨" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

def bot_reply(text, delay=1.2):
    """Simula que el bot está escribiendo para mejorar la experiencia humana UX."""
    with st.chat_message("assistant", avatar="👩‍🎨"):
        with st.spinner("Escribiendo..."):
            time.sleep(delay)
        st.markdown(text)
    # Guardamos el mensaje del bot
    st.session_state.messages.append({"role": "assistant", "content": text})
    st.rerun() # Recarga la página para mostrar los cambios

def add_user_msg(text):
    """Guarda un mensaje del usuario en el historial visual."""
    st.session_state.messages.append({"role": "user", "content": text})

step = st.session_state.step

# Paso 0: Esperando el Nombre
if step == 0:
    if name := st.chat_input("Escribe tu nombre aquí..."):
        add_user_msg(name)
        st.session_state.data["nombre"] = name.title()
        st.session_state.step = 1
        st.rerun()

# Paso 1: Esperando el Nombre de la Marca
elif step == 1:
    # Si acabamos de pasar al paso 1, el bot debe responder primero
    if st.session_state.messages[-1]["role"] == "user":
        name = st.session_state.data["nombre"]
        bot_reply(f"¡Un gusto conocerte, **{name}**! 🌟\n\n**¿Cuál es el nombre de tu marca o proyecto?**")

    # Esperamos el input de la marca
    if marca := st.chat_input("Nombre de tu marca..."):
        add_user_msg(marca)
        st.session_state.data["marca"] = marca
        st.session_state.step = 2
        st.rerun()

elif step == 2:
    if st.session_state.messages[-1]["role"] == "user":
        marca = st.session_state.data["marca"]
        bot_reply(f"¡Excelente! **{marca}** suena con mucho potencial.\n\n**¿Qué servicio necesitas?**")

    # UX MEJORA: Botones interactivos en lugar de pedir que digiten números
    cols = st.columns(2)
    with cols[0]:
        if st.button("1️⃣ Branding (Desde cero)", use_container_width=True):
            add_user_msg("Branding")
            st.session_state.data["servicio"] = "Branding"
            st.session_state.step = 3
            st.rerun()
    with cols[1]:
        if st.button("2️⃣ Rebranding (Renovación)", use_container_width=True):
            add_user_msg("Rebranding")
            st.session_state.data["servicio"] = "Rebranding"
            st.session_state.step = 3
            st.rerun()

elif step == 3:
    if st.session_state.messages[-1]["role"] == "user":
        servicio = st.session_state.data["servicio"]
        bot_reply(f"Tu proyecto ha sido clasificado como **{servicio}**.\n\n**¿Tu marca ya cuenta con un logo?**")

    cols = st.columns(2)
    with cols[0]:
        if st.button("✅ Sí, ya tengo logo", use_container_width=True):
            add_user_msg("Sí")
            st.session_state.data["logo"] = "Sí"
            st.session_state.step = 4
            st.rerun()
    with cols[1]:
        if st.button("❌ No, aún no", use_container_width=True):
            add_user_msg("No")
            st.session_state.data["logo"] = "No"
            st.session_state.step = 4
            st.rerun()

elif step == 4:
    if st.session_state.messages[-1]["role"] == "user":
        logo = st.session_state.data["logo"]
        if logo == "Sí":
            bot_reply("¡Genial! Tienes una identidad visual previa que podemos potenciar.\n\n**¿Qué tan urgente es tu proyecto?**")
        else:
            bot_reply("¡No hay problema! Crearemos una identidad visual increíble desde cero.\n\n**¿Qué tan urgente es tu proyecto?**")

    # UX MEJORA: Evita el ciclo while de errores mostrando opciones exactas
    cols = st.columns(3)
    if cols[0].button("🔥 Alta", use_container_width=True):
        add_user_msg("Alta")
        st.session_state.data["urgencia"] = "Alta"
        st.session_state.step = 5
        st.rerun()
    if cols[1].button("⏳ Media", use_container_width=True):
        add_user_msg("Media")
        st.session_state.data["urgencia"] = "Media"
        st.session_state.step = 5
        st.rerun()
    if cols[2].button("🌿 Baja", use_container_width=True):
        add_user_msg("Baja")
        st.session_state.data["urgencia"] = "Baja"
        st.session_state.step = 5
        st.rerun()

elif step == 5:
    if st.session_state.messages[-1]["role"] == "user":
        bot_reply("Anotado. Finalmente, **¿deseas agendar una reunión para hablar a detalle?**")

    cols = st.columns(2)
    if cols[0].button("📅 Sí, agendar reunión", use_container_width=True):
        add_user_msg("Sí")
        st.session_state.data["reunion"] = "Sí"
        st.session_state.step = 6
        st.rerun()
    if cols[1].button("✉️ No por ahora", use_container_width=True):
        add_user_msg("No")
        st.session_state.data["reunion"] = "No"
        st.session_state.step = 6
        st.rerun()

elif step == 6:
    if st.session_state.messages[-1]["role"] == "user":
        reunion = st.session_state.data["reunion"]
        d = st.session_state.data
        
        # Condicional final
        if reunion == "Sí":
            msg_final = "¡Perfecto! La conversación será transferida con Juliana para agendar tu espacio. 🗓️"
        else:
            msg_final = "¡Gracias por comunicarte! Tu información fue registrada de forma segura. 🔒"
            
        # Generación del resumen
        summary = f"""{msg_final}

---
### 📋 Resumen Final de tu Solicitud
* **👤 Cliente:** {d.get('nombre')}
* **🏢 Marca:** {d.get('marca')}
* **💼 Servicio:** {d.get('servicio')}
* **🎨 Tiene Logo:** {d.get('logo')}
* **⏱️ Urgencia:** {d.get('urgencia')}

*¡Fin del chatbot! Si deseas empezar de nuevo, recarga esta página web.*
"""
        bot_reply(summary, delay=2.0)