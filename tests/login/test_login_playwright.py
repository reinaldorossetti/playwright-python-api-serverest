import csv
import json
from pathlib import Path

import allure
import pytest
from assertpy import assert_that
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
    assert_that(create_resp.status).is_equal_to(201)

    login_resp = post_json(api_request, "/login", {"email": email, "password": password})

    assert_that(login_resp.status).is_equal_to(200)
    body = parse_response_body(login_resp)
    assert_that(body["message"]).is_equal_to("Login realizado com sucesso")
    assert_that(body.get("authorization")).is_not_none()


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
    assert_that(response_body).snapshot()


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("_row", load_required_fields_rows())
def test_ct03_validate_required_fields_on_login(_row: dict[str, str], api_request: APIRequestContext):
    resp1 = post_json(api_request, "/login", {"email": "", "password": "senha123"})
    assert_that(resp1.status).is_equal_to(400)
    body1 = parse_response_body(resp1)
    assert_that(body1).snapshot()

    resp2 = post_json(api_request, "/login", {"email": "test@email.com", "password": ""})
    assert_that(resp2.status).is_equal_to(400)
    body2 = parse_response_body(resp2)
    assert_that(body2).snapshot()

    resp3 = post_json(api_request, "/login", {"email": "", "password": ""})
    assert_that(resp3.status).is_equal_to(400)
    body3 = parse_response_body(resp3)
    assert_that(body3).snapshot()


@allure.severity(allure.severity_level.CRITICAL)
def test_ct04_login_and_use_token_in_protected_route(api_request: APIRequestContext):
    user_email = random_email()
    user_password = "SenhaSegura@123"

    create_resp = create_user(api_request, user_email, user_password, admin=False)
    assert_that(create_resp.status).is_equal_to(201)

    login_resp = post_json(api_request, "/login", {"email": user_email, "password": user_password})
    assert_that(login_resp.status).is_equal_to(200)

    login_body = parse_response_body(login_resp)
    assert_that(login_body["message"]).is_equal_to("Login realizado com sucesso")
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

    assert_that(product_resp.status).is_equal_to(403)
    product_body = parse_response_body(product_resp)
    assert_that(product_body).snapshot()


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("invalid_email", load_invalid_email_values())
def test_ct05_validate_invalid_email_format(invalid_email: str, api_request: APIRequestContext):
    resp = post_json(api_request, "/login", {"email": invalid_email, "password": "senha123"})

    assert_that(resp.status).is_equal_to(400)
    response_body = parse_response_body(resp)
    assert_that(response_body).contains_key("email")
