"""Superclasse abstrata de todos os perfis do sistema."""
import hashlib
import hmac
import os
import re
from abc import ABC, abstractmethod

_ITERACOES = 100_000


class Usuario(ABC):
    """Dados comuns e comportamento de acesso de qualquer usuário.

    Não conhece repositórios, serviços nem a interface de terminal.
    """

    def __init__(self, id, cpf, nome, telefone, senha=None,
                 senha_hash=None, ativo=True):
        """Cria um usuário.

        Informe `senha` (texto puro) ao cadastrar alguém novo, ou
        `senha_hash` ao recarregar um usuário já salvo (ex.: do JSON).
        """
        self._id = id
        self.cpf = cpf          # passa pelo setter (valida)
        self.nome = nome        # passa pelo setter (valida)
        self._telefone = telefone
        self._ativo = ativo

        if senha_hash is not None:
            self._senha_hash = senha_hash
        elif senha:
            self._senha_hash = self._gerar_hash(senha)
        else:
            raise ValueError("Informe a senha.")

    # ---------- propriedades ----------
    @property
    def id(self):
        """Identificador único do usuário."""
        return self._id

    @property
    def cpf(self):
        """CPF guardado só com os 11 dígitos."""
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        digitos = re.sub(r"\D", "", str(valor))
        if len(digitos) != 11:
            raise ValueError("CPF deve ter 11 dígitos numéricos.")
        self._cpf = digitos

    @property
    def nome(self):
        """Nome do usuário."""
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not str(valor).strip():
            raise ValueError("Nome não pode ser vazio.")
        self._nome = str(valor).strip()

    @property
    def telefone(self):
        """Telefone do usuário."""
        return self._telefone

    @telefone.setter
    def telefone(self, valor):
        self._telefone = valor

    @property
    def senha_hash(self):
        """Hash da senha (é o que vai para o JSON, nunca a senha pura)."""
        return self._senha_hash

    @property
    def ativo(self):
        """True se a conta está ativa."""
        return self._ativo

    # ---------- senha ----------
    @staticmethod
    def _gerar_hash(senha):
        """Gera 'salt:hash' em hexadecimal, com salt aleatório."""
        salt = os.urandom(16)
        hash_ = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, _ITERACOES)
        return f"{salt.hex()}:{hash_.hex()}"

    def _senha_confere(self, senha):
        """Confere se a senha bate com o hash guardado."""
        salt_hex, hash_hex = self._senha_hash.split(":")
        novo = hashlib.pbkdf2_hmac(
            "sha256", senha.encode(), bytes.fromhex(salt_hex), _ITERACOES
        )
        return hmac.compare_digest(novo.hex(), hash_hex)

    # ---------- comportamento ----------
    def autenticar(self, senha):
        """Retorna True se a senha estiver certa e a conta ativa."""
        if not self._ativo:
            return False
        return self._senha_confere(senha)

    def alterar_senha(self, senha_atual, nova_senha):
        """Troca a senha, exigindo a senha atual correta."""
        if not self._senha_confere(senha_atual):
            raise ValueError("Senha atual incorreta.")
        if not nova_senha:
            raise ValueError("A nova senha não pode ser vazia.")
        self._senha_hash = self._gerar_hash(nova_senha)

    def inativar_conta(self):
        """Inativa a conta do usuário."""
        self._ativo = False

    @abstractmethod
    def exibir_painel(self):
        """Devolve o texto do painel do perfil (cada perfil faz o seu)."""