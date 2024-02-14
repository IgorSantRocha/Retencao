from fastapi import FastAPI

from core.configs import settings
from api.V1.api import api_router

app = FastAPI(title='Integração Central de Retenção',
              root_path="/Retencao")
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("")
def get_index():
    return {'msg': 'Funciona!'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001,
                log_level='info', reload=True)
