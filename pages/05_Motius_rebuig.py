import pandas as pd
import csv
import altair as alt
from navigation import make_sidebar
import streamlit as st
alt.data_transformers.disable_max_rows()

st.set_page_config(
    page_title = "Motius pulmons rebutjats",
    layout = "wide"
)
make_sidebar()
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Causes rebuig / no trasplantament")

data = pd.read_csv("rebutjats2.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")

color_scale = alt.Scale(domain=['Alteració prova imatge', 'Manca receptor compatible', 'Logística', 'Diferència mida', 
          'Crossmatch + ', 'Gasometria', 'Infecció respiratòria', 'Antecedents', 'Edat'], range =[  # blue
    '#d53e4f',  # orange
    '#f46d43',  # green
    '#fdae61',  # red
    '#fee08b',  # purple # brown
    '#e0ee97',  # pink
    '#b4deae',  # gray
    '#66c2a5', 
    '#3288bd',
     '#5e4fa2' # olive
])

causes_order = ['Alteració prova imatge', 'Manca receptor compatible', 'Logística', 'Diferència mida', 
          'Crossmatch + ', 'Gasometria', 'Infecció respiratòria', 'Antecedents', 'Edat']


# Create the bar chart
chart_propis = alt.Chart(data).mark_bar().encode(
    y=alt.Y('Causa:N', title='', sort=causes_order),
    x=alt.X('count:Q', title='Acumulatiu'),
    color=alt.Color('Causa:N', scale=color_scale, title='Categoria', legend=None),
    tooltip=['Causa', alt.Tooltip('count:Q', title='Valor')]
).properties(
    width=1000,
    height=450,
)

text_propis = alt.Chart(data).mark_text(align='center', baseline='middle', dx=12, fontSize=20).encode(
    y=alt.Y('Causa:N', sort=causes_order),
    x = alt.X('count:Q'),
    text=alt.Text('count:Q', format='.0f'),
    color = alt.value("black"),
)

final_propis = (chart_propis+text_propis).configure_axis(
    labelFontSize=18,
    titleFontSize=20,
    labelLimit=1000 
).configure_header(
    labelFontSize=18,
    titleFontSize=20
).configure_title( fontSize=28)

st.altair_chart(final_propis)
