"""Leitura e gravação de arquivos JSON dentro da pasta data/."""
import json
import os
import shutil
from abc import abstractmethod
from pathlib import Path

from src.repositories.base_repository import BaseRepository

# raiz do projeto / data
DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def ler_json(nome_arquivo):
    """Lê a lista guardada no arquivo.

    Cria o arquivo se não existir. Arquivo vazio ou corrompido devolve
    lista vazia (o corrompido é copiado para '.corrompido' antes).
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    caminho = DATA_DIR / nome_arquivo

    if not caminho.exists():
        caminho.write_text("[]", encoding="utf-8")
        return []

    texto = caminho.read_text(encoding="utf-8").strip()
    if not texto:
        return []

    try:
        dados = json.loads(texto)
    except json.JSONDecodeError:
        shutil.copy(caminho, str(caminho) + ".corrompido")
        return []

    return dados if isinstance(dados, list) else []


def gravar_json(nome_arquivo, dados):
    """Grava a lista no arquivo (escreve num temporário e troca)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    caminho = DATA_DIR / nome_arquivo
    temporario = Path(str(caminho) + ".tmp")
    temporario.write_text(
        json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    os.replace(temporario, caminho)


class RepositorioJson(BaseRepository):
    """Base para repositórios que guardam em JSON.

    Cada repositório concreto diz como converter a entidade em
    dicionário (`_para_dict`) e de volta (`_de_dict`).
    O dicionário precisa ter a chave "id".
    """

    def __init__(self, nome_arquivo):
        """`nome_arquivo` é só o nome, ex.: 'usuarios.json'."""
        self._arquivo = nome_arquivo

    @abstractmethod
    def _para_dict(self, entidade):
        """Converte a entidade em dicionário."""

    @abstractmethod
    def _de_dict(self, dados):
        """Converte o dicionário de volta em entidade."""

    def salvar(self, entidade):
        """Cria ou atualiza a entidade no arquivo."""
        dados = ler_json(self._arquivo)
        novo = self._para_dict(entidade)
        for i, item in enumerate(dados):
            if item.get("id") == entidade.id:
                dados[i] = novo
                break
        else:
            dados.append(novo)
        gravar_json(self._arquivo, dados)
        return entidade

    def buscar_por_id(self, id):
        """Devolve a entidade ou None."""
        for item in ler_json(self._arquivo):
            if item.get("id") == id:
                return self._de_dict(item)
        return None

    def listar(self):
        """Devolve todas as entidades."""
        return [self._de_dict(item) for item in ler_json(self._arquivo)]

    def remover(self, id):
        """Remove pelo id. Devolve True se removeu."""
        dados = ler_json(self._arquivo)
        restantes = [item for item in dados if item.get("id") != id]
        if len(restantes) == len(dados):
            return False
        gravar_json(self._arquivo, restantes)
        return True