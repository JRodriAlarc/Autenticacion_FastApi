from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

ryvers = APIRouter(prefix='/login-basic', tags=['login-basic'])
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

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
        'password': 'qwerty000'
    },
    "Carlos3": {
        'username': 'Carlos3',
        'name': 'Carlos Hernandez',
        'mail': 'arlosH3r@mail.com',
        'role': 'cliente',
        'disabled': True,
        'password': 'qwerty000'
    },
    "LucasP": {
        'username': 'LucasP',
        'name': 'Lucas Perez',
        'mail': 'lucasPerz65@mail.com',
        'role': 'admin',
        'disabled': False,
        'password': 'qwerty123'
    }
}


def buscarUsuario(username: str):
    if username in users_db:
        return Persona(**users_db[username])
    

def buscarUsuarioEnBaseDatos(username: str):
    if username in users_db:
        return PersonaDB(**users_db[username])
    

async def personaActual(token: str = Depends(oauth2)):
    persona = buscarUsuario(token)
    if not persona:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciales de autenticación inválidas', headers={'WWW-Authenticate': 'Bearer'})
    
    if persona.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Usuario Deshabilitado')

    return persona


@ryvers.post('/')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='El usuario no es correcto')
    
    persona = buscarUsuarioEnBaseDatos(form.username)
    
    if not form.password == persona.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='La Contraseña no es correcta')
    
    return {'access_token': persona.username, 'token_type': 'bearer'}


@ryvers.get('/me')
async def miUsuario(persona: Persona = Depends(personaActual)):
    return persona