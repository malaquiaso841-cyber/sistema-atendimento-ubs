"""Contrato de acesso a dados do sistema."""
from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """Contrato que todo repositório deve seguir.

    As regras de negócio dependem desta classe, e não de onde os
    dados ficam guardados (memória, JSON ou banco).
    A entidade precisa ter o atributo `id`.
    """

    @abstractmethod
    def salvar(self, entidade):
        """Guarda a entidade (cria nova ou atualiza se o id já existe)."""

    @abstractmethod
    def buscar_por_id(self, id):
        """Devolve a entidade com esse id, ou None se não existir."""

    @abstractmethod
    def listar(self):
        """Devolve a lista de todas as entidades."""

    @abstractmethod
    def remover(self, id):
        """Remove pelo id. Devolve True se removeu, False se não achou."""