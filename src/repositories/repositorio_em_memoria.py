"""Repositório em memória, usado como 'repositório falso' nos testes."""
from src.repositories.base_repository import BaseRepository


class RepositorioEmMemoria(BaseRepository):
    """Guarda as entidades em um dicionário. Nada vai para disco."""

    def __init__(self):
        """Cria o repositório vazio."""
        self._itens = {}

    def salvar(self, entidade):
        """Guarda ou atualiza a entidade."""
        self._itens[entidade.id] = entidade
        return entidade

    def buscar_por_id(self, id):
        """Devolve a entidade ou None."""
        return self._itens.get(id)

    def listar(self):
        """Devolve todas as entidades."""
        return list(self._itens.values())

    def remover(self, id):
        """Remove a entidade. Devolve True se existia."""
        return self._itens.pop(id, None) is not None