create or replace view usr_django_auth as
select 
u.username,
u.lastname,
u.firstname,
u.middlename,
db.account_status,
u.logindisabled,
u.canworkinfrontoffice,
phone,email,job
 from dba_users db ,users u, usergrouplink ugl
where db.username=u.username and ugl.userid=u.id and ugl.usergroupid=1000 and u.logindisabled=0
