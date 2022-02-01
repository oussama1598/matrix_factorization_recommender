from typing import Optional, List

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from app.settings import settings


class KNNUserRecommender:
    def __init__(self):
        self.K: int = 10

        self.dataset: Optional[pd.DataFrame] = None
        self.books: Optional[pd.DataFrame] = None

        self.user_mapper = None
        self.book_mapper = None
        self.user_inv_mapper = None
        self.book_inv_mapper = None

        self.matrix = None

        self.__load_dataset()
        self.__create_matrix()
        self.__train_model()

    def __load_dataset(self):
        self.dataset = pd.read_csv(settings.DATASET_PATH)
        self.books = pd.read_csv(settings.BOOKS_DIR)

    def __create_matrix(self):
        user_ids = self.dataset['user_id']
        books_ids = self.dataset['book_id']

        N = len(user_ids.unique())
        M = len(books_ids.unique())

        # Map Ids to indices
        self.user_mapper = dict(zip(np.unique(user_ids), list(range(N))))
        self.book_mapper = dict(zip(np.unique(books_ids), list(range(M))))

        # Map indices to IDs
        self.user_inv_mapper = dict(zip(list(range(N)), np.unique(user_ids)))
        self.book_inv_mapper = dict(zip(list(range(M)), np.unique(books_ids)))

        user_index = [self.user_mapper[i] for i in user_ids]
        book_index = [self.book_mapper[i] for i in books_ids]

        self.matrix = csr_matrix((self.dataset['rating'], (book_index, user_index)), shape=(M, N))

    def __train_model(self):
        self.model = NearestNeighbors(n_neighbors=self.K, algorithm="brute", metric='cosine')
        self.model.fit(self.matrix)

    def get_top_n(self, user_id: int):
        similar_ids = []
        user_ind = self.user_mapper[user_id]
        user_vec = self.matrix[user_ind]

        neighbour = self.model.kneighbors(user_vec, return_distance=False)

        for i in range(0, self.K):
            n = neighbour.item(i)
            similar_ids.append(self.user_inv_mapper[n])

        recommend_books = []
        weights = []
        for i in similar_ids:
            for x in self.dataset.loc[self.dataset.user_id == i].book_id.values.tolist():
                avg = self.books.loc[self.books.id == x].average_rating.values[0]
                recommend_books.append(x)
                weights.append(avg)
        recommend_books = np.unique(recommend_books)
        weights = np.unique(weights)
        recommend_books = recommend_books.tolist()
        weights = weights.tolist()
        recommend_books = pd.DataFrame(list(zip(recommend_books, weights)), columns=["books", "rating"]).sort_values(
            by="rating", ascending=False).iloc[0:11].books.values.tolist()

        return recommend_books
