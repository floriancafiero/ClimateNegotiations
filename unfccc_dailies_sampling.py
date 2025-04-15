import pandas as pd
import os

# Path to the attached file
filename = "/content/ENB_UNFCCC 1995-2024 - final_data_UNFCCC.csv"

# UNFCCC Member States
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
    "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
    "Great Britain", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau",
    "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia",
    "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
    "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan",
    "Lao People's Democratic Republic", "Latvia", "Lebanon", "Lesotho",
    "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg",
    "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
    "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Federated states of Micronesia", "Micronesia",
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
    "United States of America", "United States", "USA", "the US", "Uruguay", "Uzbekistan",
    "Vanuatu", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

# Negotiation coalitions
negotiation_coalitions = [
    "Umbrella Group", "the EU", "EU", "European Union", "G77", "G-77", "G77+China", "G-77/CHINA",
    "Like-Minded Developing Countries", "LMDC", "LMDCs", "Like-Minded Group", "G 77",
    "BASIC", "BASIC Group", "Alliance of Small Island States", "AOSIS",
    "Least Developed Countries", "LDC", "LDCs", "African Group", "Arab Group",
    "High Ambition Coalition", "HAC", "Climate Vulnerable Forum", "CVF",
    "AILAC", "GST", "EIG", "Environmental Integrity Group", "ALLIANCE OF SMALL ISLAND STATES",
    "COALITION FOR RAINFOREST NATIONS", "CfRN"
]

# Target phrases
phrases = [
    "developing country", "developed country", "annex i country",
    "non-annex i country", "annex ii country", "delegat",
    "one party", "a party", "some parties", "other parties"
]

def contains_any(text, items):
    text_lower = text.lower()
    return any(item.lower() in text_lower for item in items)

def meets_condition(paragraph):
    """
    Returns True if the paragraph contains at least one
    Member State, negotiation coalition, or target phrase.
    """
    para_str = str(paragraph)
    return (
        contains_any(para_str, member_states) or
        contains_any(para_str, negotiation_coalitions) or
        contains_any(para_str, phrases)
    )

# --- 1) READ AND FILTER THE DATA ---
df = pd.read_csv(filename)

# Filter for year N
df = df[df['Year'] == 2021]

# Make sure is_daily_report is TRUE
df = df[df['daily'].astype(str).str.upper() == "TRUE"]

# Count words
df['word_count'] = df['paragraph'].apply(lambda x: len(str(x).split()))

# Keep only paragraphs >= 17 words
df = df[df['word_count'] >= 17]

# (Optional) Tag with source file if you like
df['source_file'] = os.path.basename(filename)

# --- 2) DETERMINE TOTAL COUNT (AFTER FILTERS) ---
total_count = len(df)
print(f"Total paragraphs for 2022 (daily, >=17 words): {total_count}")

# --- 3) FIND PARAGRAPHS THAT MEET THE CONDITION ---
condition_mask = df['paragraph'].apply(meets_condition)
condition_df = df[condition_mask].copy()
cond_count = len(condition_df)
print(f"Paragraphs meeting the condition: {cond_count}")

# --- 4) CALCULATE TARGET SAMPLE (15% OF total_count) ---
target_sample_size = int(0.15 * total_count)

# --- 5) SAMPLE OR TAKE ALL IF TOO FEW ---
if cond_count <= target_sample_size:
    # If fewer paragraphs meet the condition than target_sample_size,
    # take them all.
    sampled_df = condition_df
else:
    # Otherwise, randomly sample exactly target_sample_size
    sampled_df = condition_df.sample(n=target_sample_size, random_state=42)

# Drop temporary columns if desired
sampled_df = sampled_df.drop(columns=['word_count'], errors='ignore')

# --- 6) EXPORT ---
output_file = "/content/sampled_paragraphs_2021.csv"
sampled_df.to_csv(output_file, index=False)
print(f"{len(sampled_df)} paragraph(s) exported to: {output_file}")
