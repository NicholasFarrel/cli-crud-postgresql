# Relatório - CRUD e implementação de índice.

## Introdução

Este relatório traz uma visão geral do que foi implementado para o funcionamento de uma aplicação via terminal (CLI) que realiza operações CRUD (Create, Read, Update, Delete) em um banco de dados PostgreSQL. A aplicação foi desenvolvida em Python, utilizando a biblioteca `psycopg2` para a integração com o banco de dados.

Além das funções básicas de CRUD, foram implementados códigos auxiliares que permitem realizar uma análise comparativa de desempenho de buscas com e sem o uso de índices, explorando o funcionamento de `Index Scan` e `Seq Scan` através de planos de execução (`EXPLAIN ANALYZE`).

Para suportar essa análise, foram criados dois schemas distintos no banco de dados:

- `VerticalLife` — com índices aplicados às colunas de interesse;
- `VerticalLifeNoIdx` — sem índices, permitindo observar o comportamento da busca em um cenário não otimizado.

Ao longo do relatório, serão descritas as principais etapas de implementação, as adaptações realizadas para garantir suporte multi-schema, bem como os resultados obtidos na análise de desempenho.

## 1 Aplicação via terminal - CRUD `crudVerticalLife.py`
### 1.1 Funções de conexão e escolha de schema, tabela e coluna

#### `connect_db()`

**Objetivo:** Estabelece uma conexão com o banco de dados PostgreSQL.

**Tratamento de exceções:** Em caso de erro na conexão, exibe a mensagem e encerra o programa.

#### `choose_schema(cursor)`

**Objetivo:** Exibe um menu com os schemas disponíveis no banco de dados (exceto schemas internos) e permite que o usuário escolha um schema.

**Tratamento de exceções:** Inclui `try/except` para lidar com entradas inválidas do usuário.

#### `choose_table(cursor, schema)`

**Objetivo:** Exibe um menu com as tabelas disponíveis no schema especificado e permite que o usuário escolha uma tabela.

**Tratamento de exceções:** Inclui `try/except` para lidar com entradas inválidas do usuário

#### `choose_column(cursor, schema_name, table_name)`

**Objetivo:** Exibe um menu com as colunas disponíveis na tabela especificada e permite que o usuário escolha uma coluna.

**Tratamento de Exceções:** Inclui `try/except` para lidar com entradas inválidas do usuário

### 1.2. Função de conversão de tipo

#### `get_column_value(cursor, schema_name, table_name, column_name)`

**Objetivo:** Pede ao usuário um valor de filtro ou inserção para a coluna especificada e o retorna convertido corretamente para o tipo da coluna.

**Tratamento de exceções:** Contém um `try/except` que tenta converter a entrada do usuário para o tipo de dado esperado da coluna. Se a conversão falhar, uma mensagem de erro é exibida e o usuário é solicitado a tentar novamente.

### 1.3. Operações CRUD

A implementação das operações CRUD foi feita com foco em segurança e robustez:

- Todas as operações de modificação do banco de dados (Create, Update, Delete) utilizam **parâmetros** (`%s`) na construção das queries, prevenindo ataques de SQL Injection.
- As transações são controladas de forma explícita dentro das funções de modificação: um `commit` é executado apenas se a operação for bem-sucedida; em caso de erro, um `rollback` é realizado. Isso garante que transações não sejam deixadas em aberto e que o banco mantenha sua integridade.

```python
# Exemplo de uso de parâmetros em create_record
colunas_str = ", ".join(valores.keys())
placeholders = ", ".join(["%s"] * len(valores))
sql_insert = f"INSERT INTO {schema_name}.{table_name} ({colunas_str}) VALUES ({placeholders});"
cursor.execute(sql_insert, tuple(valores.values()))

# Exemplo de uso de parâmetros em read_records (com filtro)
sql_select = f"""
    SELECT * FROM {schema_name}.{table_name}
    WHERE {filter_column} = %s;
"""
cursor.execute(sql_select, (filtro_valor,))
```

Nesses exemplos, `schema_name`, `table_name` e `filter_column` são nomes de objetos do banco de dados (tabelas e colunas), que não são fornecidos diretamente pelo usuário, mas sim selecionados a partir de listas predefinidas ou consultadas do próprio esquema do banco de dados, o que já adiciona uma camada de segurança. Os valores reais (`valores.values()` e `filtro_valor`) são passados como uma tupla para o segundo argumento de `cursor.execute()`. Essa separação entre a definição da consulta e os valores que a preenchem impede ataques de SQL Injection. Como os valores fornecidos pelo usuário não são concatenados diretamente na string da query, mas passados separadamente como parâmetros, o banco de dados trata esses valores como dados literais, e não como parte da lógica da consulta SQL. Isso bloqueia tentativas de injetar código malicioso através das entradas de usuário.

#### `create_record(conn, cursor, schema_name, table_name)`

**Objetivo:** Insere um novo registro na tabela especificada. Consulta dinamicamente as colunas da tabela (exceto colunas identity/serial) e solicita ao usuário os valores correspondentes.

#### `read_records(cursor, schema_name, table_name)`

**Objetivo:** Consulta e exibe os registros da tabela especificada. Permite ao usuário escolher opcionalmente um filtro (condição WHERE), com conversão de tipos adequada.

#### `update_record(conn, cursor, schema_name, table_name)`

**Objetivo:** Atualiza um ou mais registros da tabela especificada. Permite que o usuário escolha a coluna que deseja atualizar e o novo valor, bem como a coluna de filtro e o valor de filtro.

#### `delete_record(conn, cursor, schema_name, table_name)`

**Objetivo:** Exclui um ou mais registros da tabela especificada. Permite que o usuário escolha a coluna de filtro e o valor de filtro.

### 1.4. Banner ASCII

#### `print_ascii_banner()`

**Objetivo:** Exibir um banner ASCII com o nome "Vertical Life" no console, utilizando a biblioteca `pyfiglet`. Esta função é puramente estética e serve para dar um toque visual ao iniciar a aplicação.

### 1.5. Função `main()`

A função `main` é o ponto central de controle da aplicação CRUD. Ela permite que o usuário navegue de forma interativa por três etapas principais:

- **Escolha do schema:** o usuário seleciona em qual schema do banco de dados deseja operar (`choose_schema`). O `search_path` é ajustado dinamicamente para o schema escolhido.
- **Escolha da tabela:** o usuário escolhe a tabela que deseja manipular (`choose_table`).
- **Execução de operações CRUD:** um menu interativo permite executar as operações CRUD sobre a tabela selecionada.

A função `main` utiliza loops aninhados para permitir uma navegação fluida:

- O loop externo permite mudar de schema a qualquer momento.
- O loop intermediário permite mudar de tabela dentro do schema.
- O loop interno controla o menu CRUD da tabela escolhida.

Essa estrutura torna a aplicação flexível e adaptada a um cenário de múltiplos schemas e múltiplas tabelas.

## 2. Implementação de índices e busca
### 2.1. Análise de performance com Índices

Para avaliar o impacto dos índices na performance de consultas, foram criados dois schemas distintos no banco de dados: um com índice (`VerticalLife`) e outro sem índice (`VerticalLifeNoIdx`) na coluna de nome dos escaladores. Para simular um ambiente com grande volume de dados e tornar os testes de performance mais realistas, foram geradas 100.000 entradas de nomes para cada um dos schemas. Essa população de dados foi realizada utilizando o script Python `name_generator.py`, que automatiza a criação de nomes aleatórios e sua inserção no banco de dados.

Os testes foram executados utilizando o script `teste_busca_indices.py`, que emprega o comando `EXPLAIN ANALYZE` para medir o tempo de execução e analisar o plano de consulta nos dois schemas. Para cada um deles, foram realizadas buscas em dois casos distintos:

- **Nome mais fácil de encontrar:** o primeiro escalador da tabela, ou seja, o registro com o menor IDEscalador. Este registro é considerado fácil de encontrar em um banco sem índice porque um Sequential Scan percorre a tabela em ordem física, e o primeiro registro é encontrado logo no início da varredura.

- **Nome mais difícil de encontrar:** o último escalador da tabela, ou seja, o registro com o maior IDEscalador. Este registro é considerado difícil de encontrar sem índice porque, em um Sequential Scan, o SGBD precisa percorrer toda a tabela até o final para localizar o registro, resultando em um tempo de execução proporcional ao tamanho da tabela.

Com o uso de índice (Index Scan), a posição física do registro deixa de impactar o tempo de busca, tornando o acesso igualmente rápido para qualquer nome, independentemente de sua posição na tabela.

```
1 - Testar busca pelo primeiro nome (VerticalLife)------------------------------------------

== EXPLAIN ANALYZE para nome 'Calango' no schema VerticalLife ==
Index Scan using idx_escalador_nomeescalador on escalador  (cost=0.42..8.44 rows=1 width=18) (actual time=0.037..0.037 rows=1 loops=1)
  Index Cond: ((nomeescalador)::text = 'Calango'::text)

Planning Time: 0.053 ms
Execution Time: 0.046 ms

2 - Testar busca pelo último nome (VerticalLife)--------------------------------------------

== EXPLAIN ANALYZE para nome 'James Bruyere' no schema VerticalLife ==
Index Scan using idx_escalador_nomeescalador on escalador  (cost=0.42..8.44 rows=1 width=18) (actual time=0.035..0.036 rows=1 loops=1)
  Index Cond: ((nomeescalador)::text = 'James Bruyere'::text)

Planning Time: 0.045 ms
Execution Time: 0.044 ms

3 - Testar busca pelo primeiro nome (VerticalLifeNoIdx)-------------------------------------

== EXPLAIN ANALYZE para nome 'Calango' no schema VerticalLifeNoIdx ==
Seq Scan on escalador  (cost=0.00..1867.06 rows=1 width=18) (actual time=0.005..4.640 rows=1 loops=1)
  Filter: ((nomeescalador)::text = 'Calango'::text)
  Rows Removed by Filter: 100004

Planning Time: 0.029 ms
Execution Time: 4.649 ms

4 - Testar busca pelo último nome (VerticalLifeNoIdx)----------------------------------------

== EXPLAIN ANALYZE para nome 'James Clark' no schema VerticalLifeNoIdx ==
Seq Scan on escalador  (cost=0.00..1867.06 rows=1 width=18) (actual time=0.954..5.257 rows=4 loops=1)
  Filter: ((nomeescalador)::text = 'James Clark'::text)
  Rows Removed by Filter: 100001

Planning Time: 0.038 ms
Execution Time: 5.265 ms

```

### 2.2. Análise dos Resultados

Os resultados confirmam a eficácia dos índices na otimização de buscas. No schema `VerticalLife` (com índice), tanto a busca pelo primeiro quanto pelo último nome apresentaram tempos de execução extremamente baixos (na casa dos milissegundos), e o plano de execução mostra um `Index Scan`. Isso demonstra que o índice permitiu ao SGBD localizar os registros diretamente, sem a necessidade de varrer a tabela inteira.

Por outro lado, no schema `VerticalLifeNoIdx` (sem índice), as buscas resultaram em `Seq Scan` (varredura sequencial da tabela). Embora a busca pelo primeiro nome tenha sido relativamente rápida, a busca pelo último nome levou significativamente mais tempo. Isso ocorre porque o SGBD precisou percorrer a tabela inteira até encontrar o registro desejado, o que é ineficiente para grandes volumes de dados. A diferença de tempo entre as buscas com e sem índice é clara, evidenciando o ganho de performance proporcionado pela indexação.



