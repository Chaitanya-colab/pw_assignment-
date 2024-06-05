# 4. Develop a recommendation system using Flask that suggests content to users based on their preferences.

from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)

books = pd.read_csv('books.csv')


tfidf = TfidfVectorizer(stop_words='english')
books['description'] = books['description'].fillna('')
tfidf_matrix = tfidf.fit_transform(books['description'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


def get_recommendations(title, cosine_sim=cosine_sim):
    idx = books[books['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    book_indices = [i[0] for i in sim_scores]
    return books.iloc[book_indices]

@app.route('/')
def index():
    return render_template('index3.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    title = request.form['title']
    recommendations = get_recommendations(title)
    return render_template('recommendations.html', recommendations=recommendations.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)