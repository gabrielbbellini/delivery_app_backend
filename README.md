## Para rodar a API de fretes: 🚚

Crie na raiz do projeto um arquivo .env definindo as seguintes variáveis:
```env
SECRET_KEY="sua_senha_super_secreta"
ALGORITHM="HS256"

DATABASE_URL="postgresql+psycopg2://usuario:senha@localhost:5432/nome_do_banco"

CEP_ABERTO_TOKEN="seu_token_cep_aberto"
```

### Como instalar as dependências? 📦
`pip install -r requirements.txt`

### Rodar a api
`uvicorn src.main:app --reload`

### Como executar os testes? ⚙️
`pytest`
