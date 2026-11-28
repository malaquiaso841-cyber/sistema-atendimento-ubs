"""Paciente: o cidadão atendido na UBS."""
from datetime import date

from src.models.usuarios.usuario import Usuario


class Paciente(Usuario):
    """Usuário que solicita agendamentos e reserva medicamentos.

    Os métodos que dependem de services recebem o service por parâmetro
    (Inversão de Dependência), sem importar a camada de cima.
    """

    def __init__(self, id, cpf, nome, telefone, cartao_sus, data_nascimento,
                 endereco, mobilidade_reduzida=False, senha=None,
                 senha_hash=None, ativo=True, prontuario=None):
        """Cria um paciente. `prontuario` é opcional (composição, Issue 7)."""
        super().__init__(id, cpf, nome, telefone, senha, senha_hash, ativo)
        self.cartao_sus = cartao_sus
        self.data_nascimento = data_nascimento
        self._endereco = endereco
        self._mobilidade_reduzida = bool(mobilidade_reduzida)
        self._prontuario = prontuario

    # ---------- propriedades ----------
    @property
    def cartao_sus(self):
        """Cartão do SUS (15 dígitos)."""
        return self._cartao_sus

    @cartao_sus.setter
    def cartao_sus(self, valor):
        digitos = "".join(c for c in str(valor) if c.isdigit())
        if len(digitos) != 15:
            raise ValueError("Cartão SUS deve ter 15 dígitos.")
        self._cartao_sus = digitos

    @property
    def data_nascimento(self):
        """Data de nascimento (objeto date)."""
        return self._data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, valor):
        if isinstance(valor, str):
            try:
                valor = date.fromisoformat(valor)
            except ValueError:
                raise ValueError("Data deve estar no formato AAAA-MM-DD.")
        if not isinstance(valor, date):
            raise ValueError("Data de nascimento inválida.")
        if valor > date.today():
            raise ValueError("Data de nascimento não pode ser no futuro.")
        self._data_nascimento = valor

    @property
    def endereco(self):
        """Endereço do paciente."""
        return self._endereco

    @endereco.setter
    def endereco(self, valor):
        self._endereco = valor

    @property
    def mobilidade_reduzida(self):
        """True se o paciente tem mobilidade reduzida."""
        return self._mobilidade_reduzida

    @property
    def prontuario(self):
        """Prontuário do paciente (pode ser None até a Issue 7)."""
        return self._prontuario

    @prontuario.setter
    def prontuario(self, valor):
        self._prontuario = valor

    # ---------- comportamento ----------
    def calcular_idade(self, hoje=None):
        """Idade em anos completos (considera se já fez aniversário)."""
        hoje = hoje or date.today()
        nasc = self._data_nascimento
        fez_aniversario = (hoje.month, hoje.day) >= (nasc.month, nasc.day)
        return hoje.year - nasc.year - (0 if fez_aniversario else 1)

    def solicitar_agendamento(self, agendamento_service, data_hora,
                              tipo="consulta", visita_domiciliar=False):
        """Pede um agendamento ao service. A regra é checada lá."""
        return agendamento_service.solicitar(
            self, data_hora, tipo, visita_domiciliar
        )

    def cancelar_agendamento(self, agendamento_service, agendamento):
        """Pede ao service o cancelamento de um agendamento."""
        return agendamento_service.cancelar(agendamento, self)

    def reservar_medicamento(self, farmacia_service, medicamento, receita):
        """Pede ao service a reserva de um medicamento."""
        return farmacia_service.reservar(self, medicamento, receita)

    def exibir_painel(self):
        """Resumo do painel do paciente (só texto, sem menu de terminal)."""
        return (
            f"Painel do Paciente: {self.nome}\n"
            f"Idade: {self.calcular_idade()} anos\n"
            "Ações: solicitar agendamento, cancelar agendamento, "
            "reservar medicamento"
        )