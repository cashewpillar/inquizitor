'''
ASSUMPTIONS ====================================================
Users cannot create accounts, only update password thru forgot password
Accounts are created by admin via script using data gathered
	- survey sampling > hand out google forms > process google sheets data
	- how will we select respondents? bulletin board? student list?


STUFF TO DO (in order) ==========================================
CONTINUE
Quiz crud - add models for student and teacher + factories
	REFERENCES
		https://quizapi.io/docs/1.0/endpoints
		https://data-flair.training/blogs/create-quiz-application-python-django/
		https://techvidvan.com/tutorials/quiz-web-app-python-django/
		https://www.google.com/search?q=python+models+for+quiz+taking&oq=python+models+for+quiz+taking&aqs=chrome..69i57.6841j0j7&sourceid=chrome&ie=UTF-8

		https://github.com/learningequality/kolibri/blob/release-v0.15.x/kolibri/core/exams/models.py
		https://github.com/instructure/canvas-lms/blob/master/app/models/quizzes/quiz.rb

USER TESTS - checking if superuser & stuff

MIGRATIONS - [Reads](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
App Settings/ Configurations for Development, Deployment etc.
Password reset

LEGEND ===========================================================
TODO - to do
DOING - here here
NOTE - remember me
'''


from fastapi_tut import create_app
from fastapi_tut.commands import cli

app = create_app()

if __name__ == "__main__":
	cli()