# Advanced Multi-Agent System

Um framework multi-agente avançado construído sobre o Microsoft AutoGen, com consciência arquitetural, validação em múltiplos estágios e segurança de nível empresarial.

## 🚀 Funcionalidades Principais

### Diferenciais Competitivos

1. **Consciência Arquitetural & Contexto Dinâmico**
   - Grafo de dependências em tempo real
   - Memória de Decisões Arquiteturais (ADRs)
   - Contexto cross-repo/monorepo

2. **Validação Multi-Camada & Auto-Cura**
   - Pipeline de validação em estágios (lint → test → security → perf)
   - Replay determinístico e debugging temporal
   - Geração auto-curativa de testes

3. **Segurança Granular & Sandboxing Político**
   - Sandbox com políticas por ferramenta
   - Guardrails de cadeia de suprimentos
   - Capacidades baseadas em intenção

4. **Eficiência & Roteamento Inteligente**
   - Roteamento tiered de modelos (barato vs. topo)
   - Cache semântico + prompting diferenciável
   - Geração incremental com patch-apply

5. **Colaboração Humano-IA Transparente**
   - Modo co-pilot baseado em intenção
   - Histórico git em linguagem natural
   - Loop de preferência com RLHF leve

6. **Propostas Únicas**
   - Architecture Debt Tracker
   - Cognitive Agent Profiles
   - Live Documentation Sync
   - Modo Compliance & Regulação

## 📦 Instalação

```bash
pip install -e .
```

Para desenvolvimento:

```bash
pip install -e ".[dev]"
```

## 🏗️ Arquitetura

### Agentes Disponíveis

| Agente | Responsabilidade |
|--------|------------------|
| `PlannerAgent` | Análise de requisitos e decomposição de tarefas |
| `CoderAgent` | Geração e edição de código |
| `ReviewerAgent` | Revisão de código e garantia de qualidade |
| `TesterAgent` | Geração e execução de testes |
| `GitAgent` | Operações de versionamento |
| `ComplianceAgent` | Validação de segurança e conformidade |
| `ArchitectureLedgerAgent` | Gestão de decisões arquiteturais |

### Estrutura do Projeto

```
src/
├── agents/           # Implementações dos agentes
│   ├── base.py       # Classe base abstrata
│   ├── planner.py    # Agente planejador
│   ├── coder.py      # Agente codificador
│   ├── reviewer.py   # Agente revisor
│   ├── tester.py     # Agente testador
│   └── ...
├── orchestration/    # Gerenciamento de conversas multi-agente
├── memory/           # Sistema de memória e ADRs
├── tools/            # Ferramentas utilitárias
└── validators/       # Validadores multi-estágio
```

## 🔧 Uso Básico

```python
from src.agents import PlannerAgent, CoderAgent, ReviewerAgent
from src.orchestration import GroupChatManager

# Configurar agentes
planner = PlannerAgent(llm_config={"model": "gpt-4"})
coder = CoderAgent(llm_config={"model": "gpt-4"})
reviewer = ReviewerAgent(llm_config={"model": "gpt-4"})

# Criar gerenciador de grupo
manager = GroupChatManager(
    agents=[planner, coder, reviewer],
    max_rounds=10
)

# Executar tarefa
result = manager.run("Crie uma função que calcula fibonacci")
print(result["messages"])
```

## 🛡️ Segurança

O sistema implementa múltiplas camadas de segurança:

- **Sandboxing**: Execução de código em containers Docker isolados
- **Políticas de Acesso**: Permissões granulares por ferramenta
- **Compliance**: Verificação de licenças e vulnerabilidades
- **Audit Trail**: Log completo de todas as decisões e ações

## 📊 Roadmap

### Fase 1: Fundação ✅
- [x] Estrutura básica do projeto
- [x] Agentes fundamentais
- [x] Orquestração multi-agente

### Fase 2: Validação
- [ ] Pipeline de validação multi-estágio
- [ ] Integração com linters e test frameworks
- [ ] Security scanning com semgrep

### Fase 3: Otimização
- [ ] Roteamento tiered de modelos
- [ ] Cache semântico
- [ ] Geração incremental de patches

### Fase 4: Diferenciais
- [ ] Architecture Debt Tracker
- [ ] Cognitive Agent Profiles
- [ ] Live Documentation Sync

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o repositório
2. Crie um branch para sua feature (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para o branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

## 📄 Licença

MIT License - veja o arquivo LICENSE para detalhes.

## 🙏 Agradecimentos

- Microsoft AutoGen pela base do framework
- Comunidade open-source pelas ferramentas integradas
