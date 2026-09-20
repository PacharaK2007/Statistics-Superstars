import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

from src.visualizations import (
    plot_histogram_with_distribution,
    create_correlation_heatmap,
    plot_boxplots_by_category,
    create_interactive_scatter,
    plot_qq_comparison,
    dashboard_layout,
)


@pytest.fixture
def sample_df():
    rng = np.random.default_rng(4)
    return pd.DataFrame({
        "a": rng.normal(10, 2, 120),
        "b": rng.normal(5, 1, 120),
        "category": rng.choice(["X", "Y", "Z"], size=120),
    })


def test_plot_histogram_with_distribution(sample_df):
    fig = plot_histogram_with_distribution(sample_df["a"], "normal", "a")
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_plot_histogram_with_distribution_invalid():
    with pytest.raises(ValueError):
        plot_histogram_with_distribution([1, 2, 3], "not-a-distribution")


def test_create_correlation_heatmap(sample_df):
    fig = create_correlation_heatmap(sample_df)
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_plot_boxplots_by_category(sample_df):
    fig = plot_boxplots_by_category(sample_df, "a", "category")
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_create_interactive_scatter(sample_df):
    fig = create_interactive_scatter(sample_df, "a", "b", "category")
    assert isinstance(fig, go.Figure)


def test_create_interactive_scatter_no_color(sample_df):
    fig = create_interactive_scatter(sample_df, "a", "b")
    assert isinstance(fig, go.Figure)


def test_plot_qq_comparison(sample_df):
    fig = plot_qq_comparison(sample_df["a"], "norm", "a")
    assert isinstance(fig, plt.Figure)
    plt.close(fig)


def test_dashboard_layout():
    config = dashboard_layout()
    assert config["page_title"] == "Statistics Superstars"
    assert "Overview" in config["analysis_types"]
