import psycopg2
import datetime
import pyfiglet

def connect_db():
    """
    Estabelece uma conexão com o banco de dados PostgreSQL.

    Returns:
        psycopg2.extensions.connection: Objeto de conexão com o banco de dados.

    Em caso de erro na conexão, exibe uma mensagem e encerra o programa.
    """

    try:
        # objeto de conexão ao banco de dados
        conn = psycopg2.connect(
            user="nicholas",
            password="bddosguri",
            host="10.61.49.168",
            port="5432",
            dbname="nicholas"
        )
        # objeto usado para executar SQL
        cursor = conn.cursor()
        print("Conexão realizada com sucesso!")
        return conn
    except Exception as e:
        print("Erro ao conectar no banco:", e)
        exit()

def choose_schema(cursor):
    """
    Exibe um menu com os schemas disponíveis no banco de dados (exceto schemas internos)
    e permite que o usuário escolha um schema.

    Args:
        cursor (psycopg2.extensions.cursor): Cursor de banco de dados já conectado.

    Returns:
        str: Nome do schema escolhido pelo usuário, ou None se não houver schemas disponíveis.
    """

    # Consulta os schemas disponíveis no banco, exceto os internos do PostgreSQL
    cursor.execute("""
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name NOT IN ('information_schema', 'pg_catalog', 'pg_toast')
        ORDER BY schema_name;
    """)

    # Monta uma lista com o nome de cada schema retornado
    schemas = [row[0] for row in cursor.fetchall()]

    # Se não houver schemas encontrados, avisa e retorna None
    if not schemas:
        print("Nenhum schema encontrado.")
        return None

    # Loop para exibir o menu e esperar uma escolha válida do usuário
    while True:
        print("\n==== Menu de Schemas ====")
        
        # Exibe cada schema com um número correspondente
        for i, schema in enumerate(schemas, start=1):
            print(f"{i} - {schema}")

        # Pede para o usuário digitar o número da opção desejada
        opcao = input("Escolha o schema que deseja: ")

        try:
            # Tenta converter a entrada para um número inteiro (índice da lista)
            index = int(opcao) - 1

            # Verifica se o índice está dentro dos limites da lista de schemas
            if 0 <= index < len(schemas):
                # Retorna o schema escolhido
                return schemas[index]
            else:
                # Se o índice não for válido, avisa o usuário
                print("Opcao invalida. Tente novamente.")
        except ValueError:
            # Se o usuário não digitar um número, trata o erro e avisa
            print("Digite um numero valido.")

def choose_table(cursor, schema):
    """
    Exibe um menu com as tabelas disponíveis no schema especificado
    e permite que o usuário escolha uma tabela.

    Esta função deve ser utilizada em conjunto com um sistema multi-schema, 
    onde o schema a ser utilizado é explicitamente especificado.

    Usa %s com tupla (schema,) para evitar SQL Injection — o parâmetro é passado de forma segura.

    Args:
        cursor (psycopg2.extensions.cursor): Cursor de banco de dados já conectado.
        schema (str): Nome do schema selecionado.

    Returns:
        str: Nome da tabela escolhida pelo usuário, ou None se não houver tabelas disponíveis.
    """

    # Consulta as tabelas do schema escolhido, considerando apenas as tabelas "normais" (BASE TABLE)
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """, (schema,))

    # Monta uma lista com os nomes das tabelas encontradas
    tabelas = [row[0] for row in cursor.fetchall()]

    # Se não houver tabelas no schema, avisa e retorna None
    if not tabelas:
        print(f"Nenhuma tabela encontrada no schema {schema}.")
        return None

    # Loop para exibir o menu e esperar uma escolha válida do usuário
    while True:
        print(f"\n==== Menu de Tabelas (Schema: {schema}) ====")
        
        # Exibe cada tabela com um número correspondente
        for i, tabela in enumerate(tabelas, start=1):
            print(f"{i} - {tabela}")

        # Pede para o usuário digitar o número da opção desejada
        opcao = input("Escolha a tabela que deseja: ")

        try:
            # Tenta converter a entrada para um número inteiro (índice da lista)
            index = int(opcao) - 1

            # Verifica se o índice está dentro dos limites da lista de tabelas
            if 0 <= index < len(tabelas):
                # Retorna o nome da tabela escolhida
                return tabelas[index]
            else:
                # Se o índice não for válido, avisa o usuário
                print("Opcao invalida. Tente novamente.")
        except ValueError:
            # Se o usuário não digitar um número, trata o erro e avisa
            print("Digite um numero valido.")

def choose_column(cursor, schema_name, table_name):
    """
    Exibe um menu com as colunas disponíveis na tabela especificada
    do schema especificado, e permite que o usuário escolha uma coluna.

    Args:
        cursor (psycopg2.extensions.cursor): Cursor de banco de dados já conectado.
        schema_name (str): Nome do schema onde a tabela está localizada.
        table_name (str): Nome da tabela selecionada.

    Returns:
        str: Nome da coluna escolhida pelo usuário, ou None se não houver colunas disponíveis.
    """

    # Consulta as colunas da tabela escolhida
    cursor.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = %s
        AND table_schema = %s
        AND is_identity = 'NO'
        ORDER BY ordinal_position;
    """, (table_name, schema_name))


    # Monta uma lista com os nomes das colunas
    columns = [row[0] for row in cursor.fetchall()]

    # Se não houver colunas, avisa e retorna None
    if not columns:
        print(f"Nenhuma coluna encontrada na tabela {table_name}.")
        return None

    # Loop para exibir o menu e esperar uma escolha válida do usuário
    while True:
        print(f"\n==== Menu de Colunas (Tabela: {table_name}) ====")
        
        # Exibe cada coluna com um número correspondente
        for i, column in enumerate(columns, start=1):
            print(f"{i} - {column}")

        # Pede para o usuário digitar o número da opção desejada
        opcao = input("Escolha a coluna que deseja: ")

        try:
            # Tenta converter a entrada para um número inteiro (índice da lista)
            index = int(opcao) - 1

            # Verifica se o índice está dentro dos limites da lista de colunas
            if 0 <= index < len(columns):
                # Retorna o nome da coluna escolhida
                return columns[index]
            else:
                print("Opcao invalida. Tente novamente.")
        except ValueError:
            # Se o usuário não digitar um número, trata o erro e avisa
            print("Digite um numero valido.")

def get_column_value(cursor, schema_name, table_name, column_name):
    """
    Pede ao usuário um valor de filtro para a coluna especificada,
    e retorna o valor convertido corretamente para o tipo da coluna.

    Args:
        cursor (psycopg2.extensions.cursor): Cursor conectado ao banco.
        schema_name (str): Nome do schema onde a tabela está localizada.
        table_name (str): Nome da tabela.
        column_name (str): Nome da coluna para a qual o filtro será aplicado.

    Returns:
        O valor convertido, pronto para ser usado em uma cláusula WHERE.
    """

    # Descobrir o tipo da coluna
    cursor.execute("""
        SELECT data_type
        FROM information_schema.columns
        WHERE table_name = %s
        AND table_schema = %s
        AND column_name = %s;
    """, (table_name, schema_name, column_name))

    data_type = cursor.fetchone()[0]


    # Pedir o valor de filtro
    while True:
        valor_digitado = input(f"Digite o valor para {column_name} ({data_type}): ")

        try:
            if valor_digitado.upper() == 'NULL':
                valor_final = None
            elif data_type in ('integer', 'smallint', 'bigint'):
                valor_final = int(valor_digitado)
            elif data_type in ('numeric', 'double precision', 'real', 'decimal'):
                valor_final = float(valor_digitado)
            elif data_type == 'boolean':
                if valor_digitado.lower() in ('true', '1', 'yes'):
                    valor_final = True
                elif valor_digitado.lower() in ('false', '0', 'no'):
                    valor_final = False
                else:
                    raise ValueError("Valor inválido para boolean (esperado true/false/1/0)")
            elif data_type == 'date':
                valor_final = datetime.datetime.strptime(valor_digitado, "%Y-%m-%d").date()
            else:
                valor_final = valor_digitado
            break
        except Exception as e:
            print(f"Entrada inválida para {column_name} ({data_type}): {e}. Tente novamente.")

    return valor_final

def create_record(conn, cursor, schema_name, table_name):
    """
    Insere um novo registro na tabela especificada do schema especificado.

    Consulta dinamicamente as colunas da tabela (exceto colunas identity/serial)
    e solicita ao usuário os valores correspondentes, com conversão de tipo apropriada.

    Args:
        conn (psycopg2.extensions.connection): Conexão ativa com o banco de dados.
        cursor (psycopg2.extensions.cursor): Cursor de banco de dados já conectado.
        schema_name (str): Nome do schema onde a tabela está localizada.
        table_name (str): Nome da tabela onde o registro será inserido.

    Returns:
        None
    """

    # Consulta colunas + tipo de dado (sem a coluna id)
    cursor.execute("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = %s
        AND table_schema = %s
        AND is_identity = 'NO'
        ORDER BY ordinal_position;
    """, (table_name, schema_name))


    columns_info = cursor.fetchall()

    if not columns_info:
        print(f"Nenhuma coluna para inserção encontrada na tabela {table_name}.")
        return

    # Dicionário para armazenar os valores que o usuário vai digitar
    valores = {}

    print(f"\n==== Inserindo registro na tabela {table_name} ====")

    # Para cada coluna, pede o valor ao usuário
    for column_name, data_type in columns_info:
        valor_final = get_column_value(cursor, schema_name, table_name, column_name)
        valores[column_name] = valor_final

    # Monta a query dinamicamente
    colunas_str = ", ".join(valores.keys())
    placeholders = ", ".join(["%s"] * len(valores))
    sql_insert = f"INSERT INTO {schema_name}.{table_name} ({colunas_str}) VALUES ({placeholders});"

    try:
        cursor.execute(sql_insert, tuple(valores.values()))
        conn.commit()
        print("Registro criado com sucesso!")
    except Exception as e:
        print("Erro na criação de registro:", e)
        conn.rollback()

def read_records(cursor, schema_name, table_name):
    """
    Consulta e exibe os registros da tabela especificada do schema especificado.

    Permite ao usuário escolher opcionalmente um filtro (condição WHERE),
    com conversão de tipos adequada (utilizando a função get_column_value).

    Args:
        cursor (psycopg2.extensions.cursor): Cursor de banco de dados já conectado.
        schema_name (str): Nome do schema onde a tabela está localizada.
        table_name (str): Nome da tabela a ser consultada.

    Returns:
        None
    """

    print("\n==== Leitura de registros ====")

    # Perguntar se o usuário deseja aplicar um filtro
    aplicar_filtro = input("Deseja aplicar um filtro? (s/n): ").lower()

    if aplicar_filtro == 's':
        # Escolher coluna de filtro (WHERE)
        filter_column = choose_column(cursor, schema_name, table_name)

        # Pedir o valor de filtro (com função genérica)
        filtro_valor = get_column_value(cursor, schema_name, table_name, filter_column)

        # Montar e executar a query SELECT com WHERE
        sql_select = f"""
            SELECT * FROM {schema_name}.{table_name}
            WHERE {filter_column} = %s;
        """

        cursor.execute(sql_select, (filtro_valor,))
        registros = cursor.fetchall()

        if registros:
            print("Registros encontrados:")
            for reg in registros:
                print(reg)
        else:
            print("Nenhum registro encontrado com o filtro especificado.")

    else:
        # SELECT sem filtro
        sql = f"SELECT * FROM {schema_name}.{table_name};"
        cursor.execute(sql)
        registros = cursor.fetchall()

        if registros:
            print("Registros encontrados:")
            for reg in registros:
                print(reg)
        else:
            print("Nenhum registro encontrado.")

def update_record(conn, cursor, schema_name, table_name):
    """
    Atualiza um ou mais registros da tabela especificada no schema especificado.

    Permite que o usuário escolha a coluna que deseja atualizar e o novo valor,
    bem como a coluna de filtro (condição WHERE) e o valor de filtro.

    Usa a função get_column_value para garantir consistência na conversão de tipos.

    Args:
        conn (psycopg2.extensions.connection): Conexão ativa com o banco de dados.
        cursor (psycopg2.extensions.cursor): Cursor de banco de dados já conectado.
        schema_name (str): Nome do schema onde a tabela está localizada.
        table_name (str): Nome da tabela onde o registro será atualizado.

    Returns:
        None
    """

    print("\n==== Atualização de registros ====")
    try:
        # Escolher qual coluna atualizar
        print("\nEscolha a coluna e o valor para atualização:")
        column_to_update = choose_column(cursor, schema_name, table_name)

        # Pedir o novo valor para a coluna (com função genérica)
        novo_valor = get_column_value(cursor, schema_name, table_name, column_to_update)

        # Escolher coluna de filtro (WHERE)
        print("\nAgora escolha a condição para selecionar o(s) registro(s) que deseja atualizar:")
        filter_column = choose_column(cursor, schema_name, table_name)

        # Pedir o valor de filtro (com função genérica)
        filtro_valor = get_column_value(cursor, schema_name, table_name, filter_column)

        # Montar e executar a query UPDATE
        sql_update = f"""
            UPDATE {schema_name}.{table_name}
            SET {column_to_update} = %s
            WHERE {filter_column} = %s;
        """

        cursor.execute(sql_update, (novo_valor, filtro_valor))
        conn.commit()
        print(f"Registro(s) atualizado(s) com sucesso!")

    except Exception as e:
        print("Erro na atualização de registro:", e)
        conn.rollback()

def delete_record(conn, cursor, schema_name, table_name):
    """
    Exclui um ou mais registros da tabela especificada no schema especificado.

    Permite que o usuário escolha a coluna de filtro (condição WHERE) e o valor de filtro,
    com conversão de tipos adequada (utilizando a função get_column_value).

    Apenas os registros que satisfazem a condição de filtro são excluídos.

    Args:
        conn (psycopg2.extensions.connection): Conexão ativa com o banco de dados.
        cursor (psycopg2.extensions.cursor): Cursor de banco de dados já conectado.
        schema_name (str): Nome do schema onde a tabela está localizada.
        table_name (str): Nome da tabela onde o registro será excluído.

    Returns:
        None
    """

    print("\n==== Exclusão de registros ====")

    try:
        # Escolher coluna de filtro (WHERE)
        print("Escolha a condição para selecionar o(s) registro(s) que deseja excluir:")
        filter_column = choose_column(cursor, schema_name, table_name)

        # Pedir o valor de filtro (com função genérica)
        filtro_valor = get_column_value(cursor, schema_name, table_name, filter_column)

        # Montar e executar a query DELETE
        sql_delete = f"""
            DELETE FROM {schema_name}.{table_name}
            WHERE {filter_column} = %s;
        """

        cursor.execute(sql_delete, (filtro_valor,))
        conn.commit()
        print("Registro(s) excluído(s) com sucesso!")

    except Exception as e:
        print("Erro na exclusão de registro:", e)
        conn.rollback()


def print_ascii_banner():
    ascii_banner = pyfiglet.figlet_format("Vertical Life")
    print(ascii_banner)

def main():
    conn = connect_db()
    cursor = conn.cursor()

    print_ascii_banner()

    # Loop externo: permite escolher outro schema quando quiser
    while True:
        # Passo 1 - Escolher schema
        schema = choose_schema(cursor)
        print(f"Schema escolhido: {schema}")

        # Setar o search_path para o schema escolhido
        cursor.execute(f"SET search_path TO {schema};")
        conn.commit()

        # Loop de escolha de tabela dentro do schema
        while True:
            # Passo 2 - Escolher tabela
            table = choose_table(cursor, schema)
            print(f"Tabela escolhida: {table}")

            # Loop CRUD para a tabela escolhida
            while True:
                print(f"\n==== Menu CRUD - Schema: {schema} | Tabela: {table} ====")
                print("1 - Criar registro")
                print("2 - Ler registros")
                print("3 - Atualizar registro")
                print("4 - Excluir registro")
                print("5 - Escolher outra tabela")
                print("6 - Escolher outro schema")
                print("7 - Sair")
                opcao = input("Escolha a operação desejada: ")


                ## o inínico das transações é dado no interior das funções CRUD
                ## caso não haja erro, as alterações são comitadas
                ## caso haja erro, a transação é finalizada com ROLLBACK
                if opcao == '1':
                    create_record(conn, cursor, schema, table)
                elif opcao == '2':
                    # SELECT não precisa de transação
                    try:
                        read_records(cursor, schema, table)
                    except Exception as e:
                        print("Erro na leitura de registros:", e)
                elif opcao == '3':
                    update_record(conn, cursor, schema,  table)
                elif opcao == '4':
                    delete_record(conn, cursor, schema, table)
                elif opcao == '5':
                    # Quebra o loop CRUD → volta para escolher outra tabela no mesmo schema
                    break
                elif opcao == '6':
                    # Quebra o loop CRUD e o loop de tabelas → volta para escolher outro schema
                    break_outer = True
                    break
                elif opcao == '7':
                    print("Encerrando a aplicação...")
                    cursor.close()
                    conn.close()
                    return
                else:
                    print("Opção inválida! Tente novamente.")


            # Se a opção foi escolher outro schema, sai também do loop de tabelas
            if 'break_outer' in locals() and break_outer:
                del break_outer
                break
                
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()

    