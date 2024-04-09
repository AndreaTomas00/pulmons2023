import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar
alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Ofertes",
    layout = "wide"
)
make_sidebar()
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Global ofertes pulmonars")

data = pd.read_csv("PULMONS.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")


color_scale = alt.Scale(domain=['Acceptat i trasplantat', 'Acceptat i no trasplantat',
                                'No acceptat'],
                        range=['#09AC42', '#A9EAC0', '#AC220F'])



# Create the bar chart
chart_propis = alt.Chart(data).mark_bar().encode(
    x=alt.X('HOSPITAL TRASPLANTADOR:N', title='Hospital', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('count():Q', title='Acumulatiu'),
    color=alt.Color('RESPOSTA:N', scale=color_scale, title='Categoria'),
).properties(
    width=700,
    height=600,
)

data_grouped = data.groupby(["HOSPITAL TRASPLANTADOR"]).size().reset_index(name='count')

text_propis = alt.Chart(data_grouped).mark_text(align='center', baseline='middle', dy=-8, fontSize=16).encode(
    x="HOSPITAL TRASPLANTADOR:N",
    y = 'count:Q',
    text=alt.Text('count:Q', format='.0f'),
    color = alt.value("black"),
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
