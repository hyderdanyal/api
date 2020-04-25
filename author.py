# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 15:37:15 2020

@author: Saad
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

books = pd.read_csv('dataset/books.csv', encoding = "ISO-8859-1")
books.head()

books.shape

ratings = pd.read_csv('dataset/ratings.csv', encoding = "ISO-8859-1")
ratings.head()

book_tags = pd.read_csv('dataset/book_tags.csv', encoding = "ISO-8859-1")
book_tags.head()

tags = pd.read_csv('dataset/tags.csv')
tags.tail()

tags_join_DF = pd.merge(book_tags, tags, left_on='tag_id', right_on='tag_id', how='inner')
tags_join_DF.head()

to_read = pd.read_csv('dataset/to_read.csv')
to_read.head()

tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(books['authors'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


titles = books['title']
g_id=books['goodreads_book_id']
url=books['image_url']

indices = pd.Series(books.index, index=books['title'])

# Function that get book recommendations based on the cosine similarity score of book authors
def authors_recommendations(title):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:21]
    book_indices = [i[0] for i in sim_scores]
    #for i in book_indices:
      #  book_indices=i+1
    # print("Titles are:",titles.iloc[book_indices])
    # print("Good_read books Id is",g_id.iloc[book_indices])
    # print("URL is",url.iloc[book_indices])
    tup1 = ('title','goodread-id','url')
    tup2 = (titles.iloc[book_indices],g_id.iloc[book_indices],url.iloc[book_indices])
    res = dict(zip(tup1,tup2))
    print("Dict: " +str(res))
        
    
    #print(books[books["goodreads_book_id","title"]]==titles.iloc[book_indices])
    #return titles.iloc[book_indices]

authors_recommendations('The Hobbit')
# {
#     "id":"154":
#         {"id":"154","title":"The Two Towers (The Lord of the Rings, #2)","url":"https://images.gr-assets.com/books/1298415523m..."},
#     "id":"160":
#         {"id":"160","title":"The Return of the King (The Lord of the Rings)","url":"https://images.gr-assets.com/books/1389977161m..."}
# }