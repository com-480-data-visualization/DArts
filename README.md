# Project of Data Visualization (COM-480)

| Student's name | SCIPER |
| -------------- | ------ |
|Oussama Ghali|341478|
|Nour Guermazi|314474|
|Isabella Linde|423106|

[Milestone 1](#milestone-1) • [Milestone 2](#milestone-2) • [Milestone 3](#milestone-3)

## Milestone 1 (20th March, 5pm)

**10% of the final grade**

This is a preliminary milestone to let you set up goals for your final project and assess the feasibility of your ideas.
Please, fill the following sections about your project.

*(max. 2000 characters per section)*

### Dataset

For this project, we will use the [Museum of Modern Art (MoMA) Collection](https://github.com/MuseumofModernArt/collection) dataset, publicly available on GitHub. This dataset contains detailed metadata about artworks and artists included in the MoMA collection.

The dataset consists of two main tables:

- Artworks (~160,000 records), containing information such as title, year of creation, medium, department, dimensions, and acquisition date.

- Artists (~15,000 records), containing attributes such as nationality, gender, and birth/death year.

The dataset is well-structured and widely used in data analysis and visualization projects, making it suitable for our study. However, some preprocessing will be required before visualization.

In particular, the artworks dataset stores artist identifiers as arrays, which must be expanded and linked to the artists table. Some categorical variables (e.g., medium or classification) contain inconsistent textual values that may require normalization. Certain attributes, such as gender or nationality, contain missing values that need to be handled during analysis.

Overall, the dataset quality is high and requires moderate preprocessing, mainly involving table joins, cleaning of categorical variables, and aggregation by time periods or geographic regions. Since the data is already structured and publicly available, the focus of the project will remain on analysis and visualization rather than data collection, which aligns with the objectives of this course.

### Problematic

Museums play an important role in shaping cultural narratives by determining which artists and artworks are included in their collections. In recent years, questions about representation and diversity in major art institutions have gained increasing attention.
This project aims to explore diversity within the Museum of Modern Art (MoMA) collection by analyzing the demographic and geographic characteristics of the artists represented. In particular, we investigate how representation varies according to gender, nationality, and time period, and whether the composition of the collection has evolved over time.
Through interactive visualizations, the project seeks to reveal structural patterns that may not be immediately visible in raw data. Our planned interface includes several coordinated views: an animated timeline showing how gender and nationality balance has shifted decade by decade, an interactive world map highlighting geographic concentration and its evolution, and filterable charts allowing users to explore representation across departments and artistic mediums. These views will be linked, so that selecting a time period or region in one view updates the others, enabling fluid exploration of the data.
We plan to implement the project using D3.js for custom visualizations, combined with Svelte for building a responsive and modular interface. This stack allows us to create highly interactive, bindable components while keeping the codebase lightweight.
Rather than evaluating curatorial decisions, our goal is to provide a data-driven perspective on the composition of a major modern art collection. By visualizing these patterns, we aim to offer an intuitive and exploratory interface that allows users to better understand how representation in modern art collections has evolved.
The target audience includes students, researchers, and anyone interested in art history, cultural institutions, and the intersection between data visualization and cultural analysis.

### Exploratory Data Analysis

The exploratory data analysis was conducted using Python (pandas, matplotlib, seaborn) in a Jupyter notebook. The complete analysis can be found in `notebooks/exploratory_analysis.ipynb`.

#### Dataset Overview

**Original Datasets:**
- **Artworks**: 160,248 records with 30 columns
- **Artists**: 15,803 records with 9 columns

**After Data Cleaning:**
- **Artworks**: 144,149 records (90.0% retention rate)
- **Artists**: 11,879 records (75.2% retention rate)

#### Data Preprocessing

To ensure data quality for diversity analysis, we applied the following preprocessing steps:

1. **Column Selection**: Removed irrelevant columns (physical dimensions, administrative data, URLs)
2. **Missing Value Handling**: Kept only records with complete data in key diversity analysis columns
3. **Data Standardization**: Normalized categorical variables for consistent analysis

The cleaned dataset focuses on essential attributes for diversity analysis: demographics (gender, nationality), temporal data (creation dates), and artistic context (medium, department, classification).

#### Key Findings

**Gender Distribution (11,879 artists with complete data):**
- Male: 9,536 artists (80.3%)
- Female: 2,336 artists (19.7%)
- Non-binary/Other: 7 artists (0.1%)

The analysis reveals a significant gender imbalance, with male artists representing over 4 times as many records as female artists in the cleaned dataset.

**Geographic Distribution (Top 15 Nationalities):**
1. American: 4,872 artists (41.0%)
2. German: 883 artists (7.4%)
3. French: 782 artists (6.6%)
4. British: 779 artists (6.6%)
5. Italian: 476 artists (4.0%)
6. Japanese: 449 artists (3.8%)
7. Swiss: 257 artists (2.2%)
8. Dutch: 249 artists (2.1%)
9. Russian: 245 artists (2.1%)
10. Austrian: 225 artists (1.9%)
11. Canadian: 182 artists (1.5%)
12. Brazilian: 175 artists (1.5%)
13. Mexican: 153 artists (1.3%)
14. Argentine: 146 artists (1.2%)
15. Spanish: 142 artists (1.2%)

American artists dominate the collection (41.0%), with the top 5 nationalities representing 65.6% of all artists. This demonstrates significant geographic concentration in Western countries.

**Temporal Coverage:**
- **Span**: 1768-2026 (258 years of art history)
- **Artworks with valid dates**: 92,564 records
- **Peak periods**: Strong representation from 1960s-1980s, reflecting MoMA's focus on modern and contemporary art

**Department Distribution (144,149 artworks):**
1. Drawings & Prints: 72,279 artworks (50.1%)
2. Architecture & Design: 33,084 artworks (23.0%)
3. Photography: 30,659 artworks (21.3%)
4. Painting & Sculpture: 4,072 artworks (2.8%)
5. Media and Performance: 3,206 artworks (2.2%)
6. Fluxus Collection: 484 artworks (0.3%)
7. Film: 334 artworks (0.2%)
8. Architecture & Design - Image Archive: 31 artworks (0.0%)

Drawings & Prints dominate the collection (50.1%), while traditional Painting & Sculpture represents only 2.8% of the total collection.

#### Summary Statistics

The cleaned dataset provides a robust foundation for diversity analysis:
- **Gender imbalance**: 80.3% male vs 19.7% female representation
- **Geographic concentration**: Top 5 nationalities represent 65.6% of artists
- **Departmental focus**: Drawings & Prints dominates with 50.1% of collection
- **Temporal breadth**: 258 years of art history represented

These patterns reveal significant opportunities for exploring diversity trends and representation changes over time through interactive visualizations.

### Related work

A number of projects have been created using the MoMA collection dataset, spanning from articles to data visualizations. An article by FiveThirtyEight popularized the dataset in 2015, extrapolating statistics on the sizes of all paintings in the collection, artists with the largest number of works in the collection, aquisition data, and painting mediums. Since then, several more projects have used the dataset to analyze gender and nationality distributions and categorize aquisitions by various metrics. However, all of these existing projects produces fairly standard bar charts, pie charts, and choropleths -- none of them provide interactive ways to analyze and explore the data. 

Our project differs as it aims to highlight the pace of change of the collection's demographic and geographic characteristics, rather than presenting a static representation as well. In this way, our aim is to produce a highly interactive, accessible, and informative platform for a general audience to explore these characteristics.


> - What source of inspiration do you take? Visualizations that you found on other websites or magazines (might be unrelated to your data).

## Milestone 2 (17th April, 5pm)

**10% of the final grade**


## Milestone 3 (29th May, 5pm)

**80% of the final grade**


## Late policy

- < 24h: 80% of the grade for the milestone
- < 48h: 70% of the grade for the milestone

