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

records_all = get_records()

magazin = st.radio(
    "🏪 Magazin",
    ["Toate", "Magazin 1", "Magazin 2"],
    horizontal=True,
)

if magazin == "Toate":
    records = records_all
else:
    records = [
        r for r in records_all
        if str(r.get("Magazin", "")).strip() == magazin
    ]

total_intrare = sum(
    float(r.get("Intrare (litri)", 0) or 0)
    for r in records
)

total_iesire = sum(
    float(r.get("Iesire (litri)", 0) or 0)
    for r in records
)

stoc_curent = total_intrare - total_iesire

total_incasari = sum(
    float(r.get("Bani încasati (lei)", 0) or 0)
    for r in records
)

total_bidoane = sum(
    int(r.get("Nr. bidoane", 0) or 0)
    for r in records
)

st.markdown(
    """
    <style>
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        width: 100%;
        margin-top: 5px;
        margin-bottom: 10px;
    }

    .kpi-card {
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        padding: 14px 16px;
        min-width: 0;
    }

    .kpi-label {
        font-size: 14px;
        margin-bottom: 7px;
        opacity: 0.8;
        white-space: nowrap;
    }

    .kpi-value {
        font-size: 25px;
        font-weight: 700;
        line-height: 1.2;
        word-break: break-word;
    }

    @media screen and (max-width: 768px) {
        .kpi-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 8px;
        }

        .kpi-card {
            padding: 11px 10px;
            border-radius: 10px;
        }

        .kpi-label {
            font-size: 12px;
            white-space: normal;
        }

        .kpi-value {
            font-size: 19px;
        }
    }
    /* Zona celor două butoane */
.st-key-action_buttons div[data-testid="stHorizontalBlock"] {
    flex-wrap: nowrap;
}
/* Butoanele Salvează și Istoric */
.st-key-action_buttons div[data-testid="stHorizontalBlock"] {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: space-between;
}

.st-key-action_buttons div[data-testid="column"] {
    width: 50% !important;
    flex: 1 1 50% !important;
    min-width: 0 !important;
}

.st-key-action_buttons div[data-testid="column"]:last-child {
    display: flex;
    justify-content: flex-end;
}
    </style>
    """,
    unsafe_allow_html=True,
)

kpi_html = f"""
<div class="kpi-grid">
<div class="kpi-card">
<div class="kpi-label">🍷 Stoc curent</div>
<div class="kpi-value">{stoc_curent:,.0f} L</div>
</div>
<div class="kpi-card">
<div class="kpi-label">💰 Încasări totale</div>
<div class="kpi-value">{total_incasari:,.0f} lei</div>
</div>
<div class="kpi-card">
<div class="kpi-label">🫙 Bidoane</div>
<div class="kpi-value">{total_bidoane:,}</div>
</div>
<div class="kpi-card">
<div class="kpi-label">📝 Înregistrări</div>
<div class="kpi-value">{len(records)}</div>
</div>
</div>
"""

st.markdown(kpi_html, unsafe_allow_html=True)

st.markdown(
    "<hr style='margin-top:5px; margin-bottom:15px;'>",
    unsafe_allow_html=True,
)

if magazin == "Toate":
    st.info("Selectează un magazin pentru a adăuga o înregistrare.")
    st.stop()

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
    min_value=0,
    step=1,
    format="%d",
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
        min_value=0,
        step=1,
        format="%d",
    )

    nr_bidoane = st.number_input(
        "Nr. bidoane",
        min_value=0,
        step=1,
    )

    produs_special = st.number_input(
        "Produs special (litri)",
        min_value=0,
        step=1,
        format="%d",
    )


col_save, col_history = st.columns(2)

with col_save:
    salveaza = st.button(
        "💾 Salvează",
        type="primary",
    )

with col_history:
    st.link_button(
        "📋 Istoric",
        "https://docs.google.com/spreadsheets/d/1UIUAf1Ajsw3cPyCltQGVxFkVbgiMlnOzbEjGRGqK9Y4/edit",
    )

if salveaza:
    if intrare == 0 and iesire == 0 and bani == 0:
        st.warning(
            "Completează cel puțin o intrare, o ieșire "
            "sau o sumă încasată."
        )

    else:
        try:
            record_id = save_record(
                magazin=magazin,
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