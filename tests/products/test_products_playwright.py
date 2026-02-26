import json
import time
import uuid

import allure
import pytest
from playwright.sync_api import APIRequestContext

from tests.utils.api_utils import JSON_HEADERS, load_json_resource, parse_response_body, post_json, put_json


def get_admin_token(request: APIRequestContext) -> str:
    email = f"admin.{uuid.uuid4()}@example.com"
    password = "SenhaSegura@123"

    user_payload = {
        "nome": "Admin User",
        "email": email,
        "password": password,
        "administrador": "true",
    }

    post_json(request, "/usuarios", user_payload)
    login_resp = post_json(request, "/login", {"email": email, "password": password})
    assert login_resp.status == 200

    login_body = parse_response_body(login_resp)
    return login_body["authorization"]


@allure.severity(allure.severity_level.CRITICAL)
def test_ct01_list_all_products_and_validate_json_structure(api_request: APIRequestContext):
    resp = api_request.get("/produtos")
    assert resp.status == 200

    body = parse_response_body(resp)
    quantidade = body["quantidade"]
    produtos = body["produtos"]

    assert quantidade >= 0
    assert produtos is not None

    for product in produtos:
        assert "nome" in product
        assert "preco" in product
        assert "descricao" in product
        assert "quantidade" in product
        assert "_id" in product


@allure.severity(allure.severity_level.CRITICAL)
def test_ct02_create_new_product_as_administrator(api_request: APIRequestContext):
    token = get_admin_token(api_request)
    product_name = f"Product {int(time.time() * 1000)}"
    product_payload = {
        "nome": product_name,
        "preco": 250,
        "descricao": "Automated test product",
        "quantidade": 100,
    }

    create_resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(product_payload, ensure_ascii=False),
    )

    assert create_resp.status == 201

    create_body = parse_response_body(create_resp)
    assert create_body["message"] == "Cadastro realizado com sucesso"
    assert create_body.get("_id") is not None

    product_id = create_body["_id"]

    get_resp = api_request.get(f"/produtos/{product_id}")
    assert get_resp.status == 200

    product = parse_response_body(get_resp)
    assert product["nome"] == product_name
    assert product["preco"] == 250
    assert product["quantidade"] == 100


@allure.severity(allure.severity_level.CRITICAL)
def test_ct03_validate_error_on_duplicate_product_name(api_request: APIRequestContext):
    token = get_admin_token(api_request)
    name = f"Duplicate Product Test {int(time.time() * 1000)}"

    product_payload = {
        "nome": name,
        "preco": 150,
        "descricao": "First product",
        "quantidade": 50,
    }

    first = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(product_payload, ensure_ascii=False),
    )
    assert first.status == 201

    second = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(product_payload, ensure_ascii=False),
    )
    assert second.status == 400

    second_body = parse_response_body(second)
    assert second_body["message"] == "Já existe produto com esse nome"


@allure.severity(allure.severity_level.NORMAL)
def test_ct04_search_for_products_with_filters(api_request: APIRequestContext):
    resp = api_request.get("/produtos?nome=Logitech")
    assert resp.status == 200

    body = parse_response_body(resp)
    produtos = body["produtos"]
    if produtos:
        for product in produtos:
            assert "Logitech" in product["nome"]

    price_resp = api_request.get("/produtos?preco=100")
    assert price_resp.status == 200


@allure.severity(allure.severity_level.CRITICAL)
def test_ct05_update_existing_product(api_request: APIRequestContext):
    token = get_admin_token(api_request)
    product_name = f"Product {int(time.time() * 1000)}"

    initial_product = {
        "nome": product_name,
        "preco": 100,
        "descricao": "Original description",
        "quantidade": 50,
    }

    create_resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(initial_product, ensure_ascii=False),
    )
    assert create_resp.status == 201

    create_body = parse_response_body(create_resp)
    product_id = create_body["_id"]

    updated_product = {
        "nome": product_name,
        "preco": 200,
        "descricao": "Updated description",
        "quantidade": 75,
    }

    update_resp = put_json(
        api_request,
        f"/produtos/{product_id}",
        updated_product,
        headers={"Authorization": token},
    )
    assert update_resp.status == 200

    update_body = parse_response_body(update_resp)
    assert update_body["message"] == "Registro alterado com sucesso"

    get_resp = api_request.get(f"/produtos/{product_id}")
    assert get_resp.status == 200
    product = parse_response_body(get_resp)
    assert product["preco"] == 200
    assert product["descricao"] == "Updated description"
    assert product["quantidade"] == 75


@allure.severity(allure.severity_level.NORMAL)
def test_ct06_validate_price_calculations_and_comparisons(api_request: APIRequestContext):
    resp = api_request.get("/produtos")
    assert resp.status == 200

    body = parse_response_body(resp)
    produtos = body["produtos"]

    if not produtos:
        return

    prices = [float(item["preco"]) for item in produtos]

    max_price = max(prices, default=0)
    min_price = min(prices, default=0)

    for price in prices:
        assert price > 0
        assert price < 100000

    assert max_price >= min_price


@allure.severity(allure.severity_level.CRITICAL)
def test_ct07_create_product_without_token(api_request: APIRequestContext):
    product_payload = {
        "nome": "Product Without Auth",
        "preco": 100,
        "descricao": "Test",
        "quantidade": 10,
    }

    resp = post_json(api_request, "/produtos", product_payload)

    assert resp.status == 401
    body = parse_response_body(resp)
    assert body["message"] == "Token de acesso ausente, inválido, expirado ou usuário do token não existe mais"


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.parametrize("number_field", [1, 2, 3, 4])
def test_ct08_validate_required_fields_when_creating_product(number_field: int, api_request: APIRequestContext):
    token = get_admin_token(api_request)

    payload_by_case = {
        1: {"preco": 0.55, "descricao": "Test without name", "quantidade": 10},
        2: {"nome": "Product Without Description", "descricao": "", "quantidade": 10},
        3: {"nome": "Product Without Quantity", "preco": 100, "quantidade": -1},
        4: {"nome": "null", "preco": 1.99, "descricao": "null"},
    }

    payload = payload_by_case[number_field]
    resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(payload, ensure_ascii=False),
    )

    assert resp.status == 400


@allure.severity(allure.severity_level.MINOR)
def test_ct09_work_with_complex_json_data(api_request: APIRequestContext):
    resp = api_request.get("/produtos")
    assert resp.status == 200

    body = parse_response_body(resp)
    produtos = body["produtos"]

    if produtos is None:
        return

    cheap_products = [p for p in produtos if float(p["preco"]) < 100]
    medium_products = [p for p in produtos if 100 <= float(p["preco"]) < 500]
    expensive_products = [p for p in produtos if float(p["preco"]) >= 500]

    assert cheap_products is not None
    assert medium_products is not None
    assert expensive_products is not None


@allure.severity(allure.severity_level.CRITICAL)
def test_ct10_delete_existing_product(api_request: APIRequestContext):
    token = get_admin_token(api_request)
    product_name = f"Product {int(time.time() * 1000)}"

    product_payload = {
        "nome": product_name,
        "preco": 100,
        "descricao": "Product to delete",
        "quantidade": 10,
    }

    create_resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(product_payload, ensure_ascii=False),
    )
    assert create_resp.status == 201

    create_body = parse_response_body(create_resp)
    product_id = create_body["_id"]

    delete_resp = api_request.delete(f"/produtos/{product_id}", headers={"Authorization": token})
    assert delete_resp.status == 200

    delete_body = parse_response_body(delete_resp)
    assert delete_body["message"] == "Registro excluído com sucesso"

    get_resp = api_request.get(f"/produtos/{product_id}")
    assert get_resp.status == 400

    get_body = parse_response_body(get_resp)
    assert get_body["message"] == "Produto não encontrado"


@allure.severity(allure.severity_level.NORMAL)
def test_ct11_create_product_from_fixed_json_payload(api_request: APIRequestContext):
    token = get_admin_token(api_request)

    product_payload = load_json_resource("products/productPayload.json")
    product_payload["nome"] = f"Product {int(time.time() * 1000)}"

    resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(product_payload, ensure_ascii=False),
    )

    assert resp.status == 201
    body = parse_response_body(resp)
    assert body["message"] == "Cadastro realizado com sucesso"
    assert body.get("_id") is not None


@allure.severity(allure.severity_level.CRITICAL)
def test_ct12_prevent_deleting_product_in_cart(api_request: APIRequestContext):
    admin_token = get_admin_token(api_request)

    product_payload = {
        "nome": f"Product {int(time.time() * 1000)}",
        "preco": 300,
        "descricao": "Product linked to cart",
        "quantidade": 10,
    }

    create_product_resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": admin_token},
        data=json.dumps(product_payload, ensure_ascii=False),
    )
    assert create_product_resp.status == 201

    create_product_body = parse_response_body(create_product_resp)
    product_id = create_product_body["_id"]

    user_email = f"cart.user.{int(time.time() * 1000)}@example.com"
    user_password = "SenhaSegura@123"

    user_data = {
        "nome": "Cart User",
        "email": user_email,
        "password": user_password,
        "administrador": "false",
    }

    post_json(api_request, "/usuarios", user_data)

    login_resp = post_json(api_request, "/login", {"email": user_email, "password": user_password})
    assert login_resp.status == 200

    login_body = parse_response_body(login_resp)
    user_token = login_body["authorization"]

    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": user_token})

    cart_body = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}
    cart_resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": user_token},
        data=json.dumps(cart_body, ensure_ascii=False),
    )
    assert cart_resp.status == 201

    delete_resp = api_request.delete(f"/produtos/{product_id}", headers={"Authorization": admin_token})
    assert delete_resp.status == 400

    delete_body = parse_response_body(delete_resp)
    assert delete_body["message"] == "Não é permitido excluir produto que faz parte de carrinho"


@allure.severity(allure.severity_level.CRITICAL)
def test_ct13_restrict_product_creation_to_administrators_only(api_request: APIRequestContext):
    user_email = f"non.admin.{int(time.time() * 1000)}@example.com"
    user_password = "SenhaSegura@123"

    user_data = {
        "nome": "Non Admin User",
        "email": user_email,
        "password": user_password,
        "administrador": "false",
    }

    post_json(api_request, "/usuarios", user_data)

    login_resp = post_json(api_request, "/login", {"email": user_email, "password": user_password})
    assert login_resp.status == 200

    login_body = parse_response_body(login_resp)
    non_admin_token = login_body["authorization"]

    product_data = {
        "nome": "Restricted Product",
        "preco": 500,
        "descricao": "Product should be created only by admins",
        "quantidade": 5,
    }

    product_resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": non_admin_token},
        data=json.dumps(product_data, ensure_ascii=False),
    )

    assert product_resp.status == 403
    product_body = parse_response_body(product_resp)
    assert product_body["message"] == "Rota exclusiva para administradores"
