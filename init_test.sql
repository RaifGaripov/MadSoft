DO
$do$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test_memes') THEN
      PERFORM dblink_exec('dbname=' || current_database()
                        , 'CREATE DATABASE test_memes');
   END IF;
END
$do$;