# 🐍 Playwright API Testing com Python + Pytest (ServeRest)

Suíte de testes de API escrita em Python usando **Playwright**, **Pytest** e **Allure**, cobrindo os principais fluxos da API [ServeRest](https://serverest.dev/?lang=pt-BR).

---

## Estrutura do projeto

```
tests/
├── conftest.py                        # Fixtures globais (sessão Playwright e APIRequestContext)
├── login/
│   └── test_login_playwright.py       # CT01 a CT05
├── users/
│   └── test_users_playwright.py       # CT01 a CT16
├── products/
│   └── test_products_playwright.py    # CT01 a CT13
├── carts/
│   └── test_carts_playwright.py       # CT01 a CT08
├── resources/
│   ├── login/                         # CSVs com payloads de login inválidos
│   ├── products/
│   │   └── productPayload.json
│   └── users/
│       └── userPayload.json
└── utils/
    ├── api_utils.py                   # Helpers HTTP: post_json, put_json, parse_response_body, load_json_resource
    └── faker_utils.py                 # Geradores de dados: random_name, random_email, random_product
__snapshots/                           # Snapshots gerados pelo assertpy para comparação de respostas
allure-results/                        # Saída gerada pelo pytest para o Allure Report
pytest.ini                             # Configuração do Pytest (marcadores, diretório de resultados Allure etc.)
requirements.txt                       # Dependências do projeto
```

---

## Dependências principais

| Pacote            | Versão  | Finalidade                                |
|-------------------|---------|-------------------------------------------|
| `pytest`          | 8.4.2   | Framework de testes                       |
| `playwright`      | 1.58.0  | Cliente HTTP via `APIRequestContext`      |
| `allure-pytest`   | 2.15.3  | Integração com relatórios Allure          |
| `assertpy`        | 1.1     | Assertions fluentes                       |
| `pytest-xdist`    | 3.8.0   | Execução paralela de testes               |

---

## Pré-requisitos

- Python 3.11+
- Dependências listadas em `requirements.txt`

---

## Instalação

```bash
python -m pip install -r requirements.txt
python -m playwright install
```

---

## Execução

### Suíte completa

```bash
pytest tests
```

### Por módulo

```bash
pytest tests/login/test_login_playwright.py
pytest tests/users/test_users_playwright.py
pytest tests/products/test_products_playwright.py
pytest tests/carts/test_carts_playwright.py
```

### Em paralelo (pytest-xdist)

```bash
pytest tests -n auto
```

### Gerando relatório Allure

```bash
# Executar testes e salvar resultados
pytest tests --alluredir=allure-results

# Abrir relatório interativo no browser
allure serve allure-results
```

---

## Fixtures (conftest.py)

| Fixture               | Escopo    | Descrição                                                         |
|-----------------------|-----------|-------------------------------------------------------------------|
| `playwright_instance` | `session` | Instância única do Playwright reutilizada em toda a sessão        |
| `api_request`         | `function`| `APIRequestContext` com `base_url=https://serverest.dev`, descartado após cada teste |

---

## assert_that (assertpy)

Todos os testes usam `assert_that` da biblioteca [assertpy](https://github.com/assertpy/assertpy) para realizar asserções fluentes e legíveis.

### Importação

```python
from assertpy import assert_that
```

### Asserções mais utilizadas neste projeto

| Método                            | O que valida                                          |
|-----------------------------------|-------------------------------------------------------|
| `.is_equal_to(value)`             | Igualdade exata                                       |
| `.is_not_equal_to(value)`         | Diferença entre valores                               |
| `.is_not_none()`                  | Valor não é `None`                                    |
| `.is_none()`                      | Valor é `None`                                        |
| `.contains(substr)`               | String ou lista contém o valor informado              |
| `.does_not_contain(substr)`       | String ou lista não contém o valor                    |
| `.is_true()` / `.is_false()`      | Booleano verdadeiro / falso                           |
| `.is_greater_than(n)`             | Numérico maior que `n`                                |
| `.is_less_than(n)`                | Numérico menor que `n`                                |
| `.is_between(a, b)`               | Numérico dentro do intervalo `[a, b]`                 |
| `.is_length(n)`                   | Sequência com tamanho exato `n`                       |
| `.is_empty()` / `.is_not_empty()` | Sequência vazia ou não vazia                          |
| `.has_size(n)`                    | Coleção com `n` elementos                             |
| `.snapshot()`                     | Compara com snapshot salvo em `__snapshots/` (ver abaixo) |

### Exemplo de uso

```python
from assertpy import assert_that

resp = api_request.get("/usuarios")
assert_that(resp.status).is_equal_to(200)

body = resp.json()
assert_that(body.get("quantidade")).is_greater_than(0)
assert_that(body.get("usuarios")).is_not_empty()
```

### Snapshot testing

O método `.snapshot()` salva a resposta na primeira execução e nas execuções seguintes verifica se o conteúdo é idêntico ao snapshot armazenado. Os arquivos ficam em `__snapshots/`.

```python
body = parse_response_body(resp)
assert_that(body).snapshot()   # cria ou valida __snapshots/<nome-do-arquivo>.json
```

> Para atualizar um snapshot existente, apague o arquivo correspondente em `__snapshots/` e execute o teste novamente.

### Encadeamento de asserções

```python
assert_that(body["message"]) \
    .is_not_none() \
    .contains("sucesso")
```

---

## Allure Report — decorators disponíveis no Python

O `allure-pytest` oferece decorators e helpers para enriquecer o relatório gerado. Abaixo estão todas as anotações disponíveis.

### Decorators de nível de teste / função

| Decorator                               | Descrição                                             | Exemplo                                            |
|-----------------------------------------|-------------------------------------------------------|----------------------------------------------------|
| `@allure.severity(level)`               | Define a criticidade do teste (ver tabela abaixo)     | `@allure.severity(allure.severity_level.CRITICAL)` |
| `@allure.title("Título")`               | Título legível exibido no relatório                   | `@allure.title("CT01 - Login válido")`             |
| `@allure.description("Descrição")`      | Descrição longa do teste                              | `@allure.description("Valida token JWT retornado")`|
| `@allure.description_html("html")`      | Descrição em HTML                                     | `@allure.description_html("<b>Login</b>")`         |
| `@allure.feature("Feature")`            | Agrupa testes por funcionalidade                      | `@allure.feature("Login")`                         |
| `@allure.story("Story")`                | Subdivide features em histórias                       | `@allure.story("Login com credenciais válidas")`   |
| `@allure.epic("Epic")`                  | Agrupa features em épicos (maior granularidade)       | `@allure.epic("Autenticação")`                     |
| `@allure.tag("tag1", "tag2")`           | Tags livres para categorização                        | `@allure.tag("smoke", "regression")`               |
| `@allure.label("name", "value")`        | Label customizado de formato chave-valor              | `@allure.label("layer", "api")`                    |
| `@allure.link(url, name="texto")`       | Link genérico no relatório                            | `@allure.link("https://serverest.dev")`            |
| `@allure.issue(url, name="texto")`      | Link para issue/bug tracker                           | `@allure.issue("https://github.com/org/repo/1")`  |
| `@allure.testcase(url, name="texto")`   | Link para caso de teste em ferramenta de gestão       | `@allure.testcase("https://jira.example.com/TC-1")`|

### Níveis de severidade (`allure.severity_level`)

| Constante                          | Uso                                        |
|------------------------------------|--------------------------------------------|
| `allure.severity_level.BLOCKER`    | Impede a execução; bloqueia o release      |
| `allure.severity_level.CRITICAL`   | Fluxo principal; falha impacta diretamente |
| `allure.severity_level.NORMAL`     | Importante, mas não bloqueia o fluxo core  |
| `allure.severity_level.MINOR`      | Pouco impacto; melhoria ou detalhe         |
| `allure.severity_level.TRIVIAL`    | Cosmético ou edge case irrelevante         |

### Steps e contextos dentro dos testes

```python
import allure

# Passo nomeado no relatório
with allure.step("Criar usuário administrador"):
    post_json(request, "/usuarios", new_user)

# Decorator de step reutilizável em funções helper
@allure.step("Fazer login e obter token")
def get_token(request, email, password):
    resp = post_json(request, "/login", {"email": email, "password": password})
    return resp.json()["authorization"]
```

### Anexar evidências ao relatório

```python
import allure, json

# Texto puro
allure.attach("Corpo da resposta: ...", name="Response body", attachment_type=allure.attachment_type.TEXT)

# JSON formatado
allure.attach(json.dumps(body, indent=2), name="Response JSON", attachment_type=allure.attachment_type.JSON)

# Outros tipos disponíveis em allure.attachment_type:
# TEXT, JSON, XML, HTML, PNG, JPG, MP4, CSV, URI_LIST, ...
```

### Exemplo completo de um teste anotado

```python
import allure
from assertpy import assert_that

@allure.epic("Autenticação")
@allure.feature("Login")
@allure.story("Login com credenciais válidas")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("CT01 - Login válido retorna token JWT")
@allure.tag("smoke", "regression")
def test_ct01_valid_login_returns_token(api_request):
    with allure.step("Enviar requisição de login com credenciais válidas"):
        resp = post_json(api_request, "/login", {"email": "user@qa.com", "password": "Senha@123"})

    with allure.step("Validar status 200 e presença do token"):
        assert_that(resp.status).is_equal_to(200)
        body = parse_response_body(resp)
        assert_that(body.get("authorization")).is_not_none()
```

---

## Observações gerais

- Os cenários cobrem fluxos positivos (happy path), negativos e de validação de regras de negócio da API ServeRest.
- A suíte usa `APIRequestContext` do Playwright para chamadas HTTP — sem browser, apenas HTTP client.
- Dados dinâmicos (e-mails, nomes, produtos) são gerados em `tests/utils/faker_utils.py` para evitar conflitos entre execuções.
- Fixtures de escopo `session` mantêm a instância do Playwright aberta durante toda a execução; fixtures de escopo `function` criam e descartam o contexto HTTP por teste, garantindo isolamento.
