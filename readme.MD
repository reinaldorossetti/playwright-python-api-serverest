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
- [Funcionalidades do Playwright](#-funcionalidades-do-playwright)
- [Relatórios](#-relatórios)
- [Boas Práticas](#-boas-práticas)
- [Recursos Adicionais](#-recursos-adicionais)

---

## 🧪 Sobre o Playwright

**Playwright** é um framework open-source da Microsoft, conhecido por testes E2E em browser e também por uma API robusta para testes HTTP via `APIRequestContext`, ideal para automação de APIs em Python.

### ✨ Principais Características

- **🔥 APIRequestContext fluente**: Requisições HTTP com `get`, `post`, `put`, `delete`
- **🚀 Suporte completo a REST**: operações GET, POST, PUT, PATCH e DELETE com JSON
- **🎯 Assertions nativas do Python**: validações claras e objetivas com `assert`
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
- Foque na clareza do código, usando as asserções nativas (`assert`).

---

## 📦 Dependências e Versões (requirements.txt)

| Componente                         | Versão  | Descrição  |
|------------------------------------|---------|------------|
| `pytest`                           | 8.4.2   | Framework principal de testes unitários/integrados |
| `playwright`                       | 1.58.0  | Engine para chamadas e requisições HTTP |
| `pytest-xdist`                     | 3.8.0   | Suporte à execução simultânea e multiprocessos |
| `allure-pytest`                    | 2.15.3  | Geração unificada de relatórios visuais com Allure |

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
pytest
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
@allure.severity(allure.severity_level.CRITICAL)
def test_ct01_login_with_valid_credentials_and_validate_token(api_request: APIRequestContext):
    email = "usuario_valido@email.com"
    password = "SenhaSegura@123"

    login_resp = post_json(api_request, "/login", {"email": email, "password": password})

    assert login_resp.status == 200
    body = login_resp.json()
    assert body["message"] == "Login realizado com sucesso"
    assert body.get("authorization") is not None
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

    assert resp.status == 401
    response_body = resp.json()
    assert response_body["message"] == "Email e/ou senha inválidos"
```

### Exemplo 4: Validação de campos obrigatórios (Data-driven com Pytest)

```python
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("_row", load_required_fields_rows())
def test_ct03_validate_required_fields_on_login(_row: dict[str, str], api_request: APIRequestContext):
    resp = post_json(api_request, "/login", {"email": "", "password": "senha123"})
    assert resp.status == 400
    body = resp.json()
    assert body.get("email") is not None
```

### Exemplo 5: Uso de token dinâmico recebido em Auth

```python
@allure.severity(allure.severity_level.CRITICAL)
def test_ct04_login_and_use_token_in_protected_route(api_request: APIRequestContext):
    auth_token = "Bearer XXXX"  # Recebido de requests anteriores do setup

    product_payload = {"nome": "Teste", "preco": 100, "descricao": "Teste", "quantidade": 10}

    product_resp = api_request.post(
        "/produtos",
        headers={"Authorization": auth_token, "Content-Type": "application/json"},
        data=json.dumps(product_payload),
    )

    assert product_resp.status == 403
    assert product_resp.json()["message"] == "Rota exclusiva para administradores"
```

### Exemplo 6: Teste iterando em arquivos CSV via Pathlib

```python
def load_invalid_email_values() -> list[str]:
    # Utilizando Path do Python
    pass

@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("invalid_email", load_invalid_email_values())
def test_ct05_validate_invalid_email_format(invalid_email: str, api_request: APIRequestContext):
    resp = post_json(api_request, "/login", {"email": invalid_email, "password": "senha123"})

    assert resp.status == 400
    assert resp.json().get("email") is not None
```

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

Para transformar os dados JSON de saída do Pytest na interface gráfica robusta do allure:

```bash
allure serve allure-results
```

O dashboard exibe:
- ✅ Cenários OK, Skipped e Failed detalhadamente
- ⏱️ Tempos exatos capturados via Hooks do Pytest 
- 📋 Stack Trace de Erros
- 📊 Análise das execuções em timeline

### 🏷️ Exemplos de marcações Allure nos Testes (Decorators)

O plugin `allure-pytest` suporta metadados extremamente ricos em cima das functions diretamente:

```python
import allure

@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Login")
@allure.story("Login com credenciais inválidas")
@allure.description("Valida que o endpoint retorna 401 para credencial incorreta de usuário")
@allure.issue("SRV-123")
def test_ct02_login_with_invalid_credentials(api_request: APIRequestContext):
    with allure.step("Realizar post com credencial incorreta"):
        resp = api_request.post("/login", data={"email": "...", "password": "..."})

    with allure.step("Validar assert no status do endpoint login"):
        assert resp.status == 401
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
