import pandas as pd
import re

# Load the CSV into a DataFrame
df = pd.read_csv('/content/ENB_UNFCCC 1995-2022 - final_data_UNFCCC.csv')  

# Step 1: Exclude paragraphs with fewer than 17 words.

# Create a temporary word count column based on the 'paragraph' column.
df['word_count'] = df['paragraph'].apply(lambda x: len(str(x).split()))
df_filtered = df[df['word_count'] >= 17]

# Step 2: Include only paragraphs that name a UNFCCC member state and a negotiation coalition.

# Replace these lists with the actual names as appropriate.
member_states = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus",
    "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
    "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada",
    "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros",
    "Republic of the Congo", "Cook Islands", "Costa Rica", "Côte d'Ivoire", "Croatia",
    "Cuba", "Cyprus", "Czech Republic", "Democratic People's Republic of Korea",
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica",
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "European Union", "Fiji",
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Great Britain",
    "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana",
    "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia",
    "Iran", "Iraq", "Ireland", "Israel", "Italy",
    "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
    "Kuwait", "Kyrgyzstan", "Lao People's Democratic Republic", "Latvia",
    "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
    "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
    "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico",
    "Micronesia", "Monaco", "Mongolia", "Montenegro",
    "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal",
    "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue",
    "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland",
    "Portugal", "Qatar", "Republic of Korea", "Republic of Moldova", "Romania",
    "Russian Federation", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
    "Saint Vincent and the Grenadines", "Samoa", "San Marino",
    "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles",
    "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
    "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan",
    "Suriname", "Sweden", "Switzerland", "Syrian Arab Republic", "Tajikistan",
    "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago",
    "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom", "UK",
    "United States of America", "United States", "USA", "Uruguay", "Uzbekistan", "Vanuatu",
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]
negotiation_coalitions = [
    "Umbrella Group",
    "EU", "European Union",
    "G77", "G-77", "G77+China", "G 77",
    "Like-Minded Developing Countries", "LMDC", "LMDCs", "Like-Minded Group",
    "BASIC", "BASIC Group",
    "Alliance of Small Island States", "AOSIS",
    "Least Developed Countries", "LDC", "LDCs",
    "High Ambition Coalition", "HAC",
    "Climate Vulnerable Forum", "CVF"
]
def contains_any(text, items):
    """Check if any of the items are present in the text (case-insensitive)."""
    text_lower = text.lower()
    return any(item.lower() in text_lower for item in items)

df_filtered = df_filtered[
    df_filtered['paragraph'].apply(lambda x: contains_any(str(x), member_states)) &
    df_filtered['paragraph'].apply(lambda x: contains_any(str(x), negotiation_coalitions))
]

# Step 3: Filter paragraphs that contain at least one of the key phrases.
phrases = [
    "developing country",
    "developed country",
    "annex i country",
    "non-annex i country",
    "annex ii country",
    "delegat",    # to Ian: covers "delegate", "delegates", etc. Equivalent of your "delegat*"
    "one party",
    "a party",
    "some parties",
    "other parties"
]

df_filtered = df_filtered[
    df_filtered['paragraph'].apply(lambda x: any(phrase in str(x).lower() for phrase in phrases))
]

# Step 4: From the filtered set, randomly select 15% of the paragraphs for review.

# Setting a random_state ensures reproducibility.
sampled_df = df_filtered.sample(frac=0.15, random_state=42)

# Optionally, drop the temporary word count column if no longer needed. But can be useful ?
sampled_df = sampled_df.drop(columns=['word_count'])

# Output the sampled DataFrame
print(sampled_df)

# Save the final sampled DataFrame to a CSV file
output_file = "sampled_paragraphs.csv"
sampled_df.to_csv(output_file, index=False)
print(f"Output saved to {output_file}")

import pandas as pd
import os

# Liste des fichiers (assurez-vous qu’ils soient bien uploadés dans `/content/`)
files = [
    "/content/bonn-climate-change-conference-sbi58-sbsta58.csv",
    "/content/bonn-climate-change-conference-sbi60-sbsta60.csv",
    "/content/united-arab-emirates-climate-change-conference-cop28.csv",
    "/content/baku-un-climate-change-conference-cop29.csv"
]

# États membres UNFCCC
member_states = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas",
    "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin",
    "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei",
    "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon",
    "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia",
    "Comoros", "Republic of the Congo", "Cook Islands", "Costa Rica", "Côte d'Ivoire",
    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Democratic People's Republic of Korea",
    "Democratic Republic of the Congo", "Denmark", "Djibouti", "Dominica",
    "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea",
    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "European Union", "Fiji",
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
    "Great Britain", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia",
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
    "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
    "Lao People's Democratic Republic", "Latvia", "Lebanon", "Lesotho",
    "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
    "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia",
    "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar",
    "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua",
    "Niger", "Nigeria", "Niue", "North Macedonia", "Norway", "Oman",
    "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay", "Peru",
    "Philippines", "Poland", "Portugal", "Qatar", "Republic of Korea",
    "Republic of Moldova", "Romania", "Russian Federation", "Rwanda",
    "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines",
    "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal",
    "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
    "Solomon Islands", "Somalia", "South Africa", "South Sudan", "Spain",
    "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland",
    "Syrian Arab Republic", "Tajikistan", "Thailand", "Timor-Leste", "Togo",
    "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
    "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "UK",
    "United States of America", "United States", "USA", "Uruguay", "Uzbekistan",
    "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

# Coalitions de négociation
negotiation_coalitions = [
    "Umbrella Group", "EU", "European Union", "G77", "G-77", "G77+China", "G 77",
    "Like-Minded Developing Countries", "LMDC", "LMDCs", "Like-Minded Group",
    "BASIC", "BASIC Group", "Alliance of Small Island States", "AOSIS",
    "Least Developed Countries", "LDC", "LDCs", "High Ambition Coalition", "HAC",
    "Climate Vulnerable Forum", "CVF"
]

# Expressions cibles
phrases = [
    "developing country", "developed country", "annex i country",
    "non-annex i country", "annex ii country", "delegat",
    "one party", "a party", "some parties", "other parties"
]

def contains_any(text, items):
    text_lower = text.lower()
    return any(item.lower() in text_lower for item in items)

def process_file(filepath):
    df = pd.read_csv(filepath)
    if 'paragraph' not in df.columns:
        raise ValueError(f"'paragraph' column not found in {filepath}")

    df['word_count'] = df['paragraph'].apply(lambda x: len(str(x).split()))
    df_filtered = df[df['word_count'] >= 17]

    df_filtered = df_filtered[
        df_filtered['paragraph'].apply(lambda x: contains_any(str(x), member_states)) &
        df_filtered['paragraph'].apply(lambda x: contains_any(str(x), negotiation_coalitions))
    ]

    df_filtered = df_filtered[
        df_filtered['paragraph'].apply(lambda x: any(p in str(x).lower() for p in phrases))
    ]

    df_filtered['source_file'] = os.path.basename(filepath)
    return df_filtered.drop(columns=['word_count'])

# Appliquer à tous les fichiers
all_filtered = pd.concat([process_file(f) for f in files], ignore_index=True)

# Échantillonnage 15 %
sampled_df = all_filtered.sample(frac=0.15, random_state=42)

# Export
output_file = "/content/sampled_paragraphs_all_conferences.csv"
sampled_df.to_csv(output_file, index=False)
print(f"{len(sampled_df)} paragraphes exportés dans : {output_file}")




