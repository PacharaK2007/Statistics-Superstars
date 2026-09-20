from typing import List, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

sns.set_theme(style="whitegrid")


def plot_histogram_with_distribution(data: List[float],
                                      distribution: str = "normal",
                                      column_name: str = "Value") -> plt.Figure:
    arr = np.asarray(pd.Series(data).dropna(), dtype=float)

    dist_map = {
        "normal": stats.norm,
        "exponential": stats.expon,
        "gamma": stats.gamma,
        "lognormal": stats.lognorm,
        "uniform": stats.uniform,
    }
    dist_key = distribution.lower()
    if dist_key not in dist_map:
        raise ValueError(f"Unsupported distribution: {distribution}")
    dist = dist_map[dist_key]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(arr, stat="density", bins=30, color="#4C72B0",
                 alpha=0.6, ax=ax, label="Observed data")

    params = dist.fit(arr)
    x = np.linspace(arr.min(), arr.max(), 300)
    ax.plot(x, dist.pdf(x, *params), color="#C44E52", lw=2,
            label=f"Fitted {distribution.title()}")

    ax.axvline(arr.mean(), color="black", linestyle="--", lw=1,
               label=f"Mean = {arr.mean():.2f}")
    ax.set_title(f"Distribution of {column_name}")
    ax.set_xlabel(column_name)
    ax.set_ylabel("Density")
    ax.legend()
    fig.tight_layout()
    return fig


def create_correlation_heatmap(df: pd.DataFrame, method: str = "pearson") -> plt.Figure:
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    corr = df[numeric_cols].corr(method=method)

    fig, ax = plt.subplots(figsize=(8, 7))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, square=True, linewidths=0.5, ax=ax)
    ax.set_title(f"Correlation Heatmap ({method.title()})")
    fig.tight_layout()
    return fig


def plot_boxplots_by_category(df: pd.DataFrame, numeric_col: str,
                               category_col: str) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 5))
    order = sorted(df[category_col].dropna().unique().tolist(), key=str)
    sns.boxplot(data=df, x=category_col, y=numeric_col, order=order,
                hue=category_col, legend=False, palette="Set2", ax=ax)
    sns.stripplot(data=df, x=category_col, y=numeric_col, order=order,
                  color="black", alpha=0.3, size=3, ax=ax)
    ax.set_title(f"{numeric_col} by {category_col}")
    ax.set_xlabel(category_col)
    ax.set_ylabel(numeric_col)
    fig.tight_layout()
    return fig


def create_interactive_scatter(df: pd.DataFrame, x_col: str, y_col: str,
                                color_col: Optional[str] = None) -> go.Figure:
    fig = px.scatter(
        df, x=x_col, y=y_col, color=color_col,
        opacity=0.75,
        title=f"{y_col} vs {x_col}" + (f" by {color_col}" if color_col else ""),
        hover_data=df.columns[:6],
    )
    fig.update_layout(template="plotly_white")
    return fig


def plot_qq_comparison(data: List[float], distribution: str = "norm",
                        column_name: str = "Value") -> plt.Figure:
    arr = np.asarray(pd.Series(data).dropna(), dtype=float)

    fig, ax = plt.subplots(figsize=(6, 6))
    stats.probplot(arr, dist=distribution, plot=ax)
    ax.set_title(f"Q-Q Plot: {column_name}")
    ax.get_lines()[0].set_markerfacecolor("#4C72B0")
    ax.get_lines()[0].set_markeredgecolor("#4C72B0")
    ax.get_lines()[1].set_color("#C44E52")

    if len(arr) >= 3:
        _, p_value = stats.shapiro(arr)
        ax.text(0.05, 0.95, f"Shapiro-Wilk p = {p_value:.3f}",
                transform=ax.transAxes, va="top",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.6))
    fig.tight_layout()
    return fig


def dashboard_layout() -> dict:
    return {
        "page_title": "Statistics Superstars",
        "page_icon": "\U0001F4CA",
        "layout": "wide",
        "analysis_types": ["Overview", "Distributions", "Hypothesis Testing", "Correlations"],
    }
