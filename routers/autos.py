from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

ryvers = APIRouter(prefix='/autos', tags=['autos'], responses={404: {'error': 'Auto No encontrado'}})

# Modelo Autos
class Autos(BaseModel):
    id: int
    modelo: str
    marca: str
    costo: int

bd_autos = [Autos(id=1, modelo='RS8', marca='Audi', costo=50000),
            Autos(id=2, modelo='MSR9', marca='Maseratti', costo=120000),
            Autos(id=3, modelo='GT500', marca='Mustang', costo=100000)]

# Ver los Autos Disponibles
@ryvers.get('/')
async def listarAutos():
    return bd_autos

# Buscar Autos por ID
@ryvers.get('/{id}')
async def buscarAuto(id: int):
    return busarPorId(id)

# Añadir un nuevo Auto
@ryvers.post('/add', response_model=Autos, status_code=201) # Estado Http por deecto
async def agregarAuto(auto: Autos):
    if type(busarPorId(auto.id)) == Autos:  # Manejo de errores
        raise HTTPException(status_code=404, detail='Ya existe un Automovil con ese ID')

    bd_autos.append(auto)
    return auto

# Actualizar los Datos de un Auto
@ryvers.put('/update', response_model=Autos)
async def actualizarDatosAuto(auto: Autos):
    if type(busarPorId(auto.id)) != Autos:
        raise HTTPException(status_code=404, detail='No existe un Automovil con ese ID, por lo que no se ha Actualizado')

    encontrado = False

    for index, autoGuardado in enumerate(bd_autos):
        if autoGuardado.id == auto.id:
            bd_autos[index] = auto
            encontrado = True

    if not encontrado:
        raise HTTPException(status_code=204, detail='No se ha Actualizado el Usuario')
    
    return auto

# Eliminar un Auto
@ryvers.delete('/delete/{id}')
async def eliminarAuto(id: int):
    if type(busarPorId(id)) != Autos:
        raise HTTPException(status_code=404, detail='No existe un Automovil con ese ID')

    encontrado = False

    for index, autoGuardado in enumerate(bd_autos):
        if autoGuardado.id == id:
            del bd_autos[index]
            encontrado = True

    if not encontrado:
        raise HTTPException(status_code=204, detail='No se ha Eiminado el Automovil')


# Metodo de Busqueda de Autos
def busarPorId(id: int):
    autos = filter(lambda autos: autos.id == id, bd_autos)
    try:
        return list(autos)[0]
    except:
        raise HTTPException(status_code=404, detail='No se ha encontrado a ningun Automovil con este ID')