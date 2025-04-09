import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Step 1: Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Step 2: Load the dataset
dataset_path = "C:/Users/admin/.cache/kagglehub/datasets/itachi9604/disease-symptom-description-dataset/versions/2/symptom_Description.csv"
df = pd.read_csv(dataset_path)

# Step 3: Preprocess the text
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

# Apply preprocessing to the 'Description' column
df['processed_description'] = df['Description'].apply(preprocess_text)

# Print the original and processed data
print("Original Data:")
print(df[['Disease', 'Description']].head())

print("\nProcessed Data:")
print(df[['Disease', 'processed_description']].head())

# Step 4: Vectorize the descriptions using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['processed_description']).toarray()

# Step 5: Encode disease labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['Disease'])

# Step 6: Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 7: Train the model using Logistic Regression
model = LogisticRegression()
model.fit(X_train, y_train)

# Step 8: Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"\nModel Accuracy: {accuracy * 100:.2f}%")

# Step 9: Make predictions with a new description
new_description = "A person experiences severe dizziness, nausea, and blurred vision."
processed_new_description = preprocess_text(new_description)
new_description_vector = vectorizer.transform([processed_new_description]).toarray()
predicted_label = model.predict(new_description_vector)
predicted_disease = label_encoder.inverse_transform(predicted_label)

print(f"\nPredicted Disease for new description: {predicted_disease[0]}")
