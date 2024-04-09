import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar
alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Pulmons trasplantats",
    layout = "wide"
)
make_sidebar()
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Pulmons trasplantats")

data = pd.read_csv("PULMONS.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")


color_scale = alt.Scale(domain=['PULMO BILATERAL', 'PULMO DRET',
                                'PULMO ESQUERRE'],
                        range=['#fdae61', '#abdda4', '#70b9e5'])

orden = ["PULMO DRET", "PULMO ESUQERRE", "PULMO BILATERAL"]
# Create the bar chart
chart_propis = alt.Chart(data).mark_bar().encode(
    x=alt.X('HOSPITAL TRASPLANTADOR:N',axis=alt.Axis(labelAngle=0), title='Hospital'),
    y=alt.Y('count():Q', title='Acumulatiu'),
    color=alt.Color('ORGAN:N', scale=color_scale, title='Categoria', ),
    order = 'orden:N'
).transform_filter(alt.datum['RESPOSTA'] == "Acceptat i trasplantat").properties(
    width=700,
    height=600,
)

text_propis = alt.Chart(data).mark_text(align='center', baseline='middle', dy=-10, fontSize=20).encode(
    x=alt.X('HOSPITAL TRASPLANTADOR:N'),
    y = alt.Y('sum_count:Q'),
    text=alt.Text('sum_count:Q', format='.0f'),
    color = alt.value("black"),
).transform_filter(alt.datum['RESPOSTA'] == "Acceptat i trasplantat").transform_aggregate(
    sum_count='count()',
    groupby=["HOSPITAL TRASPLANTADOR"]
)

final_propis = (chart_propis+text_propis).configure_axis(
    labelFontSize=18,
    titleFontSize=20
).configure_header(
    labelFontSize=18,
    titleFontSize=20
).configure_legend(labelLimit=500,labelFontSize=18,
    titleFontSize=20).configure_title( fontSize=28)

st.altair_chart(final_propis)
