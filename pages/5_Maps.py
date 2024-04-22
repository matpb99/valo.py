import base64
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
from sqlite3 import connect

def init_data():
    players_maps_data_df = pd.read_csv("player_data_by_map.csv")
    with open("last_update.txt", "r") as archivo:
        last_update = archivo.read()

    return players_maps_data_df, last_update

def init_conn(df):
    conn = connect(':memory:')
    df.to_sql(name='test_data', con=conn)
    return conn
        
def load_image(filename, folder):
    with open("./{}/{}.jpg".format(folder.lower(), filename.lower()), "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data

def draw_agent_map_composition(map_name):

    with st.container(border=True):

        st.title("{}".format(map_name))

        sql_query = """SELECT Agent, COUNT(Agent) AS Times, Role
        FROM test_data
        WHERE Map == "{}"
        GROUP BY Agent
        ORDER BY COUNT(Agent) DESC
        LIMIT 5;""".format(map_name)

        df_data = pd.read_sql(sql_query, conn)

        col1, col2, col3, col4, col5 = st.columns(5)
        col_list = [col1, col2, col3, col4, col5]
        aux = 0

        for col in col_list:
            agent, value = df_data["Agent"][aux], df_data["Times"][aux]
            title = str(agent).capitalize()
            text = ["{} Times Played in {} All VCTs".format(value, map_name.capitalize())]
            
            with col:
                card(
                    title = title,
                    text = text,
                    image = load_image(agent, "agents"),
                    styles={
                        "card": {
                            "width": "100%",
                            "height": "400px"
                                }
                            }
                    )
            aux+=1

        st.dataframe(df_data.head(5), hide_index=True, use_container_width=True)

st.set_page_config(layout = "wide", initial_sidebar_state = "auto", page_title = "Valo.py")
players_maps_data_df, last_update = init_data()
conn = init_conn(players_maps_data_df)

st.header('Valo.py', divider='blue')
st.subheader("_Last Update:_ :green[{}]".format(last_update))

st.title("Top Composition By Maps")

draw_agent_map_composition("Sunset")

draw_agent_map_composition("Lotus")

draw_agent_map_composition("Breeze")

draw_agent_map_composition("Icebox")

draw_agent_map_composition("Bind")

draw_agent_map_composition("Split")

draw_agent_map_composition("Ascent")