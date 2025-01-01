import pandas as pd
from pymongo import MongoClient
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer, WordNetLemmatizer
from datetime import datetime
import sys
import json

# Ensure NLTK resources are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')
db = client['news_database']
collection = db['headlines']

# Load data from MongoDB into a DataFrame
data = pd.DataFrame(list(collection.find()))

# Convert timestamp to datetime format
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce', utc=True)

# Parse command-line arguments
if len(sys.argv) != 3:
    print(json.dumps({"error": "Usage: python b.py <start_date> <end_date>"}))
    sys.exit(1)

start_date_str = sys.argv[1]
end_date_str = sys.argv[2]

# Convert date strings to datetime objects, including timezone info
start_date = pd.to_datetime(start_date_str, errors='coerce', utc=True)
end_date = pd.to_datetime(end_date_str, errors='coerce', utc=True)

if pd.isna(start_date) or pd.isna(end_date):
    print(json.dumps({"error": "Invalid date format."}))
    sys.exit(1)

# Remove timezone info if necessary for comparison
start_date = start_date.tz_localize(None)
end_date = end_date.tz_localize(None)

# Filter data by date range
data_filtered = data[(data['timestamp'].dt.date >= start_date.date()) & (data['timestamp'].dt.date <= end_date.date())]

if data_filtered.empty:
    print(json.dumps({"error": "No data found in the specified date range."}))
    sys.exit(1)

# Preprocess text data with stemming and lemmatization
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]
    tokens = [stemmer.stem(word) for word in tokens]  # Apply stemming
    tokens = [lemmatizer.lemmatize(word) for word in tokens]  # Apply lemmatization
    return tokens

# Tokenize and preprocess headlines
data_filtered['tokens'] = data_filtered['headline'].apply(preprocess_text)

# Flatten list of tokens for all headlines
all_tokens = [token for sublist in data_filtered['tokens'] for token in sublist]

# Compute frequency distribution
freq_dist = FreqDist(all_tokens)

# Get the most common words (not limited to top 50)
top_words_set = set(dict(freq_dist).keys())

# Determine the most relevant headlines (example criteria: most common words appearing in headlines)
def relevance_score(tokens, common_words):
    return sum(1 for word in tokens if word in common_words)

# List to store relevant headlines with scores
relevant_headlines = []

# Filter headlines with more than 4 words
def is_long_headline(headline):
    return len(word_tokenize(headline)) > 4

for index, row in data_filtered.iterrows():
    if is_long_headline(row['headline']):
        tokens = row['tokens']
        score = relevance_score(tokens, top_words_set)
        if score > 0:  # Threshold for relevance, adjust as needed
            relevant_headlines.append({
                'headline': row['headline'],
                'link': row['link'],
                'source': row['source'],
                'timestamp': row['timestamp'].isoformat(),
                'score': score
            })

# Convert to DataFrame for easy sorting and display
relevant_df = pd.DataFrame(relevant_headlines)

# Ensure 'score' column is present
if 'score' not in relevant_df.columns:
    print(json.dumps({"error": "'score' column is missing."}))
    sys.exit(1)

# Sort by score in descending order
sorted_relevant_news = relevant_df.sort_values(by='score', ascending=False)

# Output the results as JSON
print(json.dumps(sorted_relevant_news.to_dict(orient='records')))
