import streamlit as st
from utils import load_combined_data, compute_summary, perform_stat_tests, plot_boxplot, plot_ranking_bar

st.set_page_config(layout="wide", page_title="Solar Dashboard")

# Load and cache data
@st.cache_data
def get_data():
    return load_combined_data()

df = get_data()
if df.empty:
    st.error("Failed to load data. Ensure CSVs are in the `data/` folder.")
    st.stop()

# Sidebar filters
st.sidebar.title("Controls")
metric = st.sidebar.selectbox("Select Metric", ['GHI', 'DNI', 'DHI'])
countries = st.sidebar.multiselect("Select Countries", df['Country'].unique(), default=df['Country'].unique())
filtered_df = df[df['Country'].isin(countries)]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📦 Boxplot", "📈 Summary", "🧪 Stats Test", "📊 Ranking"])

with tab1:
    st.header(f"{metric} by Country")
    st.pyplot(plot_boxplot(filtered_df, metric))

with tab2:
    st.header("Summary Table")
    st.dataframe(compute_summary(filtered_df, metric))

with tab3:
    st.header("Statistical Testing")
    anova_p, kruskal_p = perform_stat_tests(filtered_df, metric)
    if anova_p is not None:
        st.markdown(f"**ANOVA p-value:** `{anova_p:.2e}`")
        st.markdown(f"**Kruskal–Wallis p-value:** `{kruskal_p:.2e}`")
    else:
        st.warning("Not enough data to run statistical tests.")

with tab4:
    st.header("GHI Average by Country")
    st.pyplot(plot_ranking_bar(filtered_df))
