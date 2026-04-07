"""
🔥 FastAPI Agent
Создаёт FastAPI бэкенды с async/await
"""

from orchestrator.core.task_executor import BaseAgentExecutor
from orchestrator.core.database import Task
from typing import Dict


class FastAPIAgentExecutor(BaseAgentExecutor):
    """
    🔥 FastAPI Developer Agent
    
    Генерирует:
    - FastAPI приложения
    - Async endpoints
    - Pydantic models
    - SQLAlchemy ORM
    - JWT Auth
    """
    
    AGENT_TYPE = 'fastapi'
    NAME = 'FastAPI Agent'
    EMOJI = '🔥'
    
    def can_execute(self, task: Task) -> bool:
        return task.agent_type in ['fastapi', 'python', 'backend', 'api']
    
    def execute(self, task: Task) -> Dict:
        title = task.title.lower()
        
        if 'auth' in title or 'login' in title:
            return self._create_auth_api(task)
        elif 'crud' in title or 'rest' in title:
            return self._create_crud_api(task)
        else:
            return self._create_default_api(task)
    
    def _create_auth_api(self, task: Task) -> Dict:
        main_py = '''from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

app = FastAPI(title="Auth API", version="1.0.0")

# Настройки безопасности
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Модели
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Фейковая БД
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    }
}

# Хелперы
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/")
async def root():
    return {"message": "Auth API is running"}
'''

        requirements = '''fastapi==0.109.0
uvicorn==0.27.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
'''

        return {
            'success': True,
            'message': f'✅ FastAPI Auth API создан!',
            'artifacts': {
                'main.py': main_py,
                'requirements.txt': requirements,
                'README.md': '# FastAPI Auth\n\nJWT authentication with FastAPI'
            }
        }
    
    def _create_crud_api(self, task: Task) -> Dict:
        main_py = '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI(title="CRUD API", version="1.0.0")

# Модели
class Item(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

# Фейковая БД
db: List[Item] = []

@app.get("/")
async def root():
    return {"message": "CRUD API is running"}

@app.get("/items", response_model=List[Item])
async def get_items():
    return db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: str):
    item = next((i for i in db if i.id == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item)
async def create_item(item: ItemCreate):
    new_item = Item(id=str(uuid4()), **item.dict())
    db.append(new_item)
    return new_item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item_update: ItemCreate):
    index = next((i for i, item in enumerate(db) if item.id == item_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = Item(id=item_id, **item_update.dict())
    db[index] = updated_item
    return updated_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    global db
    db = [i for i in db if i.id != item_id]
    return {"message": "Item deleted"}
'''

        return {
            'success': True,
            'message': f'✅ FastAPI CRUD API создан!',
            'artifacts': {
                'main.py': main_py,
                'requirements.txt': 'fastapi==0.109.0\nuvicorn==0.27.0',
                'README.md': '# FastAPI CRUD\n\nBasic CRUD operations'
            }
        }
    
    def _create_default_api(self, task: Task) -> Dict:
        return {
            'success': True,
            'message': f'✅ FastAPI приложение создано!',
            'artifacts': {
                'main.py': '''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}
''',
                'requirements.txt': 'fastapi\nuvicorn'
            }
        }
