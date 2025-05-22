import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway, kruskal


def load_combined_data():
    try:
        benin = pd.read_csv("data/benin_clean.csv")
        sierraleone = pd.read_csv("data/sierraleone_clean.csv")
        togo = pd.read_csv("data/togo_clean.csv")
    except FileNotFoundError:
        return pd.DataFrame()

    benin["Country"] = "Benin"
    sierraleone["Country"] = "Sierra Leone"
    togo["Country"] = "Togo"

    return pd.concat([benin, sierraleone, togo], ignore_index=True)


def compute_summary(df, metric):
    summary = df.groupby("Country")[[metric]].agg(['mean', 'median', 'std']).round(2)
    summary.columns = ['_'.join(col) for col in summary.columns]
    return summary


def perform_stat_tests(df, metric):
    grouped = [group[metric].dropna().values for _, group in df.groupby("Country")]
    if len(grouped) < 2:
        return None, None
    return f_oneway(*grouped).pvalue, kruskal(*grouped).pvalue


def plot_boxplot(df, metric):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x="Country", y=metric, palette="pastel", ax=ax)
    return fig


def plot_ranking_bar(df):
    avg_ghi = df.groupby('Country')['GHI'].mean().sort_values()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=avg_ghi.values, y=avg_ghi.index, palette='viridis', ax=ax)
    ax.set_xlabel("Average GHI")
    return fig
