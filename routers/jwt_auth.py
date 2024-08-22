from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta

algoritmo = 'HS256'
duracionToken = 1
secret = 'IOWIJDMNLKkodweil;'

ryvers = APIRouter(prefix='/login-jwt', tags=['login-jwt'])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
crypth = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Persona(BaseModel):
    username: str
    name: str
    mail: str
    role: str
    disabled: bool

class PersonaDB(Persona):
    password: str

users_db = {
    "Emma12": {
        'username': 'Emma12',
        'name': 'Emma',
        'mail': 'Emma012@mail.com',
        'role': 'cliente',
        'disabled': False,
        'password': '$2a$12$NUxJzznMNzCZCJl4q3P/2ODZ/eHUrqSrbjCaC/NtLgwTqUtFiOyZ.' #qwerty000
    },
    "Carlos3": {
        'username': 'Carlos3',
        'name': 'Carlos Hernandez',
        'mail': 'arlosH3r@mail.com',
        'role': 'cliente',
        'disabled': True,
        'password': '$2a$12$NUxJzznMNzCZCJl4q3P/2ODZ/eHUrqSrbjCaC/NtLgwTqUtFiOyZ.' # qwerty000
    },
    "LucasP": {
        'username': 'LucasP',
        'name': 'Lucas Perez',
        'mail': 'lucasPerz65@mail.com',
        'role': 'admin',
        'disabled': False,
        'password': '$2a$12$gUzHSaLUXtnADHqRydPCiuwFnIKjvS7j0kQryESPLnLeKqobuiioK' # qwerty123
    }
}

def buscarUsuario(username: str):
    if username in users_db:
        return Persona(**users_db[username])

def buscarUsuarioEnBaseDatos(username: str):
    if username in users_db:
        return PersonaDB(**users_db[username])
    
async def auth_persona(token: str = Depends(oauth2)):

    exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales de autenticación inválidas', headers={'WWW-Authenticate': 'Bearer'})
    
    try:
        personaName = jwt.decode(token, secret, algorithms=[algoritmo]).get('sub')

        if personaName is None:
            raise exeption

    except InvalidTokenError:
        raise exeption
        
    return buscarUsuario(personaName)
    
async def personaActual(persona: Persona = Depends(auth_persona)):   
    if persona.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuario Deshabilitado')

    return persona

@ryvers.post('/')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario no es correcto')
    
    persona = buscarUsuarioEnBaseDatos(form.username)
    
    if not crypth.verify(form.password, persona.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La Contraseña no es correcta')
    
    accessToken = {'sub': persona.username, 'exp': datetime.utcnow() + timedelta(minutes=duracionToken)}
    
    return {'access_token': jwt.encode(accessToken, secret, algorithm=algoritmo), 'token_type': 'bearer'}

@ryvers.get('/me')
async def miUsuario(persona: Persona = Depends(personaActual)):
    return persona