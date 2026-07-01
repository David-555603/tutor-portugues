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
# --- MÓDULO: TEORÍA Y CLASES ---
# --- MÓDULO: TEORÍA Y CLASES ---
elif modulo == "📚 Teoría y Clases":
    st.title("📚 Módulo de Gramática y Supervivencia")
    st.write("Aprende las reglas, domina los sonidos y ponte a prueba para sobrevivir en Brasil.")

    # Añadimos la pestaña de Restaurante y ampliamos a 5 pestañas
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗣️ Pronunciación", "🤝 Saludos", "🏃‍♂️ Verbos Clave", "🍽️ Restaurante", "📝 Quiz"])

    with tab1:
        st.header("Los Sonidos del Portugués (Fase 1)")
        st.write("Si lees el portugués como se escribe en español, los brasileños no te entenderán. Memoriza estas 5 reglas de oro:")
        
        st.info("**1. La 'R' al principio de la palabra suena como 'J' suave:**")
        st.write("* *Restaurante* se pronuncia 'Jestauranchi'.")
        st.write("* *Rio de Janeiro* se pronuncia 'Hio dji Janeiru'.")
        
        st.info("**2. La 'D' y la 'T' antes de la 'E' y la 'I' cambian:**")
        st.write("* **DE / DI** suenan como 'Y' o 'LL': *Bom dia* (Bom yía) / *Saudade* (Saudayi).")
        st.write("* **TE / TI** suenan como 'CH': *Noite* (Noichi) / *Tudo* (Tudo - la u se mantiene).")
        
        st.info("**3. La 'O' al final de la palabra suena como 'U':**")
        st.write("* *Obrigado* suena 'Obrigadu'.")
        st.write("* *Queijo* (Queso) suena 'Queishu'.")

        st.info("**4. LH y NH (Las letras mágicas):**")
        st.write("* **LH** suena como nuestra 'LL' o 'Y': *Trabalho* (Trabayu).")
        st.write("* **NH** suena como nuestra 'Ñ': *Banheiro* (Bañeiru - Baño).")
        
        st.info("**5. El sonido nasal (La tilde ~):**")
        st.write("* Las palabras con **ão** suenan como si hablaras con la nariz tapada.")
        st.write("* *Pão* (Pan) suena nasal. ¡Cuidado de no decir 'Pau' con la boca abierta porque significa otra cosa muy distinta en Brasil!")
        st.write("* *Não* (No) suena como un 'Ná-o' nasal.")

    with tab2:
        st.header("Saludos y Cortesía Básica")
        st.write("Lo mínimo indispensable para ser un turista educado y caerle bien a los locales.")
        
        st.markdown("""
        * **Bom dia / Boa tarde / Boa noite:** Buenos días / tardes / noches.
        * **Oi, tudo bem?:** Hola, ¿todo bien? (El saludo más común).
        * **Tudo joia?:** ¿Todo excelente? (Una alternativa informal y muy amigable).
        * **Obrigado (hombres) / Obrigada (mujeres):** Gracias.
        * **De nada / Imagina:** De nada. ("Imagina" se usa muchísimo).
        * **Por favor:** Por favor.
        * **Com licença:** Con permiso.
        * **Desculpe:** Disculpa.
        * **Prazer:** Mucho gusto.
        """)

    with tab3:
        st.header("Verbos de Supervivencia")
        st.write("No necesitas conjugar todos los tiempos perfectos, solo necesitas saber pedir cosas.")
        
        with st.expander("Querer (Eu quero) - Directo y al grano"):
            st.write("**Eu quero:** Yo quiero.")
            st.write("*Ejemplo:* Eu quero uma água, por favor. (Quiero un agua, por favor).")
        
        with st.expander("Gostar (Eu gostaria de) - La forma educada"):
            st.write("**Eu gostaria de...:** Me gustaría...")
            st.write("*Ejemplo:* Eu gostaria de pedir a conta. (Me gustaría pedir la cuenta).")
            
        with st.expander("Ter (Ter/Tener) - Para preguntar si hay algo"):
            st.write("**Tem...?:** ¿Hay...? / ¿Tienen...?")
            st.write("*Ejemplo:* Tem banheiro? (¿Hay baño?).")
            st.write("*Ejemplo:* Tem cardápio em espanhol? (¿Tienen menú en español?).")
        
        with st.expander("Poder (Eu posso) - Para pedir permiso o ayuda"):
            st.write("**Você pode me ajudar?:** ¿Me puedes ayudar?")
            st.write("**Posso pagar com cartão?:** ¿Puedo pagar con tarjeta?")

    with tab4:
        st.header("🍽️ En el Restaurante")
        st.write("El vocabulario sagrado para disfrutar de la comida brasileña sin estrés.")
        
        st.subheader("Vocabulario Esencial")
        st.markdown("""
        * **O Cardápio:** El menú.
        * **O Garçom / A Garçonete:** El mesero / La mesera.
        * **A Conta:** La cuenta.
        * **O Troco:** El cambio (vuelto).
        * **Para levar:** Para llevar.
        * **Sobremesa:** Postre.
        * **Copo / Taça:** Vaso / Copa.
        """)
        
        st.subheader("Frases Salvavidas")
        st.info("**Para pedir la mesa:**")
        st.write("* *Uma mesa para dois, por favor.* (Una mesa para dos, por favor).")
        st.info("**Para ordenar:**")
        st.write("* *Você tem o cardápio, por favor?* (¿Tienes el menú, por favor?).")
        st.write("* *O que você recomenda?* (¿Qué recomiendas?).")
        st.write("* *Eu vou querer a picanha.* (Voy a querer la picanha).")
        st.info("**Para pagar:**")
        st.write("* *A conta, por favor.* (La cuenta, por favor).")
        st.write("* *Vocês aceitam cartão ou só Pix?* (¿Aceptan tarjeta o solo Pix?).")
        
        st.warning("💡 **Tip Cultural:** En Brasil, la propina (*gorjeta* o *taxa de serviço*) de 10% ya viene incluida casi siempre en el total de la cuenta. No necesitas dejar dinero extra en la mesa a menos que quieras.")

    with tab5:
        st.header("📝 Prueba tu conocimiento")
        st.write("Veamos si prestaste atención a las reglas. Responde este pequeño test:")
        
        q1 = st.radio("1. Si ves un letrero que dice 'Banheiro', ¿cómo lo pronuncias?", 
                      ["Ban-hei-ro", "Ba-ñei-ru", "Ba-ne-iro"], key="q1")
        
        q2 = st.radio("2. Eres hombre y te acaban de traer tu café, ¿qué dices?", 
                      ["Obrigada", "Gracias", "Obrigado"], key="q2")
        
        q3 = st.radio("3. ¿Cómo pides la cuenta en el restaurante?", 
                      ["A conta, por favor.", "O cardápio, por favor.", "O troco, por favor."], key="q3")
                      
        q4 = st.radio("4. ¿Qué es la 'taxa de serviço'?", 
                      ["El impuesto del gobierno", "La propina del 10% incluida", "El costo de usar el baño"], key="q4")
        
        if st.button("Revisar mis respuestas"):
            puntaje = 0
            
            if q1 == "Ba-ñei-ru":
                st.success("1. ¡Correcto! NH suena como Ñ, y la O final suena como U.")
                puntaje += 1
            else:
                st.error("1. Incorrecto. Recuerda la regla del NH y la O final.")
                
            if q2 == "Obrigado":
                st.success("2. ¡Correcto! Los hombres dicen Obrigado.")
                puntaje += 1
            else:
                st.error("2. Incorrecto. Depende de tu género.")
                
            if q3 == "A conta, por favor.":
                st.success("3. ¡Correcto! 'A conta' es la cuenta. 'Cardápio' es el menú.")
                puntaje += 1
            else:
                st.error("3. Incorrecto. Revisa la pestaña del Restaurante.")
                
            if q4 == "La propina del 10% incluida":
                st.success("4. ¡Correcto! Te ahorrará confusiones al pagar.")
                puntaje += 1
            else:
                st.error("4. Incorrecto. Es la propina de los meseros.")
                
            st.write(f"**Tu puntaje: {puntaje}/4**")
