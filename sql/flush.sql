DELETE FROM "DJANGO_CONTENT_TYPE";

DECLARE
    table_value integer;
    seq_value integer;
BEGIN
    SELECT NVL(MAX("ID"), 0) INTO table_value FROM "DJANGO_ADMIN_LOG";
    SELECT NVL(last_number - cache_size, 0) INTO seq_value FROM user_sequences
           WHERE sequence_name = 'DJANGO_ADMIN_LOG_SQ';
    WHILE table_value > seq_value LOOP
        SELECT "DJANGO_ADMIN_LOG_SQ".nextval INTO seq_value FROM dual;
    END LOOP;
END;
/

DECLARE
    table_value integer;
    seq_value integer;
BEGIN
    SELECT NVL(MAX("ID"), 0) INTO table_value FROM "AUTH_PERMISSION";
    SELECT NVL(last_number - cache_size, 0) INTO seq_value FROM user_sequences
           WHERE sequence_name = 'AUTH_PERMISSION_SQ';
    WHILE table_value > seq_value LOOP
        SELECT "AUTH_PERMISSION_SQ".nextval INTO seq_value FROM dual;
    END LOOP;
END;
/

DECLARE
    table_value integer;
    seq_value integer;
BEGIN
    SELECT NVL(MAX("ID"), 0) INTO table_value FROM "AUTH_GROUP";
    SELECT NVL(last_number - cache_size, 0) INTO seq_value FROM user_sequences
           WHERE sequence_name = 'AUTH_GROUP_SQ';
    WHILE table_value > seq_value LOOP
        SELECT "AUTH_GROUP_SQ".nextval INTO seq_value FROM dual;
    END LOOP;
END;
/

DECLARE
    table_value integer;
    seq_value integer;
BEGIN
    SELECT NVL(MAX("ID"), 0) INTO table_value FROM "AUTH_USER";
    SELECT NVL(last_number - cache_size, 0) INTO seq_value FROM user_sequences
           WHERE sequence_name = 'AUTH_USER_SQ';
    WHILE table_value > seq_value LOOP
        SELECT "AUTH_USER_SQ".nextval INTO seq_value FROM dual;
    END LOOP;
END;
/

DECLARE
    table_value integer;
    seq_value integer;
BEGIN
    SELECT NVL(MAX("ID"), 0) INTO table_value FROM "DJANGO_CONTENT_TYPE";
    SELECT NVL(last_number - cache_size, 0) INTO seq_value FROM user_sequences
           WHERE sequence_name = 'DJANGO_CONTENT_TYPE_SQ';
    WHILE table_value > seq_value LOOP
        SELECT "DJANGO_CONTENT_TYPE_SQ".nextval INTO seq_value FROM dual;
    END LOOP;
END;
/

COMMIT;
