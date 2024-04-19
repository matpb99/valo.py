import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from streamlit_card import card
import base64

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")


def load_image(filename, folder):
    with open("./{}/{}.jpg".format(folder.lower(), filename.lower()), "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data)
    data = "data:image/png;base64," + encoded.decode("utf-8")
    return data

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################


st.header('Valo.py', divider='blue')
st.subheader('_Website_ :blue[to know all about competitive Valorant] :red[road to Champions 2024] Last Update: ')

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):

        most_rating = pd.read_csv("./outputs/players/most_rating.csv")

        player, rating = most_rating["Name"][0], most_rating["Rating"][0]
    
        player_rating = card(
        title = str(player).capitalize(),
        text = [str(rating)+" Rating", "Most Rating in All VCTs"],
        image = load_image(player, "players"),
        styles={
            "card": {
                "width": "100%",
                "height": "400px"
                    }
        }
        )
        
        st.dataframe(most_rating.head(5), hide_index=True, use_container_width=True)

with col2:
    with st.container(border=True):

        most_acs = pd.read_csv("./outputs/players/most_acs.csv")

        player, acs = most_acs["Name"][0], most_acs["ACS"][0]
    
        player_acs = card(
        title = str(player).capitalize(),
        text = [str(acs)+" ACS", "Most Average Combat Score in All VCTs"],
        image = load_image(player, "players"),
        styles={
            "card": {
                "width": "100%",
                "height": "500px"
                    }
                }
                        )

        with st.expander("Show Ranking"):
    
            st.dataframe(most_acs.head(5), hide_index=True, use_container_width=True)

with col3:
    with st.container(border=True):
    
        most_kills = pd.read_csv("./outputs/players/most_kills.csv")

        player, kills = most_kills["Name"][0], most_kills["Kills"][0]
    
        player_kills = card(
        title = str(player).capitalize(),
        text = [str(kills)+" Kills", "Most Kills in All VCTs"],
        image = load_image(player, "players"),
        styles={
            "card": {
                "width": "100%",
                "height": "450px"
                    }
        }
        )

        st.dataframe(most_kills.head(5), hide_index=True, use_container_width=True)

with col4:
    with st.container(border=True):
        most_assists = pd.read_csv("./outputs/players/most_assists.csv")

        player, assists = most_assists["Name"][0], most_assists["Assists"][0]
    
        player_assists = card(
        title = str(player).capitalize(),
        text = [str(assists)+" Assists", "Most Assists in All VCTs"],
        image = load_image(player, "players"),
        styles={
            "card": {
                "width": "100%",
                "height": "500px"
                    }
        }
        )

        st.dataframe(most_assists.head(5), hide_index=True, use_container_width=True)


###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Teams")

col5, col6, col7, col8 = st.columns(4)


with col5:
    
    most_rating = pd.read_csv("./outputs/teams/most_rating.csv")

    team, rating = most_rating["Team"][0], most_rating["Rating"][0]
  
    team_rating = card(
    title = str(team).upper(),
    text = [str(rating)+" Rating", "Most Team Rating in All VCTs"],
    image = load_image(team, "teams"),
    styles={
        "card": {
            "width": "100%",
            "height": "500px"
                }
    }
    )

    st.dataframe(most_rating.head(5), hide_index=True, use_container_width=True)

with col6:
    
    most_acs = pd.read_csv("./outputs/teams/most_acs.csv")

    team, acs = most_acs["Team"][0], most_acs["ACS"][0]
  
    team_acs = card(
    title = str(team).upper(),
    text = [str(acs)+" ACS", "Most Team Average Combat Score in All VCTs"],
    image = load_image(team, "teams"),
    styles={
        "card": {
            "width": "100%",
            "height": "500px"
                }
    }
    )

    st.dataframe(most_acs.head(5), hide_index=True, use_container_width=True)

with col7:
    
    most_kills = pd.read_csv("./outputs/teams/most_kills.csv")

    team, kills = most_kills["Team"][0], most_kills["Kills"][0]
  
    team_kills = card(
    title = str(team).upper(),
    text = [str(kills)+" Kills", "Most Team Kills in All VCTs"],
    image = load_image(team, "teams"),
    styles={
        "card": {
            "width": "100%",
            "height": "400px"
                }
    }
    )

    st.dataframe(most_kills.head(5), hide_index=True, use_container_width=True)

with col8:
    
    most_assists = pd.read_csv("./outputs/teams/most_assists.csv")

    team, assists = most_assists["Team"][0], most_assists["Assists"][0]
  
    team_assists = card(
    title = str(team).upper(),
    text = [str(assists)+" Assists", "Most Team Assists in All VCTs"],
    image = load_image(team, "teams")
    )

    st.dataframe(most_assists.head(5), hide_index=True, use_container_width=True)


###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

st.title("Top Players in One Match")

col13, col14, col15, col16 = st.columns(4)


with col13:
    
    most_rating = pd.read_csv("./outputs/matches/players/most_rating.csv")

    player, rating, matchteams = most_rating["Name"][0], most_rating["Rating"][0], most_rating["MatchTeams"][0]
  
    player_rating_match = card(
    title = str(player).capitalize(),
    text = [str(rating)+" Rating", "Most Rating in One Match in All VCTs", matchteams],
    image = load_image(player, "players")
    )

    st.dataframe(most_rating.head(5), hide_index=True, use_container_width=True)

with col14:
    
    most_kills = pd.read_csv("./outputs/matches/players/most_kills.csv")

    player, kills, matchteams = most_kills["Name"][0], most_kills["Kills"][0], most_kills["MatchTeams"][0]
  
    player_kill_match = card(
    title = str(player).capitalize(),
    text = [str(kills)+" Kills", "Most Kills in One Match in All VCTs", matchteams],
    image = load_image(player, "players")
    )

    st.dataframe(most_kills.head(5), hide_index=True, use_container_width=True)

with col15:
    
    most_hs = pd.read_csv("./outputs/matches/players/most_hs.csv")

    player, hs, matchteams = most_hs["Name"][0], most_hs["HS Rate"][0], most_hs["MatchTeams"][0]
  
    player_hs_match = card(
    title = str(player).capitalize(),
    text = [str(hs)+" HS Rate", "Most HS Rate in One Match in All VCTs", matchteams],
    image = load_image(player, "players")
    )

    st.dataframe(most_hs.head(5), hide_index=True, use_container_width=True)


with col16:
    
    most_fk = pd.read_csv("./outputs/matches/players/most_fk.csv")

    player, fk, matchteams = most_fk["Name"][0], most_fk["First Kills"][0], most_fk["MatchTeams"][0]
  
    player_fk_match = card(
    title = str(player).capitalize(),
    text = [str(fk)+" First Kills", "Most First Kills in One Match in All VCTs", matchteams],
    image = load_image(player, "players")
    )

    st.dataframe(most_fk.head(5), hide_index=True, use_container_width=True)


###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################


st.title("Top Players in One Single Map")

col9, col10, col11, col12 = st.columns(4)


with col9:
    
    most_rating = pd.read_csv("./outputs/maps/players/most_rating.csv")

    player, rating, map_name, matchteams = most_rating["Name"][0], most_rating["Rating"][0], most_rating["Map"][0], most_rating["MatchTeams"][0]
  
    player_rating_map = card(
    title = str(player).capitalize(),
    text = [str(rating)+" Rating", "Most Rating in One Single Map in All VCTs", map_name, matchteams],
    image = load_image(player, "players")
    )

    st.dataframe(most_rating.head(5), hide_index=True, use_container_width=True)

with col10:
    
    most_kills = pd.read_csv("./outputs/maps/players/most_kills.csv")

    player, kills, map_name, matchteams = most_kills["Name"][0], most_kills["Kills"][0], most_kills["Map"][0], most_kills["MatchTeams"][0]
  
    player_kill_map = card(
    title = str(player).capitalize(),
    text = [str(kills)+" Kills", "Most Kills in One Single Map in All VCTs", map_name, matchteams],
    image = load_image(player, "players")
    )

    st.dataframe(most_kills.head(5), hide_index=True, use_container_width=True)

with col11:
    
    most_hs = pd.read_csv("./outputs/maps/players/most_hs.csv")

    player, hs, map_name, matchteams = most_hs["Name"][0], most_hs["HS Rate"][0], most_hs["Map"][0], most_hs["MatchTeams"][0]
  
    player_hs_map = card(
    title = str(player).capitalize(),
    text = [str(hs)+" HS Rate", "Most HS Rate in One Single Map in All VCTs", map_name, matchteams],
    image = load_image(player, "players")
    )

    st.dataframe(most_hs.head(5), hide_index=True, use_container_width=True)

with col12:
    
    most_fk = pd.read_csv("./outputs/maps/players/most_fk.csv")

    player, fk, map_name, matchteams = most_fk["Name"][0], most_fk["First Kills"][0], most_fk["Map"][0], most_fk["MatchTeams"][0]
  
    player_fk_map = card(
    title = str(player).capitalize(),
    text = [str(fk)+" First Kills", "Most First Kills in One Single Map in All VCTs", map_name, matchteams],
    image = load_image(player, "players")
    )

    st.dataframe(most_fk.head(5), hide_index=True, use_container_width=True)

###############################################################################################################################################################################################################
###############################################################################################################################################################################################################
###############################################################################################################################################################################################################

