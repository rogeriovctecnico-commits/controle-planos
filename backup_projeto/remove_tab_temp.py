import sqlite3, sys, os, shutil

DEFAULT_DB = r"D:\JornadaPython\Controle_Clientes_adapta\ControleClientes\Projeto-Python\controle_de_planos_Flask\planos.db"

def main():
    db = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DB
    db = os.path.abspath(db)
    if not os.path.exists(db):
        print(f"Arquivo não encontrado: {db}")
        return
    # backup adicional
    bak = db + ".pre_drop.bak"
    shutil.copy2(db, bak)
    print(f"Backup adicional criado: {bak}")
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS _alembic_tmp_administradoras;")
        conn.commit()
        print("Tabela temporária removida (se existia).")
    except Exception as e:
        print("Erro ao remover tabela:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()