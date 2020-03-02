# earnup-project
1. Create a Python 3 virtual env and activate it
2. Change directories to "earnup-project/earnup" directory
3. Install required packages: `pip install -r requirements.txt`
4. [Optional] Add configuration to use Postgres as the backing database.
<br>Note: Text search results will be better if using Postgres as the backing
database instead of the default SQLite.  In order to use Postgres, the
following environment variables must be present:
    <br>'EARNUP_DB_HOST' (will default to '127.0.0.1' if not present)
    <br>'EARNUP_DB_PORT' (will default to '5432' if not present)
    <br>'EARNUP_DB_NAME' (no default)
    <br>'EARNUP_DB_USERNAME' (no default - user must have read-write access to db)
    <br>'EARNUP_DB_PASSWORD' (no default - user must have read-write access to db)
5. Migrate the database: `python manage.py migrate`
6. Load the data: `python manage.py load_data <path to read data file> <path to write error output file>`
7. Start up the app: `python manage.py runserver`
8. Send POST requests to http://127.0.0.1:8000/search to query the imported data
<br>As shown in the project description, request payload should have the form:
<br>`{"latitude": 41, "longitude": -73, "distance": 300.7, "query": "near the empire state building"}`
<br>(all keys optional)
