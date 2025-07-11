
import psycopg2

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
        return conn, cursor
    except Exception as e:
        print("Erro ao conectar no banco:", e)
        exit()

def get_first_name(cursor, schema_name):
    """Retorna o primeiro NomeEscalador do schema."""
    try:
        cursor.execute(f"""
            SELECT NomeEscalador 
            FROM {schema_name}.Escalador 
            ORDER BY IDEscalador ASC 
            LIMIT 1;
        """)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao obter primeiro nome no schema {schema_name}: {e}")
        return None

def get_last_name(cursor, schema_name):
    """Retorna o último NomeEscalador do schema."""
    try:
        cursor.execute(f"""
            SELECT NomeEscalador 
            FROM {schema_name}.Escalador 
            ORDER BY IDEscalador DESC 
            LIMIT 1;
        """)
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao obter último nome no schema {schema_name}: {e}")
        return None

def test_busca_explain(cursor, schema_name, nome_escalador):
    """
    Executa EXPLAIN ANALYZE para uma busca por nome de escalador no schema especificado.
    """
    try:
        print(f"\n== EXPLAIN ANALYZE para nome '{nome_escalador}' no schema {schema_name} ==")
        sql_explain = f"""
            EXPLAIN ANALYZE 
            SELECT * 
            FROM {schema_name}.Escalador 
            WHERE NomeEscalador = %s;
        """
        cursor.execute(sql_explain, (nome_escalador,))
        resultado = cursor.fetchall()
        
        for linha in resultado:
            print(linha[0])

    except Exception as e:
        print(f"Erro ao executar EXPLAIN ANALYZE: {e}")

def main():
    conn, cursor = connect_db()

    while True:
        print("\n==== Menu de Teste de Índices ====")
        print("1 - Testar busca pelo primeiro nome (VerticalLife)")
        print("2 - Testar busca pelo último nome (VerticalLife)")
        print("3 - Testar busca pelo primeiro nome (VerticalLifeNoIdx)")
        print("4 - Testar busca pelo último nome (VerticalLifeNoIdx)")
        print("5 - Sair")
        
        opcao = input("Escolha a operação desejada: ")

        if opcao == '1':
            nome = get_first_name(cursor, "VerticalLife")
            if nome:
                test_busca_explain(cursor, "VerticalLife", nome)

        elif opcao == '2':
            nome = get_last_name(cursor, "VerticalLife")
            if nome:
                test_busca_explain(cursor, "VerticalLife", nome)

        elif opcao == '3':
            nome = get_first_name(cursor, "VerticalLifeNoIdx")
            if nome:
                test_busca_explain(cursor, "VerticalLifeNoIdx", nome)

        elif opcao == '4':
            nome = get_last_name(cursor, "VerticalLifeNoIdx")
            if nome:
                test_busca_explain(cursor, "VerticalLifeNoIdx", nome)

        elif opcao == '5':
            print("Encerrando...")
            break

        else:
            print("Opção inválida. Tente novamente.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
