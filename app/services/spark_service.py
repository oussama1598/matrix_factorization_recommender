from functools import lru_cache

from pyspark.sql import SparkSession


@lru_cache()
def get_session() -> SparkSession:
    return SparkSession.builder.appName('Recommender-app').getOrCreate()
