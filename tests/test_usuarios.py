import unittest
from datetime import date

from src.models.usuarios.atendente import Atendente
from src.models.usuarios.paciente import Paciente
from src.models.usuarios.usuario import Usuario


def novo_paciente(**extra):
    dados = dict(id=1, cpf="123.456.789-09", nome="Ana", telefone="88999999999",
                 cartao_sus="123456789012345", data_nascimento=date(2000, 5, 10),
                 endereco="Rua A, 1", senha="segredo")
    dados.update(extra)
    return Paciente(**dados)


def novo_atendente(**extra):
    dados = dict(id=2, cpf="98765432100", nome="Bia", telefone="88988888888",
                 matricula="A-001", setor="recepção", senha="segredo")
    dados.update(extra)
    return Atendente(**dados)


class TestUsuario(unittest.TestCase):
    def test_usuario_e_abstrata(self):
        with self.assertRaises(TypeError):
            Usuario(1, "12345678909", "Ana", "8899", "123")

    def test_cpf_guarda_so_digitos(self):
        self.assertEqual(novo_paciente().cpf, "12345678909")

    def test_cpf_invalido(self):
        with self.assertRaises(ValueError):
            novo_paciente(cpf="123")

    def test_nome_vazio(self):
        with self.assertRaises(ValueError):
            novo_paciente(nome="  ")

    def test_setter_valida(self):
        p = novo_paciente()
        with self.assertRaises(ValueError):
            p.cpf = "abc"
        with self.assertRaises(ValueError):
            p.nome = ""

    def test_senha_nao_fica_em_texto_puro(self):
        p = novo_paciente()
        self.assertNotIn("segredo", p.senha_hash)

    def test_autenticar(self):
        p = novo_paciente()
        self.assertTrue(p.autenticar("segredo"))
        self.assertFalse(p.autenticar("errada"))

    def test_conta_inativa_nao_autentica(self):
        p = novo_paciente()
        p.inativar_conta()
        self.assertFalse(p.ativo)
        self.assertFalse(p.autenticar("segredo"))

    def test_alterar_senha(self):
        p = novo_paciente()
        with self.assertRaises(ValueError):
            p.alterar_senha("errada", "nova")
        p.alterar_senha("segredo", "nova")
        self.assertTrue(p.autenticar("nova"))
        self.assertFalse(p.autenticar("segredo"))

    def test_recarregar_com_hash(self):
        p = novo_paciente()
        copia = novo_paciente(senha=None, senha_hash=p.senha_hash)
        self.assertTrue(copia.autenticar("segredo"))


class TestPaciente(unittest.TestCase):
    def test_cartao_sus_invalido(self):
        with self.assertRaises(ValueError):
            novo_paciente(cartao_sus="123")

    def test_data_no_futuro(self):
        with self.assertRaises(ValueError):
            novo_paciente(data_nascimento=date(2999, 1, 1))

    def test_data_em_texto(self):
        self.assertEqual(novo_paciente(data_nascimento="2000-05-10")
                         .data_nascimento, date(2000, 5, 10))

    def test_idade_antes_do_aniversario(self):
        p = novo_paciente(data_nascimento=date(2000, 5, 10))
        self.assertEqual(p.calcular_idade(date(2026, 5, 9)), 25)

    def test_idade_no_aniversario(self):
        p = novo_paciente(data_nascimento=date(2000, 5, 10))
        self.assertEqual(p.calcular_idade(date(2026, 5, 10)), 26)

    def test_mobilidade_exposta(self):
        self.assertFalse(novo_paciente().mobilidade_reduzida)
        self.assertTrue(novo_paciente(mobilidade_reduzida=True).mobilidade_reduzida)

    def test_nao_tem_metodos_do_atendente(self):
        self.assertFalse(hasattr(novo_paciente(), "dar_baixa_reserva"))


class TestAtendente(unittest.TestCase):
    def test_setor_normalizado(self):
        self.assertEqual(novo_atendente(setor="Farmácia").setor, "farmacia")

    def test_setor_invalido(self):
        with self.assertRaises(ValueError):
            novo_atendente(setor="financeiro")

    def test_matricula_vazia(self):
        with self.assertRaises(ValueError):
            novo_atendente(matricula="")

    def test_nao_tem_metodos_do_paciente(self):
        self.assertFalse(hasattr(novo_atendente(), "reservar_medicamento"))

    def test_paineis_diferentes(self):
        self.assertNotEqual(novo_paciente().exibir_painel(),
                            novo_atendente().exibir_painel())


if __name__ == "__main__":
    unittest.main()