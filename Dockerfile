FROM python:3.11

WORKDIR /code

COPY ./alembic.ini /code/alembic.ini

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./alembic /code/alembic

# COPY entrypoint.sh /code 

# RUN chmod +x entrypoint.sh

# ENTRYPOINT ["./entrypoint.sh"]
