## SETUP

0. Install poetry globally using `pip install poetry`
1. Make a copy of the file `.env.example`, rename it to `.env`, and set environment variables. Or don't change content of file to use default values for development. See `.env.example` file for reference
2. Within cmd (working directory @ root of project folder), activate virtual environment using: `poetry shell`
3. Install project dependencies using: `poetry install`
4. Initialize database using: `main.py initial-data`
5. Run tests using `pytest`
6. Run the app using: `uvicorn main:app --reload`

<br>



## [API DOCUMENTATION](http://127.0.0.1:8000/docs)

- Authorization credentials: admin@admin.com | Password: superadmin

- Reset database using: `main.py initial-data`

- View sqlite database using [sqlitebrowser](https://sqlitebrowser.org/dl/) , otherwise use pgadmin

  - if using sqlite, run the installed sqlitebrowser

  - on the main white space upon running the app, drag&drop the `data.db` file (found within app module after running initial-data)  

  - under the Tables(n) tab, right-click the table you want to view and select 'Browse'

 <br>





## DOCS

#### THESIS 1 OUTPUT

- [data gathering](https://docs.google.com/forms/d/10Sh3mFSDDFLDSU0zRs4IrazD_ZwYSRBrY1eimmVAwJc/edit?fbclid=IwAR3YJFv_XsLop_dh6Td7LHfF1bf--9Qhy898PfDq5_2NUN96UITpSBCoY-Y)  -   [data responses](https://docs.google.com/spreadsheets/d/1GQnv96uQBPZYlaVhxOGUgCY3Ud92jL2Jrgcnp3KmR1E/edit?resourcekey#gid=1853497657)  -  [initial chapters 1-3](https://docs.google.com/document/d/1SogCDHCalx5yzXk1QAynxyxSCE_Q6m_-3kUshWWt8EQ/edit?fbclid=IwAR0JfOrIGcBSTkASUMgGMLQgoHv0P4M9USD2_ZPazmwYFejI2mY5o2sl7Z4#heading=h.vpxlmrhqpcpg)

#### POETRY BASIC USAGE

- [poetry docs](](https://python-poetry.org/docs/basic-usage/))

#### PYTHON FUNCTION ANNOTATIONS | TYPE HINTS

* NOTE: used throughout fastapi docs

- [refresher from fastapi](https://fastapi.tiangolo.com/python-types/) - [stackoverflow](https://stackoverflow.com/questions/14379753/what-does-mean-in-python-function-definitions)  -  [python pep](https://www.python.org/dev/peps/pep-3107/	)

<br>




## QOL

##### FASTAPI SHEET

- [path parameter types | data conversion | data parsing](https://fastapi.tiangolo.com/tutorial/path-params/#path-parameters-with-types)


##### SUBLIME3 SHEET

- [vertical split](https://forum.sublimetext.com/t/how-to-split-window-vertically/3652/2) USE: alt+shift+8
- [google search](https://www.google.com/search?q=sublime+text+split+screen+vertically&oq=sublime+text+split+screen+vertically&aqs=chrome..69i57j0l2j0i22i30l7.7151j0j7&sourceid=chrome&ie=UTF-8)
- [switch editor window](https://stackoverflow.com/questions/38447486/in-sublime-how-to-switch-between-panels-in-a-2-column-view/38447556)
- [space to tabs](https://stackoverflow.com/questions/22529265/sublime-text-3-convert-spaces-to-tabs)


##### OTHERS

- admin page refs
  - [flask-admin docs](https://flask-admin.readthedocs.io/en/latest/) - [getting started](https://flask-admin.readthedocs.io/en/latest/introduction/#getting-started)
  - [django admin sample](https://youtu.be/BJfyATa9nX0?t=184)