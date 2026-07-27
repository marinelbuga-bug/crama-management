import streamlit as st

from sheets import get_products, save_record


st.set_page_config(
    page_title="Crama",
    page_icon="🍷",
    layout="wide",
)

st.title("🍷 Evidență Cramă")
st.subheader("Adaugă o înregistrare")


# Citim produsele din Google Sheets
try:
    produse_data = get_products()

    produse = [rand["Produs"] for rand in produse_data]

    preturi = {
        rand["Produs"]: float(rand["Pret Litru"])
        for rand in produse_data
    }

except Exception as error:
    st.error(f"Nu am putut încărca produsele: {error}")
    st.stop()


col1, col2 = st.columns(2)

with col1:
    produs = st.selectbox(
        "Produs",
        produse,
    )

    data = st.date_input("Data")

    intrare = st.number_input(
        "Intrare (litri)",
        min_value=0.0,
        step=1.0,
    )

    pret = st.number_input(
        "Preț / litru",
        min_value=0.0,
        value=preturi.get(produs, 0.0),
        step=0.5,
        key=f"pret_{produs}",
    )

with col2:
    bani = st.number_input(
        "Bani încasați",
        min_value=0.0,
        step=10.0,
    )

    iesire = st.number_input(
        "Ieșire (litri)",
        min_value=0.0,
        step=1.0,
    )

    nr_bidoane = st.number_input(
        "Nr. bidoane",
        min_value=0,
        step=1,
    )

    produs_special = st.number_input(
        "Produs special (litri)",
        min_value=0.0,
        step=1.0,
    )


if st.button("💾 Salvează", type="primary"):
    if intrare == 0 and iesire == 0 and bani == 0:
        st.warning(
            "Completează cel puțin o intrare, o ieșire "
            "sau o sumă încasată."
        )

    else:
        try:
            record_id = save_record(
                data=data.strftime("%d.%m.%Y"),
                produs=produs,
                intrare=intrare,
                pret_litru=pret,
                bani_incasati=bani,
                iesire=iesire,
                nr_bidoane=nr_bidoane,
                produs_special=produs_special,
            )

            st.success(
                f"Înregistrarea cu ID-ul {record_id} "
                "a fost salvată în Google Sheets!"
            )

        except Exception as error:
            st.error(f"Înregistrarea nu a putut fi salvată: {error}")