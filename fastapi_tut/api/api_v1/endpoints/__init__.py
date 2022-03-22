'''
SCRATCH PAD

# ======================================================
# API ENDPOINTS FOR ADMINISTERING ONLINE EXAMS (PROTOTYPE), WITH BUILT-IN CHEATING DETECTION
# ======================================================


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