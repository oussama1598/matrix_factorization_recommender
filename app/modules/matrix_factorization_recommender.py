from typing import Optional, List

import pandas as pd
from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.pandas import DataFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, IntegerType, FloatType, StructField

from app.schemas.schemas import BookRating
from app.services import spark_service
from app.settings import settings


class MatrixFactorizationRecommender:
    def __init__(self):
        self.spark_session: SparkSession = spark_service.get_session()

        self.model: Optional[ALSModel] = None
        self.dataset: Optional[DataFrame] = None

        self.__load_dataset()
        self.__train_model()

    def __load_dataset(self):
        schema = StructType([
            StructField('book_id', IntegerType(), True),
            StructField('user_id', IntegerType(), True),
            StructField('rating', FloatType(), True)])

        self.dataset = self.spark_session.read.csv(settings.DATASET_PATH, header=True, schema=schema)

    def __train_model(self):
        self.model = ALS(maxIter=5, regParam=0.01, userCol='user_id', itemCol='book_id', ratingCol='rating',
                         coldStartStrategy='drop').fit(self.dataset)

    def get_top_n(self, user_id: int, n: int) -> List[BookRating]:
        ratings = self.model.recommendForUserSubset(
            self.spark_session.createDataFrame(
                pd.DataFrame([user_id], columns=['user_id'])
            ),
            n
        ).select('recommendations.book_id', 'recommendations.rating').first()

        return [
            BookRating(
                book_id=book_id,
                rating=ratings.rating[i]
            ) for i, book_id in enumerate(ratings.book_id)
        ]
