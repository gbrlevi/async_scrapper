# 1. Scraper Assíncrono com Python, Docker e PostgreSQL

Este é um projeto de um web scraper de alta performance.

O objetivo é demonstrar um pipeline de coleta de dados robusto, capaz de baixar e processar múltiplas páginas web concorrentemente. O script utiliza `asyncio` e `aiohttp` para paralelizar requisições de I/O, `BeautifulSoup` para "parsear" o HTML, e `SQLAlchemy` para salvar os dados em um banco de dados PostgreSQL.

Todo o ambiente (o script Python e o banco de dados) é 100% containerizado usando **Docker Compose**, permitindo que qualquer pessoa rode o projeto com um único comando.

## 2. 🛠️ Stack de Tecnologias

* **Linguagem:** Python 3.10
* **Containerização:** Docker & Docker Compose
* **Banco de Dados:** PostgreSQL (SQL)
* **Processamento Assíncrono:** `asyncio`
* **Requisições HTTP:** `aiohttp` (para `asyncio`)
* **Parsing de HTML:** `BeautifulSoup4`
* **Conexão com BD:** `SQLAlchemy` (com `psycopg2`)

## 3. ⚙️ Como Executar

Você não precisa instalar Python ou PostgreSQL na sua máquina. Apenas o **Docker Desktop**.

**1. Clone o Repositório**
```bash
git clone [https://github.com/gbrlevi/async_scrapper.git](https://github.com/gbrlevi/async_scrapper.git)
cd async_scrapper
```
2. Execute o Docker Compose Este é o único comando necessário. Ele irá:

    Construir a imagem do script Python (usando o Dockerfile).

    Baixar e iniciar um contêiner do banco de dados PostgreSQL.

    Iniciar o contêiner do scraper, que se conectará ao banco e salvará os dados.

Bash

docker-compose up

Você verá o script rodar e, ao final, o contêiner async_scrapper-scraper-1 sairá com "código 0" (sucesso), enquanto o contêiner async_scrapper-db-1 continuará rodando.

4. ✅ Verificando os Dados

O script salva as 100 cotações extraídas do quotes.toscrape.com no banco scraper_db.

Para se conectar e ver os dados, use seu cliente de banco de dados preferido (DBeaver, DataGrip, ou a extensão do VS Code) com as seguintes credenciais:

    Host: localhost

    Porta: 5432 (requer a adição de ports: - "5432:5432" no docker-compose.yml)

    Usuário: user

    Senha: password

    Banco de Dados: scraper_db

Rode a query SELECT * FROM quotes; para ver os resultados.

5. 🛑 Parando o Ambiente

Para parar e remover os contêineres e a rede criada pelo Docker Compose, rode:
Bash

docker-compose down