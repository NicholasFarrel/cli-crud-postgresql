import psycopg2
import names

def connect_db():
    """
    Estabelece uma conexão com o banco de dados PostgreSQL.

    Returns:
        psycopg2.extensions.connection: Objeto de conexão com o banco de dados.
    """
    try:
        conn = psycopg2.connect(
            user="nicholas",
            password="bddosguri",
            host="10.61.49.168",
            port="5432",
            dbname="nicholas"
        )
        cursor = conn.cursor()
        print("Conexão realizada com sucesso!")
        return conn
    except Exception as e:
        print("Erro ao conectar no banco:", e)
        exit()

def insert_escaladores(conn, schema_name, quantidade):
    """
    Insere múltiplos escaladores com nomes aleatórios na tabela Escalador.

    Args:
        conn: conexão ativa com o banco de dados
        schema_name (str): nome do schema onde a tabela Escalador está
        quantidade (int): número de escaladores a serem inseridos
    """
    cursor = conn.cursor()

    # pegar o último IDEscalador atual (caso já tenha registros na tabela)
    cursor.execute(f"SELECT COALESCE(MAX(IDEscalador), 0) FROM {schema_name}.Escalador;")
    last_id = cursor.fetchone()[0]

    for i in range(1, quantidade + 1):
        id_escalador = last_id + i
        nome = names.get_full_name()
        try:
            cursor.execute(
                f"INSERT INTO {schema_name}.Escalador (IDEscalador, NomeEscalador) VALUES (%s, %s);",
                (id_escalador, nome)
            )
            if i % 100 == 0 or i == quantidade:
                print(f"{i} escaladores inseridos...")
        except Exception as e:
            print(f"Erro ao inserir escalador ID {id_escalador}: {e}")
            conn.rollback()
            continue

    conn.commit()
    print(f"\n{quantidade} escaladores inseridos com sucesso no schema {schema_name}!")

def main():
    conn = connect_db()

    while True:
        # Menu para escolher schema
        print("\n==== Escolha o schema onde deseja inserir escaladores ====")
        print("1 - VerticalLife (com índice)")
        print("2 - VerticalLifeNoIdx (sem índice)")
        print("3 - Sair")

        schema_opcao = input("Escolha o schema desejado: ")

        if schema_opcao == '1':
            schema_name = 'VerticalLife'
        elif schema_opcao == '2':
            schema_name = 'VerticalLifeNoIdx'
        elif schema_opcao == '3':
            print("Encerrando...")
            break
        else:
            print("Opção inválida. Tente novamente.")
            continue

        # Perguntar quantidade
        try:
            quantidade = int(input(f"Quantos escaladores você deseja inserir em {schema_name}? (Digite 0 para voltar ao menu de schema) "))
            if quantidade == 0:
                continue
            elif quantidade < 0:
                print("Por favor, insira um número positivo.")
                continue
            insert_escaladores(conn, schema_name, quantidade)
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")

    conn.close()

if __name__ == "__main__":
    main()
