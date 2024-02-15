from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from core.configs import settings
from api.V1.api import api_router

app = FastAPI(title='Integração Central de Retenção',
              root_path="/Retencao",
              version='0.0.1',
              description='API criada para integração do chatbot com o sistema da Central de Retenção',
              contact={
                  "name": "C-Trends BPO!",
                  "url": "https://www.c-trends.com.br/",
                  "email": "ti@c-trends.com.br",
              })
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/Retencao/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/Retencao/openapi.json", title="API Docs")

# Rota para o esquema OpenAPI


@app.get("/Retencao/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return get_openapi(title="API Docs", version="0.0.1", routes=app.routes)


@app.get("/Retencao/", description='Resposta somente para validar se a API subiu corretamente. Sem nenhuma conexão com o banco de dados.',
         summary='Valida se API está no ar')
def get_index():
    return {'msg': 'API está no ar!'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8001,
                log_level='info', reload=True)
