from typing import List

from app.modules.knn_content_recommender import KNNContentRecommender
from app.modules.knn_item_recommender import KNNItemRecommender
from app.modules.knn_user_recommender import KNNUserRecommender
from app.modules.matrix_factorization_recommender import MatrixFactorizationRecommender

recommenders = {
    'matrix_factorization': MatrixFactorizationRecommender(),
    'knn_item': KNNItemRecommender(),
    'knn_user': KNNUserRecommender(),
    'knn_content': KNNContentRecommender()
}


def get_recommender(recommender_name: str):
    return recommenders[recommender_name]


def get_available_recommenders() -> List[str]:
    return list(recommenders.keys())
