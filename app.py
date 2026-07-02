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
# --- MÓDULO: SIMULADOR (ROLEPLAY) ---
elif modulo == "💬 Simulador (Roleplay)":
    from gtts import gTTS 
    import io

    st.title("💬 Simulador de Escenarios (Roleplay)")
    st.write("Practica situaciones reales. Escucha al personaje, lee la traducción y mantén la conversación.")

    # --- FUNCIÓN GLOBAL PARA LAS VOCES ---
    def reproducir_voz(texto):
        tts = gTTS(text=texto, lang='pt', tld='com.br')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')

    # Selector de escenarios
    escenario = st.selectbox("Selecciona dónde estás:", [
        "🍽️ En el Restaurante", 
        "👋 Conociendo a alguien", 
        "✈️ En el Aeropuerto (Próximamente)"
    ])

    # ==========================================
    # ESCENARIO 1: EL RESTAURANTE
    # ==========================================
    if escenario == "🍽️ En el Restaurante":
        st.subheader("Escenario: Cenando en la Churrascaria")
        
        if "paso_restaurante" not in st.session_state:
            st.session_state.paso_restaurante = 1

        if st.button("🔄 Reiniciar conversación", key="btn_rest"):
            st.session_state.paso_restaurante = 1
            st.rerun()

        if st.session_state.paso_restaurante == 1:
            dialogo = "Olá! Boa noite. Seja bem-vindo! Você já sabe o que vai pedir ou gostaria de ver o cardápio?"
            st.info(f"🤵 **El Garçom diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Hola! Buenas noches. ¡Bienvenido! ¿Ya sabes qué vas a pedir o te gustaría ver el menú?*")
            reproducir_voz(dialogo) 
            st.write("🎯 **Tu objetivo:** Saluda y pídele el menú (ej. *'Boa noite, o cardápio por favor'*).")

        elif st.session_state.paso_restaurante == 2:
            dialogo = "Com certeza, aqui está o cardápio! Hoje a nossa picanha está maravilhosa. O que você vai querer comer?"
            st.info(f"🤵 **El Garçom diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Claro que sí, aquí tienes el menú! Hoy nuestra picanha está maravillosa. ¿Qué vas a querer comer?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Pide tu comida (ej. *'Eu quero a picanha, por favor'*).")

        elif st.session_state.paso_restaurante == 3:
            dialogo = "Excelente escolha! Aqui está o seu prato... Algo mais ou posso trazer a conta?"
            st.info(f"🤵 **El Garçom diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Excelente elección! Aquí está tu plato... ¿Algo más o puedo traer la cuenta?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Pide la cuenta (ej. *'A conta, por favor'*).")
        
        elif st.session_state.paso_restaurante == 4:
            st.success("🎉 ¡Felicidades! Completaste toda la conversación.")
            dialogo = "Perfeito! Aqui está a conta. Muito obrigado pela visita e boa viagem pelo Brasil!"
            st.info(f"🤵 **El Garçom diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Perfecto! Aquí tienes la cuenta. ¡Muchas gracias por tu visita y buen viaje por Brasil!*")
            reproducir_voz(dialogo)

        if st.session_state.paso_restaurante < 4:
            st.markdown("---")
            audio_bytes = audio_recorder(text="Haz clic para responder falando 🎤", recording_color="#e83a30", neutral_color="#6aa36f", key="mic_rest")
            
            if audio_bytes:
                st.info("🧠 Escuchando tu acento...")
                r = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    audio_data = r.record(source)
                    try:
                        texto = r.recognize_google(audio_data, language="pt-BR").lower()
                        st.success(f"🗣️ **Te escuché decir:** '{texto}'")
                        
                        if st.session_state.paso_restaurante == 1 and ("cardápio" in texto or "cardapio" in texto):
                            st.session_state.paso_restaurante = 2
                            st.rerun()
                        elif st.session_state.paso_restaurante == 2 and ("quero" in texto or "gostaria" in texto or "picanha" in texto or "comer" in texto):
                            st.session_state.paso_restaurante = 3
                            st.rerun()
                        elif st.session_state.paso_restaurante == 3 and "conta" in texto:
                            st.balloons()
                            st.session_state.paso_restaurante = 4
                            st.rerun()
                        else:
                            st.error("❌ No logré validar la palabra clave para este paso. ¡Intenta de nuevo!")
                    except:
                        st.error("🎙️ No te entendí bien. Habla un poco más fuerte o claro.")

    # ==========================================
    # ESCENARIO 2: CHARLA CASUAL
    # ==========================================
    elif escenario == "👋 Conociendo a alguien":
        st.subheader("Escenario: Haciendo un amigo en la playa 🏖️")
        
        if "paso_casual" not in st.session_state:
            st.session_state.paso_casual = 1

        if st.button("🔄 Reiniciar conversación", key="btn_cas"):
            st.session_state.paso_casual = 1
            st.rerun()

        if st.session_state.paso_casual == 1:
            dialogo = "Oi! Tudo bem? Que dia bonito, né? Meu nome é Lucas. E você, como se chama?"
            st.info(f"👦 **Lucas diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Hola! ¿Todo bien? Qué día tan bonito, ¿verdad? Mi nombre es Lucas. Y tú, ¿cómo te llamas?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Responde al saludo y di tu nombre (ej. *'Tudo bem, meu nome é...'* o *'Eu sou o...'*).")

        elif st.session_state.paso_casual == 2:
            dialogo = "Prazer em conhecer! O seu sotaque é diferente. De onde você é?"
            st.info(f"👦 **Lucas diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Un placer conocerte! Tu acento es diferente. ¿De dónde eres?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Dile de qué país eres (ej. *'Eu sou da Colômbia'*, *'Eu sou do México'*, *'Eu sou da Espanha'*).")

        elif st.session_state.paso_casual == 3:
            dialogo = "Que legal! Eu sempre quis conhecer lá. E o que você está fazendo aqui no Brasil? Está de férias?"
            st.info(f"👦 **Lucas diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Qué genial! Siempre quise conocer ahí. ¿Y qué estás haciendo aquí en Brasil? ¿Estás de vacaciones?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Confirma que estás de viaje/vacaciones (ej. *'Sim, estou de férias'* o *'Sim, estou a passeio'*).")

        elif st.session_state.paso_casual == 4:
            st.success("🎉 ¡Felicidades! Tuviste tu primera charla casual en portugués.")
            dialogo = "Muito bacana! Bom, foi um prazer falar com você. Aproveite muito a viagem! Tchau, tchau!"
            st.info(f"👦 **Lucas diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Muy chévere! Bueno, fue un placer hablar contigo. ¡Disfruta mucho el viaje! ¡Chao, chao!*")
            reproducir_voz(dialogo)

        if st.session_state.paso_casual < 4:
            st.markdown("---")
            audio_bytes = audio_recorder(text="Haz clic para responder falando 🎤", recording_color="#e83a30", neutral_color="#6aa36f", key="mic_casual")
            
            if audio_bytes:
                st.info("🧠 Escuchando tu acento...")
                r = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    audio_data = r.record(source)
                    try:
                        texto = r.recognize_google(audio_data, language="pt-BR").lower()
                        st.success(f"🗣️ **Te escuché decir:** '{texto}'")
                        
                        # Validación del paso 1
                        if st.session_state.paso_casual == 1:
                            if "nome" in texto or "chamo" in texto or "sou" in texto or len(texto) > 2:
                                st.session_state.paso_casual = 2
                                st.rerun()
                            else:
                                st.error("❌ Lucas no escuchó tu nombre. Intenta decir 'Meu nome é...'.")
                        
                        # Validación del paso 2
                        elif st.session_state.paso_casual == 2:
                            if "sou" in texto or "de" in texto or "da" in texto or "do" in texto:
                                st.session_state.paso_casual = 3
                                st.rerun()
                            else:
                                st.error("❌ Lucas no entendió. Intenta decir 'Eu sou de...' o 'Eu sou do/da...'.")
                                
                        # Validación del paso 3
                        elif st.session_state.paso_casual == 3:
                            if "sim" in texto or "férias" in texto or "ferias" in texto or "passeio" in texto or "turismo" in texto:
                                st.balloons()
                                st.session_state.paso_casual = 4
                                st.rerun()
                            else:
                                st.error("❌ Lucas no entendió bien tu respuesta. Intenta decir 'Sim, estou de férias'.")
                                
                    except sr.UnknownValueError:
                        st.error("🎙️ No te entendí bien. Habla un poco más fuerte o claro.")
                    except sr.RequestError:
                        st.error("🌐 Error de conexión.")
# --- MÓDULO: GIMNASIO (FLASHCARDS) ---
elif modulo == "🧠 Gimnasio (Flashcards)":
    st.title("🧠 Gimnasio de Vocabulario")
    st.write("Entrena tu memoria. Di la traducción correcta para avanzar.")

    # 1. Obtener palabras de Supabase
    respuesta = supabase.table("vocabulario").select("*").execute()
    biblioteca = respuesta.data

    if not biblioteca:
        st.warning("Tu biblioteca está vacía. Agrega palabras en Supabase para empezar a entrenar.")
    else:
        # --- MEMORIA DEL GIMNASIO ---
        if "indice_flashcard" not in st.session_state:
            st.session_state.indice_flashcard = 0
            st.session_state.mostar_respuesta = False

        # Barra de progreso
        total = len(biblioteca)
        progreso = (st.session_state.indice_flashcard + 1) / total
        st.progress(progreso)
        st.write(f"Palabra {st.session_state.indice_flashcard + 1} de {total}")

        # Palabra actual
        palabra_actual = biblioteca[st.session_state.indice_flashcard]

        # --- DISEÑO DE LA TARJETA ---
        st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 40px; border-radius: 20px; text-align: center; border: 2px solid #6aa36f;">
                <h3 style="color: #555;">¿Cómo se dice en portugués?</h3>
                <h1 style="font-size: 50px; color: #1e293b;">{palabra_actual['espanol']}</h1>
            </div>
        """, unsafe_allow_html=True)

        st.write(" ") # Espacio

        # --- ACCIÓN: GRABAR RESPUESTA ---
        col1, col2 = st.columns(2)
        
        with col1:
            audio_bytes = audio_recorder(
                text="Responder hablando 🎤", 
                recording_color="#e83a30", 
                neutral_color="#6aa36f",
                key="mic_gym"
            )
        
        with col2:
            if st.button("👁️ Mostrar respuesta"):
                st.session_state.mostar_respuesta = True

        # --- LÓGICA DE VALIDACIÓN ---
        if audio_bytes:
            r = sr.Recognizer()
            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                audio_data = r.record(source)
                try:
                    texto_usuario = r.recognize_google(audio_data, language="pt-BR").lower()
                    respuesta_correcta = palabra_actual['portugues'].lower()

                    st.write(f"🗣️ **Dijiste:** {texto_usuario}")

                    # Verificamos si la palabra clave está en lo que dijo el usuario
                    if respuesta_correcta in texto_usuario or texto_usuario in respuesta_correcta:
                        st.success("¡Excelente! Es correcto. 🎉")
                        st.session_state.mostar_respuesta = True
                    else:
                        st.error(f"Casi... la respuesta esperada era: **{palabra_actual['portugues']}**")
                        st.session_state.mostar_respuesta = True
                        
                except:
                    st.error("No pude entender el audio. Intenta de nuevo.")

        # --- MOSTRAR DETALLES Y SIGUIENTE ---
        if st.session_state.mostar_respuesta:
            st.markdown("---")
            st.info(f"🇧🇷 **Portugués:** {palabra_actual['portugues']}")
            st.write(f"📝 **Ejemplo:** {palabra_actual['ejemplo']}")
            
            if st.button("Siguiente palabra ➡️"):
                if st.session_state.indice_flashcard < total - 1:
                    st.session_state.indice_flashcard += 1
                else:
                    st.balloons()
                    st.success("¡Completaste todo tu vocabulario por hoy! 🚀")
                    st.session_state.indice_flashcard = 0
                
                st.session_state.mostar_respuesta = False
                st.rerun()

        # Botón para reiniciar sesión
        if st.sidebar.button("🔄 Reiniciar Gimnasio"):
            st.session_state.indice_flashcard = 0
            st.session_state.mostar_respuesta = False
            st.rerun()

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
