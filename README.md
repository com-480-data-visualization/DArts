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
 
The full exploratory analysis is available in `notebooks/exploratory_analysis.ipynb`.
 
#### Dataset Overview
 
The original dataset contains 160,248 artworks (30 columns) and 15,803 artists (9 columns). After cleaning (removing irrelevant columns, handling missing values, and normalizing categories) we retained 144,149 artworks (90.0%) and 11,879 artists (75.2%).
 
#### Key Findings
 
**Gender distribution** reveals a significant imbalance: male artists represent 80.3% of the collection (9,536), while female artists account for only 19.7% (2,336), with just 7 non-binary artists.
 
**Geographic concentration** is equally pronounced. American artists dominate at 41.0% (4,872), followed by German (7.4%), French (6.6%), British (6.6%), and Italian (4.0%). The top 5 nationalities alone represent 65.6% of all artists, with a strong skew toward Western countries.
 
**Temporal coverage** spans from 1768 to 2026 across 92,564 dated artworks, with peak representation in the 1960s–1980s, reflecting MoMA's modern and contemporary focus.
 
**Department distribution** is dominated by Drawings & Prints (50.1%), followed by Architecture & Design (23.0%) and Photography (21.3%). Traditional Painting & Sculpture accounts for only 2.8%.
 
#### Summary
 
These patterns (a 4:1 male-to-female ratio, strong Western geographic concentration, and departmental imbalances) confirm that meaningful diversity trends exist in the data and provide a strong foundation for interactive visual exploration over time.

### Related work

A number of projects have been created using the MoMA collection dataset, spanning from articles to data visualizations. An article by FiveThirtyEight popularized the dataset in 2015, extrapolating statistics on the sizes of all paintings in the collection, artists with the largest number of works in the collection, aquisition data, and painting mediums. Since then, several more projects have used the dataset to analyze gender and nationality distributions and categorize aquisitions by various metrics. However, all of these existing projects produces fairly standard bar charts, pie charts, and choropleths -- none of them provide interactive ways to analyze and explore the data. 

Our project differs as it aims to highlight the pace of change of the collection's demographic and geographic characteristics, rather than presenting a static representation as well. In this way, our aim is to produce a more interactive and accessible platform for a general audience to explore these characteristics.

We are taking inspiration from a previous project by one of our team members, found [here](https://epfl-ada.github.io/ada-2025-project-market-miners/frontend/index.html). It employs several distinct visualizations, but the method we are most inspired by is a 3D, interactive globe that presents geographical data and allows users to click on different parts of the globe to read about certain events. This map, as well as the other visualizations on the page, can be filtered by key parameters as the user desires. 

## Milestone 2 (17th April, 5pm)

**10% of the final grade**


## Milestone 3 (29th May, 5pm)

**80% of the final grade**


## Late policy

- < 24h: 80% of the grade for the milestone
- < 48h: 70% of the grade for the milestone

