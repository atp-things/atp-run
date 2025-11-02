import logging
import os
import subprocess

from pydantic import BaseModel


class AtpRunScriptConfig(BaseModel):
    run: str
    environment: dict[str, str] | None = None
    env_file: list[str] | None = None
    dotenv_group: str | None = None


def _export_env_var_from_file(file_path: str) -> None:
    if not os.path.exists(file_path):
        logging.warning(f"Env file '{file_path}' does not exist.")
        return None

    with open(file_path) as f:
        for line in f:
            # if line is empty or a comment, skip
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            key, _, value = line.partition("=")
            if len(key) > 0 and len(value) > 0:
                os.environ[key] = value

    return None


class AtpRunScript:
    def __init__(self, name: str, script: AtpRunScriptConfig) -> None:
        self.name: str = name
        self.script: AtpRunScriptConfig = script
        return None

    def _export_env_var(self) -> None:
        if self.script.environment is not None:
            for key, value in self.script.environment.items():
                os.environ[key] = value
        return None

    def _export_env_var_from_files(self) -> None:
        if self.script.env_file is not None:
            for file in self.script.env_file:
                _export_env_var_from_file(file)
        return None

    def _export_env_var_from_dotenv_group(self) -> None:
        if self.script.dotenv_group is None or len(self.script.dotenv_group) == 0:
            return None

        dotenv_files: list[str] = [
            ".env",
            ".env.local",
            f".env.{self.script.dotenv_group}",
            f".env.{self.script.dotenv_group}.local",
        ]

        for file in dotenv_files:
            _export_env_var_from_file(file)
        return None

    def _command_run(self) -> None:
        command: str = self.script.run
        if len(command) <= 0:
            raise ValueError("No 'run' is empty")
        subprocess.run(
            args=command,
            shell=True,
        )
        return None

    def _script_validate(self) -> None:
        # `run` - validation
        if len(self.script.run) == 0:
            raise ValueError("Script 'run' cannot be empty")

        # dotenv_group can not be empty string
        if self.script.dotenv_group is not None and len(self.script.dotenv_group) == 0:
            raise ValueError("If 'dotenv_group' is set, it cannot be an empty string")

        # Coexistence validation
        if self.script.env_file is not None and self.script.dotenv_group is not None:
            raise ValueError(
                "Cannot use both 'env_file' and 'dotenv_group' in the same script"
            )

        return None

    def run(self) -> None:
        self._script_validate()
        self._export_env_var_from_dotenv_group()
        self._export_env_var_from_files()
        self._export_env_var()
        self._command_run()

        return None
