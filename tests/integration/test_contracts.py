def test_service_contract_placeholders() -> None:
    expected_services = {"web-dashboard", "api-java", "ml-python", "matcher-cpp"}

    assert "api-java" in expected_services
    assert "ml-python" in expected_services

