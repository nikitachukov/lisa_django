-- Create the user 
create user DJANGO
  default tablespace USERS
  temporary tablespace TEMP
  profile DEFAULT
  quota 1000m on users;
-- Grant/Revoke object privileges 
grant select on USR_DJANGO_AUTH to DJANGO;
-- Grant/Revoke system privileges 
grant create indextype to DJANGO;
grant create sequence to DJANGO;
grant create session to DJANGO;
grant create table to DJANGO;
grant create trigger to DJANGO;
grant create type to DJANGO;
grant create view to DJANGO;
