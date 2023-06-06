import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))



import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


import warnings
warnings.filterwarnings('ignore')

books=pd.read_csv(r"C:\Users\MyVampire\Desktop\AML\books\Books.csv")
ratings=pd.read_csv(r"C:\Users\MyVampire\Desktop\AML\books\Ratings.csv")
users=pd.read_csv(r"C:\Users\MyVampire\Desktop\AML\books\Users.csv")

books.isnull().sum()


ratings_with_name = ratings.merge(books,on ='ISBN')
ratings_with_name


num_ratings_df =ratings_with_name.groupby('Book-Title').count()['Book-Rating'].reset_index()


num_ratings_df.rename(columns ={'Book-Rating': 'Num-Rating'},inplace= True)
num_ratings_df


avg_ratings_df =ratings_with_name.groupby('Book-Title').mean()['Book-Rating'].reset_index()
avg_ratings_df.rename(columns ={'Book-Rating': 'AVG-Rating'},inplace= True)
avg_ratings_df


Popular_df = num_ratings_df.merge(avg_ratings_df , on = 'Book-Title')
Popular_df


Popular_df =Popular_df[Popular_df['Num-Rating']>= 250].sort_values('AVG-Rating',ascending=False).head(50)



Popular_df = Popular_df.merge(books , on = 'Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author', 'Image-URL-M','Num-Rating','AVG-Rating']]


x = ratings_with_name.groupby('User-ID').count()['Book-Rating']>200
y_u = x[x].index

filterd_rating = ratings_with_name[ratings_with_name['User-ID'].isin(y_u)]
filterd_rating

Y = filterd_rating.groupby('Book-Title').count()['Book-Rating']>=50
famous_books =Y[Y].index


final_ratings = filterd_rating[filterd_rating['Book-Title'].isin(famous_books)]


pt =final_ratings.pivot_table(index = 'Book-Title', columns = 'User-ID', values = 'Book-Rating')
pt.shape

pt.fillna(0 , inplace=True)
pt


from sklearn.metrics.pairwise import cosine_similarity
similarity_score =cosine_similarity(pt)


def recommend(book_name):
    #index fetch
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])), key = lambda x:x[1], reverse= True )[1:10]
    
    for i in similar_items:
        print(pt.index[i[0]])


recommend('Secrets')

###############################################################################################################################################



# Create the main application window
window = tk.Tk()
window.title("Book Recommender")
window.geometry("400x300")

# Function to handle the recommendation
def recommend_book():
    book_name = entry_book.get()
    # Call the recommend function from the original code
    recommended_books = recommend(book_name)
    # Display the recommended books in a message box
    messagebox.showinfo("Recommended Books", "\n".join(recommended_books))

# Create GUI elements
label_book = ttk.Label(window, text="Enter a Book Title:")
label_book.pack()

entry_book = ttk.Entry(window)
entry_book.pack()

button_recommend = ttk.Button(window, text="Recommend", command=recommend_book)
button_recommend.pack()

# Start the GUI event loop
window.mainloop()
