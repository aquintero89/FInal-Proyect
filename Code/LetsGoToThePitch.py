import streamlit as st
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min, pairwise_distances
import difflib
import base64
from fuzzywuzzy import process


# Suppress the deprecation warning related to file upload encoding
st.set_option('deprecation.showfileUploaderEncoding', False)

# Lets go with the Dataset
Fifa22 = pd.read_csv('PAGES/Fifa2022.csv')

attributes = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'attacking_crossing',
              'attacking_finishing', 'attacking_heading_accuracy', 'attacking_short_passing', 'attacking_volleys',
              'skill_dribbling', 'skill_curve', 'skill_fk_accuracy', 'skill_long_passing', 'skill_ball_control',
              'movement_acceleration', 'movement_sprint_speed', 'movement_agility', 'movement_reactions',
              'movement_balance', 'power_shot_power', 'power_jumping', 'power_stamina', 'power_strength',
              'power_long_shots', 'mentality_aggression', 'mentality_interceptions', 'mentality_positioning',
              'mentality_vision', 'mentality_penalties', 'defending_marking_awareness', 'defending_standing_tackle',
              'defending_sliding_tackle']

# Dataset with the selected attributes
X = Fifa22[attributes]

# KMeans object and fit the model
X_array = np.array(X)
kmeans = KMeans(n_clusters=29, random_state=0, n_init=10).fit(X_array)


# Adding the information to the app

# Lets start with the background image:

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpeg"};base64,{encoded_string.decode()});
            background-size: cover
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg_from_local('Images/campo.jpg')


st.markdown(
    f'<h1 style="font-size:60px">PlayPRO Analytics</h1>',
    unsafe_allow_html=True
)

# Now the beatiful code:

# Input field for the player name
player_name = st.text_input("Enter the name of the player you want to compare:")

if not player_name:
    st.warning("Please enter a player name.")
    st.stop()

top_5_players = pd.DataFrame() # initialize the variable


# Search for the player with the exact name
chosen_player = Fifa22[Fifa22["long_name"] == player_name]
if len(chosen_player) != 1:
    # No player found with exact name, look for similar names
    similar_players = process.extract(player_name, Fifa22["long_name"], limit=5)
    st.warning(f"No player found with the name '{player_name}'. Did you mean one of these?")
    for i, (similar_name, score, index) in enumerate(similar_players):
        st.write(f"{i+1}: {similar_name}")
    player_index = st.text_input("Enter the index of the correct player from the list above:")
    try:
        chosen_player_index = int(player_index) - 1
        chosen_player = Fifa22.loc[similar_players[chosen_player_index][2]]
    except (ValueError, IndexError):
        st.warning("Please enter a valid index, it has to be a number from 1 to 5.")
        st.stop()
else:
    # Handle case where only one player has the exact name entered by the user
    chosen_player_index = chosen_player.index[0]
    chosen_player = chosen_player.iloc[0]

# Update chosen_player_image, chosen_player_logo, and chosen_player_nationality
chosen_player_image = chosen_player["player_face_url"]
chosen_player_logo = chosen_player["club_logo_url"]
chosen_player_nationality = chosen_player["nation_flag_url"]

player_attributes = chosen_player[attributes]
chosen_player_name = chosen_player["long_name"]


# Display the player's name, image, and attributes

st.write(f"<p style='font-size: 24px; font-weight: bold;'>{'Your chosen player is: '}</p>", unsafe_allow_html=True)
st.write(f"<p style='font-size: 28px; font-weight: bold;'>{chosen_player_name}</p>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])  # 2/3 of the width for the image and 1/3 for the attributes

with col1:
    st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'><img src='{chosen_player_image}' width='215'></div>", 
                unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'><img src='{chosen_player_logo}' width='100'></div>", 
                unsafe_allow_html=True)
    st.markdown(f"<div style='text-align: center; margin-bottom: 20px;'><img src='{chosen_player_nationality}' width='100'></div>", 
                unsafe_allow_html=True)

with col2:
    for attribute in ['shooting', 'passing', 'dribbling', 'defending', 'physic']:
        if attribute == 'shooting':
            st.image('Images/shooting.png', width=30)
        elif attribute == 'physic':
            st.image('Images/physic.png', width=30)
        elif attribute == 'dribbling':
            st.image('Images/dribling.png', width=30)
        elif attribute == 'defending':
            st.image('Images/defense.png', width=30)
        elif attribute == 'passing':
            st.image('Images/passing.png', width=30)
        st.write(f"<span style='font-weight: bold;'>{attribute.title()}:</span> <span style='font-weight: bold;'>{player_attributes[attribute]}</span>", unsafe_allow_html=True)


# Define the market value ranges in EUR millions. and player positions
market_value_ranges = ["All", "Below 10", "10 to 30", "30 to 60", "60 to 100", "100 to 150", "150 to 200", "Above 200"]
player_positions = ["All", "CAM", "CB", "CDM", "CF", "CM", "LB", "LM", "LW", "LWB", "RB", "RM", "RW", "RWB", "ST"]

#Define select box for player position
selected_position = st.selectbox("Select player position:", options=player_positions, index=0)

# Input fields for the age range and market value range
min_age = st.number_input("Enter minimum age:", value=18, min_value=18, max_value=50)
max_age = st.number_input("Enter maximum age:", value=35, min_value=18, max_value=50)
if max_age < min_age:
    st.warning("Max age is less than min age. Swapping values.")
    max_age, min_age = min_age, max_age

selected_range = st.selectbox("Select market value range (in millions of EUR):", options=market_value_ranges, index=0)

if selected_range == "All":
    min_value, max_value = 0, 5_000_000_000
else:
    if selected_range == "Below 10":
        min_value, max_value = 0, 10_000_000
    elif selected_range == "10 to 30":
        min_value, max_value = 10_000_000, 30_000_000
    elif selected_range == "30 to 60":
        min_value, max_value = 30_000_000, 60_000_000
    elif selected_range == "60 to 100":
        min_value, max_value = 60_000_000, 100_000_000
    elif selected_range == "100 to 150":
        min_value, max_value = 100_000_000, 150_000_000
    elif selected_range == "150 to 200":
        min_value, max_value = 150_000_000, 200_000_000
    else:
        min_value, max_value = 200_000_000, 5_000_000_000

# Filter the dataset for the age and market value range
age_value_filtered = Fifa22[(Fifa22['age'] >= min_age) & (Fifa22['age'] <= max_age) &
                            (Fifa22['value_eur'] >= min_value) & (Fifa22['value_eur'] <= max_value)]

# Check if there are any players left after filtering
if len(age_value_filtered) == 0:
    st.warning("No players can be found with your specifications")
    st.stop()

# Get the indices of players in the same cluster as the chosen player, after applying all filters
same_cluster_indices = [i for i, label in enumerate(kmeans.labels_) if label == kmeans.labels_[chosen_player_index]
and Fifa22.iloc[i]['age'] >= min_age and Fifa22.iloc[i]['age'] <= max_age
and Fifa22.iloc[i]['value_eur'] >= min_value and Fifa22.iloc[i]['value_eur'] <= max_value
and (selected_position == "All" or selected_position in Fifa22.iloc[i]['player_positions'])]

# Check if there are any players in the same cluster with the chosen player, after applying tall filters
if not same_cluster_indices:
    st.warning("No players can be found with your specifications")
    st.stop()

# Create dataframe with names, clubs, nationalities, player faces, wage and value of players in the same cluster
same_cluster_players = age_value_filtered.loc[same_cluster_indices, ["long_name", "club_name", "club_logo_url", "nation_flag_url", "player_face_url", "wage_eur", "value_eur", "shooting", "passing", "dribbling", "defending", "physic"]]

# Calculate the distances between the chosen player and all other players in the same cluster
distances = pairwise_distances(player_attributes.values.reshape(1, -1), X.loc[same_cluster_indices],
                               metric='euclidean')[0]

# Get the names, clubs, nationalities, player faces, wage and value of the top 5 most similar players, excluding the chosen player
top_5_indices = np.argsort(distances)[1:6]  # exclude the first index which is the chosen player
top_5_players = same_cluster_players.iloc[top_5_indices]

# Create a table to display the top 5 similar players
table_data = {
    "Index": [i+1 for i in range(len(top_5_players))],
    "Name": list(top_5_players["long_name"]),
    "Player Face": [url for url in list(top_5_players["player_face_url"])],
    "Club Logo": [url for url in list(top_5_players["club_logo_url"])],
    "Club": list(top_5_players["club_name"]),
    "Nationality": [url for url in list(top_5_players["nation_flag_url"])],
    "Wage (EUR)": list(top_5_players["wage_eur"]),
    "Value (EUR)": list(top_5_players["value_eur"]),
    "Shooting": list(top_5_players["shooting"]),
    "Passing": list(top_5_players["passing"]),
    "Dribbling": list(top_5_players["dribbling"]),
    "Defending": list(top_5_players["defending"]),
    "Physic": list(top_5_players["physic"]),
}

# Create a table to display the top 5 similar players
table_df = pd.DataFrame(table_data)

for index, row in table_df.iterrows():
    st.write(f"<h4>{row['Index']}. {row['Name']}</h4>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([3, 2, 2])
    
    with col1:
        st.markdown("""
            <div style="display: flex; flex-direction: column; align-items: center; margin-bottom: 30px;">
                <img src='{}' width='215'>
                <img src='{}' width='100'>
                <p style="text-align: center; font-weight: bold;">Club: {}</p>
                <img src='{}' width='100'>
            </div>
        """.format(row["Player Face"], row["Club Logo"], row['Club'], row["Nationality"]), unsafe_allow_html=True)

    with col2:
        for attribute in ['Shooting', 'Passing', 'Dribbling', 'Defending', 'Physic']:
            if attribute == 'Shooting':
                st.image('Images/shooting.png', width=30)
                st.markdown(f"<span style='font-weight: bold;'>{attribute}: </span> <span style='font-weight: bold;'>{row[attribute]}</span>", unsafe_allow_html=True)
            elif attribute == 'Physic':
                st.image('Images/physic.png', width=30)
                st.markdown(f"<span style='font-weight: bold;'>{attribute}: </span> <span style='font-weight: bold;'>{row[attribute]}</span>", unsafe_allow_html=True)
            elif attribute == 'Dribbling':
                st.image('Images/dribling.png', width=30)
                st.markdown(f"<span style='font-weight: bold;'>{attribute}: </span> <span style='font-weight: bold;'>{row[attribute]}</span>", unsafe_allow_html=True)
            elif attribute == 'Defending':
                st.image('Images/defense.png', width=30)
                st.markdown(f"<span style='font-weight: bold;'>{attribute}: </span> <span style='font-weight: bold;'>{row[attribute]}</span>", unsafe_allow_html=True)
            elif attribute == 'Passing':
                st.image('Images/passing.png', width=30)
                st.markdown(f"<span style='font-weight: bold;'>{attribute}: </span> <span style='font-weight: bold;'>{row[attribute]}</span>", unsafe_allow_html=True)


    with col3:
        for label, value in [("Monthly wage", row['Wage (EUR)']), ("Market value", row['Value (EUR)'])]:
            st.markdown(f"<b style='font-size:22px;text-decoration: underline'>{label}:</b>", unsafe_allow_html=True)
            st.write("")
            st.markdown(f"<span style='font-size:22px'>EUR {value:,.0f}</span>", unsafe_allow_html=True)
            st.write("")

