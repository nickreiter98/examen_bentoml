import numpy as np
import bentoml
from bentoml.io import NumpyNdarray, JSON, Text
from bentoml.exceptions import BentoMLException
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from datetime import datetime, timedelta

# Secret key and algorithm for JWT authentication
JWT_SECRET_KEY = "123456"
JWT_ALGORITHM = "HS256"

# User credentials for authentication
USERS = {
    "user123": "password123",
    "user456": "password456"
}

class MyResponseModel(BaseModel):
    message: str
    status: int

class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path == "/v1/models/uni_acceptance/predict":
            token = request.headers.get("Authorization")
            if not token:
                return {'status_code': 401, 'error': 'Missing authentication token'}

            try:
                token = token.split()[1]  # Remove 'Bearer ' prefix
                payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            except jwt.ExpiredSignatureError:
                return {'status_code': 401, 'error': 'Token has expired'}
            except jwt.InvalidTokenError:
                return {'status_code': 401, 'error': 'Invalid token'}

            request.state.user = payload.get("sub")

        response = await call_next(request)
        return response

# Pydantic model to validate input data
class InputModel(BaseModel):
    gre: int
    toefl: int
    uni_rating: int
    sop: float
    lor: float
    cgpa: float
    research: int

# Get the model from the Model Store
uni_acceptance_runner = bentoml.sklearn.get("uni_acceptance_lr:latest").to_runner()

# Create a service API
uni_acceptance_service = bentoml.Service("uni_acceptance_service", runners=[uni_acceptance_runner])

# Add the JWTAuthMiddleware to the service
uni_acceptance_service.add_asgi_middleware(JWTAuthMiddleware)

# Create an API endpoint for the service
@uni_acceptance_service.api(input=JSON(), output=JSON())
def login(credentials: dict) -> dict:
    username = credentials.get("username")
    password = credentials.get("password")

    if username in USERS and USERS[username] == password:
        token = create_jwt_token(username)
        return {"token": token}
    else:
        return {'status_code': 401, 'error': 'Invalid credentials'}

# Create an API endpoint for the service
@uni_acceptance_service.api(
    input=JSON(pydantic_model=InputModel),
    output=JSON(),
    route='v1/models/uni_acceptance/predict'
)
async def predict(input_data: InputModel, ctx: bentoml.Context) -> dict:
    request = ctx.request
    user = request.state.user if hasattr(request.state, 'user') else None

    # Convert the input data to a numpy array
    input_series = np.array([input_data.gre, input_data.toefl, input_data.uni_rating,
                            input_data.sop, input_data.lor, input_data.cgpa, input_data.research])

    result = await uni_acceptance_runner.predict.async_run(input_series.reshape(1, -1))

    return {
        "prediction": result.tolist(),
        "user": user
    }

# Function to create a JWT token
def create_jwt_token(user_id: str):
    expiration = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": user_id,
        "exp": expiration
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token