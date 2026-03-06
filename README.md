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

For this project, we will use the Museum of Modern Art (MoMA) Collection dataset, publicly available on GitHub. This dataset contains detailed metadata about artworks and artists included in the MoMA collection.

The dataset consists of two main tables:

Artworks (~160,000 records), containing information such as title, year of creation, medium, department, dimensions, and acquisition date.

Artists (~15,000 records), containing attributes such as nationality, gender, and birth/death year.

The dataset is well-structured and widely used in data analysis and visualization projects, making it suitable for our study. However, some preprocessing will be required before visualization.

In particular:

The artworks dataset stores artist identifiers as arrays, which must be expanded and linked to the artists table.

Some categorical variables (e.g., medium or classification) contain inconsistent textual values that may require normalization.

Certain attributes, such as gender or nationality, contain missing values that need to be handled during analysis.

Overall, the dataset quality is high and requires moderate preprocessing, mainly involving table joins, cleaning of categorical variables, and aggregation by time periods or geographic regions. Since the data is already structured and publicly available, the focus of the project will remain on analysis and visualization rather than data collection, which aligns with the objectives of this course.
https://github.com/MuseumofModernArt/collection

### Problematic

Museums play an important role in shaping cultural narratives by determining which artists and artworks are included in their collections. In recent years, questions about representation and diversity in major art institutions have gained increasing attention.

This project aims to explore diversity within the Museum of Modern Art (MoMA) collection by analyzing the demographic and geographic characteristics of the artists represented. In particular, we investigate how representation varies according to gender, nationality, and time period, and whether the composition of the collection has evolved over time.

Through interactive visualizations, the project seeks to reveal structural patterns that may not be immediately visible in raw data. For example, we will explore how gender representation changes across decades, how artists are geographically distributed, and whether certain artistic mediums or periods exhibit stronger diversity patterns.

Rather than evaluating curatorial decisions, our goal is to provide a data-driven perspective on the composition of a major modern art collection. By visualizing these patterns, we aim to offer an intuitive and exploratory interface that allows users to better understand how representation in modern art collections has evolved.

The target audience includes students, researchers, and anyone interested in art history, cultural institutions, and the intersection between data visualization and cultural analysis.

### Exploratory Data Analysis

> Pre-processing of the data set you chose
> - Show some basic statistics and get insights about the data

### Related work


> - What others have already done with the data?
> - Why is your approach original?
> - What source of inspiration do you take? Visualizations that you found on other websites or magazines (might be unrelated to your data).
> - In case you are using a dataset that you have already explored in another context (ML or ADA course, semester project...), you are required to share the report of that work to outline the differences with the submission for this class.

## Milestone 2 (17th April, 5pm)

**10% of the final grade**


## Milestone 3 (29th May, 5pm)

**80% of the final grade**


## Late policy

- < 24h: 80% of the grade for the milestone
- < 48h: 70% of the grade for the milestone

