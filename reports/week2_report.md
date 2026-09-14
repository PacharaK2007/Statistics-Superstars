# Week 2 Report: Statistical Analysis

## Team: Statistical Superstar
**Date:** 13/9/2026

---

## 1. Hypothesis Testing Results

### 1.1 T-Tests

| Test | Variable 1 | Variable 2 | t-statistic | p-value | Significant |
|------|-----------|-----------|-------------|---------|--------------|
| One-sample | flipper_length_mm | 200 | 1.180 | 0.2387 | No |
| Independent | body_mass_g (Adelie) | body_mass_g (Chinstrap) | -0.473 | 0.6367 | No |

**Interpretation:**
- The mean flipper length is not significantly different from 200 mm (p = 0.24 > 0.05). The observed mean (200.9 mm) is close enough to 200 mm that we cannot conclude a real difference exists.
- Mean body mass does not differ significantly between the Adelie and Chinstrap species (p = 0.64). These two species have similar body mass in this sample.

### 1.2 ANOVA

| Variable | Groups | F-statistic | p-value | Significant |
|----------|--------|-------------|---------|--------------|
| body_mass_g | species (3 groups) | 337.587 | < 0.0001 | Yes |

**Interpretation:**
- When comparing mean body mass across all three species (Adelie, Chinstrap, Gentoo) simultaneously, the difference is highly significant (p < 0.0001), meaning at least one species has a mean body mass that differs from the others.
- Interestingly, the pairwise t-test in 1.1 found no significant difference between Adelie and Chinstrap, yet the ANOVA is highly significant. This is likely driven by the third species, Gentoo, which is noticeably larger than the other two — pulling the overall group comparison toward significance.

### 1.3 Chi-Square Test

| Variable 1 | Variable 2 | χ²-statistic | p-value | Significant |
|-----------|-----------|--------------|---------|--------------|
| species | island | 299.550 | < 0.0001 | Yes |

**Interpretation:**
- Species and island are significantly associated (p < 0.0001). This means penguin species are not randomly distributed across islands — each species tends to be concentrated on specific islands.

---

## 2. Distribution Fitting

### 2.1 Best-Fitting Distributions

| Column | Best Fit | p-value | Good Fit? |
|--------|----------|---------|-----------|
| [column name] | [best-fitting distribution] | [p-value] | [Yes/No] |
| [column name] | [best-fitting distribution] | [p-value] | [Yes/No] |
| [column name] | [best-fitting distribution] | [p-value] | [Yes/No] |

> Open `reports/distribution_fitting_summary.csv` from Task 3 and copy the actual values into this table.

### 2.2 Distribution Visualizations

![Distribution Fit](figures/distribution_fit_flipper_length_mm.png)

**Interpretation:**
- [State which variables are approximately normally distributed]
- [State the implications for downstream analysis — e.g., if a variable is not normal, a non-parametric test may be more appropriate than a t-test/ANOVA]

---

## 3. Confidence Intervals

### 3.1 Traditional Confidence Intervals (95%)

| Column | Mean | CI Lower | CI Upper | Width |
|--------|------|----------|----------|-------|
| [column name] | [...] | [...] | [...] | [...] |
| [column name] | [...] | [...] | [...] | [...] |

### 3.2 Bootstrap Confidence Intervals (95%)

| Column | Mean | CI Lower | CI Upper | Width |
|--------|------|----------|----------|-------|
| [column name] | [...] | [...] | [...] | [...] |
| [column name] | [...] | [...] | [...] | [...] |

> Open `reports/ci_comparison.csv` from Task 4 and copy the actual values into both tables above.

**Comparison:**
- [State whether the traditional and bootstrap intervals are similar in width]
- [Explain why — when data are approximately normal and the sample size is reasonably large (n≥30), the two methods typically produce similar intervals]

![CI Comparison](figures/confidence_intervals_comparison.png)

---

## 4. Key Statistical Findings

1. **Normality**: [X] variables are approximately normally distributed, [Y] are not (see Table 2.1)
2. **Significant Differences**: A significant difference in body mass was found across penguin species (ANOVA, p < 0.0001), and a significant association was found between species and island (Chi-square, p < 0.0001)
3. **Distribution**: The best-fitting distributions overall are [fill in from Table 2.1]
4. **Confidence**: We are 95% confident that the true mean of each variable falls within the ranges shown in Tables 3.1/3.2

---

## 5. Interpretation & Conclusions

### 5.1 What the Results Mean
- Penguin body mass varies clearly by species, with Gentoo notably larger than the other species, while Adelie and Chinstrap are similar in size.
- Penguin species tend to inhabit specific islands rather than being randomly distributed across all islands.
- [Add further conclusions based on the distribution fitting and confidence interval results]

### 5.2 Limitations
- [State the sample size (n) used — this affects how reliable the results are]
- T-tests and ANOVA assume each group is approximately normally distributed with similar variances; these assumptions should be checked further before drawing strong conclusions.
- Potential confounding variables were not accounted for in this analysis, such as sex or the season data was collected.

### 5.3 Recommendations for Week 3
- Create visualizations comparing variable distributions across species more clearly (e.g., a boxplot of body_mass_g by species).
- Consider building an interactive dashboard that lets users explore relationships between variables.
- [Add further recommendations as the team sees fit]

---

## 6. Team Contributions

| Team Member | Tasks Completed | Hours |
|-------------|------------------|-------|
| Student A | Data prep, environment management | [hours] |
| Student B | All statistical tests & analysis | [hours] |
| Student C | Visualization support | [hours] |

---

## Appendix

**Files Generated:**
- `../reports/hypothesis_tests_summary.csv`
- `../reports/distribution_fitting_summary.csv`
- `../reports/ci_comparison.csv`
- `../reports/figures/distribution_fit_*.png`
- `../reports/figures/confidence_intervals_comparison.png`

**Notebooks:**
- `notebooks/02_hypothesis_testing.ipynb`
- `notebooks/03_distribution_fitting.ipynb`
- `notebooks/04_confidence_intervals.ipynb`