import json

import altair as alt
import pandas as pd
import streamlit as st

alt.data_transformers.disable_max_rows()

user = st.sidebar.selectbox(
        "Who do you want to analyze?", ["Mork", "Artur", "Attila", "Tristan"])
# song_data = pd.read_csv(f'data/{user}_detailed.csv')
if user == "Tristan" or user == "Mork":
    song_data = pd.read_csv(f'data/{user}_albumtracks.csv')
else:
    song_data = pd.read_csv(f'data/{user}_detailed.csv')

song_data['month_added'] = [str(t)[:7] for t in song_data.added_at]
song_data['year_added'] = [int(str(t)[:4]) for t in song_data.added_at]
song_data['time_added'] = [str(t)[11:13] for t in song_data.added_at]
song_data['zeroed_valence'] = [v-0.5 for v in song_data.valence]
song_data['duration_sec'] = [v//1000 for v in song_data.duration_ms]
song_data['release_year'] = [str(d)[:4] for d in song_data.release_date]

constants = pd.DataFrame(data={'val_50': [50], 'val_0.5': [0.5]})

st.write(f"# Hello there, {user}")

first_year = min(song_data['year_added'])
last_year = max(song_data['year_added'])

filter_min, filter_max = st.slider("Filter by year added:", first_year, last_year, (first_year, last_year), 1)
song_data = song_data[song_data["year_added"] >= filter_min]
song_data = song_data[song_data["year_added"] <= filter_max]

st.write("## __Activity__ *(number of songs liked over time)*")
expl = st.checkbox("Split by explicit")
if expl:
    activity = (alt.Chart(song_data).mark_line(point=True, strokeWidth=5).encode(
        alt.X("month_added:O"),
        y='count()',
        color='explicit',
        tooltip=['month_added', 'count()']
        )
        .properties(width=1200, height=500)
        .interactive()
        .configure_point(size=200)
    )
else:
    activity = (alt.Chart(song_data).mark_line(point=True, strokeWidth=5).encode(
        alt.X("month_added:O"),
        y='count()',
        # color='explicit',
        tooltip=['month_added', 'count()']
        )
        .properties(width=1200, height=500)
        .interactive()
        .configure_point(size=200)
    )
activity

st.write("## Popularity against time added")
popularity_chart = (alt.Chart(song_data).mark_circle(size=120).encode(
    x='month_added',
    y='popularity',
    color='explicit',
    tooltip=['name', 'artist_name', 'popularity']
    )
    .properties(width=1200, height=500)
    .interactive()
 )

popularity_chart

st.write("## Danceability against happiness scatterplot")
dance_against_valence = (alt.Chart(song_data).mark_circle(size=120).encode(
    x='danceability',
    y='valence',
    color='explicit',
    # size='popularity',
    tooltip=['name', 'artist_name', 'popularity']
    )
    .properties(width=1200, height=500)
    .interactive()
 )

dance_against_valence

st.write("## Sadboiness histogram (overall happiness distribution)")
sadboiness = (alt.Chart(song_data).mark_bar().encode(
    alt.X("valence:Q", bin=alt.Bin(maxbins=50)),
    y='count()',
    tooltip='count()'
    )
    .properties(width=1200, height=500)
    .interactive()
)

sadb_mean = alt.Chart(song_data).mark_rule(color='orange', strokeWidth=5).encode(
    x='average(valence):Q', 
    tooltip=[alt.Tooltip('average(valence):Q', title='Your average')]
)

sadb_50 = alt.Chart(song_data).mark_rule(color='lightblue', strokeWidth=5).encode(
    x='median(valence):Q',
    tooltip=[alt.Tooltip('median(valence):Q', title='Popularity median')]
)

(sadboiness + sadb_mean) # + sadb_50)

st.write("## Happiness over time")
avg_valence_over_time = (alt.Chart(song_data).mark_bar().encode(
    alt.X("month_added:O"),
    y='average(zeroed_valence):Q',
    tooltip='average(zeroed_valence):Q'
    )
    .properties(width=1200, height=500)
    .interactive()
)
avg_valence_over_time

st.write("## Danceability against speechiness scatterplot")
dance_against_speech = (alt.Chart(song_data).mark_circle(size=120).encode(
    x='danceability',
    y='speechiness',
    color='explicit',
    size='popularity',
    tooltip=['name', 'artist_name', 'popularity']
    )
    .properties(width=1200, height=500)
    .interactive()
 )

dance_against_speech

st.write("## Danceability against energy scatterplot")
dance_against_energy = (alt.Chart(song_data).mark_circle(size=120).encode(
    x='danceability',
    y='energy',
    color='explicit',
    size='popularity',
    tooltip=['name', 'artist_name', 'popularity']
    )
    .properties(width=1200, height=500)
    .interactive()
 )

dance_against_energy

st.write("## Time of day when a song is liked")
tod = (alt.Chart(song_data).mark_bar().encode(
    alt.X("time_added:O"),
    y='count()',
    tooltip='count()'
    )
    .properties(width=1200, height=500)
    .interactive()
)
tod

st.write("## Normie distribution (histogram of song popularity)")
basicness = (alt.Chart(song_data[song_data['popularity'] > 0]).mark_bar().encode(
    alt.X("popularity:Q", bin=alt.Bin(maxbins=30)),
    y='count()',
    tooltip='count()'
    )
    .properties(width=1200, height=500)
    .interactive()
)

rule = alt.Chart(song_data[song_data['popularity'] > 0]).mark_rule(color='orange', strokeWidth=5).encode(
    x='average(popularity):Q', 
    tooltip=[alt.Tooltip('average(popularity):Q', title='Your average')]
)

rule2 = alt.Chart(constants).mark_rule(color='lightblue', strokeWidth=5).encode(
    x='val_50:Q',
    tooltip=[alt.Tooltip('val_50:Q', title='Popularity median')]
)

(basicness + rule + rule2)

st.write("## Song duration histogram")
duration_hist = (alt.Chart(song_data).mark_bar().encode(
    alt.X("duration_sec:Q", bin=alt.Bin(maxbins=200)),
    y='count()',
    tooltip='count()'
    )
    .properties(width=1200, height=500)
    .interactive()
)

duration_mean = alt.Chart(song_data).mark_rule(color='orange', strokeWidth=5).encode(
    x='average(duration_sec):Q', 
    tooltip=[alt.Tooltip('average(duration_sec):Q', title='Average length')]
)
(duration_hist + duration_mean)

release_year = (alt.Chart(song_data).mark_bar().encode(
        alt.X("release_year:O"),
        y='count()',
        color='explicit',
        tooltip=['release_year:O', 'count()']
        )
        .properties(width=1200, height=500)
        .interactive()
    )
release_year

r_year = st.selectbox(
        "Select a release year", sorted(list(set(song_data['release_year']))))
st.write(song_data[song_data['release_year'] == r_year])
