from faker import Faker
import os
import psycopg2


def main():
    fake = Faker("es_MX")

    host = os.getenv("BRONZE_PG_HOST", "postgres")
    db = os.getenv("BRONZE_PG_DB", "bronze_db")
    user = os.getenv("BRONZE_PG_USER", "bronze_user")
    password = os.getenv("BRONZE_PG_PASSWORD", "bronze_pass")

    conn = psycopg2.connect(
        host=host,
        dbname=db,
        user=user,
        password=password
    )
    cur = conn.cursor()

    # 1) Crear tabla bronce si no existe
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios_bronce (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            email TEXT,
            direccion TEXT,
            fecha_insercion TIMESTAMP DEFAULT NOW()
        );
        """
    )

    # 2) Insertar 10 registros sintéticos
    registros = []
    for _ in range(10):
        registros.append(
            (
                fake.name(),
                fake.email(),
                fake.address()
            )
        )

    insert_sql = """
        INSERT INTO usuarios_bronce (nombre, email, direccion)
        VALUES (%s, %s, %s);
    """
    cur.executemany(insert_sql, registros)

    conn.commit()
    cur.close()
    conn.close()

    print(
        f"Se insertaron {len(registros)} registros en la tabla usuarios_bronce (capa bronce)."
    )


if __name__ == "__main__":
    main()
