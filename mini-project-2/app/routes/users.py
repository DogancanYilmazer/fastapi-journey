from fastapi import APIRouter, HTTPException, status

from database.connection import Database
from models.users import User, UserSignIn, UserSignUp


router = APIRouter(prefix="/user", tags=["Users"])
user_database = Database(User)


@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignUp) -> User:
	users = await user_database.get_all()
	if any(existing_user.email == user.email for existing_user in users):
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="User with this email already exists",
		)

	new_user = User(email=user.email, password=user.password)
	return await user_database.save(new_user)


@router.post("/signin")
async def signin(credentials: UserSignIn) -> dict:
	users = await user_database.get_all()

	for user in users:
		if user.email == credentials.email and user.password == credentials.password:
			return {"message": "Signin successful"}

	raise HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Invalid email or password",
	)

