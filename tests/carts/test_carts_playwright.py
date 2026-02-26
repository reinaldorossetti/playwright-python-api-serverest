import json

import allure
from playwright.sync_api import APIRequestContext

from tests.utils.api_utils import JSON_HEADERS, parse_response_body, post_json
from tests.utils.faker_utils import random_email, random_product


def login_with_default_payload(request: APIRequestContext) -> str:
    user_email = random_email()
    user_password = "SenhaSegura@123"

    new_user = {
        "nome": "Cart Default User",
        "email": user_email,
        "password": user_password,
        "administrador": "true",
    }

    post_json(request, "/usuarios", new_user)
    resp = post_json(request, "/login", {"email": user_email, "password": user_password})
    assert resp.status == 200

    login_body = parse_response_body(resp)
    return login_body["authorization"]


def create_admin_user_and_get_token(request: APIRequestContext) -> str:
    user_email = random_email()
    user_password = "SenhaSegura@123"

    new_user = {
        "nome": "Cart User",
        "email": user_email,
        "password": user_password,
        "administrador": "true",
    }

    post_json(request, "/usuarios", new_user)
    resp = post_json(request, "/login", {"email": user_email, "password": user_password})
    assert resp.status == 200

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
    assert product_resp.status == 201

    product_body = parse_response_body(product_resp)
    assert product_body["message"] == "Cadastro realizado com sucesso"
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
    assert create_cart_resp.status == 201

    create_cart_body = parse_response_body(create_cart_resp)
    assert create_cart_body["message"] == "Cadastro realizado com sucesso"
    assert create_cart_body.get("_id") is not None

    cart_id = create_cart_body["_id"]
    get_cart_resp = api_request.get(f"/carrinhos/{cart_id}")
    assert get_cart_resp.status == 200

    get_cart_body = parse_response_body(get_cart_resp)

    produtos = get_cart_body["produtos"]
    assert len(produtos) == 1
    assert get_cart_body.get("precoTotal") is not None
    assert get_cart_body.get("quantidadeTotal") is not None
    assert get_cart_body.get("idUsuario") is not None
    assert get_cart_body["_id"] == cart_id

    conclude_resp = api_request.delete("/carrinhos/concluir-compra", headers={"Authorization": token})
    assert conclude_resp.status == 200

    conclude_body = parse_response_body(conclude_resp)
    assert "Registro excluído com sucesso" in conclude_body["message"]


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
    assert create_cart_resp.status == 201

    cancel_resp = api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": token})
    assert cancel_resp.status == 200

    cancel_body = parse_response_body(cancel_resp)
    assert cancel_body.get("message") is not None


@allure.severity(allure.severity_level.CRITICAL)
def test_ct03_prevent_creating_cart_without_authentication_token(api_request: APIRequestContext):
    cart_body = {"produtos": [{"idProduto": "BeeJh5lz3k6kSIzA", "quantidade": 1}]}

    resp = api_request.post(
        "/carrinhos",
        headers=JSON_HEADERS,
        data=json.dumps(cart_body, ensure_ascii=False),
    )

    assert resp.status == 401
    body = parse_response_body(resp)
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


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
    assert first_resp.status == 201

    second_resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(first_cart, ensure_ascii=False),
    )
    assert second_resp.status == 400

    second_body = parse_response_body(second_resp)
    assert "Não é permitido ter mais de 1 carrinho" in second_body["message"]


@allure.severity(allure.severity_level.NORMAL)
def test_ct05_cart_not_found_by_id(api_request: APIRequestContext):
    resp = api_request.get("/carrinhos/invalid-cart-id-123")
    assert resp.status == 400

    body = parse_response_body(resp)
    assert body["id"] == "id deve ter exatamente 16 caracteres alfanuméricos"


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

    assert resp.status == 400
    body = parse_response_body(resp)
    assert "Produto não possui quantidade suficiente" in body["message"]


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

    assert resp.status == 400
    body = parse_response_body(resp)
    assert "Não é permitido possuir produto duplicado" in body["message"]


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

    assert resp.status == 400
    body = parse_response_body(resp)
    assert "Produto não encontrado" in body["message"]
