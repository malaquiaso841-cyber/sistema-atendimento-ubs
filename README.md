# SRU — Saúde Regional Unificada

Sistema de atendimento para Unidades Básicas de Saúde (UBS), feito em Python com Programação Orientada a Objetos.

Projeto da disciplina de POO (ES0008) — Universidade Federal do Cariri (UFCA).

---

## Sobre o projeto

Hoje, as informações de um paciente na UBS costumam ficar espalhadas em papéis e registros diferentes. Isso dificulta o atendimento, gera retrabalho e faz o paciente repetir o mesmo histórico a cada visita.

O **SRU** reúne em um só sistema os dados de pacientes, profissionais de saúde, agendamentos, prontuários e medicamentos de uma UBS, para facilitar o acesso à informação e organizar o fluxo de atendimento.

### Problemas que o sistema resolve

- Falta de acesso rápido ao histórico e ao prontuário do paciente.
- Falta de controle sobre agendamentos, triagem e prioridade de atendimento.
- Dificuldade de controlar a emissão de receitas, exames e encaminhamentos.
- Falta de controle do estoque de medicamentos e das reservas feitas pelos pacientes.

### Quem usa o sistema

| Perfil | O que faz |
|---|---|
| **Paciente** | Solicita e cancela agendamentos, reserva medicamentos e acompanha seus dados |
| **Atendente** (recepção e farmácia) | Confirma agendamentos, cadastra medicamentos e dá baixa nas reservas |
| **Médico** | Atende, emite receitas, pede exames e faz encaminhamentos |
| **Enfermeiro** | Faz o acolhimento e registra a triagem com classificação de risco |

---

## Funcionalidades

- Cadastro e autenticação de usuários, com painel diferente para cada perfil.
- Agendamento de consultas, inclusive visitas domiciliares para pacientes com mobilidade reduzida.
- Triagem com classificação de risco, que define a prioridade do atendimento.
- Prontuário com alergias, vacinas e histórico de documentos clínicos.
- Emissão de receitas, solicitações de exame e encaminhamentos para especialistas.
- Controle de estoque de medicamentos (lote e validade) e reserva para retirada.

### Regras de negócio

- Só médicos emitem receitas e só enfermeiros registram a triagem.
- A prioridade do atendimento depende da classificação de risco, da idade e da mobilidade reduzida do paciente.
- O agendamento segue estados (solicitado, confirmado, concluído, cancelado) e não aceita conflito de horário nem cancelamento fora do prazo.
- A reserva de medicamento só é aceita com estoque disponível, receita dentro da validade e lote não vencido.
- O prontuário avisa quando um medicamento conflita com uma alergia registrada.

---

## Estrutura de pastas

```
sistema-atendimento-ubs/
├── .gitignore
├── LICENSE
├── README.md
├── data/                          # arquivos de dados (persistência em JSON)
│   └── .gitkeep
├── docs/
│   ├── diagrama-classes.png       # diagrama UML de classes
│   └── proposta-projeto.md        # documento de planejamento do projeto
├── src/
│   ├── __init__.py
│   ├── main.py                    # ponto de entrada do sistema
│   ├── exceptions/                # exceções de domínio
│   │   ├── agendamento_exception.py
│   │   ├── autenticacao_exception.py
│   │   └── farmacia_exception.py
│   ├── models/                    # classes de domínio
│   │   ├── clinica/
│   │   │   ├── agendamento.py
│   │   │   ├── prontuario.py
│   │   │   ├── triagem.py
│   │   │   └── unidade_saude.py
│   │   ├── documentos/
│   │   │   ├── documento_clinico.py
│   │   │   ├── encaminhamento.py
│   │   │   ├── receita_medica.py
│   │   │   └── solicitacao_exame.py
│   │   ├── farmacia/
│   │   │   ├── medicamento.py
│   │   │   └── reserva_medicamento.py
│   │   └── usuarios/
│   │       ├── atendente.py
│   │       ├── enfermeiro.py
│   │       ├── medico.py
│   │       ├── paciente.py
│   │       ├── profissional_saude.py
│   │       └── usuario.py
│   ├── repositories/              # acesso e armazenamento dos dados
│   │   ├── agendamento_repository.py
│   │   ├── farmacia_repository.py
│   │   ├── persistencia_json.py
│   │   └── usuario_repository.py
│   └── services/                  # regras de negócio
│       ├── agendamento_service.py
│       ├── atendimento_service.py
│       ├── auth_service.py
│       └── farmacia_service.py
└── tests/
    └── __init__.py
```

### O que cada pasta faz

| Pasta | Responsabilidade |
|---|---|
| `src/models/` | Classes de domínio, separadas por área: `usuarios`, `clinica`, `documentos` e `farmacia` |
| `src/services/` | Regras de negócio. Recebem os repositórios por parâmetro |
| `src/repositories/` | Isolam o armazenamento dos dados (hoje em JSON, na pasta `data/`) |
| `src/exceptions/` | Erros próprios do sistema, sem misturar validação com interface |
| `data/` | Onde ficam os arquivos de dados gerados pelo sistema |
| `docs/` | Proposta do projeto e diagrama UML |
| `tests/` | Testes do sistema |

---

## Modelo de domínio

O modelo tem **16 classes de domínio**:

`Usuario`, `Paciente`, `Atendente`, `ProfissionalSaude`, `Medico`, `Enfermeiro`, `UnidadeSaude`, `Agendamento`, `Triagem`, `Prontuario`, `DocumentoClinico`, `ReceitaMedica`, `SolicitacaoExame`, `Encaminhamento`, `Medicamento` e `ReservaMedicamento`.

O diagrama completo está em [`docs/diagrama-classes.png`](docs/diagrama-classes.png).

### Hierarquias

**Usuários**
```
Usuario (abstrata)
├── Paciente
├── Atendente
└── ProfissionalSaude (abstrata)
    ├── Medico
    └── Enfermeiro
```

**Documentos clínicos**
```
DocumentoClinico (abstrata)
├── ReceitaMedica
├── SolicitacaoExame
└── Encaminhamento
```

**Exceções**
```
Exception
├── AutenticacaoException   # login inválido, conta inativa, acesso não autorizado
├── AgendamentoException    # conflito de horário, status inválido, cancelamento fora do prazo
└── FarmaciaException       # estoque zerado, receita vencida, lote vencido
```

### Relacionamentos

- **Composição:** `Paciente` 1 — 1 `Prontuario` e `Agendamento` 1 — 0..1 `Triagem` (o filho não existe sem o pai).
- **Agregação:** `Prontuario` 1 — 0..* `DocumentoClinico` e `UnidadeSaude` 1 — 0..* `Medicamento` (o filho existe sozinho).
- **Associações:** `Paciente` solicita `Agendamento`; `ProfissionalSaude` atende `Agendamento`; `UnidadeSaude` sedia `Agendamento`; `Paciente` realiza `ReservaMedicamento`; `ReservaMedicamento` refere-se a `Medicamento`; `Medico` emite `DocumentoClinico`.

### Polimorfismo

O fluxo principal trata os objetos pela abstração, e cada classe concreta se comporta do seu jeito:

- `exibirPainel()` em cada tipo de usuário.
- `realizarProcedimento()` em cada profissional de saúde.
- `gerarResumo()` em cada documento clínico.

---

## Padrões de projeto

| Padrão | Onde é usado |
|---|---|
| **Strategy** | Cálculo de prioridade do atendimento (`Triagem.calcularPrioridade()`). Cada critério de risco é uma estratégia separada |
| **Factory Method** | `UsuarioFactory` (cria paciente, atendente, médico ou enfermeiro) e `DocumentoClinicoFactory` (cria receita, exame ou encaminhamento) |
| **Observer** | Notificações quando um agendamento é confirmado, cancelado ou reagendado, e quando uma reserva de medicamento está perto de expirar |
| **Repository** | Pasta `src/repositories/`, que isola o armazenamento dos dados da regra de negócio |

---

## Princípios SOLID

- **S (Responsabilidade Única):** cada classe cuida de uma coisa só. Regras ficam nos `services`, dados nos `repositories`, erros nas `exceptions`.
- **O (Aberto/Fechado):** para um novo tipo de documento (ex.: `AtestadoMedico`), basta criar uma subclasse de `DocumentoClinico`. Para uma nova regra de prioridade, basta criar uma nova estratégia.
- **L (Substituição de Liskov):** `Medico` e `Enfermeiro` funcionam onde se espera um `ProfissionalSaude`. O `Prontuario` guarda qualquer `DocumentoClinico` e chama `gerarResumo()` sem saber o tipo.
- **I (Segregação de Interfaces):** contratos pequenos, como `Notificavel` e `Priorizavel`, feitos como classes abstratas (ABC).
- **D (Inversão de Dependência):** os `services` recebem o repositório por parâmetro, em vez de criá-lo dentro de si. Isso facilita trocar o armazenamento e testar com repositórios falsos.


## Equipe — SRU

| Integrante | GitHub |
|---|---|
| Pedro Kauan Cardoso da Silva | [@DevPKauan01](https://github.com/DevPKauan01) |
| Ramona Vitoria Clemente Cardoso | [@ramona-dev](https://github.com/ramona-dev) |
| José Welton de Sousa Melo | [@jweltu](https://github.com/jweltu) |
| Grazielly Bibiano do Nascimento | [@graziellybn](https://github.com/graziellybn) |
| Malaquias de Oliveira Nascimento | [@omalaquias285-dev](https://github.com/omalaquias285-dev) |

---

