import json
import time
import uuid

import allure
import pytest
from assertpy import assert_that
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
    assert_that(login_resp.status).is_equal_to(200)

    login_body = parse_response_body(login_resp)
    return login_body["authorization"]


@allure.severity(allure.severity_level.CRITICAL)
def test_ct01_list_all_products_and_validate_json_structure(api_request: APIRequestContext):
    resp = api_request.get("/produtos")
    assert_that(resp.status).is_equal_to(200)

    body = parse_response_body(resp)
    quantidade = body["quantidade"]
    produtos = body["produtos"]

    assert_that(quantidade).is_greater_than_or_equal_to(0)
    assert_that(produtos).is_not_none()

    for product in produtos:
        assert_that(product).contains_key("nome")
        assert_that(product).contains_key("preco")
        assert_that(product).contains_key("descricao")
        assert_that(product).contains_key("quantidade")
        assert_that(product).contains_key("_id")


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

    assert_that(create_resp.status).is_equal_to(201)

    create_body = parse_response_body(create_resp)
    assert_that(create_body["message"]).is_equal_to("Cadastro realizado com sucesso")
    assert_that(create_body.get("_id")).is_not_none()

    product_id = create_body["_id"]

    get_resp = api_request.get(f"/produtos/{product_id}")
    assert_that(get_resp.status).is_equal_to(200)

    product = parse_response_body(get_resp)
    assert_that(product["nome"]).is_equal_to(product_name)
    assert_that(product["preco"]).is_equal_to(250)
    assert_that(product["quantidade"]).is_equal_to(100)


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
    assert_that(first.status).is_equal_to(201)

    second = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": token},
        data=json.dumps(product_payload, ensure_ascii=False),
    )
    assert_that(second.status).is_equal_to(400)

    second_body = parse_response_body(second)
    assert_that(second_body).snapshot()


@allure.severity(allure.severity_level.NORMAL)
def test_ct04_search_for_products_with_filters(api_request: APIRequestContext):
    resp = api_request.get("/produtos?nome=Logitech")
    assert_that(resp.status).is_equal_to(200)

    body = parse_response_body(resp)
    produtos = body["produtos"]
    if produtos:
        for product in produtos:
            assert_that(product["nome"]).contains("Logitech")

    price_resp = api_request.get("/produtos?preco=100")
    assert_that(price_resp.status).is_equal_to(200)


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
    assert_that(create_resp.status).is_equal_to(201)

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
    assert_that(update_resp.status).is_equal_to(200)

    update_body = parse_response_body(update_resp)
    assert_that(update_body["message"]).is_equal_to("Registro alterado com sucesso")

    get_resp = api_request.get(f"/produtos/{product_id}")
    assert_that(get_resp.status).is_equal_to(200)
    product = parse_response_body(get_resp)
    assert_that(product["preco"]).is_equal_to(200)
    assert_that(product["descricao"]).is_equal_to("Updated description")
    assert_that(product["quantidade"]).is_equal_to(75)


@allure.severity(allure.severity_level.NORMAL)
def test_ct06_validate_price_calculations_and_comparisons(api_request: APIRequestContext):
    resp = api_request.get("/produtos")
    assert_that(resp.status).is_equal_to(200)

    body = parse_response_body(resp)
    produtos = body["produtos"]

    if not produtos:
        return

    prices = [float(item["preco"]) for item in produtos]

    max_price = max(prices, default=0)
    min_price = min(prices, default=0)

    for price in prices:
        assert_that(price).is_greater_than(0)
        assert_that(price).is_less_than(100000)

    assert_that(max_price).is_greater_than_or_equal_to(min_price)


@allure.severity(allure.severity_level.CRITICAL)
def test_ct07_create_product_without_token(api_request: APIRequestContext):
    product_payload = {
        "nome": "Product Without Auth",
        "preco": 100,
        "descricao": "Test",
        "quantidade": 10,
    }

    resp = post_json(api_request, "/produtos", product_payload)

    assert_that(resp.status).is_equal_to(401)
    body = parse_response_body(resp)
    assert_that(body).snapshot()


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

    assert_that(resp.status).is_equal_to(400)


@allure.severity(allure.severity_level.MINOR)
def test_ct09_work_with_complex_json_data(api_request: APIRequestContext):
    resp = api_request.get("/produtos")
    assert_that(resp.status).is_equal_to(200)

    body = parse_response_body(resp)
    produtos = body["produtos"]

    if produtos is None:
        return

    cheap_products = [p for p in produtos if float(p["preco"]) < 100]
    medium_products = [p for p in produtos if 100 <= float(p["preco"]) < 500]
    expensive_products = [p for p in produtos if float(p["preco"]) >= 500]

    assert_that(cheap_products).is_not_none()
    assert_that(medium_products).is_not_none()
    assert_that(expensive_products).is_not_none()


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
    assert_that(create_resp.status).is_equal_to(201)

    create_body = parse_response_body(create_resp)
    product_id = create_body["_id"]

    delete_resp = api_request.delete(f"/produtos/{product_id}", headers={"Authorization": token})
    assert_that(delete_resp.status).is_equal_to(200)

    delete_body = parse_response_body(delete_resp)
    assert_that(delete_body).snapshot()

    get_resp = api_request.get(f"/produtos/{product_id}")
    assert_that(get_resp.status).is_equal_to(400)

    get_body = parse_response_body(get_resp)
    assert_that(get_body).snapshot()


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

    assert_that(resp.status).is_equal_to(201)
    body = parse_response_body(resp)
    assert_that(body["message"]).is_equal_to("Cadastro realizado com sucesso")
    assert_that(body.get("_id")).is_not_none()


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
    assert_that(create_product_resp.status).is_equal_to(201)

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
    assert_that(login_resp.status).is_equal_to(200)

    login_body = parse_response_body(login_resp)
    user_token = login_body["authorization"]

    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": user_token})

    cart_body = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}
    cart_resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": user_token},
        data=json.dumps(cart_body, ensure_ascii=False),
    )
    assert_that(cart_resp.status).is_equal_to(201)

    delete_resp = api_request.delete(f"/produtos/{product_id}", headers={"Authorization": admin_token})
    assert_that(delete_resp.status).is_equal_to(400)

    delete_body = parse_response_body(delete_resp)
    assert_that(delete_body["message"]).is_equal_to("Não é permitido excluir produto que faz parte de carrinho")
    assert_that(delete_body.get("idCarrinhos")).is_not_none().is_not_empty()


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
    assert_that(login_resp.status).is_equal_to(200)

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

    assert_that(product_resp.status).is_equal_to(403)
    product_body = parse_response_body(product_resp)
    assert_that(product_body).snapshot()
