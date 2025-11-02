import logging
import os
import subprocess

from pydantic import BaseModel


class AtpRunScriptConfig(BaseModel):
    run: str  # TODO: validate len(run) > 0
    name: str | None = None
    # description: str | None = None
    environment: dict[str, str] | None = None
    env_file: list[str] | None = None
    # dot_env_group: str | None = None
    # uv_group


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

    def _command_run(self) -> None:
        command: str = self.script.run
        if len(command) <= 0:
            raise ValueError("No 'run' is empty")
        subprocess.run(
            args=command,
            shell=True,
        )
        return None

    def run(self) -> None:
        self._export_env_var_from_files()
        self._export_env_var()
        self._command_run()

        return None
