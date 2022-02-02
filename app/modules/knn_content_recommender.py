from typing import Optional, List

import nltk
import numpy as np
from nltk.corpus import stopwords
import string
from nltk.stem.wordnet import WordNetLemmatizer
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from app.settings import settings

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

stop_en = stopwords.words('english')
stop_en.append("toread")
stop_en.append("currentlyreading")
stop_en = set(stop_en)
stop_fr = set(stopwords.words('french'))
stop = stop_en.union(stop_fr)
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()


def clean_text(name):
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ.')
    return ''.join(filter(whitelist.__contains__, name)).strip()


def clean(text):
    stop_free = ' '.join([word for word in text.lower().split() if word not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = ' '.join([lemma.lemmatize(word) for word in punc_free.split()])
    return normalized


class KNNContentRecommender:
    def __init__(self):
        self.K: int = 10

        self.dataset: Optional[pd.DataFrame] = None
        self.matrix = None

        self.book_mapper = None
        self.book_inv_mapper = None

        self.__load_dataset()
        self.__train_model()

    def __load_dataset(self):
        self.books = pd.read_csv(settings.BOOKS_PATH)
        self.tags = pd.read_csv(settings.TAGS_PATH)
        self.book_tags = pd.read_csv(settings.BOOK_TAGS_PATH)

    def __train_model(self):
        self.tags.tag_name = self.tags.tag_name.apply(lambda x: clean_text(x))
        self.dataset = self.book_tags.merge(self.tags, on='tag_id')
        self.dataset.tag_name = self.dataset.tag_name.apply(lambda x: x + ' ')

        self.dataset = self.dataset[["goodreads_book_id", "tag_name"]].groupby(by="goodreads_book_id").sum()
        self.dataset = self.dataset.reset_index()

        self.dataset.tag_name = self.dataset.tag_name.apply(lambda x: clean(x))

        tf = TfidfVectorizer(analyzer=lambda s: s.split())
        self.matrix = tf.fit_transform(self.dataset.tag_name)

        self.book_mapper = dict(zip(np.unique(self.dataset["goodreads_book_id"]), list(range(self.matrix.shape[0]))))
        self.book_inv_mapper = dict(
            zip(list(range(self.matrix.shape[0])), np.unique(self.dataset["goodreads_book_id"])))

        self.model = NearestNeighbors(n_neighbors=self.K, algorithm="brute", metric='cosine')
        self.model.fit(self.matrix)

    def get_top_n(self, book_id: int) -> List[int]:
        neighbour_ids = []

        book_ind = self.book_mapper[book_id]
        book_vec = self.matrix[book_ind].reshape(1, -1)

        neighbour = self.model.kneighbors(book_vec, return_distance=False)

        for i in range(0, self.K):
            n = neighbour.item(i)
            neighbour_ids.append(self.book_inv_mapper[n])

        book_ids = dict(zip(self.books['book_id'], self.books['id']))

        return [
            book_ids[b_id] for b_id in neighbour_ids
        ]
