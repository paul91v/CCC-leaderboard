import streamlit as st
import pandas as pd
from pathlib import Path

# Sample data
def highlight_top_rows(s):
    return ['background-color: gold'] * len(s) if s.name < 4 else [''] * len(s)
    
try:
    base_dir =  Path(__file__).parent
except:
    base_dir = Path.cwd()
    
def format_batch(batch):
    batch = batch.upper()
    if batch == "1:1" or len(batch) > 5:
        batch = "Individual"
    return batch

data_path = base_dir/"Data" 
leaderboard_files = [f for f in data_path.iterdir() if f.is_file() and f.suffix == '.csv']
leaderboard_file = sorted(leaderboard_files, key =  lambda f: f.name)[-1].resolve()
updated_time_file = data_path/"updated_time.txt"
with open(updated_time_file,"r") as f:
    update_time = f.read()

df = pd.read_csv(str(leaderboard_file), index_col = 0)
df = df[['Student Name','total_points','classical_games','classical_points', 'rapid_games',  'rapid_points','Coach', 'Current Level', 'Batch','Lichess ID']]
df.columns = ['Student Name','Total Points','Classical Games','Classical Points', 'Rapid Games',  'Rapid Points','Coach', 'Current Level', 'Batch','Lichess ID']
level1_df = df[df['Current Level'] == 'Level 1']
print("Students in Level 1 with Lichess IDs:")
print(level1_df['Student Name'])
empty_level_dfs = df[df['Current Level'].isnull()]
print("Students with no levels:")
print(empty_level_dfs)
final_df = df[~df['Current Level'].isin(['Level 1'])]
final_df = final_df[final_df['Current Level'].notnull()]
final_df['Batch'] = final_df['Batch'].apply(format_batch)
levels = sorted(final_df['Current Level'].unique())

st.set_page_config(layout="wide")
left_col, center_col, right_col = st.columns([3,8,2])
with left_col:
    st.markdown("### &nbsp;", unsafe_allow_html=True)
    st.markdown("## &nbsp;", unsafe_allow_html=True)
    current_level = st.selectbox("Select Student's Level", levels)
    filtered_df = final_df[final_df['Current Level'] == current_level].sort_values(by='Total Points', ascending=False).reset_index(drop=True)
    listed_batches = ['All Batches'] + sorted(filtered_df['Batch'].unique())
    filtered_df.drop("Current Level", axis = 1, inplace = True)
    filtered_df.index += 1  # Rank starts from 1
    trophies = {1: "🥇", 2: "🥈", 3: "🥉"}
    current_batch = st.selectbox("Select Student's Batch", listed_batches)
    if current_batch != "All Batches":
        trophies = {}
        filtered_df = filtered_df[filtered_df['Batch'] == current_batch].sort_values(by='Total Points', ascending=False)
        filtered_df.index = list(range(1, 1+len(filtered_df)))
    filtered_df.index = [str(x)+trophies[x] if x in trophies else x for x in filtered_df.index]
    filtered_df.index.name = 'Rank'

with center_col:
    st.markdown("<h1 style='text-align: center;'>Chennai Chess Club</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center;'>Leaderboard for October - {current_level}</h1>", unsafe_allow_html=True)
    df_height = 35*(filtered_df.shape[0]+1)
    #filtered_df = filtered_df.style.apply(highlight_top_rows, axis=1)
    st.dataframe(filtered_df, use_container_width = True, height = df_height)
with right_col:
    st.markdown("<br><br><br><br><br><br>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: right; font-size: 14px; color: gray;'>Last updated at:<br> {update_time}</p>", unsafe_allow_html=True)
# =============================================================================
#     top3 = filtered_df.head(3)
#     st.markdown("### 🏆 Students of the Month")
#     for i, row in top3.iterrows():
#         st.markdown(f"""
#         <div style='
#             background-color: #f0f2f6;
#             padding: 10px 20px;
#             margin-bottom: 10px;
#             border-left: 5px solid gold;
#             border-radius: 8px;
#         '>
#             <h4 style='margin: 0;'>{i}. {row['Student Name']} ({row['Total Points']} pts)</h4>
#             <p style='margin: 0; font-size: 14px;'>Coach: {row['Coach']} | Lichess ID: {row['Lichess ID']}</p>
#         </div>
#         """, unsafe_allow_html=True)
# =============================================================================
st.markdown("""
    <style>
    .right-text {
        position: fixed;
        bottom: 50px;
        right: 10px;
        font-size: 14px;
        color: #888;
    }
    </style>
    
    <div class="right-text">
        © 2025 Chennai Chess Club
    </div>
""", unsafe_allow_html=True)

