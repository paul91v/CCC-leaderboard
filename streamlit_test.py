import streamlit as st
import pandas as pd
from pathlib import Path

# Sample data
def highlight_top_rows(s):
    return ['background-color: gold'] * len(s) if s.name < 3 else [''] * len(s)
    
leaderboard_path = Path("E:\Python scripts\CCC work\CCC Leaderboard\Data")
leaderboard_path = Path("\Data")
try:
    base_dir =  Path(__file__).parent
except:
    base_dir = Path.cwd()
    
leaderboard_path = base_dir/"Data" 
leaderboard_files = [f for f in leaderboard_path.iterdir() if f.is_file() and f.suffix == '.csv']
leaderboard_file = sorted(leaderboard_files, key =  lambda f: f.name)[-1].resolve()

df = pd.read_csv(str(leaderboard_file), index_col = 0)
df = df[['Student Name','total_points','classical_games','classical_points', 'rapid_games',  'rapid_points','Coach', 'Current Level', 'Lichess ID']]
df.columns = ['Student Name','Total Points','Classical Games','Classical Points', 'Rapid Games',  'Rapid Points','Coach', 'Current Level', 'Lichess ID']
# Step 1: Let user choose a category
current_level = st.selectbox("Select a category", df['Current Level'].unique())

# Step 2: Filter and sort
filtered_df = df[df['Current Level'] == current_level].sort_values(by='Total Points', ascending=False).reset_index(drop=True)
filtered_df.index += 1  # Rank starts from 1
filtered_df.index.name = 'Rank'
#filtered_df = filtered_df.style.apply(highlight_top_rows, axis=1)

# Step 3: Display leaderboard
st.subheader(f"Leaderboard for Level '{current_level}'")
st.dataframe(filtered_df)
