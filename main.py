from fastapi import FastAPI
from routers import users, autos, basic_auth, jwt_auth
from fastapi.staticfiles import StaticFiles

ryvers = FastAPI()

# Routers
ryvers.include_router(users.ryvers)
ryvers.include_router(autos.ryvers)
ryvers.include_router(basic_auth.ryvers)
ryvers.include_router(jwt_auth.ryvers)

# Exponer Recursos Estaticos, Descargar Formatos/Archivos PDF del Server
ryvers.mount('/static', StaticFiles(directory='static'), name='static')


@ryvers.get('/')
async def root():
    return {'mensaje': '¡Hello World desde FastApi!'}

@ryvers.get('/array')
async def array():
    return {'clave': 'valor'}