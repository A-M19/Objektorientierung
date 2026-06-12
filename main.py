import streamlit as st
from source.person import Person, get_person_data, get_person_object_by_full_name
from source.ekgdata import EKGdata

# ── Titel ──────────────────────────────────────────────────────────────────
st.write("# EKG APP")

# ── Personen laden ─────────────────────────────────────────────────────────
st.write("## Versuchsperson auswählen")

person_list = get_person_data()
person_names = [p.get_full_name() for p in person_list]  # Format: "Huber, Julian"

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
    ekg_options = {f"Test {t['id']} – {t['date']}": t for t in person.ekg_tests}
    selected_ekg_label = st.selectbox("EKG-Test", options=list(ekg_options.keys()))
    ekg_dict = ekg_options[selected_ekg_label]

    # ── EKG-Objekt erstellen & plotten ─────────────────────────────────────
    ekg = EKGdata(ekg_dict)
    ekg.plot_time_series()
    st.plotly_chart(ekg.fig, use_container_width=True)
else:
    st.info("Für diese Person sind keine EKG-Tests vorhanden.")