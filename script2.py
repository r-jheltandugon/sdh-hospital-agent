import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Text preprocessing function
def preprocess_text(text):
    # Lowercasing the text
    text = text.lower()

    # Tokenize the text and remove stopwords
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatize each word to its base form
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Join tokens back into a string
    return " ".join(tokens)

# Apply preprocessing to the Description column
df['processed_description'] = df['Description'].apply(preprocess_text)

# Check the results
print(df[['Disease', 'processed_description']].head())
