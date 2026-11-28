"""Atendente: equipe de recepção e farmácia."""
import unicodedata

from src.models.usuarios.usuario import Usuario

SETORES = ("recepcao", "farmacia")


def _normalizar(texto):
    """Minúsculo e sem acento: 'Recepção' -> 'recepcao'."""
    sem_acento = unicodedata.normalize("NFD", str(texto))
    sem_acento = "".join(c for c in sem_acento
                         if unicodedata.category(c) != "Mn")
    return sem_acento.strip().lower()


class Atendente(Usuario):
    """Usuário administrativo que confirma agendamentos e cuida da farmácia."""

    def __init__(self, id, cpf, nome, telefone, matricula, setor,
                 senha=None, senha_hash=None, ativo=True):
        """Cria um atendente. `setor` é 'recepção' ou 'farmácia'."""
        super().__init__(id, cpf, nome, telefone, senha, senha_hash, ativo)
        self.matricula = matricula
        self.setor = setor

    @property
    def matricula(self):
        """Matrícula do atendente."""
        return self._matricula

    @matricula.setter
    def matricula(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("Matrícula não pode ser vazia.")
        self._matricula = str(valor).strip()

    @property
    def setor(self):
        """Setor: 'recepcao' ou 'farmacia'."""
        return self._setor

    @setor.setter
    def setor(self, valor):
        setor = _normalizar(valor)
        if setor not in SETORES:
            raise ValueError("Setor deve ser 'recepção' ou 'farmácia'.")
        self._setor = setor

    def confirmar_agendamento(self, agendamento_service, agendamento):
        """Pede ao service a confirmação de um agendamento."""
        return agendamento_service.confirmar(agendamento, self)

    def cadastrar_medicamento(self, farmacia_service, medicamento):
        """Pede ao service o cadastro de um medicamento."""
        return farmacia_service.cadastrar_medicamento(medicamento)

    def dar_baixa_reserva(self, farmacia_service, reserva):
        """Pede ao service a baixa de uma reserva (retirada)."""
        return farmacia_service.dar_baixa(reserva, self)

    def exibir_painel(self):
        """Resumo do painel do atendente (só texto, sem menu de terminal)."""
        return (
            f"Painel do Atendente: {self.nome} ({self.setor})\n"
            "Ações: confirmar agendamento, cadastrar medicamento, "
            "dar baixa em reserva"
        )