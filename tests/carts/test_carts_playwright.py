import json
import os
from pathlib import Path

import allure
from assertpy import assert_that
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext

from tests.utils.api_utils import JSON_HEADERS, parse_response_body, post_json
from tests.utils.faker_utils import random_email, random_product

load_dotenv(Path(__file__).resolve().parents[2] / "user.env")
USER_PASSWORD = os.getenv("USER_PASSWORD")


def login_with_default_payload(request: APIRequestContext) -> str:
    user_email = random_email()

    new_user = {
        "nome": "Cart Default User",
        "email": user_email,
        "password": USER_PASSWORD,
        "administrador": "true",
    }

    post_json(request, "/usuarios", new_user)
    resp = post_json(request, "/login", {"email": user_email, "password": USER_PASSWORD})
    assert_that(resp.status).is_equal_to(200)

    login_body = parse_response_body(resp)
    return login_body["authorization"]


def create_admin_user_and_get_token(request: APIRequestContext) -> str:
    user_email = random_email()

    new_user = {
        "nome": "Cart User",
        "email": user_email,
        "password": USER_PASSWORD,
        "administrador": "true",
    }

    post_json(request, "/usuarios", new_user)
    resp = post_json(request, "/login", {"email": user_email, "password": USER_PASSWORD})
    assert_that(resp.status).is_equal_to(200)

    login_body = parse_response_body(resp)
    return login_body["authorization"]


def create_product(
    request: APIRequestContext,
    token: str,
    price: int,
    quantity: int,
    description: str,
) -> str:
    product_data = {
        "nome": random_product(),
        "preco": price,
        "descricao": description,
        "quantidade": quantity,
    }

    product_resp = request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(product_data, ensure_ascii=False),
    )
    assert_that(product_resp.status).is_equal_to(201)

    product_body = parse_response_body(product_resp)
    assert_that(product_body["message"]).is_equal_to("Cadastro realizado com sucesso")
    return product_body["_id"]


@allure.severity(allure.severity_level.CRITICAL)
def test_ct01_full_cart_lifecycle_for_authenticated_user(api_request: APIRequestContext):
    token = create_admin_user_and_get_token(api_request)

    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})

    product_id = create_product(api_request, token, 150, 10, "Product created for cart lifecycle test")
    cart_body = {"produtos": [{"idProduto": product_id, "quantidade": 2}]}

    create_cart_resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(cart_body, ensure_ascii=False),
    )
    assert_that(create_cart_resp.status).is_equal_to(201)

    create_cart_body = parse_response_body(create_cart_resp)
    assert_that(create_cart_body["message"]).is_equal_to("Cadastro realizado com sucesso")
    assert_that(create_cart_body.get("_id")).is_not_none()

    cart_id = create_cart_body["_id"]
    get_cart_resp = api_request.get(f"/carrinhos/{cart_id}")
    assert_that(get_cart_resp.status).is_equal_to(200)

    get_cart_body = parse_response_body(get_cart_resp)

    produtos = get_cart_body["produtos"]
    assert_that(len(produtos)).is_equal_to(1)
    assert_that(get_cart_body.get("precoTotal")).is_not_none()
    assert_that(get_cart_body.get("quantidadeTotal")).is_not_none()
    assert_that(get_cart_body.get("idUsuario")).is_not_none()
    assert_that(get_cart_body["_id"]).is_equal_to(cart_id)

    conclude_resp = api_request.delete("/carrinhos/concluir-compra", headers={"Authorization": token})
    assert_that(conclude_resp.status).is_equal_to(200)

    conclude_body = parse_response_body(conclude_resp)
    assert_that(conclude_body["message"]).contains("Registro excluído com sucesso")


@allure.severity(allure.severity_level.CRITICAL)
def test_ct02_cancel_purchase_and_return_products_to_stock(api_request: APIRequestContext):
    token = login_with_default_payload(api_request)

    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})

    product_id = create_product(api_request, token, 200, 5, "Product for cancel purchase test")
    cart_body = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}

    create_cart_resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(cart_body, ensure_ascii=False),
    )
    assert_that(create_cart_resp.status).is_equal_to(201)

    cancel_resp = api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})
    assert_that(cancel_resp.status).is_equal_to(200)

    cancel_body = parse_response_body(cancel_resp)
    assert_that(cancel_body.get("message")).is_not_none()


@allure.severity(allure.severity_level.CRITICAL)
def test_ct03_prevent_creating_cart_without_authentication_token(api_request: APIRequestContext):
    cart_body = {"produtos": [{"idProduto": "BeeJh5lz3k6kSIzA", "quantidade": 1}]}

    resp = api_request.post(
        "/carrinhos",
        headers=JSON_HEADERS,
        data=json.dumps(cart_body, ensure_ascii=False),
    )

    assert_that(resp.status).is_equal_to(401)
    body = parse_response_body(resp)
    assert_that(body).snapshot()


@allure.severity(allure.severity_level.CRITICAL)
def test_ct04_prevent_creating_more_than_one_cart_for_same_user(api_request: APIRequestContext):
    token = login_with_default_payload(api_request)

    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})

    product_id = create_product(api_request, token, 120, 3, "Product for multiple cart test")
    first_cart = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}

    first_resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(first_cart, ensure_ascii=False),
    )
    assert_that(first_resp.status).is_equal_to(201)

    second_resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(first_cart, ensure_ascii=False),
    )
    assert_that(second_resp.status).is_equal_to(400)

    second_body = parse_response_body(second_resp)
    assert_that(second_body["message"]).contains("Não é permitido ter mais de 1 carrinho")


@allure.severity(allure.severity_level.NORMAL)
def test_ct05_cart_not_found_by_id(api_request: APIRequestContext):
    resp = api_request.get("/carrinhos/invalid-cart-id-123")
    assert_that(resp.status).is_equal_to(400)

    body = parse_response_body(resp)
    assert_that(body).snapshot()


@allure.severity(allure.severity_level.CRITICAL)
def test_ct06_prevent_cart_creation_when_product_stock_is_insufficient(api_request: APIRequestContext):
    token = login_with_default_payload(api_request)

    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})

    product_id = create_product(api_request, token, 100, 1, "Low stock product for cart test")
    cart_body = {"produtos": [{"idProduto": product_id, "quantidade": 2}]}

    resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(cart_body, ensure_ascii=False),
    )

    assert_that(resp.status).is_equal_to(400)
    body = parse_response_body(resp)
    assert_that(body["message"]).contains("Produto não possui quantidade suficiente")


@allure.severity(allure.severity_level.CRITICAL)
def test_ct07_prevent_cart_creation_with_duplicated_products_in_same_cart(api_request: APIRequestContext):
    token = login_with_default_payload(api_request)

    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})

    product_id = create_product(api_request, token, 150, 10, "Product created for duplicated products cart test")
    duplicated_cart_body = {
        "produtos": [
            {"idProduto": product_id, "quantidade": 1},
            {"idProduto": product_id, "quantidade": 1},
        ]
    }

    resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(duplicated_cart_body, ensure_ascii=False),
    )

    assert_that(resp.status).is_equal_to(400)
    body = parse_response_body(resp)
    assert_that(body["message"]).contains("Não é permitido possuir produto duplicado")


@allure.severity(allure.severity_level.CRITICAL)
def test_ct08_prevent_cart_creation_with_non_existing_product(api_request: APIRequestContext):
    token = login_with_default_payload(api_request)

    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})

    invalid_cart_body = {"produtos": [{"idProduto": "AAAAAAAAAAAAAAAA", "quantidade": 1}]}

    resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(invalid_cart_body, ensure_ascii=False),
    )

    assert_that(resp.status).is_equal_to(400)
    body = parse_response_body(resp)
    assert_that(body["message"]).contains("Produto não encontrado")
