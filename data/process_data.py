"""Pre-process MoMA data into compact JSON files for the web app."""

import pandas as pd
import json
import os
import random

random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'website', 'public', 'data')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load raw data
artworks = pd.read_csv('moma-collection/Artworks.csv')
artists = pd.read_csv('moma-collection/Artists.csv')

# Clean artists
artists = artists.drop(columns=['Wiki QID', 'ULAN'])
artists_clean = artists.dropna(subset=['ArtistBio', 'Nationality', 'Gender', 'BeginDate'])

# Clean artworks
columns_to_drop = [
    'Dimensions', 'Height (cm)', 'Width (cm)', 'Depth (cm)',
    'Circumference (cm)', 'Diameter (cm)', 'Length (cm)',
    'Weight (kg)', 'Seat Height (cm)', 'Duration (sec.)',
    'AccessionNumber', 'CreditLine', 'Cataloged', 'OnView',
    'URL', 'ImageURL'
]
artworks = artworks.drop(columns=columns_to_drop)
artworks_clean = artworks.dropna(subset=[
    'Title', 'Artist', 'ConstituentID', 'ArtistBio',
    'Nationality', 'BeginDate', 'EndDate', 'Gender',
    'Date', 'Medium', 'Classification', 'Department'
])
artworks_clean = artworks_clean.copy()
artworks_clean['Date_numeric'] = pd.to_numeric(artworks_clean['Date'], errors='coerce')
artworks_clean = artworks_clean.dropna(subset=['Date_numeric'])
artworks_clean['Decade'] = (artworks_clean['Date_numeric'] // 10 * 10).astype(int)

# Filter to reasonable range
artworks_clean = artworks_clean[(artworks_clean['Decade'] >= 1860) & (artworks_clean['Decade'] <= 2020)]

# Clean nationality/gender strings (remove parentheses)
artworks_clean['Nationality'] = artworks_clean['Nationality'].str.strip('()')
artists_clean = artists_clean.copy()
artists_clean['Nationality'] = artists_clean['Nationality'].str.strip('()')
artworks_clean['Gender'] = artworks_clean['Gender'].str.strip('()')
artists_clean['Gender'] = artists_clean['Gender'].str.strip('()')


# === Nationality to ISO country code mapping (for globe) ===
NATIONALITY_TO_ISO = {
    'American': 'USA', 'French': 'FRA', 'German': 'DEU', 'British': 'GBR',
    'Italian': 'ITA', 'Japanese': 'JPN', 'Swiss': 'CHE', 'Dutch': 'NLD',
    'Canadian': 'CAN', 'Austrian': 'AUT', 'Spanish': 'ESP', 'Brazilian': 'BRA',
    'Mexican': 'MEX', 'Russian': 'RUS', 'Argentine': 'ARG', 'Swedish': 'SWE',
    'Danish': 'DNK', 'Belgian': 'BEL', 'Israeli': 'ISR', 'Australian': 'AUS',
    'Polish': 'POL', 'Czech': 'CZE', 'Indian': 'IND', 'Chinese': 'CHN',
    'Korean': 'KOR', 'Colombian': 'COL', 'Cuban': 'CUB', 'Chilean': 'CHL',
    'Norwegian': 'NOR', 'Finnish': 'FIN', 'South African': 'ZAF',
    'Irish': 'IRL', 'Portuguese': 'PRT', 'Venezuelan': 'VEN',
    'Peruvian': 'PER', 'Greek': 'GRC', 'Turkish': 'TUR', 'Romanian': 'ROU',
    'Hungarian': 'HUN', 'Croatian': 'HRV', 'Icelandic': 'ISL',
    'Nigerian': 'NGA', 'Egyptian': 'EGY', 'Iranian': 'IRN',
    'Pakistani': 'PAK', 'Thai': 'THA', 'Filipino': 'PHL',
    'Uruguayan': 'URY', 'Ecuadorian': 'ECU', 'Guatemalan': 'GTM',
    'Taiwanese': 'TWN', 'New Zealander': 'NZL', 'Lithuanian': 'LTU',
    'Latvian': 'LVA', 'Estonian': 'EST', 'Serbian': 'SRB',
    'Slovenian': 'SVN', 'Slovak': 'SVK', 'Ukrainian': 'UKR',
    'Bosnian': 'BIH', 'Albanian': 'ALB', 'Luxembourgish': 'LUX',
    'Ghanaian': 'GHA', 'Kenyan': 'KEN', 'Senegalese': 'SEN',
    'Moroccan': 'MAR', 'Tunisian': 'TUN', 'Lebanese': 'LBN',
    'Iraqi': 'IRQ', 'Kuwaiti': 'KWT', 'Emirati': 'ARE',
    'Singaporean': 'SGP', 'Malaysian': 'MYS', 'Indonesian': 'IDN',
    'Vietnamese': 'VNM', 'Cambodian': 'KHM', 'Haitian': 'HTI',
    'Jamaican': 'JAM', 'Puerto Rican': 'PRI', 'Costa Rican': 'CRI',
    'Paraguayan': 'PRY', 'Bolivian': 'BOL', 'Panamanian': 'PAN',
    'Nicaraguan': 'NIC', 'Salvadoran': 'SLV', 'Dominican': 'DOM',
    'Trinidadian': 'TTO', 'Bahamian': 'BHS',
}


# === 1. Gender distribution (artists) ===
gender = artists_clean['Gender'].value_counts().reset_index()
gender.columns = ['gender', 'count']
gender.to_json(os.path.join(OUTPUT_DIR, 'gender.json'), orient='records')


# === 2. Gender by decade (artworks) ===
gender_decade = artworks_clean.groupby(['Decade', 'Gender']).size().reset_index(name='count')
gender_decade.columns = ['decade', 'gender', 'count']
gender_decade.to_json(os.path.join(OUTPUT_DIR, 'gender_by_decade.json'), orient='records')


# === 3. Nationality distribution (artworks) ===
nat = artworks_clean['Nationality'].value_counts().head(30).reset_index()
nat.columns = ['nationality', 'count']
nat.to_json(os.path.join(OUTPUT_DIR, 'nationality.json'), orient='records')


# === 4. Nationality by decade (top 10 nationalities, artworks) ===
top10_nat = artworks_clean['Nationality'].value_counts().head(10).index.tolist()
nat_decade = artworks_clean[artworks_clean['Nationality'].isin(top10_nat)] \
    .groupby(['Decade', 'Nationality']).size().reset_index(name='count')
nat_decade.columns = ['decade', 'nationality', 'count']
nat_decade.to_json(os.path.join(OUTPUT_DIR, 'nationality_by_decade.json'), orient='records')


# === 5. Department distribution ===
dept = artworks_clean['Department'].value_counts().reset_index()
dept.columns = ['department', 'count']
dept.to_json(os.path.join(OUTPUT_DIR, 'department.json'), orient='records')


# === 6. Department by decade ===
dept_decade = artworks_clean.groupby(['Decade', 'Department']).size().reset_index(name='count')
dept_decade.columns = ['decade', 'department', 'count']
dept_decade.to_json(os.path.join(OUTPUT_DIR, 'department_by_decade.json'), orient='records')


# === 7. Classification distribution ===
classif = artworks_clean['Classification'].value_counts().head(15).reset_index()
classif.columns = ['classification', 'count']
classif.to_json(os.path.join(OUTPUT_DIR, 'classification.json'), orient='records')


# === 8. Artworks by decade (timeline) ===
timeline = artworks_clean['Decade'].value_counts().sort_index().reset_index()
timeline.columns = ['decade', 'count']
timeline.to_json(os.path.join(OUTPUT_DIR, 'timeline.json'), orient='records')


# === 9. Globe data: artist count per country + sample artists per decade ===
globe_country_counts = []
for nat_name, iso in NATIONALITY_TO_ISO.items():
    count = int((artworks_clean['Nationality'] == nat_name).sum())
    if count > 0:
        globe_country_counts.append({'iso': iso, 'nationality': nat_name, 'count': count})

with open(os.path.join(OUTPUT_DIR, 'globe_countries.json'), 'w') as f:
    json.dump(globe_country_counts, f)

# Sample artists per nationality per decade (up to 5 per combo)
artist_samples = []
for nat_name, iso in NATIONALITY_TO_ISO.items():
    subset = artworks_clean[artworks_clean['Nationality'] == nat_name]
    if len(subset) == 0:
        continue
    for decade in subset['Decade'].unique():
        dec_subset = subset[subset['Decade'] == decade]
        # Get unique artists with a sample artwork
        unique_artists = dec_subset.drop_duplicates(subset='Artist')
        sample = unique_artists.sample(n=min(5, len(unique_artists)), random_state=42)
        for _, row in sample.iterrows():
            artist_samples.append({
                'iso': iso,
                'nationality': nat_name,
                'decade': int(decade),
                'artist': row['Artist'],
                'title': row['Title'],
                'date': row['Date'],
                'medium': row['Medium'],
                'gender': row['Gender'],
            })

with open(os.path.join(OUTPUT_DIR, 'globe_artists.json'), 'w') as f:
    json.dump(artist_samples, f)


# === 10. Summary stats ===
summary = {
    'total_artworks': len(artworks_clean),
    'total_artists': len(artists_clean),
    'male_pct': round(float((artists_clean['Gender'] == 'male').sum() / len(artists_clean) * 100), 1),
    'female_pct': round(float((artists_clean['Gender'] == 'female').sum() / len(artists_clean) * 100), 1),
    'top_nationality': artists_clean['Nationality'].value_counts().index[0],
    'top_nationality_pct': round(float(artists_clean['Nationality'].value_counts().iloc[0] / len(artists_clean) * 100), 1),
    'unique_nationalities': int(artists_clean['Nationality'].nunique()),
    'date_min': int(artworks_clean['Date_numeric'].min()),
    'date_max': int(artworks_clean['Date_numeric'].max()),
    'top_department': artworks_clean['Department'].value_counts().index[0],
}
with open(os.path.join(OUTPUT_DIR, 'summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)


print("Data processing complete!")
for fn in sorted(os.listdir(OUTPUT_DIR)):
    size = os.path.getsize(os.path.join(OUTPUT_DIR, fn))
    print(f"  {fn}: {size:,} bytes")
