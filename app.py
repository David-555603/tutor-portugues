import streamlit as st
from supabase import create_client, Client
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
import io

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Tutor Pro de Portugués", page_icon="🇧🇷", layout="centered")

# --- CONEXIÓN A LA BASE DE DATOS ---
@st.cache_resource
def iniciar_conexion():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = iniciar_conexion()

# --- MENÚ LATERAL ---
st.sidebar.title("Navegación 🧭")
modulo = st.sidebar.radio(
    "Selecciona un módulo:",
    ["Inicio", "📚 Teoría y Clases", "💬 Simulador (Roleplay)", "🧠 Gimnasio (Flashcards)"]
)

# --- MÓDULO: INICIO ---
if modulo == "Inicio":
    st.title("🇧🇷 Bem-vindo ao seu Tutor de Português")
    st.write("Faltan pocos días para tu viaje a Brasil. ¡Es hora de practicar!")

# --- MÓDULO: SIMULADOR (ROLEPLAY) ---
elif modulo == "💬 Simulador (Roleplay)":
    st.title("💬 Simulador de Escenarios")
    st.write("Di algo en portugués (ej. 'Olá, tudo bem?') y la IA evaluará tu pronunciación.")
    
    # Grabador de audio
    audio_bytes = audio_recorder(
        text="Haz clic para hablar 🎤", 
        recording_color="#e83a30", 
        neutral_color="#6aa36f"
    )
    
    # Procesamiento del audio
    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        st.info("🧠 Procesando tu pronunciación...")
        
        # Convertimos el audio para que la IA lo entienda
        r = sr.Recognizer()
        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
            audio_data = r.record(source)
            try:
                # Usamos el motor de Google configurado en Portugués de Brasil (pt-BR)
                texto_reconocido = r.recognize_google(audio_data, language="pt-BR")
                st.success(f"🗣️ **Entendí que dijiste:** {texto_reconocido}")
                
            except sr.UnknownValueError:
                st.error("No pude entender el audio. Intenta hablar un poco más fuerte o claro.")
            except sr.RequestError:
                st.error("Error de conexión con el servicio de reconocimiento de voz.")

# --- MÓDULO: GIMNASIO (FLASHCARDS) ---
elif modulo == "🧠 Gimnasio (Flashcards)":
    st.title("🧠 Gimnasio de Vocabulario")
    
    respuesta = supabase.table("vocabulario").select("*").execute()
    datos = respuesta.data
    
    if len(datos) > 0:
        st.success("¡Conexión Exitosa! 🎉 Aquí están tus palabras:")
        for item in datos:
            with st.expander(f"🇪🇸 {item['espanol']}"):
                st.write(f"**🇧🇷 Portugués:** {item['portugues']}")
                st.write(f"**📝 Ejemplo:** {item['ejemplo']}")
    else:
        st.warning("La tabla está vacía. Agrega palabras en Supabase.")

# --- OTROS MÓDULOS ---
elif modulo == "📚 Teoría y Clases":
    st.title("📚 Módulo de Gramática (En construcción)")