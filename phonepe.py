import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import plotly.express as px
import pandas as pd
import requests
import json
from PIL import Image

#SQL connection

mydb = psycopg2.connect(host = 'localhost',
                        user = 'postgres',
                        port = '5432',
                        password = 'NK19',
                        database = 'phonepe_data')
cursor = mydb.cursor()

#Data frame creaation

#Agge insurance df

cursor.execute("select * from aggregated_insurance")
mydb.commit()
table1 = cursor.fetchall()

Aggre_insurance = pd.DataFrame(table1, columns=("States", "Years", "Quarter", 'Transaction_type', 'Transaction_count', "Transaction_amount"))

#Agge trans df

cursor.execute("select * from aggregated_transaction")
mydb.commit()
table2 = cursor.fetchall()

Aggre_trans = pd.DataFrame(table2, columns=('States', 'Years', 'Quarter', 'Transaction_type', 'Transaction_count','Transaction_amount'))

#Agge user df

cursor.execute("select * from aggregated_user")
mydb.commit()
table3 = cursor.fetchall()

Aggre_user = pd.DataFrame(table3, columns=('States', 'Years', 'Quarter', 'Brand', 'Transaction_count', 'Percentage'))
Aggre_user['Percentage'] = Aggre_user['Percentage'] * 100

#map insurance df

cursor.execute("select * from map_insurance")
mydb.commit()
table4 = cursor.fetchall()

map_insurance = pd.DataFrame(table4, columns=('States', 'Years', 'Quarter', 'Districts', 'Transaction_count', 'Transaction_amount'))

#msp trans df

cursor.execute("select * from map_transaction")
mydb.commit()
table5 = cursor.fetchall()

map_transaction = pd.DataFrame(table5, columns=('States', 'Years', 'Quarter', 'Districts', 'Transaction_count', 'Transaction_amount'))

#map user df

cursor.execute("select * from map_user")
mydb.commit()
table6 = cursor.fetchall()

map_user = pd.DataFrame(table6, columns=('States', 'Years', 'Quarter', 'Districts', 'RegisteredUsers', 'AppOpens'))

#top insurance df

cursor.execute("select * from top_insurance")
mydb.commit()
table7 = cursor.fetchall()

top_insurance = pd.DataFrame(table7, columns=('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count', 'Transaction_amount'))

#top trans df

cursor.execute("select * from top_transaction")
mydb.commit()
table8 = cursor.fetchall()

top_transaction = pd.DataFrame(table8, columns=('States', 'Years', 'Quarter', 'Pincodes', 'Transaction_count', 'Transaction_amount'))

#top user df

cursor.execute("select * from top_user")
mydb.commit()
table9 = cursor.fetchall()

top_user = pd.DataFrame(table9, columns=('States', 'Years', 'Quarter', 'Pincodes', 'RegisteredUsers'))

#India map details

url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
response = requests.get(url)
data1 = json.loads(response.content)
states_name = []
for feature in data1['features']:
    states_name.append(feature['properties']['ST_NM'])
states_name.sort()

#gtrans amount and count based on year

def Transaction_amount_count_Y(df, year):
    tacy = df[df['Years'] == year]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(tacyg, x= 'States', y= 'Transaction_amount', title= f'{year} TRANSATION AMOUNT',
                            color_discrete_sequence= px.colors.sequential.Aggrnyl, height= 650, width= 600)
        
        st.plotly_chart(fig_amount)

        fig_india_1 = px.choropleth(tacy, geojson= data1, locations= 'States', featureidkey= 'properties.ST_NM',
                                    color= 'Transaction_amount', color_continuous_scale= 'Rainbow',
                                    range_color= (tacyg['Transaction_amount'].min(), tacyg['Transaction_amount'].max()),
                                    hover_name= 'States', title= f'{year} TRANSACTION AMOUNT', fitbounds= 'locations', height= 650, width= 600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_count = px.bar(tacyg, x= 'States', y = 'Transaction_count', title= f'{year} TRANSACTION AMOUNT',
                           color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)
        
        st.plotly_chart(fig_count)

        fig_india_2 = px.choropleth(tacyg, geojson= data1, locations= 'States', featureidkey= 'properties.ST_NM',
                                    color= 'Transaction_count', color_continuous_scale= 'Rainbow',
                                    range_color= (tacyg['Transaction_count'].min(), tacyg['Transaction_count'].max()), hover_name= 'States',
                                    title= f'{year} TRANSACTION COUNT', fitbounds= 'locations', height= 650, width= 600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
    return tacy

#trans amount count by year and quater

def Transaction_amount_count_Y_Q(df, quarter):
    tacy = df[df['Quarter'] == quarter]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby('States')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(tacyg, x= 'States', y= 'Transaction_amount', title= f"{tacy['Years'].min()} YEAR {quarter} TRANSATION AMOUNT",
                            color_discrete_sequence= px.colors.sequential.Aggrnyl, height= 650, width= 600)
        
        st.plotly_chart(fig_amount)
    
        fig_india_1 = px.choropleth(tacyg, geojson= data1, locations= 'States', featureidkey= 'properties.ST_NM',
                                    color= 'Transaction_amount', color_continuous_scale= 'Rainbow',
                                    range_color= (tacyg['Transaction_amount'].min(), tacyg['Transaction_amount'].max()),
                                    hover_name= 'States', title= f"{tacy['Years'].min()} YEAR {quarter} QUATER TRANSATION AMOUNT",
                                    fitbounds= 'locations', height= 650, width= 600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_count = px.bar(tacyg, x= 'States', y = 'Transaction_count', title= f"{tacy['Years'].min()} YEAR {quarter} TRANSACTION COUNT",
                           color_discrete_sequence= px.colors.sequential.Bluered_r, height= 650, width= 600)
        st.plotly_chart(fig_count)
        fig_india_2 = px.choropleth(tacyg, geojson= data1, locations= 'States', featureidkey= 'properties.ST_NM', color= 'Transaction_count',
                                    color_continuous_scale= 'Rainbow', range_color= (tacyg['Transaction_count'].min(), tacyg['Transaction_count'].max()),
                                    hover_name= 'States', title= f"{tacy['Years'].min()} YEAR {quarter} QUATER TRANSACTION COUNT", fitbounds= 'locations',
                                    height= 650, width= 600)
        
        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)
    
    return tacy

#Aggre_Tran_Transaction_type

def Aggre_Tran_Transaction_type(df, state):
    tacy = df[df['States'] == state]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby('Transaction_type')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        fig_pie_1 = px.pie(data_frame= tacyg, names= 'Transaction_type', values= 'Transaction_amount', width= 600,
                           title= f"{state.upper()} TRANSACTION AMOUNT", hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2 = px.pie(data_frame= tacyg, names= 'Transaction_type', values= 'Transaction_count', width= 600,
                           title= f"{state.upper()} TRANSACTION COUNT", hole= 0.5)
        st.plotly_chart(fig_pie_2)
    
#Agger user plot 1

def Aggre_user_plot_1(df, year):
    aguy = df[df['Years'] == year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg = pd.DataFrame(aguy.groupby(['Brand'])['Transaction_count'].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1 = px.bar(data_frame= aguyg, x= 'Brand', y= 'Transaction_count', title= f'{year} BRANDS AND TRANSACTION COUNT',
                       width= 1000, color_discrete_sequence= px.colors.sequential.haline_r, hover_name= 'Brand')
    st.plotly_chart(fig_bar_1)

    return aguy

#Agger user plot 2

def Aggre_user_plot_2(df,quater):
    aguyq = df[df['Quarter'] == quater]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg = pd.DataFrame(aguyq.groupby(['Brand'])['Transaction_count'].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1 = px.bar(data_frame= aguyqg, x= 'Brand', y= 'Transaction_count', title= f'{quater} QUARTER, BRANDS AND TRANSACTION COUNT',
                       width= 1000, color_discrete_sequence= px.colors.sequential.Magenta_r, hover_name= 'Brand')
    st.plotly_chart(fig_bar_1)

    return aguyq

#Agger user with state

def Aggre_user_plot_3(df, state):
    aguyqs = df[df['States'] == state]
    aguyqs.reset_index(drop= True, inplace= True)

    fig_line_1 = px.line(data_frame= aguyqs, x= 'Brand', y= 'Transaction_count', hover_data= {'Percentage': ':.2f'},
                         title= 'BRANDS TRANSATION COUNT WITH PERCENTAGE', width= 1000, markers= True)
    st.plotly_chart(fig_line_1)

#Map insurance district 

def map_insur_district(df, state):
    tacy = df[df['States'] == state]
    tacy.reset_index(drop= True, inplace= True)

    tacyg = tacy.groupby('Districts')[['Transaction_count','Transaction_amount']].sum()
    tacyg.reset_index(inplace= True)

    col1, col2 = st.columns(2)
    with col1:
        fig_bar_1 = px.bar(data_frame= tacyg, x= 'Transaction_amount', y= 'Districts', orientation= "h", height= 600,
                           title= f"{state.upper()}'S DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2 = px.bar(data_frame= tacyg, x= 'Transaction_count', y= 'Districts', orientation= "h", height= 600,
                           title= f"{state.upper()}'S DISTRICT AND TRANSACTION COUNT", color_discrete_sequence= px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)

#map user plot 1

def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x= "States", y= ["RegisteredUsers", "AppOpens"], title= f"{year} REGISTERED USER, APPOPENS",
                        width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

#map user plot 2

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUsers", "AppOpens"], title= f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USER, APPOPENS",
                        width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muyq

#Map user plot 3

def map_user_plot_3(df, states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        fig_map_user_bar_1 = px.bar(muyqs, x= "RegisteredUsers", y= 'Districts', orientation= 'h', title= f"{states.upper()} REGISTERED USER", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2 = px.bar(muyqs, x= "AppOpens", y= 'Districts', orientation= 'h', title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

#top insurance plot

def top_insur_plot_1(df, states):
    tiy= df[df["States"]== states]
    tiy.reset_index(drop= True, inplace= True)

    col1, col2 = st.columns(2)

    with col1:
        fig_top_insur_bar_1 = px.bar(tiy, x= 'Quarter', y= 'Transaction_amount' , hover_data= ['Pincodes'], title= f"REGISTERED USER", height= 650, width= 600, color_discrete_sequence= px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_insur_bar_1)

    with col2:
        fig_top_insur_bar_2= px.bar(tiy, x= "Quarter", y= "Transaction_count", hover_data= ['Pincodes'], title= "TRANSACTION COUNT", height= 650,width= 600, color_discrete_sequence= px.colors.sequential.Agsunset_r)
        st.plotly_chart(fig_top_insur_bar_2)


#Top user 1

def top_user_plot_1(df, year):
    tuy = df[df['Years'] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg = pd.DataFrame(tuy.groupby(['States', 'Quarter'])['RegisteredUsers', 'Pincodes'].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1 = px.bar(tuyg, x= 'States', y= 'RegisteredUsers', color= 'Quarter', width= 1000, height= 800, color_discrete_sequence= px.colors.sequential.Burgyl, hover_name= tuyg['States'], title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


#top user 2

def top_user_plot_2(df, state):
    tuys = df[df['States'] == state]
    tuys.reset_index(drop= True, inplace= True)

    fig_top_plot_1 = px.bar(tuys, x= 'Quarter', y= 'RegisteredUsers', title= 'State', width= 1000, height= 800, color= 'RegisteredUsers', hover_data= ['Pincodes'], color_continuous_scale = px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)


def top_chart_transaction_amount(table_name):
    #plot_1
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))
    
    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)



def top_chart_transaction_count(table_name):
    #plot_1
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)



def top_chart_registered_user(table_name, state):
    #plot_1
    query1= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "registereduser"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="registereduser", title="TOP 10 OF REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "registereduser"))

    fig_amount_3= px.bar(df_3, y="districts", x="registereduser", title="AVERAGE OF REGISTERED USER", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


def top_chart_appopens(table_name, state):
    #plot_1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("districts", "appopens"))


    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("districts", "appopens"))

    with col2:

        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title="LAST 10 APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)


def top_chart_registered_users(table_name):
    #plot_1
    query1= f'''SELECT states, SUM({table_name}.registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers DESC
                LIMIT 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1= pd.DataFrame(table_1, columns=("states", "registeredusers"))
    
    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(df_1, x="states", y="registeredusers", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2= pd.DataFrame(table_2, columns=("states", "registeredusers"))

    with col2:

        fig_amount_2= px.bar(df_2, x="states", y="registeredusers", title="LAST 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(registeredusers) AS registeredusers
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "registeredusers"))

    fig_amount_3= px.bar(df_3, y="states", x="registeredusers", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)



#streamlit part

st.set_page_config(layout= 'wide')
st.title("PhonePe data Visualization and Exploration")

with st.sidebar:
    
    select = option_menu("Main Menu", ['Home', 'Data Exploration', 'Top Charts'])

if select == 'Home':

    col1,col2= st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.write("This Streamlit application is developed only for educational purposes")
        st.write("PhonePe is a comprehensive digital payments platform that enables users to make payments, transfer money, recharge mobile phones, pay utility bills, shop online, and more, directly from their smartphones. Built on the Unified Payments Interface (UPI) platform, PhonePe allows users to make instant bank-to-bank transfers using their mobile numbers linked with their bank accounts. The app also offers features like bill payments, online shopping, split bills, request money, investments, insurance, credit services, QR code payments, and various cashback offers and discounts. Overall, PhonePe provides a seamless and convenient digital payments experience to its users.")
        st.markdown("[Click here to visit PhonePe's website](https://www.phonepe.com/)")

    with col2:
        st.image(Image.open(r"C:/Users/91807/Downloads/56e754191495401.Y3JvcCwxMDI4LDgwNCwyNSwxMzc.png"),width= 600)

    col3,col4= st.columns(2)
    with col3:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.image(Image.open(r"C:/Users/91807/Downloads/10-types-of-data-visualization-1-1024x614.jpg"),width= 600)

    with col4:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****Dynamic data visualization****")
        st.write("****Interactive charts and graphs****")
        st.write("****Real-time data updates****")
        st.write("****Customizable dashboard****")
        st.write("****User-friendly interface****")
        st.write("****Seamless integration with Python****")
        st.write("****Responsive design for various devices****")
        st.write("****Intuitive user interactions****")
        st.write("****Quick prototyping and development****")



    col5,col6= st.columns(2)
    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****Developed only for educational purposes****")
        st.write("****Developed by NK19****")

elif select == 'Data Exploration':
    tab1, tab2, tab3 = st.tabs(['Aggregated Analysis','Map Analysis', 'Top Analysis'])



    with tab1:
        method = st.radio("Select the method given bellow:",['Aggregated Insurance Analysis', 'Aggregated Transaction Analysis', 'Aggregated User Analysis'])

        if method == 'Aggregated Insurance Analysis':
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the year", Aggre_insurance['Years'].min(), Aggre_insurance['Years'].max(), Aggre_insurance['Years'].min())
            tac_y = Transaction_amount_count_Y(Aggre_insurance, years)
            
            #here the col1 and col2 is again reassigned because, to get the slider below the year plots
            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the quarter", tac_y['Quarter'].min(), tac_y['Quarter'].max(), tac_y['Quarter'].min())
            Transaction_amount_count_Y_Q(tac_y, quarters)

        elif method == 'Aggregated Transaction Analysis':
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year", Aggre_trans['Years'].min(), Aggre_trans['Years'].max(), Aggre_trans['Years'].min())
            Aggre_tran_tac_y = Transaction_amount_count_Y(Aggre_trans, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", Aggre_tran_tac_y['States'].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter", Aggre_tran_tac_y['Quarter'].min(), Aggre_tran_tac_y['Quarter'].max(), Aggre_tran_tac_y['Quarter'].min())
            Aggre_tran_tac_y_Q = Transaction_amount_count_Y_Q(Aggre_tran_tac_y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State based on Quarter", Aggre_tran_tac_y_Q['States'].unique())
            Aggre_Tran_Transaction_type(Aggre_tran_tac_y_Q, states)

        elif method == 'Aggregated User Analysis':
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year", Aggre_user['Years'].min(), Aggre_user['Years'].max(), Aggre_user['Years'].min())
            Aggre_user_Y = Aggre_user_plot_1(Aggre_user, years)

            col1, col2 = st.columns(2)
            with col1:
                quater = st.slider("Select the Quarter", Aggre_user_Y['Quarter'].min(), Aggre_user_Y['Quarter'].max(), Aggre_user_Y['Quarter'].min())
            Aggre_user_Y_Q = Aggre_user_plot_2(Aggre_user_Y, quater)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State based on Quarter", Aggre_user_Y_Q['States'].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)



    
    with tab2:
        method = st.radio("Select the method given bellow:",['Map Insurance Analysis', 'Map Transaction Analysis', 'Map User Analysis'])

        if method == 'Map Insurance Analysis':
            col1, col2 = st.columns(2)
            
            with col1:
                years = st.slider("Select the year ", map_insurance['Years'].min(), map_insurance['Years'].max(), map_insurance['Years'].min())
            map_insur_tac_Y = Transaction_amount_count_Y(map_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", map_insur_tac_Y['States'].unique())
            map_insur_district(map_insur_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter", map_insur_tac_Y['Quarter'].min(), map_insur_tac_Y['Quarter'].max(), map_insur_tac_Y['Quarter'].min())
            map_insur_tac_Y_Q = Transaction_amount_count_Y_Q(map_insur_tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State based on Quarter", map_insur_tac_Y_Q['States'].unique())
            map_insur_district(map_insur_tac_Y_Q, states)



        elif method == 'Map Transaction Analysis':

            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year ", map_transaction['Years'].min(), map_transaction['Years'].max(), map_transaction['Years'].min())
            map_tran_tac_Y = Transaction_amount_count_Y(map_transaction, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", map_tran_tac_Y['States'].unique())
            map_insur_district(map_tran_tac_Y, states)

            col1, col2 = st.columns(2)
            with col1:
                quarters = st.slider("Select the Quarter", map_tran_tac_Y['Quarter'].min(), map_tran_tac_Y['Quarter'].max(), map_tran_tac_Y['Quarter'].min())
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State based on Quarter", map_tran_tac_Y_Q['States'].unique())
            map_insur_district(map_tran_tac_Y_Q, states)



        elif method == 'Map User Analysis':
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year ", map_user['Years'].min(), map_user['Years'].max(), map_user['Years'].min())
            map_user_Y = map_user_plot_1(map_user, years)


            col1,col2= st.columns(2)
            with col1:
                quarter = st.slider("Select The Quarter ",map_user_Y["Quarter"].min(), map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot_2(map_user_Y, quarter)


            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State based on Quarter", map_user_Y_Q['States'].unique())
            map_user_plot_3(map_user_Y_Q, states)



    with tab3:
        method = st.radio("Select the method given bellow:",['Top Insurance Analysis', 'Top Transaction Analysis', 'Top User Analysis'])



        if method == 'Top Insurance Analysis':
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year ", top_insurance['Years'].min(), top_insurance['Years'].max(), top_insurance['Years'].min())
            top_insur_tac_Y = Transaction_amount_count_Y(top_insurance, years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", top_insur_tac_Y['States'].unique())
            top_insur_plot_1(top_insur_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:
                quarter = st.slider("Select The Quarter ",top_insur_tac_Y["Quarter"].min(), top_insur_tac_Y["Quarter"].max(),top_insur_tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(top_insur_tac_Y, quarter)



        elif method == 'Top Transaction Analysis':
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year", top_transaction['Years'].min(), top_transaction['Years'].max(), top_transaction['Years'].min())
            top_trans_tac_Y = Transaction_amount_count_Y(top_transaction, years)

            
            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", top_trans_tac_Y['States'].unique())
            top_insur_plot_1(top_trans_tac_Y, states)


            col1,col2= st.columns(2)
            with col1:
                quarter = st.slider("Select The Quarter",top_trans_tac_Y["Quarter"].min(), top_trans_tac_Y["Quarter"].max(),top_trans_tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(top_trans_tac_Y, quarter)



        elif method == 'Top User Analysis':
            
            col1, col2 = st.columns(2)
            with col1:
                years = st.slider("Select the year", top_user['Years'].min(), top_user['Years'].max(), top_user['Years'].min())
            top_user_Y = top_user_plot_1(top_user, years)


            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select the State", top_user_Y['States'].unique())
            top_user_plot_2(top_user_Y, states)



elif select == 'Top Charts':
    question = st.selectbox("Select the Questions", ["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. App opens of Map User",
                                                    "9. Registered users of Top User",])


    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_amount("aggregated_insurance")


    elif question == "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")
    
    elif question == "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. App opens of Map User":
        
        states= st.selectbox("Select the State", map_user["States"].unique())   
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif question == "9. Registered users of Top User":
          
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")



