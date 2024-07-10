DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'db_memes') THEN
      PERFORM dblink_exec('dbname=' || current_database()
                        , 'CREATE DATABASE db_memes');
   END IF;
END
$do$;