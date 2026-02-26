import csv
import json
from pathlib import Path

import allure
import pytest
from playwright.sync_api import APIRequestContext

from tests.utils.api_utils import JSON_HEADERS, parse_response_body, post_json
from tests.utils.faker_utils import random_email, random_product


def create_user(request: APIRequestContext, email: str, password: str, admin: bool):
    payload = {
        "nome": email,
        "email": email,
        "password": password,
        "administrador": "true" if admin else "false",
    }
    return post_json(request, "/usuarios", payload)


def load_invalid_email_values() -> list[str]:
    csv_path = Path(__file__).resolve().parent.parent / "resources" / "login" / "invalid-login-emails.csv"
    with csv_path.open("r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return [row["email"] for row in reader]


def load_required_fields_rows() -> list[dict[str, str]]:
    csv_path = Path(__file__).resolve().parent.parent / "resources" / "login" / "invalido-login.csv"
    with csv_path.open("r", encoding="utf-8") as csv_file:
        return list(csv.DictReader(csv_file))


@allure.severity(allure.severity_level.CRITICAL)
def test_ct01_login_with_valid_credentials_and_validate_token(api_request: APIRequestContext):
    email = random_email()
    password = "SenhaSegura@123"

    create_resp = create_user(api_request, email, password, admin=False)
    assert create_resp.status == 201, "User creation should return 201"

    login_resp = post_json(api_request, "/login", {"email": email, "password": password})

    assert login_resp.status == 200
    body = parse_response_body(login_resp)
    assert body["message"] == "Login realizado com sucesso"
    assert body.get("authorization") is not None


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
    response_body = parse_response_body(resp)
    assert response_body["message"] == "Email e/ou senha inválidos"
    assert response_body.get("authorization") is None


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("_row", load_required_fields_rows())
def test_ct03_validate_required_fields_on_login(_row: dict[str, str], api_request: APIRequestContext):
    resp1 = post_json(api_request, "/login", {"email": "", "password": "senha123"})
    assert resp1.status == 400
    body1 = parse_response_body(resp1)
    assert body1.get("email") is not None

    resp2 = post_json(api_request, "/login", {"email": "test@email.com", "password": ""})
    assert resp2.status == 400
    body2 = parse_response_body(resp2)
    assert body2.get("password") is not None

    resp3 = post_json(api_request, "/login", {"email": "", "password": ""})
    assert resp3.status == 400
    body3 = parse_response_body(resp3)
    assert body3.get("email") is not None
    assert body3.get("password") is not None


@allure.severity(allure.severity_level.CRITICAL)
def test_ct04_login_and_use_token_in_protected_route(api_request: APIRequestContext):
    user_email = random_email()
    user_password = "SenhaSegura@123"

    create_resp = create_user(api_request, user_email, user_password, admin=False)
    assert create_resp.status == 201

    login_resp = post_json(api_request, "/login", {"email": user_email, "password": user_password})
    assert login_resp.status == 200

    login_body = parse_response_body(login_resp)
    assert login_body["message"] == "Login realizado com sucesso"
    auth_token = login_body["authorization"]

    product_payload = {
        "nome": random_product(),
        "preco": 100,
        "descricao": "Product generated for auth test",
        "quantidade": 10,
    }

    product_resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": auth_token},
        data=json.dumps(product_payload, ensure_ascii=False),
    )

    assert product_resp.status == 403
    product_body = parse_response_body(product_resp)
    assert product_body["message"] == "Rota exclusiva para administradores"


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("invalid_email", load_invalid_email_values())
def test_ct05_validate_invalid_email_format(invalid_email: str, api_request: APIRequestContext):
    resp = post_json(api_request, "/login", {"email": invalid_email, "password": "senha123"})

    assert resp.status == 400
    response_body = parse_response_body(resp)
    assert response_body.get("email") is not None
