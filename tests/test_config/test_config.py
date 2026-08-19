from pathlib import Path

from omegaconf import OmegaConf

from plan2eplus.eppaths.logic import EpPaths
from plan2eplus.paths import Constants


def expected_install_path(env: str):
    config = OmegaConf.load(Constants.config_path / f"{env}.yaml")
    return Path(config.path_to_ep_install)  # pyright: ignore[reportAttributeAccessIssue]


def test_dev_ep_paths(monkeypatch):
    monkeypatch.setenv("APP_ENV", "dev")
    ep_paths = EpPaths()
    assert ep_paths.config.path_to_ep_install == expected_install_path("dev")


def test_prod_ep_paths(monkeypatch):
    monkeypatch.setenv("APP_ENV", "prod")
    ep_paths = EpPaths()
    assert ep_paths.config.path_to_ep_install == expected_install_path("prod")
