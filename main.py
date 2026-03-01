from agno.agent import Agent
from dotenv import load_dotenv
from agno.db.sqlite import SqliteDb
import os
from typing import List
import pathlib
import fnmatch

load_dotenv()

db = SqliteDb("db.sqlite")
BASE_PATH = os.getenv("BASE_PATH", "/home")


def get_path(path: str):
    return os.path.join(BASE_PATH, path)


def list_files(path):
    ignore_patterns = [".*", ".env", ".venv", "__pycache__", "*.bak"]
    base_path = pathlib.Path(get_path(path))
    visible_files = []

    for item in base_path.iterdir():
        # Ignore arquivos do padrão ignorado
        should_ignore = any(
            fnmatch.fnmatch(item.name, pattern) for pattern in ignore_patterns
        )

        if not should_ignore:
            visible_files.append(item.name)

    return sorted(visible_files)


def read_code(file_list: List[str]):
    combined_content = []
    separator = "\n" + "=" * 20 + "\n"

    for file_path in file_list:
        path = pathlib.Path(get_path(file_path))
        if path.is_file():
            try:
                content = path.read_text(encoding="utf-8")
                # Crie um cabeçalho para facilitar a separação dos arquivos
                header = f"--- FILE: {path.name} ---\n"
                combined_content.append(header + content)
            except Exception as e:
                combined_content.append(f"--- ERROR READING {path.name}: {e} ---")
        else:
            combined_content.append(f"--- WARNING: {path.name} not found ---")

    return separator.join(combined_content)


def write_file(filepath: str, content: str):
    with open(get_path(filepath), "w+", encoding="utf-8") as f:
        f.write(content)


instructions = """
Você é um assistente pessoal que consegue acessar certas pastas do computador pessoal e pode interagir com o mesmo.
A primeira informação que você precisa é a pasta que será usada. Salve esta informação para usar em outras ações.
Nunca inicie qualquer ação sem ter a pasta do projeto. Toda ação deve ocorrer dentro desta pasta, sem exceção.
Sempre use caminho absoluto a partir da pasta do projeto escolhido.
Exemplo: se for pedido o acesso a pasta abcd, execute sua ação passando como caminho abcd.
Se for pedido para acessar o arquivo abc.py, você deve passar o filepath abcd/abc.py
Execute ações apenas quando pedido explicitamente.
Você pode listar os arquivos de código de um determinado projeto.
Você pode ler o conteúdo de um ou mais arquivos. Neste caso, SEMPRE passe TODOS os caminhos em apenas UMA chamada, nunca uma chamada para cada caminho.
Você pode criar um arquivo com o conteúdo definido.
"""

agent = Agent(
    name="Well",
    model="openai:gpt-4.1-nano",
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    tools=[list_files, read_code, write_file],
    update_memory_on_run=True,
    instructions=instructions,
    debug_mode=True,
)

default_user = "john@doe.com"

if __name__ == "__main__":
    agent.cli_app(stream=True, debug_model=True, user_id=default_user)
