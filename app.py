import streamlit as st
from database import init_db, add_booking, get_employees, get_available_slots
from twilio_sms import send_sms
import pandas as pd

# Initialiseer database
init_db()

# Pagina-instellingen
st.set_page_config(page_title="D'or Booking", layout="centered")
st.title(f"📅 {st.secrets.get('COMPANY_NAME', 'D\\'or Booking System')}")
st.caption("Boek je afspraak online – snel, eenvoudig en 24/7 beschikbaar")

# Formulier voor nieuwe boeking
with st.form("booking_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Jouw naam*", placeholder="Jan Jansen")
    with col2:
        phone = st.text_input("Telefoonnummer*", placeholder="+31612345678")
    
    service = st.selectbox("Kies een dienst*", [
        "Consult (€30)", "Installatie (€100)", 
        "Onderhoud (€60)", "Training (€45)", 
        "Reparatie (€80)", "Schoonmaak (€50)"
    ])
    
    employee = st.selectbox("Medewerker*", get_employees())
    date = st.date_input("Datum*", min_value=pd.Timestamp.today())
    time = st.selectbox("Tijd*", get_available_slots(str(date)))

    submitted = st.form_submit_button("Boek nu!", type="primary")

    if submitted:
        if not name or not phone.startswith("+"):
            st.error("Vul naam en geldig telefoonnummer in (+316...)")
        else:
            booking_id = add_booking(name, phone, service, employee, str(date), time)
            msg = f"""
Beste {name},

Je afspraak is bevestigd! 

📅 {date} om {time}
🛠️ {service} met {employee}
🏢 {st.secrets['COMPANY_NAME']}

Tot snel!
            """.strip()
            success, sid = send_sms(phone, msg)
            if success:
                st.success(f"Afspraak bevestigd! SMS verzonden (ID: {booking_id})")
                st.balloons()
            else:
                st.warning(f"Afspraak opgeslagen, maar SMS mislukt: {sid}")
                st.info("Controleer of je telefoonnummer geverifieerd is in Twilio.")
