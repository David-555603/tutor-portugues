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
# --- MÓDULO: SIMULADOR (ROLEPLAY) ---
elif modulo == "💬 Simulador (Roleplay)":
    from gtts import gTTS 
    import io

    st.title("💬 Simulador de Escenarios (Roleplay)")
    st.write("Practica situaciones reales. Escucha al personaje, lee la traducción y mantén la conversación.")

    def reproducir_voz(texto):
        tts = gTTS(text=texto, lang='pt', tld='com.br')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')

    # Selector con los 4 escenarios
    escenario = st.selectbox("Selecciona dónde estás:", [
        "🍽️ En el Restaurante", 
        "👋 Conociendo a alguien",
        "✈️ En el Aeropuerto (Inmigración)",
        "🎓 Vida de Intercambio (Avanzado)"
    ])

    # ==========================================
    # ESCENARIO 1: EL RESTAURANTE (Oculto en código para no saturar, pero se mantiene igual)
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
            st.success("🎉 ¡Felicidades! Completaste la conversación.")
            dialogo = "Perfeito! Aqui está a conta. Muito obrigado pela visita e boa viagem!"
            st.info(f"🤵 **El Garçom diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Perfecto! Aquí tienes la cuenta. ¡Muchas gracias por tu visita y buen viaje!*")
            reproducir_voz(dialogo)

        if st.session_state.paso_restaurante < 4:
            st.markdown("---")
            audio_bytes = audio_recorder(text="Haz clic para responder falando 🎤", recording_color="#e83a30", neutral_color="#6aa36f", key="mic_rest")
            if audio_bytes:
                st.info("🧠 Escuchando...")
                r = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    try:
                        texto = r.recognize_google(r.record(source), language="pt-BR").lower()
                        st.success(f"🗣️ **Dijiste:** '{texto}'")
                        if st.session_state.paso_restaurante == 1 and ("cardápio" in texto or "cardapio" in texto):
                            st.session_state.paso_restaurante = 2; st.rerun()
                        elif st.session_state.paso_restaurante == 2 and ("quero" in texto or "gostaria" in texto or "picanha" in texto or "comer" in texto):
                            st.session_state.paso_restaurante = 3; st.rerun()
                        elif st.session_state.paso_restaurante == 3 and "conta" in texto:
                            st.balloons(); st.session_state.paso_restaurante = 4; st.rerun()
                        else: st.error("❌ No logré validar la palabra clave. ¡Intenta de nuevo!")
                    except: st.error("🎙️ No te entendí bien.")

    # ==========================================
    # ESCENARIO 2: CHARLA CASUAL
    # ==========================================
    elif escenario == "👋 Conociendo a alguien":
        st.subheader("Escenario: Haciendo un amigo en la playa 🏖️")
        if "paso_casual" not in st.session_state: st.session_state.paso_casual = 1
        if st.button("🔄 Reiniciar", key="btn_cas"): st.session_state.paso_casual = 1; st.rerun()

        if st.session_state.paso_casual == 1:
            dialogo = "Oi! Tudo bem? Meu nome é Lucas. E você, como se chama?"
            st.info(f"👦 **Lucas diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Hola! ¿Todo bien? Mi nombre es Lucas. Y tú, ¿cómo te llamas?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Objetivo:** Di tu nombre (ej. *'Meu nome é...'*).")
        elif st.session_state.paso_casual == 2:
            dialogo = "Prazer em conhecer! De onde você é?"
            st.info(f"👦 **Lucas diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Un placer conocerte! ¿De dónde eres?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Objetivo:** Dile tu país (ej. *'Eu sou da Colômbia'*).")
        elif st.session_state.paso_casual == 3:
            dialogo = "Que legal! E o que você está fazendo no Brasil? Está de férias?"
            st.info(f"👦 **Lucas diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Qué genial! ¿Y qué haces en Brasil? ¿Estás de vacaciones?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Objetivo:** Confirma que estás de viaje (ej. *'Sim, estou de férias'*).")
        elif st.session_state.paso_casual == 4:
            st.success("🎉 ¡Felicidades! Completaste la charla.")
            dialogo = "Muito bacana! Aproveite muito a viagem! Tchau!"
            st.info(f"👦 **Lucas diz:** '{dialogo}'")
            reproducir_voz(dialogo)

        if st.session_state.paso_casual < 4:
            st.markdown("---")
            audio_bytes = audio_recorder(text="Grabar 🎤", recording_color="#e83a30", neutral_color="#6aa36f", key="mic_casual")
            if audio_bytes:
                r = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    try:
                        texto = r.recognize_google(r.record(source), language="pt-BR").lower()
                        st.success(f"🗣️ **Dijiste:** '{texto}'")
                        if st.session_state.paso_casual == 1 and ("nome" in texto or "chamo" in texto or "sou" in texto):
                            st.session_state.paso_casual = 2; st.rerun()
                        elif st.session_state.paso_casual == 2 and ("sou" in texto or "de" in texto or "da" in texto or "do" in texto):
                            st.session_state.paso_casual = 3; st.rerun()
                        elif st.session_state.paso_casual == 3 and ("sim" in texto or "férias" in texto or "ferias" in texto or "passeio" in texto):
                            st.balloons(); st.session_state.paso_casual = 4; st.rerun()
                        else: st.error("❌ Intenta de nuevo.")
                    except: st.error("🎙️ Error de audio.")

    # ==========================================
    # ESCENARIO 3: EL AEROPUERTO (INMIGRACIÓN)
    # ==========================================
    elif escenario == "✈️ En el Aeropuerto (Inmigración)":
        st.subheader("Escenario: Control de Pasaportes 🛂")
        
        if "paso_aero" not in st.session_state: st.session_state.paso_aero = 1
        if st.button("🔄 Reiniciar conversación", key="btn_aero"): st.session_state.paso_aero = 1; st.rerun()

        if st.session_state.paso_aero == 1:
            dialogo = "Bom dia. Passaporte e passagem, por favor."
            st.info(f"👮 **Oficial diz:** '{dialogo}'")
            st.caption("💡 *Traducción: Buenos días. Pasaporte y pasaje, por favor.*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Entrégale el pasaporte educadamente (ej. *'Bom dia, aqui está o meu passaporte'*).")
        
        elif st.session_state.paso_aero == 2:
            dialogo = "Certo. Qual é o motivo da sua viagem? Turismo, trabalho ou estudo?"
            st.info(f"👮 **Oficial diz:** '{dialogo}'")
            st.caption("💡 *Traducción: Bien. ¿Cuál es el motivo de su viaje? ¿Turismo, trabajo o estudio?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Dile que vas a estudiar / de intercambio (ej. *'Eu venho para estudar'* o *'Eu vou fazer intercâmbio'*).")
            
        elif st.session_state.paso_aero == 3:
            dialogo = "Entendi. E quanto tempo você pretende ficar no Brasil?"
            st.info(f"👮 **Oficial diz:** '{dialogo}'")
            st.caption("💡 *Traducción: Entiendo. ¿Y cuánto tiempo pretende quedarse en Brasil?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Responde con un tiempo aproximado (ej. *'Vou ficar seis meses'* o *'Um ano'*).")
            
        elif st.session_state.paso_aero == 4:
            st.success("🎉 ¡Pasaste migración con éxito!")
            dialogo = "Tudo certo. O seu visto está aprovado. Bem-vindo ao Brasil!"
            st.info(f"👮 **Oficial diz:** '{dialogo}'")
            st.caption("💡 *Traducción: Todo en orden. Su visa está aprobada. ¡Bienvenido a Brasil!*")
            reproducir_voz(dialogo)

        if st.session_state.paso_aero < 4:
            st.markdown("---")
            audio_bytes = audio_recorder(text="Hablar 🎤", recording_color="#e83a30", neutral_color="#6aa36f", key="mic_aero")
            if audio_bytes:
                st.info("🧠 Escuchando...")
                r = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    try:
                        texto = r.recognize_google(r.record(source), language="pt-BR").lower()
                        st.success(f"🗣️ **Dijiste:** '{texto}'")
                        
                        if st.session_state.paso_aero == 1 and ("aqui" in texto or "passaporte" in texto or "sim" in texto):
                            st.session_state.paso_aero = 2; st.rerun()
                        elif st.session_state.paso_aero == 2 and ("estudo" in texto or "estudar" in texto or "intercâmbio" in texto or "intercambio" in texto or "faculdade" in texto):
                            st.session_state.paso_aero = 3; st.rerun()
                        elif st.session_state.paso_aero == 3 and ("meses" in texto or "ano" in texto or "semestre" in texto or "tempo" in texto or "ficar" in texto):
                            st.balloons(); st.session_state.paso_aero = 4; st.rerun()
                        else: st.error("❌ El oficial no comprendió. Intenta de nuevo usando las palabras sugeridas.")
                    except: st.error("🎙️ No te escuché bien. Intenta hablar más claro.")

    # ==========================================
    # ESCENARIO 4: VIDA DE INTERCAMBIO (LARGA)
    # ==========================================
    elif escenario == "🎓 Vida de Intercambio (Avanzado)":
        st.subheader("Escenario: Charla fluida con un colega de la facultad 🎒")
        st.write("💡 *Nota: Esta es una charla más rápida y con jerga ('gírias') usada por jóvenes universitarios.*")
        
        if "paso_facu" not in st.session_state: st.session_state.paso_facu = 1
        if st.button("🔄 Reiniciar conversación", key="btn_facu"): st.session_state.paso_facu = 1; st.rerun()

        if st.session_state.paso_facu == 1:
            dialogo = "Eaí! Quanto tempo! Como estão as aulas do intercâmbio? Tudo tranquilo?"
            st.info(f"👨‍🎓 **João diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Qué onda! ¡Cuánto tiempo! ¿Cómo van las clases del intercambio? ¿Todo tranquilo?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Dile que estás bien y que las clases son geniales/buenas (ej. *'Tudo bem, as aulas são muito legais'*).")
            
        elif st.session_state.paso_facu == 2:
            dialogo = "Que bom cara! E a comida brasileira? Já provou a nossa feijoada ou o famoso pão de queijo?"
            st.info(f"👨‍🎓 **João diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Qué bueno! ¿Y la comida brasileña? ¿Ya probaste nuestra feijoada o el famoso pan de queso?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Responde que sí y menciona qué probaste o que te gustó (ej. *'Sim, eu já provei pão de queijo e gostei muito'*).")
            
        elif st.session_state.paso_facu == 3:
            dialogo = "Pão de queijo é vida, né? Olha só, neste fim de semana a galera vai num barzinho perto da faculdade. Você anima ir com a gente?"
            st.info(f"👨‍🎓 **João diz:** '{dialogo}'")
            st.caption("💡 *Traducción: Pan de queso es vida, ¿verdad? Mira, este fin de semana el grupo va a un barcito cerca de la facultad. ¿Te animas a ir con nosotros?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Acepta la invitación con entusiasmo (ej. *'Sim, claro! Eu quero ir'* o *'Com certeza, eu animo'*).")
            
        elif st.session_state.paso_facu == 4:
            dialogo = "Fechado então! A gente se encontra lá pelas 20h. Quer que eu passe no seu alojamento pra gente ir junto?"
            st.info(f"👨‍🎓 **João diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Trato hecho entonces! Nos encontramos allá por las 20h. ¿Quieres que pase por tu alojamiento para ir juntos?*")
            reproducir_voz(dialogo)
            st.write("🎯 **Tu objetivo:** Confirma que te parece bien que pase por ti (ej. *'Perfeito, pode passar lá'* o *'Beleza, te espero'*).")
            
        elif st.session_state.paso_facu == 5:
            st.success("🎉 ¡Increíble! Mantuviste una conversación larga, natural y ya tienes planes para el fin de semana en Brasil.")
            dialogo = "Combinado! Então até sábado, se cuida e bons estudos aí!"
            st.info(f"👨‍🎓 **João diz:** '{dialogo}'")
            st.caption("💡 *Traducción: ¡Combinado! Entonces hasta el sábado, cuídate y buenos estudios ahí.*")
            reproducir_voz(dialogo)

        if st.session_state.paso_facu < 5:
            st.markdown("---")
            audio_bytes = audio_recorder(text="Hablar 🎤", recording_color="#e83a30", neutral_color="#6aa36f", key="mic_facu")
            if audio_bytes:
                st.info("🧠 Escuchando...")
                r = sr.Recognizer()
                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    try:
                        texto = r.recognize_google(r.record(source), language="pt-BR").lower()
                        st.success(f"🗣️ **Dijiste:** '{texto}'")
                        
                        if st.session_state.paso_facu == 1 and ("bem" in texto or "legal" in texto or "legais" in texto or "boas" in texto or "gostando" in texto):
                            st.session_state.paso_facu = 2; st.rerun()
                        elif st.session_state.paso_facu == 2 and ("sim" in texto or "provei" in texto or "comi" in texto or "gostei" in texto or "pão" in texto or "feijoada" in texto):
                            st.session_state.paso_facu = 3; st.rerun()
                        elif st.session_state.paso_facu == 3 and ("sim" in texto or "claro" in texto or "quero" in texto or "animo" in texto or "vamos" in texto):
                            st.session_state.paso_facu = 4; st.rerun()
                        elif st.session_state.paso_facu == 4 and ("perfeito" in texto or "beleza" in texto or "tá bom" in texto or "espero" in texto or "pode" in texto or "sim" in texto):
                            st.balloons(); st.session_state.paso_facu = 5; st.rerun()
                        else: st.error("❌ A João no le quedó muy claro. Intenta decirlo de otra forma guiándote por el objetivo.")
                    except: st.error("🎙️ No pude captar el audio completo.")
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
