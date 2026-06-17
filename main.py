import streamlit as st
from source.person import Person, get_person_data, get_person_object_by_full_name
from source.ekgdata import EKGdata

# ── Titel ──────────────────────────────────────────────────────────────────
st.write("# EKG APP")

# ── Personen laden ─────────────────────────────────────────────────────────
st.write("## Versuchsperson auswählen")

person_list = get_person_data()
person_names = [p.get_full_name() for p in person_list]

selected_name = st.selectbox("Versuchsperson", options=person_names, key="sbVersuchsperson")

# ── Ausgewählte Person als Objekt laden ────────────────────────────────────
person = get_person_object_by_full_name(selected_name)

# ── Personeninfos anzeigen ─────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.image(person.get_image(), caption=person.get_full_name())

with col2:
    st.write(f"**Name:** {person.get_full_name()}")
    st.write(f"**Geburtsjahr:** {person.date_of_birth}")
    st.write(f"**Geschlecht:** {person.gender}")
    st.write(f"**Max. Herzfrequenz:** {person.hr_max} bpm")

# ── EKG-Test auswählen ─────────────────────────────────────────────────────
st.write("## EKG-Test auswählen")

if person.ekg_tests:
    # 'enumerate(..., 1)' sorgt dafür, dass die Auswahl für jede Person immer bei Test 1 startet
    ekg_options = {f"Test {idx} – {t['date']}": t for idx, t in enumerate(person.ekg_tests, 1)}
    
    # Der dynamische Key sorgt dafür, dass sich das Dropdown beim Personenwechsel automatisch zurücksetzt
    selected_ekg_label = st.selectbox(
        "EKG-Test", 
        options=list(ekg_options.keys()), 
        key=f"sbEKG_{person.get_full_name()}"
    )
    ekg_dict = ekg_options[selected_ekg_label]

    # EKG-Objekt instanziieren
    ekg = EKGdata(ekg_dict)
    
    # 1. Peaks über den selbstgeschriebenen Algorithmus berechnen
    ekg.find_peaks()
    
    # 2. Herzfrequenz basierend auf den Peaks schätzen
    herzfrequenz = ekg.estimate_hr()
    
    # 3. Herzfrequenz als  Dashboard-Metrik anzeigen
    st.metric(label="Durchschnittliche Herzfrequenz", value=f"{herzfrequenz:.1f} bpm")
    
    # 4. Zeitreihe plotten (zeichnet automatisch die roten Peak-Punkte ein)
    ekg.plot_time_series()
    # 'width="stretch"' entfernt die Warnung im VS-Code Terminal
    st.plotly_chart(ekg.fig, width="stretch")
else:
    st.info("Für diese Person sind keine EKG-Tests vorhanden.")



if __name__ == "__main__":
    pass 