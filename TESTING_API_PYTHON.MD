# 🐍 Playwright API Testing com Python + Pytest (ServeRest)

Este diretório contém a versão em Python dos mesmos cenários do projeto Java.

## Estrutura

- `tests/login/test_login_playwright.py` → CT01 a CT05
- `tests/users/test_users_playwright.py` → CT01 a CT16
- `tests/products/test_products_playwright.py` → CT01 a CT13
- `tests/carts/test_carts_playwright.py` → CT01 a CT08
- `tests/resources/...` → mesmos dados CSV/JSON usados nos testes

## Pré-requisitos

- Python 3.11+
- Dependências em `requirements-python.txt`

## Instalação

```bash
python -m pip install -r requirements-python.txt
python -m playwright install
```

## Execução

### Rodar suíte completa

```bash
pytest -q tests
```

### Rodar por módulo

```bash
pytest -q tests/login/test_login_playwright.py
pytest -q tests/users/test_users_playwright.py
pytest -q tests/products/test_products_playwright.py
pytest -q tests/carts/test_carts_playwright.py
```

## Observações

- Os cenários, mensagens esperadas e regras de negócio foram mantidos equivalentes ao projeto Java.
- A suíte utiliza `APIRequestContext` do Playwright para chamadas HTTP.
- Fixtures comuns estão em `tests/conftest.py`.
