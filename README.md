## Project setup and run:

1. Install packages: `pip install -r requirements.txt`
2. Add to app/ folder config.ini file with the following config:
   ```
   [database]
   driver = postgresql
   host = localhost
   port = 5432
   database_name = your_db_name
   username = your_username
   password = your_password
   ```
3. Run command: `uvicorn app.main:app --reload`

## Database migrations:

1. Append your code with import of a new model to alembic/env.py file like in the example below:
   ```
   from app.series.models import Series
   from app.user.models import User
   ```
2. Run command: `alembic revision --autogenerate -m "<your migration message>"`
3. Apply recently created migration: `alembic upgrade head`
