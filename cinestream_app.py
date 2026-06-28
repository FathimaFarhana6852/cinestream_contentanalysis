import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="CineStream Dashboard",page_icon="🎬",layout="wide",initial_sidebar_state="expanded")
@st.cache_data
def load_data():
    df = pd.read_csv("output/cleaned_cinestream.csv")
    df["AddedDate"] = pd.to_datetime(df["AddedDate"],errors="coerce")
    return df
df = load_data()

st.title("🎬 CineStream Content Analytics Dashboard")

st.caption("Interactive dashboard for analyzing CineStream content performance.")
st.markdown("---")
st.subheader("📊 Dataset Overview")

st.markdown("""**Dataset:** CineStream Content Catalog**Time Range:** 2015 - 2024""")

with st.sidebar:
    st.header("🔍 Filters")
    st.caption("Dashboard updates automatically when filters change.")
    with st.form("filters_form"):
        apply_filters = st.form_submit_button(
            "Apply Filters",
            type="primary")

    genres = st.multiselect(
        "Genre",
        options=sorted(df["Genre"].dropna().unique()),
        default=sorted(df["Genre"].dropna().unique()))
    languages = st.multiselect(
        "Language",
        options=sorted(df["Language"].dropna().unique()),
        default=sorted(df["Language"].dropna().unique()))
    content_type = st.selectbox(
        "Type",
        ["All", "Movie", "Series", "Documentary", "Stand-up"])
    age_ratings = st.multiselect(
        "Age Rating",
        options=sorted(df["AgeRating"].dropna().unique()),
        default=sorted(df["AgeRating"].dropna().unique()))
    imdb_range = st.slider(
        "IMDb Score Range",
        min_value=1.0,
        max_value=10.0,
        value=(1.0, 10.0))
    runtime_range = st.slider(
        "Runtime Range (Minutes)",
        min_value=int(df["RuntimeMinutes"].min()),
        max_value=int(df["RuntimeMinutes"].max()),
        value=(
            int(df["RuntimeMinutes"].min()),
            int(df["RuntimeMinutes"].max())))
    min_date = df["AddedDate"].min().date()
    max_date = df["AddedDate"].max().date()

    date_range = st.date_input(
        "Added Date Range",
        value=(min_date, max_date))
    chart_color = st.color_picker(
        "Choose Chart Color",
        "#1f77b4")
filtered = df.copy()

filtered = filtered[
    filtered["Genre"].isin(genres)]

filtered = filtered[
    filtered["Language"].isin(languages)]

filtered = filtered[
    filtered["AgeRating"].isin(age_ratings)]

if content_type != "All":
    filtered = filtered[
        filtered["Type"] == content_type]
filtered = filtered[
    filtered["IMDbScore"].between(
        imdb_range[0],
        imdb_range[1])]

filtered = filtered[
    filtered["RuntimeMinutes"].between(
        runtime_range[0],
        runtime_range[1])]

filtered = filtered[
    filtered["AddedDate"].dt.date.between(
        date_range[0],
        date_range[1])]

if filtered.empty:

    st.warning(
        """
        No titles match the selected filters.

        Try:
        • Selecting more Genres
        • Expanding IMDb Score range
        • Expanding Runtime range
        • Expanding Date range
        """)

    st.stop()

with st.container():
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Titles",len(filtered))
    c2.metric("Total Views (Millions)",round(filtered["ViewsMillions"].sum(), 2))
    c3.metric("Total Watch Hours (Millions)",round(filtered["WatchHoursMillions"].sum(), 2))
    c4.metric("Average IMDb Score",round(filtered["IMDbScore"].mean(), 2))
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview","🎭 Genres & Languages","💰 Money","⚠️ Quality Alerts"])
with tab1:
    left, right = st.columns([2, 1])
    with left:
        st.subheader("📋 Sample of the Catalog")
        st.dataframe(filtered.head(10),use_container_width=True)
    with right:
        st.subheader("🏆 Top 5 Titles by Views")
        top5_df = filtered.nlargest(5,"ViewsMillions")[["Title", "ViewsMillions"]]
        st.table(top5_df.style.hide(axis="index"))
    st.subheader("📄 Example Title (JSON)")
    if len(filtered) > 0:
        st.json(filtered.iloc[0].to_dict())
    st.subheader("📈 Titles Added Per Month")
    monthly_titles = (
        filtered.groupby(
            filtered["AddedDate"].dt.to_period("M")).size())

    monthly_titles.index = monthly_titles.index.astype(str)
    st.line_chart(monthly_titles)
    st.subheader("📊 Titles by Type")
    type_count = filtered["Type"].value_counts()
    st.bar_chart(type_count)
with tab2:
    left, right = st.columns(2)
    with left:
        st.subheader("🎭 Top 10 Genres by Total Views")
        genre_views = (filtered.groupby("Genre")["ViewsMillions"].sum().nlargest(10).sort_values())
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(genre_views.index,genre_views.values,color=chart_color)
        ax.set_xlabel("Views (Millions)")
        ax.set_ylabel("Genre")
        st.pyplot(fig)
    with right:
        st.subheader("🌍 Language → Genre Treemap")
        fig_tree = px.treemap(filtered,path=["Language", "Genre"],values="ViewsMillions")
        st.plotly_chart(fig_tree,use_container_width=True)
        language_perf = (filtered.groupby("Language")["ViewsMillions"].mean())
        if len(language_perf) > 0:
           best_language = language_perf.idxmax()
           worst_language = language_perf.idxmin()
           st.success(f"Best Performing Language: {best_language}")
           st.warning(f"Worst Performing Language: {worst_language}")
with tab3:
    avg_roi = filtered["ROI_Pct"].mean()
    if avg_roi >= 0:
        st.info(f"Average ROI is Positive : {avg_roi:.2f}%")
    else:
        st.error(f"Average ROI is Negative : {avg_roi:.2f}%")
    left, right = st.columns(2)
    with left:
        st.subheader("💰 Revenue vs Production Cost")
        fig_scatter = px.scatter( filtered,x="ProductionCostCr",y="RevenueCr",color="Performance_Band",hover_name="Title")
        st.plotly_chart(fig_scatter,use_container_width=True)
    with right:
        st.subheader("📊 Average ROI by Genre")
        roi_genre = (filtered.groupby("Genre")["ROI_Pct"].mean().sort_values())
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(roi_genre.index,roi_genre.values,color=chart_color)
        ax.set_xlabel("ROI %")
        st.pyplot(fig)
with tab4:
    losing_titles = len(filtered[filtered["Profit_Cr"] < 0])
    if losing_titles == 0:
       st.success("No titles are losing money.")
    elif losing_titles <= 5:
       st.warning(f"{losing_titles} titles are losing money.")
    else:
        st.error(f"{losing_titles} titles are losing money.")
    left, right = st.columns(2)
    with left:
        st.subheader("⭐ IMDb Score Distribution")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(filtered["IMDbScore"].dropna(),bins=15,color=chart_color)
        mean_score = filtered["IMDbScore"].mean()
        ax.axvline(mean_score,color="red",linestyle="--",label=f"Mean = {mean_score:.2f}")
        ax.legend()
        st.pyplot(fig)
    with right:
        st.subheader("📈 IMDb Score vs Views")
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.scatter(filtered["IMDbScore"],filtered["ViewsMillions"],color=chart_color,alpha=0.6)
        ax2.set_xlabel("IMDb Score")
        ax2.set_ylabel("Views (Millions)")
        st.pyplot(fig2)

csv = filtered.to_csv(index=False)
today = datetime.date.today().strftime("%Y-%m-%d")
st.sidebar.download_button(label="📥 Download Filtered Catalog (CSV)",data=csv,file_name=f"cinestream_filtered_{today}.csv",mime="text/csv")
with st.expander("ℹ️ How this dashboard works"):

    st.markdown("""
### Dataset

This dashboard uses the CineStream Content Catalog dataset.

### Filters

Use the sidebar filters to narrow content by:

- Genre
- Language
- Type
- Age Rating
- IMDb Score
- Runtime
- Added Date

### Tabs

**Overview**
- Catalog preview
- Top viewed titles
- Monthly title additions
- Type distribution
**Genres & Languages**
- Top genres by views
- Language and genre treemap
**Money**
- Revenue vs Production Cost
- Average ROI by Genre

**Quality Alerts**
- IMDb distribution
- IMDb score vs views analysis""")