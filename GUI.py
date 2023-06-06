import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, jsonify

import warnings
warnings.filterwarnings('ignore')


app = Flask(__name__)

books = pd.read_csv(r"C:\Users\MyVampire\Desktop\AML\books\Books.csv")
ratings = pd.read_csv(r"C:\Users\MyVampire\Desktop\AML\books\Ratings.csv")
users = pd.read_csv(r"C:\Users\MyVampire\Desktop\AML\books\Users.csv")

ratings_with_name = ratings.merge(books, on='ISBN')

num_ratings_df = ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
num_ratings_df.rename(columns={'Book-Rating': 'Num-Rating'}, inplace=True)

avg_ratings_df = ratings_with_name.groupby('Book-Title').mean()['Book-Rating'].reset_index()
avg_ratings_df.rename(columns={'Book-Rating': 'AVG-Rating'}, inplace=True)

Popular_df = num_ratings_df.merge(avg_ratings_df, on='Book-Title')
Popular_df = Popular_df[Popular_df['Num-Rating'] >= 250].sort_values('AVG-Rating', ascending=False).head(50)

Popular_df = Popular_df.merge(books, on='Book-Title').drop_duplicates('Book-Title')[
    ['Book-Title', 'Book-Author', 'Image-URL-M', 'Num-Rating', 'AVG-Rating']]

x = ratings_with_name.groupby('User-ID').count()['Book-Rating'] > 200
y_u = x[x].index

filtered_rating = ratings_with_name[ratings_with_name['User-ID'].isin(y_u)]

Y = filtered_rating.groupby('Book-Title').count()['Book-Rating'] >= 50
famous_books = Y[Y].index

final_ratings = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]

pt = final_ratings.pivot_table(index='Book-Title', columns='User-ID', values='Book-Rating')
pt.fillna(0, inplace=True)

similarity_score = cosine_similarity(pt)

def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:10]
    recommended_books = []
    for i in similar_items:
        recommended_books.append(pt.index[i[0]])
    return recommended_books

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend_books():
    book_name = request.form['book_name']
    recommended_books = recommend(book_name)
    return jsonify(recommended_books=recommended_books)

if __name__ == '__main__':
    app.run()
