from fastapi import APIRouter
from pydantic import BaseModel

ryvers = APIRouter(tags=['usuarios'], responses={404: {'error': 'Usuario No encontrado'}})

# Entidad Usario
class User(BaseModel):
    id: int
    name: str
    edad: int

users_fake_db = [User(id=1, name="Paco", edad=25),
                 User(id=2, name="Fernanda", edad=22),
                 User(id=3, name="Mauro", edad=23)]

@ryvers.get('/class')
async def ConstruirUsuarios():
    return users_fake_db


# Valores por Path --> http://localhost:8000/userpath/2   --> Para Parametros Fijos
@ryvers.get('/userpath/{id}')
async def buscarUsuario(id: int):
    return buscarUsuarioPorId(id)


# Valores por Query --> http://localhost:8000/userquery/?id=2   --> Para Parametros Opcionales ?start=1&end=10
@ryvers.get('/userquery')
async def buscarUsuario(id: int):
    return buscarUsuarioPorId(id)


@ryvers.get('/usuarios')
async def obtenerUsers():
    return users_fake_db


# Refactorizar Código, ya que "userquery" y "userpath" ambos hacen lo mismo, con el mismo codigo
def buscarUsuarioPorId(id: int):
    user = filter(lambda user: user.id == id, users_fake_db)
    try:
        return list(user)[0]
    except:
        return {'error': 'No se ha encontrado a ningun usuario con este ID'}


@ryvers.get('/usermanual')
async def obtenerUsers():
    return [{'name': 'juan', 'edad':21}, {'name': 'pedro', 'edad':19}]


# Agregar un Nuevo Usuario
@ryvers.post('/usuarios/add')
async def agregarUsario(user: User):
    if type(buscarUsuarioPorId(user.id)) == User:
        return {'error': 'Ya existe un usuario con ese ID'}
    
    users_fake_db.append(user)


# Actuaizar un Usuario Existente
@ryvers.put('/usuarios/update')
async def actualizarUsuario(user: User):
    if type(buscarUsuarioPorId(user.id)) != User:
        return {'error': 'No existe un usuario con ese ID, por lo que no se ha Actualizado'}
    
    found = False

    for index, usuarioGuardado in enumerate(users_fake_db):
        if usuarioGuardado.id == user.id:
            users_fake_db[index] = user
            found = True

    if not found:
        return {'error': 'No se ha Actualizado el Usuario'}
    
    return user


# Eliminar un Usuario
@ryvers.delete('/usuarios/delete/{id}')
async def eliminarUsuario(id: int):

    found = False

    for index, usuarioGuardado in enumerate(users_fake_db):
        if usuarioGuardado.id == id:
            del users_fake_db[index]
            found = True

    if not found:
        return {'error': 'No se ha Eiminado el Usuario'}
    