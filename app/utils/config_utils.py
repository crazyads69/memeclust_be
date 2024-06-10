from os import getenv
from typing import Optional

import dotenv
from hydra import compose, initialize
from omegaconf import DictConfig, OmegaConf, open_dict

dotenv.load_dotenv()


def parse_value(value):
    """
    A helper function that tries to parse a value as an integer, float or boolean.
    If the value cannot be parsed, returns the original value.
    """
    if isinstance(value, str):
        _value = value.strip().lower()
        if _value == "true":
            return True
        elif _value == "false":
            return False
        else:
            try:
                return int(_value)
            except ValueError:
                pass
            try:
                return float(_value)
            except ValueError:
                pass
    return value


def env_resolver(key: str):
    value = getenv(key, None)
    if value is None:
        raise ValueError(f"environment variable '{key}' not found")
    return parse_value(value)


OmegaConf.register_new_resolver("env", env_resolver)


def get_config(module_name: Optional[str] = None) -> DictConfig:
    with initialize(config_path="../config", version_base="1.1"):
        config = compose("app.yaml")

        # Ensure environment variables are set
        with open_dict(config):
            container = OmegaConf.to_container(config, resolve=True)
            if container is None:
                raise ValueError("Config is not a valid OmegaConf object")
            for key in container:
                if str(key).startswith("env:") and not getenv(str(key)[4:], None):
                    raise ValueError(f"Environment variable '{str(key)[4:]}' not found")

        if module_name:
            module_config = config.get(module_name, {})
            return module_config
        else:
            return config
