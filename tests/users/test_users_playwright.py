import json
import re
import time

import allure
from playwright.sync_api import APIRequestContext

from tests.utils.api_utils import JSON_HEADERS, load_json_resource, parse_response_body, post_json, put_json
from tests.utils.faker_utils import random_email, random_name, random_password


@allure.severity(allure.severity_level.CRITICAL)
def test_ct01_list_all_users_and_validate_structure(api_request: APIRequestContext):
    resp = api_request.get("/usuarios")
    assert resp.status == 200

    body = parse_response_body(resp)
    quantidade = body["quantidade"]
    usuarios = body["usuarios"]

    assert quantidade > 0
    assert usuarios is not None
    assert len(usuarios) > 0

    for user in usuarios:
        assert "nome" in user
        assert "email" in user
        assert "password" in user
        assert "administrador" in user
        assert "_id" in user
        assert re.fullmatch(r".+@.+\..+", user["email"]) is not None


@allure.severity(allure.severity_level.CRITICAL)
def test_ct02_get_user_by_id(api_request: APIRequestContext):
    list_resp = api_request.get("/usuarios")
    assert list_resp.status == 200

    list_body = parse_response_body(list_resp)
    user_id = list_body["usuarios"][0]["_id"]

    get_resp = api_request.get(f"/usuarios/{user_id}")
    assert get_resp.status == 200

    user = parse_response_body(get_resp)
    assert user["_id"] == user_id
    assert user.get("nome") is not None
    assert user.get("email") is not None


@allure.severity(allure.severity_level.CRITICAL)
def test_ct03_create_user(api_request: APIRequestContext):
    email = random_email()
    name = random_name()
    password = random_password()

    payload = {
        "nome": name,
        "email": email,
        "password": password,
        "administrador": "true",
    }

    create_resp = post_json(api_request, "/usuarios", payload)
    assert create_resp.status == 201

    create_body = parse_response_body(create_resp)
    assert create_body["message"] == "Cadastro realizado com sucesso"
    assert create_body.get("_id") is not None

    new_user_id = create_body["_id"]
    get_resp = api_request.get(f"/usuarios/{new_user_id}")
    assert get_resp.status == 200

    user = parse_response_body(get_resp)
    assert user["nome"] == name
    assert user["email"] == email


@allure.severity(allure.severity_level.NORMAL)
def test_ct04_advanced_json_validations_with_filters(api_request: APIRequestContext):
    resp = api_request.get("/usuarios")
    assert resp.status == 200

    body = parse_response_body(resp)
    usuarios = body["usuarios"]

    admins = [user for user in usuarios if user.get("administrador") == "true"]
    assert len(admins) > 0

    for user in usuarios:
        assert user.get("email") is not None


@allure.severity(allure.severity_level.CRITICAL)
def test_ct05_duplicate_email_validation(api_request: APIRequestContext):
    duplicate_email = random_email()

    user1 = {
        "nome": "User 1",
        "email": duplicate_email,
        "password": "senha123",
        "administrador": "false",
    }

    first = post_json(api_request, "/usuarios", user1)
    assert first.status == 201

    user2 = {
        "nome": "User 2",
        "email": duplicate_email,
        "password": "anotherpassword",
        "administrador": "true",
    }

    second = post_json(api_request, "/usuarios", user2)
    assert second.status == 400

    second_body = parse_response_body(second)
    assert second_body["message"] == "Este email já está sendo usado"
    assert second_body.get("message") is not None


@allure.severity(allure.severity_level.NORMAL)
def test_ct06_validate_with_fuzzy_matching(api_request: APIRequestContext):
    resp = api_request.get("/usuarios?administrador=true")
    assert resp.status == 200

    body = parse_response_body(resp)
    quantidade = body["quantidade"]
    usuarios = body["usuarios"]

    assert quantidade >= 0
    for user in usuarios:
        assert user.get("nome") is not None
        assert user.get("email") is not None
        assert str(user.get("administrador")) == "true"


@allure.severity(allure.severity_level.NORMAL)
def test_ct07_conditional_validations_based_on_values(api_request: APIRequestContext):
    resp = api_request.get("/usuarios")
    assert resp.status == 200

    body = parse_response_body(resp)
    user = body["usuarios"][0]

    admin_flag = str(user.get("administrador"))
    assert admin_flag in {"true", "false"}

    email = user.get("email")
    password = user.get("password")
    assert email is not None and len(email) > 5
    assert password is not None and len(password) > 0


@allure.severity(allure.severity_level.NORMAL)
def test_ct08_validate_formats_with_regular_expressions(api_request: APIRequestContext):
    new_email = f"test.regex.{int(time.time() * 1000)}@example.com"

    user_data = {
        "nome": "Regex Test",
        "email": new_email,
        "password": "StrongPassword@123",
        "administrador": "false",
    }

    create_resp = post_json(api_request, "/usuarios", user_data)
    assert create_resp.status == 201

    create_body = parse_response_body(create_resp)
    user_id = create_body["_id"]

    get_resp = api_request.get(f"/usuarios/{user_id}")
    assert get_resp.status == 200

    user = parse_response_body(get_resp)

    assert re.fullmatch(r".+@.+\..+", user["email"]) is not None
    assert re.fullmatch(r"[A-Za-z\s]+", user["nome"]) is not None
    assert re.fullmatch(r"[A-Za-z0-9]+", user["_id"]) is not None


@allure.severity(allure.severity_level.MINOR)
def test_ct09_validate_absence_of_fields(api_request: APIRequestContext):
    resp = api_request.get("/usuarios")
    assert resp.status == 200

    body = parse_response_body(resp)
    assert body.get("error") is None
    assert body.get("errorMessage") is None

    user = body["usuarios"][0]
    assert "cpf" not in user
    assert "phone" not in user


@allure.severity(allure.severity_level.NORMAL)
def test_ct10_use_variables_for_dynamic_validations(api_request: APIRequestContext):
    expected_email = random_email()

    user_payload = load_json_resource("users/userPayload.json")
    user_payload["email"] = expected_email

    create_resp = api_request.post(
        "/usuarios",
        headers=JSON_HEADERS,
        data=json.dumps(user_payload, ensure_ascii=False),
    )
    assert create_resp.status == 201

    search_resp = api_request.get(f"/usuarios?email={expected_email}")
    assert search_resp.status == 200

    search_body = parse_response_body(search_resp)
    usuarios = search_body["usuarios"]
    assert len(usuarios) > 0
    found_user = usuarios[0]
    assert found_user["email"] == expected_email
    assert found_user.get("nome") is not None


@allure.severity(allure.severity_level.NORMAL)
def test_ct11_prepare_data_for_nested_object_validation(api_request: APIRequestContext):
    complex_email = random_email()

    complex_data = {
        "nome": "Complex User",
        "email": complex_email,
        "password": "senha123",
        "administrador": "true",
    }

    resp = post_json(api_request, "/usuarios", complex_data)
    assert resp.status == 201

    body = parse_response_body(resp)
    assert body.get("message") == "Cadastro realizado com sucesso"
    user_id = body.get("_id")
    assert user_id is not None
    assert len(user_id) > 10


@allure.severity(allure.severity_level.NORMAL)
def test_ct12_create_user_from_fixed_json_file(api_request: APIRequestContext):
    user_payload = load_json_resource("users/userPayload.json")
    user_payload["email"] = random_email()

    resp = api_request.post(
        "/usuarios",
        headers=JSON_HEADERS,
        data=json.dumps(user_payload, ensure_ascii=False),
    )

    assert resp.status == 201
    body = parse_response_body(resp)
    assert body["message"] == "Cadastro realizado com sucesso"
    assert body.get("_id") is not None


@allure.severity(allure.severity_level.CRITICAL)
def test_ct13_create_and_delete_user_based_on_json_payload(api_request: APIRequestContext):
    expected_email = random_email()
    user_payload = load_json_resource("users/userPayload.json")
    user_payload["email"] = expected_email

    create_resp = api_request.post(
        "/usuarios",
        headers=JSON_HEADERS,
        data=json.dumps(user_payload, ensure_ascii=False),
    )
    assert create_resp.status == 201

    create_body = parse_response_body(create_resp)
    assert create_body["message"] == "Cadastro realizado com sucesso"
    user_id = create_body["_id"]

    delete_resp = api_request.delete(f"/usuarios/{user_id}")
    assert delete_resp.status == 200
    delete_body = parse_response_body(delete_resp)
    assert delete_body["message"] == "Registro excluído com sucesso"

    search_resp = api_request.get(f"/usuarios?email={expected_email}")
    assert search_resp.status == 200
    search_body = parse_response_body(search_resp)
    assert search_body["quantidade"] == 0


@allure.severity(allure.severity_level.CRITICAL)
def test_ct14_prevent_deleting_user_that_has_associated_cart(api_request: APIRequestContext):
    user_email = random_email()
    user_password = "SenhaSegura@123"

    user_data = {
        "nome": "User With Cart",
        "email": user_email,
        "password": user_password,
        "administrador": "true",
    }

    create_user_resp = post_json(api_request, "/usuarios", user_data)
    assert create_user_resp.status == 201

    create_user_body = parse_response_body(create_user_resp)
    assert create_user_body["message"] == "Cadastro realizado com sucesso"
    user_id = create_user_body["_id"]

    login_resp = post_json(api_request, "/login", {"email": user_email, "password": user_password})
    assert login_resp.status == 200

    login_body = parse_response_body(login_resp)
    user_token = login_body["authorization"]

    product_data = {
        "nome": f"Product for user cart {int(time.time() * 1000)}",
        "preco": 100,
        "descricao": "Product associated to user cart",
        "quantidade": 5,
    }

    product_resp = api_request.post(
        "/produtos",
        headers={**JSON_HEADERS, "Authorization": user_token},
        data=json.dumps(product_data, ensure_ascii=False),
    )
    assert product_resp.status == 201

    product_body = parse_response_body(product_resp)
    product_id = product_body["_id"]

    api_request.delete("/carrinhos/cancelar-compra", headers={"Authorization": user_token})

    cart_body = {"produtos": [{"idProduto": product_id, "quantidade": 1}]}
    cart_resp = api_request.post(
        "/carrinhos",
        headers={**JSON_HEADERS, "Authorization": user_token},
        data=json.dumps(cart_body, ensure_ascii=False),
    )
    assert cart_resp.status == 201

    delete_resp = api_request.delete(f"/usuarios/{user_id}")
    assert delete_resp.status == 400

    delete_body = parse_response_body(delete_resp)
    assert delete_body["message"] == "Não é permitido excluir usuário com carrinho cadastrado"
    assert delete_body.get("idCarrinho") is not None


@allure.severity(allure.severity_level.CRITICAL)
def test_ct15_get_user_by_invalid_id_should_return_400(api_request: APIRequestContext):
    resp = api_request.get("/usuarios/3F7K9P2XQ8M1R6TB")
    assert resp.status == 400

    body = parse_response_body(resp)
    assert body["message"] == "Usuário não encontrado"


@allure.severity(allure.severity_level.CRITICAL)
def test_ct16_prevent_updating_user_with_duplicate_email(api_request: APIRequestContext):
    email1 = random_email()
    email2 = random_email()

    user1 = {
        "nome": "User One",
        "email": email1,
        "password": "Senha123@",
        "administrador": "false",
    }
    user2 = {
        "nome": "User Two",
        "email": email2,
        "password": "Senha456@",
        "administrador": "true",
    }

    create_user1_resp = post_json(api_request, "/usuarios", user1)
    assert create_user1_resp.status == 201

    create_user1_body = parse_response_body(create_user1_resp)
    user_id1 = create_user1_body["_id"]

    post_json(api_request, "/usuarios", user2)

    update_payload = {
        "nome": "User One Updated",
        "email": email2,
        "password": "Senha123@",
        "administrador": "true",
    }

    update_resp = put_json(api_request, f"/usuarios/{user_id1}", update_payload)
    assert update_resp.status == 400

    update_body = parse_response_body(update_resp)
    assert update_body["message"] == "Este email já está sendo usado"
