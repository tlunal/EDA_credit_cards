import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

import matplotlib.pyplot as plt
st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown("# Análisis de clientes Taiwaneses que incurrieron en impago en 2005")
st.title("Visualización de datos: Práctica II")
st.subheader("Por: Tomás Luna López")

st.markdown("### Veamos una muestra de nuestros datos")
# Cargar un archivo CSV precargado
df = pd.read_excel("default_credit_taiwan.xls", header=1)
st.dataframe(df.head())

bins = [20, 30, 40, 50, 60, 70, 80, 90, 100]
df['AGE_BINS'] = pd.cut(df['AGE'], bins)

columns_cat = ['SEX', 'EDUCATION', 'MARRIAGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 'default payment next month',
              'AGE_BINS']

columns_cat2 = ['default payment next month', 'SEX', 'EDUCATION', 'MARRIAGE', 'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6', 
              'AGE_BINS']

columns_num = ['LIMIT_BAL', 'AGE', 'BILL_AMT1', 'BILL_AMT2',
       'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1',
       'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6']

columns_num2 = ['AGE', 'BILL_AMT1', 'BILL_AMT2',
       'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6', 'PAY_AMT1',
       'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6', 'LIMIT_BAL']

df['SEX'].replace(1, 'Male', inplace=True)
df['SEX'].replace(2, 'Female', inplace=True)


df['EDUCATION'].replace(1, 'Graduate school', inplace=True)
df['EDUCATION'].replace(2, 'University', inplace=True)
df['EDUCATION'].replace(3, 'High school', inplace=True)
df['EDUCATION'].replace(4, 'Others', inplace=True)
df['EDUCATION'].replace(5, 'Others', inplace=True)
df['EDUCATION'].replace(6, 'Others', inplace=True)
df['EDUCATION'].replace(0, 'Others', inplace=True)



df['MARRIAGE'].replace(1, 'Married', inplace=True)
df['MARRIAGE'].replace(2, 'Single', inplace=True)
df['MARRIAGE'].replace(3, 'Others', inplace=True)
df['MARRIAGE'].replace(4, 'Others', inplace=True)
df['MARRIAGE'].replace(0, 'Others', inplace=True)


df['default payment next month'].replace(1, 'Yes', inplace=True)
df['default payment next month'].replace(0, 'No', inplace=True)


df[columns_cat] = df[columns_cat].astype('str')

df['AGE_BINS']=df['AGE_BINS'].astype('str')


df_num = df[columns_num].copy()
df_cat = df[columns_cat].copy()

st.markdown("### Análisis univariante")
# Seleccionar una columna para generar el gráfico
columnas = df_num.columns.tolist()
columna_x = st.selectbox("Selecciona una columna para x", columnas, key='columna_1')
#columna_y = st.selectbox("Selecciona una columna para y", columnas)
if columna_x:
    st.write("Gráfico de barras")
    fig = px.histogram(data_frame=df_num, x=columna_x, nbins=20)
    st.plotly_chart(fig)

columnas_cat = df_cat.columns.tolist()
columna_x2 = st.selectbox("Selecciona una columna para x", columnas_cat, key='columna_2')
if columna_x2:
    st.write("Gráfico de barras")
    fig = px.bar(df_cat[columna_x2].value_counts(), x=df_cat[columna_x2].value_counts().index, y=df_cat[columna_x2].value_counts().values)
    st.plotly_chart(fig)

    
st.markdown("### Análisis multivariante")

st.markdown("#### Heatmap correlación variables")

corr = df[columns_num].corr()

fig = go.Figure(data=go.Heatmap(z=corr, colorscale='Viridis', x=df[columns_num].columns, y=df[columns_num].columns))
st.plotly_chart(fig)




st.markdown("#### Variables numéricas")


columna_x4 = st.selectbox("Selecciona una columna para x", columns_num, key='columna_5')
columna_y2 = st.selectbox("Selecciona una columna para y", columns_num2, key='columna_6')
#columna_y = st.selectbox("Selecciona un filtro", columnas_cat, key='columna_4')


if columna_x4 and columna_y2:
    
    dfCategory = df.groupby([columna_x4,columna_y2])[columna_x4].count().reset_index(name="count")

    # Use that layout here
    
    fig = px.scatter(df[df['default payment next month'] == 'Yes'], x=columna_x4,
                   y=columna_y2,
                     color=df[df['default payment next month'] == 'Yes']['default payment next month'], opacity=0.3, color_discrete_sequence=px.colors.qualitative.Set1,
                   title= 'Clientes en default respecto a ' + columna_y2 + " y " + columna_x4)
    st.plotly_chart(fig)
    
    fig = px.scatter(df[df['default payment next month'] == 'No'], x=columna_x4,
                   y=columna_y2,
                     color=df[df['default payment next month'] == 'No']['default payment next month'], opacity=0.3, color_discrete_sequence=px.colors.qualitative.Plotly,
                   title= 'Clientes NO en default respecto a ' + columna_y2 + " y " + columna_x4)
    st.plotly_chart(fig)
    
    
    #fig = go.Figure(data=go.Heatmap(z=dfCategory, type='hex'))
    #st.plotly_chart(fig)


    plt.hexbin(df[columna_x4], df[columna_y2],gridsize=50, mincnt=1, edgecolors="none", cmap="plasma")
    
    plt.xlabel(columna_x4)
    plt.ylabel(columna_y2)
    plt.colorbar()
    
    st.pyplot()

    
st.markdown("#### Variables categóricas")



columna_x3 = st.selectbox("Selecciona una columna para x", columnas_cat, key='columna_3')
columna_y = st.selectbox("Selecciona una columna para y", columns_cat2, key='columna_4')

if columna_x3 and columna_y:
    
    dfCategory = df.groupby([columna_x3,columna_y])[columna_x3].count().reset_index(name="count")

    fig = px.histogram(dfCategory, x=columna_x3,
                   y="count", color=columna_y,
                   barnorm='percent', text_auto='.2f',
                   title="Porcentaje de categorías de " + columna_y + " por cada categoría de " + columna_x3)
    st.plotly_chart(fig)
    
if columna_x3 and columna_y:
    
    dfCategory = df.groupby([columna_x3,columna_y])[columna_x3].count().reset_index(name="count")

    fig = px.bar(dfCategory, x=columna_x3,
                   y="count", color=columna_y, barmode = 'group',
                   title="Freq. Absoluta de categorías de " + columna_y + " por cada categoría de " + columna_x3)
    st.plotly_chart(fig)
    
    
    
