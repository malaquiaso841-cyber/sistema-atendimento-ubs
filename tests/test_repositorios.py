import tempfile
import unittest
from pathlib import Path

from src.repositories import persistencia_json
from src.repositories.base_repository import BaseRepository
from src.repositories.persistencia_json import RepositorioJson
from src.repositories.repositorio_em_memoria import RepositorioEmMemoria


class Pessoa:
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome


class PessoaRepositorio(RepositorioJson):
    def __init__(self):
        super().__init__("pessoas_teste.json")

    def _para_dict(self, entidade):
        return {"id": entidade.id, "nome": entidade.nome}

    def _de_dict(self, dados):
        return Pessoa(dados["id"], dados["nome"])


class TestBaseRepository(unittest.TestCase):
    def test_e_abstrata(self):
        with self.assertRaises(TypeError):
            BaseRepository()


class TestEmMemoria(unittest.TestCase):
    def test_crud(self):
        repo = RepositorioEmMemoria()
        repo.salvar(Pessoa(1, "Ana"))
        self.assertEqual(repo.buscar_por_id(1).nome, "Ana")
        self.assertEqual(len(repo.listar()), 1)
        self.assertTrue(repo.remover(1))
        self.assertFalse(repo.remover(1))
        self.assertIsNone(repo.buscar_por_id(1))


class TestJson(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self._original = persistencia_json.DATA_DIR
        persistencia_json.DATA_DIR = Path(self._tmp.name)
        self.repo = PessoaRepositorio()

    def tearDown(self):
        persistencia_json.DATA_DIR = self._original
        self._tmp.cleanup()

    def test_arquivo_inexistente_devolve_lista_vazia(self):
        self.assertEqual(self.repo.listar(), [])

    def test_salva_e_recarrega(self):
        self.repo.salvar(Pessoa(1, "Ana"))
        self.repo.salvar(Pessoa(2, "Bia"))
        novo = PessoaRepositorio()  # simula reabrir o programa
        self.assertEqual([p.nome for p in novo.listar()], ["Ana", "Bia"])

    def test_atualiza_sem_duplicar(self):
        self.repo.salvar(Pessoa(1, "Ana"))
        self.repo.salvar(Pessoa(1, "Ana Maria"))
        self.assertEqual(len(self.repo.listar()), 1)
        self.assertEqual(self.repo.buscar_por_id(1).nome, "Ana Maria")

    def test_remover(self):
        self.repo.salvar(Pessoa(1, "Ana"))
        self.assertTrue(self.repo.remover(1))
        self.assertFalse(self.repo.remover(1))

    def test_arquivo_vazio(self):
        (persistencia_json.DATA_DIR / "pessoas_teste.json").write_text("")
        self.assertEqual(self.repo.listar(), [])

    def test_arquivo_corrompido(self):
        (persistencia_json.DATA_DIR / "pessoas_teste.json").write_text("{ruim")
        self.assertEqual(self.repo.listar(), [])


if __name__ == "__main__":
    unittest.main()