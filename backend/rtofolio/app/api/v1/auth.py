from fastapi import APIRouter, HTTPException, status, Request, Response
from app.schemas.user import SignUpWithEmailSchema, UserSchema, LogiSchema

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(request: Request, response: Response , user_data: SignUpWithEmailSchema):
    db = request.app.supabase
    mongo_db = request.app.mongodb
    
    existing_user = await mongo_db["users"].find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    try:
        user = db.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password
        })
    
    except AuthApiError as e:
        # 3. Catch the specific Supabase error here
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        # Catch generic errors
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")

    db_user = {
        "email" : user_data.email,
        "full_name": user_data.full_name,
        "resume_id": None,
        "is_subscribed": False,
        "password": user_data.password.encode('utf-8').hex(),
        "super_id" : user.user.id,
        "created_at": user.user.created_at
    }
    
    checked_data = UserSchema.model_validate(db_user)

    save_to_mongo = await mongo_db["users"].insert_one(checked_data.model_dump())
    print(f"User saved to MongoDB with id: {save_to_mongo.inserted_id}")
    
    response.set_cookie(key="access_token", value=f"Bearer {user.session.access_token}", httponly=True)
    return {"message": "User registered", "user": user.user}

@router.post("/login")
async def login(request: Request, response: Response, login_data: LogiSchema):
    supa = request.app.supabase
    
    try:
        logged_user = supa.auth.sign_in_with_password({
            "email": login_data.email,
            "password": login_data.password
        })

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed")
    
    response.set_cookie(key="access_token", value=f"Bearer {logged_user.session.access_token}", httponly=True)
    return {"message": "User logged in", "user": logged_user.user}

@router.post("/logout")
async def logout(request: Request ,response: Response):
    supa = request.app.supabase
    supa.auth.sign_out()
    response.delete_cookie(key="access_token")
    return {"message": "User logged out"}