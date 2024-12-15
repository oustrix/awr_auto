from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    input_directory_path: str
    output_directory_path: str

    cst_python_libs_path: str


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
