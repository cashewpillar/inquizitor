# UNUSED BCS EXTENSIONS && UNKNOWNS
# deps.get_current_user()
# create_access_token()
# fastapi_jwt_auth token expiry

# ASSUMPTIONS ===================================
# users cannot create accounts, only update password thru forgot password
# accounts are created by admin via script using data gathered
# 	- survey sampling > hand out google forms > process google sheets data
# 	- how will we select respondents? bulletin board? student list?

# STUFF TO DO (in order) ==========================================
# Refresh Tokens
	# https://indominusbyte.github.io/fastapi-jwt-auth/usage/revoking/
	# https://stackoverflow.com/questions/32060478/is-a-refresh-token-really-necessary-when-using-jwt-token-authentication
	# https://developer.okta.com/docs/guides/refresh-tokens/main/#about-refresh-tokens
	# https://stackoverflow.com/questions/62413698/how-to-use-refresh-token-with-fastapi
# Admin crud (esp for accessing mouse data)
# Exams crud
# Securing JWT Login with HttpOnly Cookie: 
# 	https://www.fastapitutorial.com/blog/fastapi-jwt-httponly-cookie/
# OAuth2 with Password (and hashing), Bearer with JWT tokens
# 	https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#update-the-dependencies
# App Settings/ Configurations for Development, Deployment etc.
# Migrations - [Reads](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

# fastapi docs   : https://fastapi.tiangolo.com/tutorial/body-multiple-params/
# fastapi tut    : https://www.fastapitutorial.com/blog/fastapi-route/
# sqlalchemy docs: https://docs.sqlalchemy.org/en/14/orm/session_basics.html#what-does-the-session-do
# vuejs tut      : https://v3.vuejs.org/guide/introduction.html#composing-with-components
# quasar docs    : https://quasar.dev/start/umd

# LEGEND:
# TODO - to do
# NOTE - remember me

from fastapi_tut import create_app
from fastapi_tut.commands import cli

app = create_app()

if __name__ == "__main__":
	cli()



# ======================================================
# API ENDPOINTS FOR ADMINISTERING ONLINE EXAMS (PROTOTYPE), WITH BUILT-IN CHEATING DETECTION
# ======================================================
'''
exam_app = FastAPI()

# Module 1: Landing 
@exam_app.get("/")
async def root():
	# [Module 4] if logged in as teacher, redirect to teacher's dashboard
	# [Module 5] if logged in as student, redirect to student's dashboard
	# else:
	return {"message": "Welcome!"}
	
# Module 2: Sign Up 
@exam_app.get("/signup")
async def signup():
	return {"message": "Sign Up"}	

# Module 3: Login 
@exam_app.get("/login")
async def login():
	return {"message": "Log In"}

# Module 6: [TEACHER] My Exams 
@exam_app.get("/exams")
async def my_exams():
	return {"message": "My Exams"}
	
# [TEACHER] [STUDENT]
@exam_app.get("/exams/{exam_id}")
async def read_exam(exam_id: int):
	return {"message": f"Exam {float(exam_id)}"}

@exam_app.get("/exams/create")
async def create_exam():
	return {"message": "Create Exam"}

# Module 7: [TEACHER] Reports 
@exam_app.get("/reports")
async def report():
	return {"message": "Reports"}

# Module 8: Update Profile
@exam_app.get("/profile/update")
async def update_profile():
	return {"message": "Profile"}

# Module 9: [STUDENT] Activities 
@exam_app.get("/activities")
async def report():
	return {"message": "Activities"}

'''



