Declare
  instance varchar(20);
begin

  select upper(instance) into instance from lisa.usr_django_instance;
  dbms_output.put_line('==============================================');
  dbms_output.put_line(instance);
  dbms_output.put_line(user);
  dbms_output.put_line('==============================================');

  if instance = 'LISA' and user = 'DJANGO' then
  
    FOR rec IN (SELECT object_name, object_type
                  FROM user_objects
                 WHERE object_type IN ('TABLE',
                                       'VIEW',
                                       'PACKAGE',
                                       'PROCEDURE',
                                       'FUNCTION',
                                       'SEQUENCE')) LOOP
    
      begin
      
        if rec.object_type = 'TABLE' then
          EXECUTE IMMEDIATE 'DROP ' || rec.object_type || ' "' ||rec.object_name || '" CASCADE CONSTRAINTS';
        else
          EXECUTE IMMEDIATE 'DROP ' || rec.object_type || ' "' ||rec.object_name || '"';
        end if;
      
        DBMS_OUTPUT.put_line('DROPED ' || rec.object_type || ' "' ||rec.object_name || '"');
      
      EXCEPTION
        WHEN OTHERS THEN
          DBMS_OUTPUT.put_line('FAILED: DROP ' || rec.object_type || ' "' ||
                               rec.object_name || '"');
        
      end;
    end loop;
  
  else
    dbms_output.put_line('wrong user ot instnce');
  end if;

end;
/
