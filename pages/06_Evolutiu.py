import pandas as pd
import csv
import altair as alt
import streamlit as st
from navigation import make_sidebar
alt.data_transformers.disable_max_rows()
st.set_page_config(
    page_title = "Evolució ofertes i trasplantaments 2023",
    layout = "wide"
)
make_sidebar()
st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)

data = pd.read_csv("PULMONS.csv", sep=";", header=0, quoting=csv.QUOTE_NONE,index_col=False, on_bad_lines="warn")
data['MONTH'] = pd.to_datetime(data['DATA'], format='%d/%m/%y').dt.month

mapping2 = {1: 'Gener', 2:'Febrer', 3: 'Març', 4: 'Abril', 5: 'Maig', 6: 'Juny', 7: 'Juliol', 8: 'Agost', 9:'Setembre', 10: 'Octubre', 11:'Novembre', 12:'Desembre'}
data['MES']=data['MONTH'].map(mapping2)
data['MES'] = pd.Categorical(data['MES'], categories=['Gener', 'Febrer', 'Març', 'Abril', 'Maig', 'Juny', 'Juliol', 'Agost', 'Setembre', 'Octubre', 'Novembre', 'Desembre'], ordered=True)


data.sort_values(by="MONTH", axis=0)
data['EXTRA'] ='Ofertes'

line = alt.Chart(data).mark_area().encode(
    x=alt.X('MES:O', title='Mes', axis=alt.Axis(labelAngle=0), sort=list(mapping2.values())),
    y = alt.Y('count():Q'),
    tooltip = ['MES:N',alt.Tooltip('count():Q', title='Valor')],
    color = alt.Color('EXTRA', scale = alt.Scale(domain=['Ofertes'], range=['#fdae61']), title='Categoria')
).properties(width=1000 ,title="")

data_ofertes = data[data['RESPOSTA']=="Acceptat i trasplantat"]
data_ofertes['EXTRA'] ='Trasplantaments'

line2 = alt.Chart(data_ofertes).mark_area(color='#b4deae').encode(
    x=alt.X('MES:O', title='Mes', axis=alt.Axis(labelAngle=0), sort=list(mapping2.values()) ),
    y = alt.Y('count():Q'), 
    tooltip = ['MES:N',alt.Tooltip('count():Q', title='Valor')],
    color = alt.Color('EXTRA', scale = alt.Scale(domain=['Trasplantaments'], range=['#b4deae']), title='Categoria')
).properties(width=1000 ,title="")

final = alt.layer(line,line2).configure_title( fontSize=26).resolve_scale(color='independent')


st.write("# Evolució ofertes i trasplantaments hospitals catalans 2023")
st.altair_chart(final)



urg = [45, 16]
Hospis = ['ONT', 'VH']
datos = pd.DataFrame()
datos['Hospital'] = Hospis
datos['count'] = urg
datos['code'] = [1,2]

chart = alt.Chart(datos).mark_bar(color='#3288bd').encode(
    x=alt.X('Hospital:N',  axis=alt.Axis(labelAngle=0), title="Hospital trasplantador", 
            scale=alt.Scale(domain=['ONT', 'VH'])),
    y=alt.Y('count:Q', title='Total'),
    tooltip = ['Hospital', alt.Tooltip('count:Q', title='Valor')],
    order = 'code:Q'
).properties(width=800 ,title="")

text_propis = alt.Chart(datos).mark_text(align='center', baseline='middle', dy=-10, fontSize=20).encode(
    x=alt.X('Hospital:N'),
    y = alt.Y('sum(count):Q'),
    text=alt.Text('sum(count):Q', format='.0f'),
    order = 'code:Q',
    color = alt.value("black"),
)

total = (chart+text_propis).configure_axis(
    labelFontSize=18,
    titleFontSize=20
).configure_header(
    labelFontSize=18,
    titleFontSize=20
).configure_legend(labelLimit=500,labelFontSize=18,
    titleFontSize=20).configure_title( fontSize=28)
st.write("# Total urgències 0 al 2023")
st.altair_chart(total)

