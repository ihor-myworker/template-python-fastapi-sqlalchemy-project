# DEPRECATED

from sqlalchemy import MetaData

from app.database.utils import get_engine_from_config
from app.series.models import Base as series_base
from app.user.models import Base as user_base

if __name__ == "__main__":
    engine = get_engine_from_config()

    # # create a metadata object
    # metadata = MetaData()
    # # bind the metadata object to the engine
    # metadata.bind = engine

    # create tables based on the models
    user_base.metadata.reflect(bind=engine)
    user_base.metadata.create_all(checkfirst=True)

    series_base.metadata.reflect(bind=engine)
    series_base.metadata.create_all(checkfirst=True)
