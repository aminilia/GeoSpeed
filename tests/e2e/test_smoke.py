def test_e2e_placeholder() -> None:
    user_journey = ["load dashboard", "inspect synthetic sign", "request prediction"]

    assert user_journey[0] == "load dashboard"
