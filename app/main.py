# app/main.py
from fastapi import FastAPI
from app.routers import auth, users,students,teachers,groups, enrollments,subjects,attendances,xp_rule,student_xp,tests,xp_transactions,payments,telegram_auth
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="EduSystem API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(groups.router)
app.include_router(enrollments.router)
app.include_router(subjects.router)
app.include_router(attendances.router)
app.include_router(xp_rule.router)
app.include_router(student_xp.router)
app.include_router(tests.router)
app.include_router(xp_transactions.router)
app.include_router(payments.router)
app.include_router(telegram_auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # yoki ["https://webapp-vert-nine.vercel.app", "https://e4c2-...ngrok-free.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "EduSystem API ishlayapti!"}
