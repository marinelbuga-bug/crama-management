import streamlit as st

st.set_page_config(
    page_title="Crama",
    page_icon="🍷",
    layout="wide"
)

st.title("🍷 Evidență Cramă")

st.subheader("Adaugă o înregistrare")

col1, col2 = st.columns(2)

with col1:
    produs = st.selectbox(
        "Produs",
        ["Vin Alb", "Vin Roșu", "Vin Roze"]
    )

    data = st.date_input("Data")

    intrare = st.number_input(
        "Intrare (litri)",
        min_value=0
    )

    pret = st.number_input(
        "Preț / litru",
        min_value=0.0
    )

with col2:
    bani = st.number_input(
        "Bani încasați",
        min_value=0.0
    )

    nr_bidoane = st.number_input(
        "Nr. bidoane",
        min_value=0
    )

    produs_special = st.number_input(
        "Produs special (litri)",
        min_value=0
    )

if st.button("💾 Salvează"):
    st.success("Înregistrarea a fost salvată!")