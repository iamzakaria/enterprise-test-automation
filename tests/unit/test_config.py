import pytest

from enterprise_qa.config import Settings


def test_local_defaults():
    assert Settings.from_env({}) == Settings("local", None, 5000)


@pytest.mark.parametrize("environment", ["qa", "staging"])
def test_remote_environment(environment):
    settings = Settings.from_env({"TEST_ENV": environment, "BASE_URL": "https://example.com"})
    assert settings.base_url == "https://example.com"
    assert settings.environment == environment


@pytest.mark.parametrize(
    "env",
    [
        {"TEST_ENV": "production"},
        {"TEST_ENV": "qa"},
        {"TEST_ENV": "staging"},
        {"BASE_URL": "file:///tmp/demo"},
        {"BASE_URL": "https://user:secret@example.com"},
        {"BASE_URL": "https://example.com?token=secret"},
        {"BASE_URL": "https://example.com:wrong"},
        {"UI_TIMEOUT_MS": "0"},
        {"UI_TIMEOUT_MS": "-1"},
        {"UI_TIMEOUT_MS": "invalid"},
    ],
)
def test_invalid_configuration_fails(env):
    with pytest.raises(ValueError):
        Settings.from_env(env)
