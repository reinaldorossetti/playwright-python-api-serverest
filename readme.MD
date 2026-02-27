# 🧪 Playwright API Testing - ServeRest

[![Playwright](https://img.shields.io/badge/Playwright-Python-45ba63.svg)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/Pytest-8.4.2-blue.svg)](https://docs.pytest.org/en/stable/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow.svg)](https://www.python.org/)

Projeto de automação de testes de API utilizando **Microsoft Playwright para Python** em conjunto com **pytest** para testar a API REST **ServeRest** - uma API gratuita que simula uma loja virtual.

Projeto estruturado com boas práticas, exemplos de testes, validações avançadas e integração com Pytest para execução e relatórios Allure.

URI do repositório: [https://github.com/reinaldorossetti/playwright-python-api-serverest](https://github.com/reinaldorossetti/playwright-python-api-serverest)

Testes realizados na API com Python + Pytest: [TESTING_API_PYTHON.MD](TESTING_API_PYTHON.MD)

---

## 📚 Índice

- [Sobre o Playwright](#-sobre-o-playwright)
- [Sobre a API ServeRest](#-sobre-a-api-serverest)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Python no Projeto](#-python-no-projeto)
- [Instalação](#-instalação)
- [Executando os Testes](#-executando-os-testes)
- [Exemplos de Testes](#-exemplos-de-testes)
- [assert_that — Assertpy](#-assert_that--assertpy)
- [Funcionalidades do Playwright](#-funcionalidades-do-playwright)
- [Relatórios](#-relatórios)
- [Allure Report — Decorators](#-allure-report--decorators)
- [Boas Práticas](#-boas-práticas)
- [Recursos Adicionais](#-recursos-adicionais)

---

## 🧪 Sobre o Playwright

**Playwright** é um framework open-source da Microsoft, conhecido por testes E2E em browser e também por uma API robusta para testes HTTP via `APIRequestContext`, ideal para automação de APIs em Python.

### ✨ Principais Características

- **🔥 APIRequestContext fluente**: Requisições HTTP com `get`, `post`, `put`, `delete`
- **🚀 Suporte completo a REST**: operações GET, POST, PUT, PATCH e DELETE com JSON
- **🎯 Assertions fluentes com assertpy**: validações legíveis e encadeáveis com `assert_that` da biblioteca `assertpy`
- **🔄 Contexto reutilizável**: configuração de `base_url`, headers e ciclo de vida via dependências/fixtures do pytest
- **📊 Integração com Allure**: relatórios ricos de execução com pytest
- **🧪 Data-Driven Testing**: suporte com `@pytest.mark.parametrize` e leitura de CSV
- **⚡ Execução Paralela**: execução simultânea de testes via `pytest-xdist`
- **🔐 Autenticação**: suporte total para tokens e headers customizados

### 💡 Por que usar Playwright para API em Python?

1. **Padronização**: mesmo framework para API e UI quando necessário
2. **Confiabilidade**: cliente HTTP moderno, veloz e estável
3. **Integração**: funciona naturalmente e se integra perfeitamente com pytest
4. **Evolução**: ecossistema ativo e muito bem documentado
5. **CI/CD**: fácil integração com GitHub Actions

---

## 🌐 Sobre a API ServeRest

[ServeRest](https://serverest.dev/) é uma API REST gratuita que simula uma loja virtual para fins educacionais e prática de testes de API.

### 🛍️ Endpoints Disponíveis

| Recurso | Endpoints | Descrição |
|---------|-----------|-----------|
| **Login** | `POST /login` | Autenticação de usuários |
| **Usuários** | `GET, POST, PUT, DELETE /usuarios` | Gerenciamento de usuários |
| **Produtos** | `GET, POST, PUT, DELETE /produtos` | Gerenciamento de produtos (requer admin) |
| **Carrinhos** | `GET, POST, DELETE /carrinhos` | Gerenciamento de carrinhos de compras |

### 🔗 Base URL

```text
https://serverest.dev
```

### 📖 Documentação Completa

- **Swagger UI**: https://serverest.dev/
- **Repositório**: https://github.com/ServeRest/ServeRest
- **Front-end (Beta)**: https://front.serverest.dev/

---

## 📁 Estrutura do Projeto

```text
playwright-python-api-serverest/
│
├── .github/
│   └── workflows/
│       └── ci.yml                       # Pipeline de CI
│
├── tests/
│   ├── conftest.py                      # Configuração base e fixtures do Pytest
│   ├── login/
│   │   └── test_login_playwright.py
│   ├── users/
│   │   └── test_users_playwright.py
│   ├── products/
│   │   └── test_products_playwright.py
│   ├── carts/
│   │   └── test_carts_playwright.py
│   ├── utils/
│   │   ├── api_utils.py                 # Funções úteis de requests e endpoints
│   │   └── faker_utils.py               # Geração de dados de teste (Faker)
│   └── resources/
│       ├── login/
│       │   ├── invalid-login-emails.csv
│       │   └── invalido-login.csv
│       ├── usuarios/
│       │   └── userPayload.json
│       └── produtos/
│           ├── productPayload.json
│           └── product.csv
│
├── pytest.ini                           # Configurações gerais do pytest (dist e allure)
├── requirements.txt                     # Dependências do projeto Python
├── TESTING_API_PYTHON.MD                # Documentação dos cenários de teste em Python
└── readme.MD                            # Este arquivo
```

---

## 🔧 Pré-requisitos

- **Python 3.10** ou superior
- **pip** (Gerenciador de pacotes do Python)
- **Virtual Environment** (recomendado usar `venv` ou similar)
- **IDE** (VS Code, PyCharm)
- Conexão com internet (para acessar a API ServeRest)

### Verificar instalação

```bash
python --version
pip --version
```

### Comando para rodar os testes no terminal:
```bash
python -m pytest tests
```
---

## 🐍 Python no Projeto

Este projeto utiliza recursos nativos e modernos do **Python** em sinergia com o **Pytest** para entregar testes legíveis, independentes e fáceis de dar manutenção.

### ✅ Exemplos práticos usados no projeto

1. **Dicionários nativos para payloads JSON**

```python
payload = {
    "nome": product_name,
    "preco": 250,
    "descricao": "Produto de teste",
    "quantidade": 10
}
```

2. **Fixtures do Pytest para injeção de dependência (`conftest.py`)**

```python
@pytest.fixture
def api_request(playwright_instance: Playwright):
    request_context = playwright_instance.request.new_context(base_url=BASE_URL)
    yield request_context
    request_context.dispose()
```

3. **Tipagem e Autocomplete (`Type Hints`)**

```python
def create_user(request: APIRequestContext, email: str, password: str, admin: bool):
    pass
```

### 💡 Boas práticas com Python para este projeto

- Mantenha `pytest.ini` e `conftest.py` otimizados para orquestrar setup/teardown.
- Use dicionários nativos para body das requisições, ao invés de conversão manual de texto.
- Use `assert_that` da biblioteca `assertpy` para asserções fluentes, legíveis e com mensagens de erro detalhadas (ex: `assert_that(resp.status).is_equal_to(200)`).

---

## 📦 Dependências e Versões (requirements.txt)

| Componente                         | Versão  | Descrição  |
|------------------------------------|---------|------------|
| `pytest`                           | 8.4.2   | Framework principal de testes unitários/integrados |
| `playwright`                       | 1.58.0  | Engine para chamadas e requisições HTTP |
| `pytest-xdist`                     | 3.8.0   | Suporte à execução simultânea e multiprocessos |
| `allure-pytest`                    | 2.15.3  | Geração unificada de relatórios visuais com Allure |
| `assertpy`                         | 1.1     | Assertions fluentes com `assert_that` |

---

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/reinaldorossetti/playwright-python-api-serverest.git
cd playwright-python-api-serverest
```

### 2. Crie e ative um ambiente virtual (Opcional, mas recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências e o Playwright

```bash
pip install -r requirements.txt
playwright install
```

---

## ▶️ Executando os Testes

As configurações padrão de execução já estão pré-definidas no `pytest.ini`.

### Executar suíte completa

```bash
python -m pytest tests
```

### Executar funcionalidade específica (Ex: login)

```bash
pytest tests/login/test_login_playwright.py
```

### Executar teste individual

```bash
pytest tests/login/test_login_playwright.py::test_ct01_login_with_valid_credentials_and_validate_token
```

### Execução paralela (via pytest-xdist)

O arquivo `pytest.ini` já está setado com o argumento `-n 6 --dist=loadscope` configurando paralelismo otimizado com as workers. Para modificar em tempo de terminal para forçar execução total da CPU, utilize `-n auto`:

```bash
pytest -n auto
```

---

## ⚙️ Esteira CI/CD - GitHub Actions

Este projeto possui integração contínua configurada no GitHub Actions em:

- Arquivo: `.github/workflows/ci.yml`

### 🔁 Quando a esteira é executada

- `push` em qualquer branch
- `pull_request` aberto ou atualizado

### 🧱 Passos principais da pipeline (`test`)

1. **Checkout do código**
2. **Configuração do Python** (`actions/setup-python@v4`)
3. **Instalação das dependências** (utilizando `pip cache`)
4. **Instalação dos browsers / dependências nativas do Playwright**
5. **Execução robusta via `pytest`** gerando artefatos para o Allure.
6. **Deploy no GitHub Pages:** Relatório final é hospedado usando `peaceiris/actions-gh-pages@v4`.

### 🌐 Acesso ao relatório no GitHub Pages

Após a execução da sua pipeline, navegue em:
`https://reinaldorossetti.github.io/playwright-python-api-serverest/allure-reports/index.html`

---

## 📝 Exemplos de Testes

### Exemplo 1: Configuração Base com Pytest Fixtures (`conftest.py`)

Em Python, abstraímos todo o gerenciador em session scopes via fixtures.

```python
import pytest
from playwright.sync_api import Playwright, sync_playwright

BASE_URL = "https://serverest.dev"

@pytest.fixture(scope="session")
def playwright_instance() -> Playwright:
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture
def api_request(playwright_instance: Playwright):
    request_context = playwright_instance.request.new_context(base_url=BASE_URL)
    yield request_context
    request_context.dispose()
```

### Exemplo 2: Login com sucesso

```python
import allure
from assertpy import assert_that
from playwright.sync_api import APIRequestContext
from tests.utils.api_utils import post_json, parse_response_body

@allure.severity(allure.severity_level.CRITICAL)
def test_ct01_login_with_valid_credentials_and_validate_token(api_request: APIRequestContext):
    email = "usuario_valido@email.com"
    password = "SenhaSegura@123"

    login_resp = post_json(api_request, "/login", {"email": email, "password": password})

    assert_that(login_resp.status).is_equal_to(200)
    body = parse_response_body(login_resp)
    assert_that(body["message"]).is_equal_to("Login realizado com sucesso")
    assert_that(body.get("authorization")).is_not_none()
```

### Exemplo 3: Login inválido

```python
@allure.severity(allure.severity_level.CRITICAL)
def test_ct02_login_with_invalid_credentials(api_request: APIRequestContext):
    resp = post_json(
        api_request,
        "/login",
        {
            "email": "usuario@inexistente.com",
            "password": "senhaerrada",
        },
    )

    assert_that(resp.status).is_equal_to(401)
    response_body = parse_response_body(resp)
    assert_that(response_body["message"]).is_equal_to("Email e/ou senha inválidos")
```

### Exemplo 4: Validação de campos obrigatórios (Data-driven com Pytest)

```python
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("_row", load_required_fields_rows())
def test_ct03_validate_required_fields_on_login(_row: dict[str, str], api_request: APIRequestContext):
    resp = post_json(api_request, "/login", {"email": "", "password": "senha123"})
    assert_that(resp.status).is_equal_to(400)
    body = parse_response_body(resp)
    assert_that(body.get("email")).is_not_none()
```

### Exemplo 5: Uso de token dinâmico recebido em Auth

```python
@allure.severity(allure.severity_level.CRITICAL)
def test_ct04_login_and_use_token_in_protected_route(api_request: APIRequestContext):
    auth_token = "Bearer XXXX"  # Recebido de requests anteriores do setup

    product_payload = {"nome": "Teste", "preco": 100, "descricao": "Teste", "quantidade": 10}

    product_resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": auth_token},
        data=json.dumps(product_payload, ensure_ascii=False),
    )

    assert_that(product_resp.status).is_equal_to(403)
    body = parse_response_body(product_resp)
    assert_that(body["message"]).is_equal_to("Rota exclusiva para administradores")
```

### Exemplo 6: Teste iterando em arquivos CSV via Pathlib

```python
from pathlib import Path
import csv

def load_invalid_email_values() -> list[str]:
    csv_path = Path("tests/resources/login/invalid-login-emails.csv")
    with csv_path.open(encoding="utf-8") as f:
        return [row["email"] for row in csv.DictReader(f)]

@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("invalid_email", load_invalid_email_values())
def test_ct05_validate_invalid_email_format(invalid_email: str, api_request: APIRequestContext):
    resp = post_json(api_request, "/login", {"email": invalid_email, "password": "senha123"})

    assert_that(resp.status).is_equal_to(400)
    body = parse_response_body(resp)
    assert_that(body.get("email")).is_not_none()
```

### Exemplo 7: Ciclo completo de carrinho (baseado em `test_carts_playwright.py`)

```python
import json
import allure
from assertpy import assert_that
from playwright.sync_api import APIRequestContext
from tests.utils.api_utils import JSON_HEADERS, parse_response_body, post_json
from tests.utils.faker_utils import random_email, random_product

@allure.severity(allure.severity_level.CRITICAL)
def test_ct01_full_cart_lifecycle_for_authenticated_user(api_request: APIRequestContext):
    # Criar usuário admin e obter token
    user_email = random_email()
    post_json(api_request, "/usuarios", {"nome": "Cart User", "email": user_email,
                                          "password": "SenhaSegura@123", "administrador": "true"})
    login_resp = post_json(api_request, "/login", {"email": user_email, "password": "SenhaSegura@123"})
    assert_that(login_resp.status).is_equal_to(200)
    token = parse_response_body(login_resp)["authorization"]

    # Garantir que não há carrinho ativo
    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})

    # Criar produto
    product_resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps({"nome": random_product(), "preco": 150,
                         "descricao": "Produto de teste", "quantidade": 10}, ensure_ascii=False),
    )
    assert_that(product_resp.status).is_equal_to(201)
    product_id = parse_response_body(product_resp)["_id"]

    # Criar carrinho
    create_cart_resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps({"produtos": [{"idProduto": product_id, "quantidade": 2}]}, ensure_ascii=False),
    )
    assert_that(create_cart_resp.status).is_equal_to(201)
    cart_id = parse_response_body(create_cart_resp)["_id"]

    # Buscar carrinho por ID e validar campos
    get_cart_resp = api_request.get(f"/carrinhos/{cart_id}")
    assert_that(get_cart_resp.status).is_equal_to(200)
    cart_body = parse_response_body(get_cart_resp)
    assert_that(cart_body["_id"]).is_equal_to(cart_id)
    assert_that(cart_body.get("precoTotal")).is_not_none()
    assert_that(cart_body.get("quantidadeTotal")).is_not_none()
    assert_that(len(cart_body["produtos"])).is_equal_to(1)

    # Concluir compra
    conclude_resp = api_request.delete("/carrinhos/concluir-compra", headers={"Authorization": token})
    assert_that(conclude_resp.status).is_equal_to(200)
    assert_that(parse_response_body(conclude_resp)["message"]).contains("Registro excluído com sucesso")
```

---

## ✅ assert_that — Assertpy

Todos os testes deste projeto utilizam `assert_that` da biblioteca [assertpy](https://github.com/assertpy/assertpy) para realizar asserções fluentes, legíveis e com mensagens de erro detalhadas.

### Importação

```python
from assertpy import assert_that
```

### Principais métodos

| Método                              | O que valida                                           |
|-------------------------------------|--------------------------------------------------------|
| `.is_equal_to(value)`               | Igualdade exata                                        |
| `.is_not_equal_to(value)`           | Diferença entre valores                                |
| `.is_not_none()`                    | Valor não é `None`                                     |
| `.is_none()`                        | Valor é `None`                                         |
| `.contains(substr)`                 | String ou lista contém o valor informado               |
| `.does_not_contain(substr)`         | String ou lista não contém o valor                     |
| `.is_true()` / `.is_false()`        | Booleano verdadeiro / falso                            |
| `.is_greater_than(n)`               | Numérico maior que `n`                                 |
| `.is_less_than(n)`                  | Numérico menor que `n`                                 |
| `.is_between(a, b)`                 | Numérico dentro do intervalo `[a, b]`                  |
| `.is_length(n)`                     | Sequência com tamanho exato `n`                        |
| `.is_empty()` / `.is_not_empty()`   | Sequência vazia ou não vazia                           |
| `.has_size(n)`                      | Coleção com `n` elementos                              |
| `.snapshot()`                       | Compara com snapshot salvo em `__snapshots/`           |

### Exemplo com status e corpo da resposta

```python
from assertpy import assert_that
from tests.utils.api_utils import parse_response_body

resp = api_request.get("/usuarios")
assert_that(resp.status).is_equal_to(200)

body = parse_response_body(resp)
assert_that(body.get("quantidade")).is_greater_than(0)
assert_that(body.get("usuarios")).is_not_empty()
```

### Encadeamento de asserções

```python
assert_that(body["message"]) \
    .is_not_none() \
    .contains("sucesso")
```

### Snapshot testing

O método `.snapshot()` grava a resposta na primeira execução e nas seguintes verifica se o conteúdo é idêntico. Os arquivos ficam em `__snapshots/`.

```python
body = parse_response_body(resp)
assert_that(body).snapshot()   # cria ou valida __snapshots/<nome>.json
```

> Para resetar um snapshot, apague o arquivo correspondente em `__snapshots/` e execute o teste novamente.

---

## 🎯 Funcionalidades e Sintaxe Nativas (Playwright Python API)

### 1. Inicialização de um contexto isolado

```python
request_context = playwright_instance.request.new_context(base_url="https://serverest.dev")
```

### 2. Requisições Fluent e Options combinadas

```python
response = request.post(
    "/login",
    headers={"Content-Type": "application/json"},
    data={"email": email, "password": password}
)
```

### 3. Extração imediata JSON de responses HTTP

```python
body_json = response.json()
authorization_token = body_json.get("authorization")
http_status = response.status
```

---

## 📊 Relatórios

Após aplicar localmente a suíte ou durante a pipeline, o Allure se integra embutidamente com Pytest. O projeto aponta suas saídas para o diretório de dados em `/allure-results`.

### Instalação do Allure CLI

Para usar o `allure serve` localmente, instale o Allure CLI globalmente via **npm** (requer Node.js 18+):

```bash
npm install -g allure-commandline
```

Verifique a instalação:

```bash
allure --version
```

> Alternativamente, no Windows com Scoop: `scoop install allure`  
> No macOS com Homebrew: `brew install allure`

### Gerando e visualizando o relatório

Para transformar os dados JSON de saída do Pytest na interface gráfica robusta do Allure:

```bash
# Executar os testes e salvar resultados
pytest tests --alluredir=allure-results

# Abrir relatório interativo no browser
allure serve allure-results
```

> Para gerar os arquivos HTML estáticos (ex: para deploy em CI/CD):
> ```bash
> allure generate allure-results --clean -o allure-report
> allure open allure-report
> ```

O dashboard exibe:
- ✅ Cenários OK, Skipped e Failed detalhadamente
- ⏱️ Tempos exatos capturados via Hooks do Pytest 
- 📋 Stack Trace de Erros
- 📊 Análise das execuções em timeline

### 🏷️ Allure Report — Decorators

O plugin `allure-pytest` suporta metadados extremamente ricos em cima das funções de teste. Todos os decorators abaixo são importados de `import allure`.

#### Decorators disponíveis

| Decorator                               | Descrição                                              | Exemplo                                              |
|-----------------------------------------|--------------------------------------------------------|------------------------------------------------------|
| `@allure.severity(level)`               | Define a criticidade do teste                          | `@allure.severity(allure.severity_level.CRITICAL)`   |
| `@allure.title("Título")`               | Título legível exibido no relatório                    | `@allure.title("CT01 - Login válido")`               |
| `@allure.description("Descrição")`      | Descrição longa do teste                               | `@allure.description("Valida token JWT retornado")`  |
| `@allure.description_html("html")`      | Descrição em HTML                                      | `@allure.description_html("<b>Login</b>")`           |
| `@allure.feature("Feature")`            | Agrupa testes por funcionalidade                       | `@allure.feature("Login")`                           |
| `@allure.story("Story")`                | Subdivide features em histórias                        | `@allure.story("Login com credenciais válidas")`     |
| `@allure.epic("Epic")`                  | Agrupa features em épicos (maior granularidade)        | `@allure.epic("Autenticação")`                       |
| `@allure.tag("tag1", "tag2")`           | Tags livres para categorização                         | `@allure.tag("smoke", "regression")`                 |
| `@allure.label("name", "value")`        | Label customizado de formato chave-valor               | `@allure.label("layer", "api")`                      |
| `@allure.link(url, name="texto")`       | Link genérico no relatório                             | `@allure.link("https://serverest.dev")`              |
| `@allure.issue(url, name="texto")`      | Link para issue/bug tracker                            | `@allure.issue("https://github.com/org/repo/1")`    |
| `@allure.testcase(url, name="texto")`   | Link para caso de teste em ferramenta de gestão        | `@allure.testcase("https://jira.example.com/TC-1")` |

#### Níveis de severidade (`allure.severity_level`)

| Constante                          | Uso                                        |
|------------------------------------|--------------------------------------------|
| `allure.severity_level.BLOCKER`    | Impede a execução; bloqueia o release      |
| `allure.severity_level.CRITICAL`   | Fluxo principal; falha impacta diretamente |
| `allure.severity_level.NORMAL`     | Importante, mas não bloqueia o fluxo core  |
| `allure.severity_level.MINOR`      | Pouco impacto; melhoria ou detalhe         |
| `allure.severity_level.TRIVIAL`    | Cosmético ou edge case irrelevante         |

#### Steps dentro dos testes

```python
import allure

# Context manager — passo nomeado no relatório
with allure.step("Criar usuário administrador"):
    post_json(request, "/usuarios", new_user)

# Decorator — reutilizável em funções helper
@allure.step("Fazer login e obter token")
def get_token(request, email, password):
    resp = post_json(request, "/login", {"email": email, "password": password})
    return parse_response_body(resp)["authorization"]
```

#### Exemplo completo com todas as anotações

```python
import allure
from assertpy import assert_that
from playwright.sync_api import APIRequestContext
from tests.utils.api_utils import post_json, parse_response_body

@allure.epic("Autenticação")
@allure.feature("Login")
@allure.story("Login com credenciais inválidas")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CT02 - Login com credenciais inválidas retorna 401")
@allure.description("Valida que o endpoint retorna 401 para credencial incorreta de usuário")
@allure.tag("smoke", "regression")
@allure.issue("https://github.com/ServeRest/ServeRest/issues/1", name="SRV-123")
def test_ct02_login_with_invalid_credentials(api_request: APIRequestContext):
    with allure.step("Realizar POST com credencial incorreta"):
        resp = post_json(api_request, "/login", {"email": "usuario@inexistente.com", "password": "senhaerrada"})

    with allure.step("Validar status 401 e mensagem de erro"):
        assert_that(resp.status).is_equal_to(401)
        body = parse_response_body(resp)
        assert_that(body["message"]).is_equal_to("Email e/ou senha inválidos")
```

---

## 🎓 Boas Práticas

### 1. Organização dos Arquivos de Tests / Suítes

- ✅ Divida os domínios (Ex: `login/test_login_playwright.py`, `users/test_users_playwright.py`, etc)
- ✅ Comece os nomes das funções validadoras com o prefixo `test_`, requisito estrutural básico para a descoberta automática de suítes pelo `pytest`.

### 2. Funções Abstratas Customizadas (`api_utils.py` e Helpers)

- ✅ Centralize chamadas longas na lógica customizada do projeto para evitar `copy/paste` nos testes (ex: `post_json`).
- ✅ Usar a biblioteca de Fake Entities (`faker`) isoladas em pacotes utilitários para construir mocks dinâmicos de dados em cada request de teste de integração.

### 3. Pytest Features:

- ✅ Usar exaustivamente propriedades como `@pytest.mark.parametrize` para simular as planilhas nativas em um único method-call.
- ✅ Reutilização absoluta de Context API: Fixtures configuradas com Pytest que operam a API em sessions otimizam a rede e alivia o overhead das instâncias locais do playwright.

---

## 📚 Recursos Adicionais

### Documentação Oficial

- 🎭 **Playwright Python**: https://playwright.dev/python/docs/api/class-apirequestcontext
- 🌐 **ServeRest**: https://serverest.dev/
- 🐍 **Pytest**: https://docs.pytest.org/
- 📊 **Allure Pytest**: https://docs.qameta.io/allure/#_pytest

### Comunidade

- [Stack Overflow - Playwright Python Tag](https://stackoverflow.com/questions/tagged/playwright-python)
- [Playwright GitHub Issues](https://github.com/microsoft/playwright-python/issues)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

Desenvolvido para fins de estudo e prática de automação de testes de API.

---

## ⭐ Agradecimentos

- **Microsoft** - Criadora do Playwright
- **Paulo Gonçalves** - Criador da API ServeRest
- Equivalente e Comunidade ao Pytest - Testes automatizados robustos
- Comunidade open-source e testers

---

Referências:
- https://playwright.dev/python/docs/intro
- https://docs.pytest.org/
- https://github.com/microsoft/playwright-python

**🚀 Happy Testing with Playwright and Python!** 🎭
