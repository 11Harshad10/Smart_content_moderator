# Smart_content_moderator
Smart Content Moderator is a machine learning-based web application designed to detect and filter toxic or harmful user-generated content. It uses a trained text classification model to assess whether a piece of text contains toxic language. The model is hosted with a simple backend (likely using Flask), and users interact via a web-based interface

# Smart Content Moderator

A machine learning-powered web application for detecting and moderating toxic user-generated content.

## 💡 Features

- Detects and classifies toxic comments using a trained ML model
- Simple web-based interface to test content
- REST API for content classification
- Pre-trained vectorizer and classifier using NLP techniques
- Integration-ready backend

## 🧠 Model

- The model is trained using NLP techniques on a dataset of toxic and non-toxic comments.
- Vectorization is done using `TfidfVectorizer`.
- Classifier is stored as `toxic_comment_classifier.pkl`.
- Includes Jupyter notebooks for training and testing (`model1.ipynb`, `predictor.ipynb`).

## 🗂️ Project Structure

Smart_content_Moderator/
│
├── backend.py # API and backend logic
├── Connect.py # Possibly handles database or API integrations
├── model1.ipynb # Model training notebook
├── predictor.ipynb # Prediction logic and experiments
├── test_api.py # Script to test the backend API
├── templates/
│ └── index.html # Web interface
├── toxic_comment_classifier.pkl # Trained classifier
├── vectorizer.pkl # Fitted TF-IDF vectorizer
└── client_secret_...json # Google API credentials (DO NOT SHARE)
