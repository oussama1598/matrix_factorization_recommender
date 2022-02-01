from typing import List

from app.modules.knn_recommender import KNNRecommender
from app.modules.matrix_factorization_recommender import MatrixFactorizationRecommender

recommenders = {
    'matrix_factorization': MatrixFactorizationRecommender(),
    'knn': KNNRecommender()
}


def get_recommender(recommender_name: str):
    return recommenders[recommender_name]


def get_available_recommenders() -> List[str]:
    return list(recommenders.keys())
