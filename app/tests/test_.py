import requests

from config import API_URL


def test_get_user(create_user):
    print(create_user["id"])
    response = requests.get(f'{API_URL}/users/{create_user["id"]}/')
    print(response.json())
    assert response.status_code == 200
    assert create_user["email"] == response.json()["email"]


def test_post_adv(create_user, title="test_title", descr="test_descr"):
    params = {
        "title": title,
        "descr": descr,
        "user_id": create_user["id"],
        "password": "password",
    }
    response = requests.post(f"{API_URL}/adv/", json=params)
    resp = requests.get(f"{API_URL}/adv/{response.json()['id']}/")
    assert response.status_code == 200
    assert resp.json()["title"] == title


def test_get_adv():
    response = requests.get(f"{API_URL}/adv/1/")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_patch_adv(
    adv_id=1, title="alt_title", descr="alt_descr", user_id=2, password="password"
):
    params = {"title": title, "descr": descr, "user_id": user_id, "password": password}
    response = requests.patch(f"{API_URL}/adv/{adv_id}/", json=params)
    assert response.status_code == 200
    assert response.json()["descr"] == descr


def test_patch_adv_wrong_user(
    adv_id=1, title="alt_title", descr="alt_descr", user_id=1, password="password"
):
    params = {"title": title, "descr": descr, "user_id": user_id, "password": password}
    response = requests.patch(f"{API_URL}/adv/{adv_id}/", json=params)
    assert response.status_code == 401


def test_delete_adv_wrong_psw(adv_id=1, user_id=2, password="123"):
    params = {"user_id": user_id, "password": password}
    response = requests.delete(f"{API_URL}/adv/{adv_id}/", json=params)
    assert response.status_code == 401


def test_delete_adv(adv_id=1, user_id=2, password="password"):
    params = {"user_id": user_id, "password": password}
    response = requests.delete(f"{API_URL}/adv/{adv_id}/", json=params)
    assert response.status_code == 200
