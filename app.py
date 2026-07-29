import streamlit as st
import pandas as pd
import plotly.express as px

from sheets import get_products, get_records, save_record


st.set_page_config(
    page_title="Crama cu Noroc",
    page_icon="🍷",
    layout="wide",
)

st.markdown("""
<style>
html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
main,
.block-container {
    max-width: 100% !important;
    overflow-x: hidden !important;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}

iframe {
    max-width: 100% !important;
}

div[data-testid="stPlotlyChart"] {
    max-width: 100% !important;
    overflow-x: hidden !important;
}

div[role="radiogroup"] {
    max-width: 100% !important;
    flex-wrap: wrap !important;
}

h1 {
    margin-top: 0rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1 class="app-title">🍷 Evidență Cramă</h1>
""", unsafe_allow_html=True)

# ===============================
# KPI-uri
# ===============================

records_all = get_records()

col_magazin, col_istoric = st.columns([4, 1])

with col_magazin:
    magazin = st.radio(
    "",
    ["Toate", "Magazin 1", "Magazin 2"],
    horizontal=True,
    label_visibility="collapsed",
    format_func=lambda x: (
        "Toate" if x == "Toate" else f"🏪 {x}"
    ),
)

with col_istoric:
    st.link_button(
        "📋 Istoric",
        "https://docs.google.com/spreadsheets/d/1UIUAf1Ajsw3cPyCltQGVxFkVbgiMlnOzbEjGRGqK9Y4/edit",
        use_container_width=True,
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
    .app-title {
    margin: 0 0 12px 0;
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.1;
}

@media screen and (max-width: 768px) {
    .app-title {
        font-size: 2.2rem;
        white-space: nowrap;
    }
}

@media (max-width: 768px) {
    .app-title {
        font-size: 2rem !important;
        line-height: 1.1;
        margin-bottom: 1rem;
        white-space: nowrap;
    }
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

# ===============================
# Grafice lunare
# ===============================

df_chart = pd.DataFrame(records)

if not df_chart.empty:

    df_chart["Data"] = pd.to_datetime(
        df_chart["Data"],
        dayfirst=True,
        errors="coerce",
    )

    df_chart["Bani încasati (lei)"] = pd.to_numeric(
        df_chart["Bani încasati (lei)"],
        errors="coerce",
    ).fillna(0)

    df_chart["Iesire (litri)"] = pd.to_numeric(
        df_chart["Iesire (litri)"],
        errors="coerce",
    ).fillna(0)

    df_chart = df_chart.dropna(subset=["Data"])

    df_chart["Luna"] = df_chart["Data"].dt.to_period("M").dt.to_timestamp()

    monthly_data = (
        df_chart.groupby("Luna", as_index=False)
        .agg(
            Incasari=("Bani încasati (lei)", "sum"),
            Litri_vanduti=("Iesire (litri)", "sum"),
        )
        .sort_values("Luna")
    )

    luni = {
        1: "Ian",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "Mai",
        6: "Iun",
        7: "Iul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Noi",
        12: "Dec",
    }

    monthly_data["Luna_afisata"] = monthly_data["Luna"].apply(
        lambda d: f"{luni[d.month]} {d.year}"
    )

    st.subheader("📊 Evoluție lunară")



    tip_grafic = st.radio(
        "",
        ["💰 Încasări", "🍷 Litri vânduți"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if tip_grafic == "💰 Încasări":
        coloana = "Incasari"
        titlu_axa = "Lei"
    else:
        coloana = "Litri_vanduti"
        titlu_axa = "Litri"

    fig_evolutie = px.bar(
        monthly_data,
        x="Luna_afisata",
        y=coloana,
        text=coloana,
    )

    fig_evolutie.update_layout(
        xaxis_title="",
        yaxis_title=titlu_axa,
        bargap=0.80,
        showlegend=False,
        margin=dict(l=20, r=20, t=20, b=20),
    )

    fig_evolutie.update_traces(
        marker_color="#9B1F45",
        textposition="inside",
    )

    st.plotly_chart(
        fig_evolutie,
        use_container_width=True,
        config={
            "staticPlot": True,
            "displayModeBar": False,
            "responsive": True,
        },
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



if st.button("💾 Salvează", type="primary"):
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