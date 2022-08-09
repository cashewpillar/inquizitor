## Setup

0. Install poetry: `pip install poetry`, then clone the repository
1. Change directory to `inquizitor` 
2. Make a copy of the file `.env.example`, rename it to `.env`, and set environment variables. Or don't change content of file to use default values for development. See `.env.example` file for reference
3. Activate virtual environment using the command `poetry shell`
   - Make sure the virtual environment is activated before running commands within the project folder
4. Install project dependencies: `poetry install`
5. Initialize database: `python main.py initial-data`
6. Run the app: `uvicorn main:app --reload`

<br>

## Dev

| Username | Password     |
| -------- | ------------ |
| admin    | superadmin   |
| teacher  | superteacher |
| student  | superstudent |

- Reset database: `python main.py initial-data`
- Run tests: `pytest`
- Use [Black Playground](https://black.vercel.app/) to check if code snippet conforms to PEP8
- View SQLite database using [sqlitebrowser](https://sqlitebrowser.org/dl/) , otherwise use pgadmin
  - if using SQLite, run the installed sqlitebrowser
  - on the main white space upon running the app, drag&drop the `data.db` file (found within app module after running initial-data)  
  - under the Tables(n) tab, right-click the table you want to view and select 'Browse'

 <br>

## Docker Setup

If you want to use Docker, it is recommended to have a free diskspace of 2 GB. Running docker-compose will eventually download 1.2 GB at the minimum.  

0. Install Docker: [Ubuntu Linux](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04) - [Windows](https://docs.docker.com/docker-for-windows/install/)
1. Run the entire app (backend and db): `docker-compose up -d`
   - Remove `-d` to enable the logs
2. Initialize/ reset the database: `docker exec inquizitor_backend_1 python main.py initial-data`

<br>

## Docker Commands

1. If you made changes to the `Dockerfile`, rebuild the docker app: `docker-compose up --build`
2. If you made changes to the `docker-compose.yml` file, re-run the app: `docker-compose up`
3. If you made changes to the backend code, restart the backend container: `docker-compose restart backend`
4. Run backend tests using: `docker exec inquizitor_backend_1 pytest`

<br>

## Documentation

to access the interactive API documentation, go to http://127.0.0.1:8000/docs

<img src="media/doc-swagger-ui.png" style="zoom: 200%;" />
