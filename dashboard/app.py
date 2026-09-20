import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
import streamlit as st

from src.data_loader import DataLoader
from src.statistics import StatisticalAnalyzer
from src.visualizations import (
    plot_histogram_with_distribution,
    create_correlation_heatmap,
    plot_boxplots_by_category,
    create_interactive_scatter,
    plot_qq_comparison,
    dashboard_layout,
)

layout_cfg = dashboard_layout()
st.set_page_config(
    page_title=layout_cfg["page_title"],
    page_icon=layout_cfg["page_icon"],
    layout=layout_cfg["layout"],
)


@st.cache_data
def load_data() -> pd.DataFrame:
    loader = DataLoader(data_dir=str(Path(__file__).resolve().parent.parent / "data"))
    return loader.load_local_data("cleaned_data.csv")


df = load_data()
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

st.sidebar.title(f"{layout_cfg['page_icon']} Data Detective")
st.sidebar.caption("Statistics Superstars — Penguins dataset")

analysis_type = st.sidebar.radio("Analysis Type", layout_cfg["analysis_types"])

st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

species_options = sorted(df["species"].dropna().unique().tolist())
island_options = sorted(df["island"].dropna().unique().tolist())
sex_options = sorted(df["sex"].dropna().unique().tolist())

selected_species = st.sidebar.multiselect("Species", species_options, default=species_options)
selected_island = st.sidebar.multiselect("Island", island_options, default=island_options)
selected_sex = st.sidebar.multiselect("Sex", sex_options, default=sex_options)

filtered_df = df[
    df["species"].isin(selected_species)
    & df["island"].isin(selected_island)
    & df["sex"].isin(selected_sex)
]

st.sidebar.markdown(f"**{len(filtered_df)}** of **{len(df)}** rows match the current filters.")

if filtered_df.empty:
    st.warning("No rows match the current filters — adjust the selections in the sidebar.")
    st.stop()

analyzer = StatisticalAnalyzer(filtered_df)

if analysis_type == "Overview":
    st.header("Dataset Overview")
    st.markdown(
        "Penguin measurements from the Palmer Archipelago, Antarctica "
        "(species, island, bill/culmen dimensions, flipper length, body mass, sex)."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", len(filtered_df))
    c2.metric("Species", filtered_df["species"].nunique())
    c3.metric("Islands", filtered_df["island"].nunique())
    c4.metric("Avg. body mass (g)", f"{filtered_df['body_mass_g'].mean():.0f}")

    st.subheader("Sample rows")
    st.dataframe(filtered_df.head(10), use_container_width=True)

    st.subheader("Summary statistics")
    st.dataframe(analyzer.all_descriptive_stats().round(3), use_container_width=True)

    st.subheader("Correlation heatmap")
    st.pyplot(create_correlation_heatmap(filtered_df))

elif analysis_type == "Distributions":
    st.header("Distribution Analysis")

    col = st.selectbox("Select a numeric variable", numeric_cols, index=numeric_cols.index("body_mass_g") if "body_mass_g" in numeric_cols else 0)
    dist_name = st.selectbox("Distribution to fit", ["normal", "exponential", "gamma", "lognormal", "uniform"])

    left, right = st.columns(2)
    with left:
        st.pyplot(plot_histogram_with_distribution(filtered_df[col], dist_name, col))
    with right:
        st.pyplot(plot_qq_comparison(filtered_df[col], "norm", col))

    st.subheader("Boxplot by species")
    st.pyplot(plot_boxplots_by_category(filtered_df, col, "species"))

    with st.expander("Best-fitting distribution (Normal / Exponential / Gamma / Lognormal / Uniform)"):
        fit_result = analyzer.fit_best_distribution(col)
        st.write(f"Best fit by K-S p-value: **{fit_result['best_fit']}** (p = {fit_result['best_p']:.4f})")
        st.json({k: {kk: vv for kk, vv in v.items() if kk != "params"} for k, v in fit_result["results"].items()})

elif analysis_type == "Hypothesis Testing":
    st.header("Statistical Tests")

    test_choice = st.radio("Test", ["One-sample t-test", "Independent t-test", "One-way ANOVA", "Chi-square test"])

    if test_choice == "One-sample t-test":
        col = st.selectbox("Variable", numeric_cols)
        popmean = st.number_input("Hypothesized mean", value=float(filtered_df[col].median()))
        result = analyzer.t_test(col, popmean)
        st.metric("t-statistic", f"{result['statistic']:.3f}")
        st.metric("p-value", f"{result['p_value']:.4f}")
        st.write(f"**{'Significant' if result['significant'] else 'Not significant'}** at α = 0.05 — {result['interpretation']}.")

    elif test_choice == "Independent t-test":
        col = st.selectbox("Variable", numeric_cols)
        group_col = st.selectbox("Group by", categorical_cols)
        groups = filtered_df[group_col].dropna().unique().tolist()
        if len(groups) < 2:
            st.warning("Need at least two groups after filtering.")
        else:
            g1 = st.selectbox("Group 1", groups, index=0)
            g2 = st.selectbox("Group 2", groups, index=1 if len(groups) > 1 else 0)
            result = analyzer.independent_t_test(col, group_col, g1, g2)
            c1, c2, c3 = st.columns(3)
            c1.metric(f"Mean ({g1})", f"{result['mean_group1']:.2f}")
            c2.metric(f"Mean ({g2})", f"{result['mean_group2']:.2f}")
            c3.metric("p-value", f"{result['p_value']:.4f}")
            st.write(f"**{'Significant' if result['significant'] else 'Not significant'}** difference at α = 0.05.")
            st.pyplot(plot_boxplots_by_category(filtered_df[filtered_df[group_col].isin([g1, g2])], col, group_col))

    elif test_choice == "One-way ANOVA":
        col = st.selectbox("Variable", numeric_cols)
        group_col = st.selectbox("Group by", categorical_cols, index=categorical_cols.index("species") if "species" in categorical_cols else 0)
        result = analyzer.anova(col, group_col)
        c1, c2 = st.columns(2)
        c1.metric("F-statistic", f"{result['f_statistic']:.3f}")
        c2.metric("p-value", f"{result['p_value']:.4g}")
        st.write(f"**{'Significant' if result['significant'] else 'Not significant'}** difference across groups at α = 0.05.")
        st.pyplot(plot_boxplots_by_category(filtered_df, col, group_col))

    else:
        col1 = st.selectbox("Variable 1", categorical_cols, index=0)
        col2 = st.selectbox("Variable 2", categorical_cols, index=min(1, len(categorical_cols) - 1))
        if col1 == col2:
            st.warning("Choose two different categorical variables.")
        else:
            result = analyzer.chi_square(col1, col2)
            c1, c2 = st.columns(2)
            c1.metric("Chi-square statistic", f"{result['chi2_statistic']:.3f}")
            c2.metric("p-value", f"{result['p_value']:.4g}")
            st.write(f"Variables appear **{'dependent' if result['significant'] else 'independent'}** at α = 0.05.")
            st.dataframe(pd.crosstab(filtered_df[col1], filtered_df[col2]), use_container_width=True)

    with st.expander("95% confidence interval & bootstrap"):
        col = st.selectbox("Variable for CI", numeric_cols, key="ci_col")
        ci = analyzer.confidence_interval(col)
        st.write(f"Mean = {ci['mean']:.3f}, 95% CI = ({ci['lower']:.3f}, {ci['upper']:.3f}) using the {ci['distribution']} distribution.")
        if st.button("Run bootstrap (2,000 resamples)"):
            lower, upper = analyzer.bootstrap_ci(col, np.mean, n_bootstrap=2000)
            st.write(f"Bootstrap 95% CI for the mean: ({lower:.3f}, {upper:.3f})")

elif analysis_type == "Correlations":
    st.header("Correlation Explorer")

    x_col = st.selectbox("X variable", numeric_cols, index=0)
    y_col = st.selectbox("Y variable", numeric_cols, index=min(1, len(numeric_cols) - 1))
    color_col = st.selectbox("Color by (optional)", ["(none)"] + categorical_cols)
    color = None if color_col == "(none)" else color_col

    fig = create_interactive_scatter(filtered_df, x_col, y_col, color)
    st.plotly_chart(fig, use_container_width=True)

    corr_val = filtered_df[[x_col, y_col]].corr().iloc[0, 1]
    st.metric(f"Pearson correlation ({x_col} vs {y_col})", f"{corr_val:.3f}")

    st.subheader("Full correlation heatmap")
    st.pyplot(create_correlation_heatmap(filtered_df))

st.sidebar.markdown("---")
st.sidebar.caption("CSX 2002 · Statistics Superstars · Week 3 dashboard")
