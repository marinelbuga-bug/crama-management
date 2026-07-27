import streamlit as st

from sheets import get_products, get_records, save_record


st.set_page_config(
    page_title="Crama",
    page_icon="🍷",
    layout="wide",
)

st.markdown("""
<style>
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

h1 {
    margin-top: 0rem;
}
</style>
""", unsafe_allow_html=True)

st.title("🍷 Evidență Cramă")

# ===============================
# KPI-uri
# ===============================

records = get_records()

total_intrare = sum(
    float(r.get("Intrare\n(litri)", 0) or 0)
    for r in records
)

total_iesire = sum(
    float(r.get("Iesire\n(litri)\n", 0) or 0)
    for r in records
)

stoc_curent = total_intrare - total_iesire

total_incasari = sum(
    float(r.get("Bani încasati\n(lei)", 0) or 0)
    for r in records
)

total_bidoane = sum(
    int(r.get("Nr.\nbidoane", 0) or 0)
    for r in records
)

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "🍷 Stoc curent",
        f"{stoc_curent:,.0f} L",
    )

with kpi2:
    st.metric(
        "💰 Încasări totale",
        f"{total_incasari:,.0f} lei",
    )

with kpi3:
    st.metric(
        "🫙 Bidoane",
        f"{total_bidoane:,}",
    )

with kpi4:
    st.metric(
        "📝 Înregistrări",
        len(records),
    )

st.markdown(
    "<hr style='margin-top:5px; margin-bottom:15px;'>",
    unsafe_allow_html=True,
)

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