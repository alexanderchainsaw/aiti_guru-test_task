from yoyo import get_backend, read_migrations


def apply_migrations(database_dsn: str, migrations_path: str) -> None:
    """
    Apply migration .sql files using yoyo-migrations
    :param database_dsn: postgresql connection string, like `"postgresql://postgres:postgres@postgres/postgres"`
    :param migrations_path: relative path to the directory containing migrations, like `"app/migrations"`
    :return: None
    """
    backend = get_backend(database_dsn)
    migrations = read_migrations(migrations_path)
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
