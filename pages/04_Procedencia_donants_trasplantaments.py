import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar
alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Procedència ofertes pulmonars",
    layout = "wide"
)
make_sidebar()

st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)
st.write("# Procedència donants trasplantaments pulmonars")

data = pd.read_csv("PULMONS.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")

data = data[data["RESPOSTA"]=="Acceptat i trasplantat"]

color_scale = alt.Scale(domain=['Acceptat i trasplantat', 'Acceptat i no trasplantat',
                                'No acceptat'],
                        range=['#09AC42', '#A9EAC0', '#AC220F'])

color_procedencia = alt.Scale(domain=[ 'Pool', 'Propi',  'Balears', 'ONT'],
                        range=['#FF8000', '#FFD966',   '#BBD2EC', '#3E77B6'], 
                        )
orden = ["Propi", "Pool", "ONT", "Balears", "FOEDUS"]
sortt = ["OCATT", "ONT", "FOEDUS"]
# Create the bar chart
chart_propis = alt.Chart(data).mark_bar().encode(
    x=alt.X('ORGANITZACIÓ:N', title='Organització de procedència', axis=alt.Axis(labelAngle=0), scale=alt.Scale(domain=["OCATT", "ONT"])),
    y=alt.Y('count():Q', title='Acumulatiu'),
    color=alt.Color('ORGANITZACIÓ2:N', scale=color_procedencia, sort= alt.Sort('descending'),  title='Categoria'),
    tooltip = [alt.Tooltip('ORGANITZACIÓ2:N', title='Procedència'), alt.Tooltip('count():Q', title='Valor')],
    order="orden:Q"
).properties(
    width=900,
    height=600,
)


# text = chart_propis.mark_text(color='red',align='center', baseline='middle', 
#     dy=35, fontSize=20).encode(
#     text=alt.Text('count():Q', format='.0f'),
#     detail='ORGANITZACIÓ2:N',
# )
text_propis = alt.Chart(data).mark_text(align='center', baseline='middle', dy=-10, fontSize=20).encode(
    x=alt.X('ORGANITZACIÓ:N'),
    y = alt.Y('count():Q'),
    text=alt.Text('count():Q', format='.0f'),
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
