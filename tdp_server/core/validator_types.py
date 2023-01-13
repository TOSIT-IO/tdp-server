from pathlib import Path

from pydantic import DirectoryPath


class ExistingDir(DirectoryPath):
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":  # type: ignore
        yield cls.validate_expanduser
        yield from DirectoryPath.__get_validators__()  # type: ignore

    @classmethod
    def validate_expanduser(cls, value: Path) -> Path:
        return Path(value).expanduser().resolve()
