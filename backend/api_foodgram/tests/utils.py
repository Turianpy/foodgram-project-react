from http import HTTPStatus


def assert_url_exists(response, url) -> None:
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f"Endpoint {url} not found, check urls.py"
    )


def check_pagination(url, response_json) -> None:
    expected_keys = ('count', 'next', 'previous', 'results')
    assert all(key in response_json for key in expected_keys), (
        f'Проверьте, что при GET запросе на {url} '
        'возвращается корректный ответ с пагинацией'
    )
    assert isinstance(response_json['results'], list), (
        f'Проверьте, что при GET запросе на {url} '
        'под ключем results возвращается список объектов'
    )
