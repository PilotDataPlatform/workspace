select 'create database workspace' where not exists (select from pg_database where datname = 'workspace')\gexec
