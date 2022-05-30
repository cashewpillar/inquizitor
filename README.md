## SETUP

0. Install poetry globally using `pip install poetry`
1. Make a copy of the file `.env.example`, rename it to `.env`, and set environment variables. Or don't change content of file to use default values for development. See `.env.example` file for reference
2. Within cmd (working directory @ root of project folder), activate virtual environment using: `poetry shell`
3. Install project dependencies using: `poetry install`
4. For windows, initialize database using: `main.py initial-data`, else use `python main.py initial-data`
5. Run tests using `pytest`
6. Run the app using: `uvicorn main:app --reload`

<br>






## [API DOCUMENTATION (run app before accessing)](http://127.0.0.1:8000/docs)

- Authorization credentials: admin | Password: superadmin

- Reset database using: `main.py initial-data` or `python main.py initial-data`

- View sqlite database using [sqlitebrowser](https://sqlitebrowser.org/dl/) , otherwise use pgadmin

  - if using sqlite, run the installed sqlitebrowser

  - on the main white space upon running the app, drag&drop the `data.db` file (found within app module after running initial-data)  

  - under the Tables(n) tab, right-click the table you want to view and select 'Browse'

 <br>
