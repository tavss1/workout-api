# Workout API

API REST para gerenciamento de atletas, categorias e centros de treinamento, desenvolvida com FastAPI, SQLAlchemy Async e PostgreSQL.

## Visao Geral

A API expoe recursos para:

- cadastrar e listar categorias
- cadastrar e listar centros de treinamento
- cadastrar, listar, buscar, atualizar e remover atletas

As rotas estao sob o prefixo:

- `/api/v1`

Documentacao interativa:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Tecnologias

- Python 3.12+
- FastAPI
- SQLAlchemy 2.x (async)
- Alembic
- PostgreSQL
- Uvicorn
- fastapi-pagination

## Estrutura do Projeto

```text
workout-api/
  alembic/
  workout_api/
    atleta/
    categoria/
    centro_treinamento/
    configs/
    contrib/
  docker-compose.yml
  alembic.ini
  requirements.txt
```

## Pre-requisitos

- Python 3.12 ou superior
- PostgreSQL local ou Docker
- PowerShell (Windows) ou shell equivalente

## Configuracao de Ambiente

### 1) Criar e ativar ambiente virtual

No PowerShell:

```powershell
python -m venv .workoutapi
.\.workoutapi\Scripts\Activate.ps1
```

### 2) Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 3) Configurar variaveis de ambiente

A aplicacao usa `DB_URL` (arquivo `workout_api/configs/settings.py`).

Exemplo (base em `.env_example`):

```env
DB_URL=postgresql+asyncpg://user:password@localhost/db
```

Opcionalmente, para subir o Postgres via Docker Compose, use as variaveis abaixo (base em `.env_example`):

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=senha
POSTGRES_DB=db
```

## Banco de Dados

## Modelagem de entidade e relacionamento - MER
![MER](/mer.jpg "Modelagem de entidade e relacionamento")

### Opcao A: Postgres via Docker Compose

```powershell
docker compose up -d db
```

Servico exposto em `localhost:5432`.

### Opcao B: Postgres local

Crie um banco e ajuste a `DB_URL` para o seu ambiente.

## Migrations (Alembic)

Aplicar migration inicial:

```powershell
alembic upgrade head
```

Gerar nova migration (quando houver mudanca de modelo):

```powershell
alembic revision --autogenerate -m "descricao"
```

## Executar a API

```powershell
uvicorn workout_api.main:app --host 0.0.0.0 --port 8000 --reload
```

A API ficara disponivel em:

- `http://localhost:8000`

## Endpoints Principais

Base path: `/api/v1`

### Categorias

- `POST /categorias/` cria categoria
- `GET /categorias/` lista categorias (paginado)
- `GET /categorias/{id}` busca categoria por id

Exemplo payload `POST /categorias/`:

```json
{
  "nome": "Scale"
}
```

### Centros de Treinamento

- `POST /centros-treinamento/` cria centro de treinamento
- `GET /centros-treinamento/` lista centros (paginado)
- `GET /centros-treinamento/{id}` busca centro por id

Exemplo payload `POST /centros-treinamento/`:

```json
{
  "nome": "CT Master",
  "endereco": "Rua das Flores, 123",
  "proprietario": "Joao Silva"
}
```

### Atletas

- `POST /atletas/` cria atleta
- `GET /atletas/` lista atletas (paginado)
- `GET /atletas/buscar?nome={nome}&cpf={cpf}` busca por nome e cpf
- `GET /atletas/{id}` busca atleta por id
- `PATCH /atletas/{id}` atualiza parcialmente atleta
- `DELETE /atletas/{id}` remove atleta

Exemplo payload `POST /atletas/`:

```json
{
  "nome": "Joao Silva",
  "cpf": "12345678900",
  "idade": 25,
  "peso": 70.5,
  "altura": 1.75,
  "sexo": "M",
  "categoria": {
    "nome": "Scale"
  },
  "centro_treinamento": {
    "nome": "CT Master"
  }
}
```

Exemplo payload `PATCH /atletas/{id}`:

```json
{
  "peso": 72.0,
  "altura": 1.76
}
```

## Fluxo Recomendado para Teste Rapido

1. Subir banco (Docker ou local)
2. Configurar `DB_URL`
3. Rodar `alembic upgrade head`
4. Subir API com Uvicorn
5. Criar categoria
6. Criar centro de treinamento
7. Criar atleta
8. Validar listagens e buscas no Swagger (`/docs`)

## Observacoes

- Endpoints de listagem usam paginacao do `fastapi-pagination`.
- No cadastro de atleta, categoria e centro de treinamento devem existir previamente.
- CPF de atleta e nome de categoria/centro possuem restricoes de unicidade no banco.

# Referências

FastAPI: https://fastapi.tiangolo.com/

Pydantic: https://docs.pydantic.dev/latest/

SQLAlchemy: https://docs.sqlalchemy.org/en/20/

Alembic: https://alembic.sqlalchemy.org/en/latest/

Fastapi-pagination: https://uriyyo-fastapi-pagination.netlify.app/
