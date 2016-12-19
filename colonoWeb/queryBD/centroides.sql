create or replace function centroides()
RETURNS integer  as
$BODY$
declare 
id integer;
vcursor refcursor;
vprospecto BIGINT;
begin 
	OPEN vcursor for  select paginas_tc_patron.idpatron from paginas_tc_patron;
	loop
		FETCH vcursor INTO vprospecto;
		EXIT WHEN NOT FOUND;
		
			UPDATE paginas_tc_patron
			SET filap = (select ((max(filac)-min(filac))/2)+min(filac) from paginas_tc_coordenada where idtablapatron_id=vprospecto),
			columnap=(select ((max(columnac)-min(columnac))/2)+min(columnac) from paginas_tc_coordenada where idtablapatron_id=vprospecto) 
			WHERE idpatron = vprospecto;
					
		END loop;
		CLOSE vcursor;
	return 100;
END;
$BODY$
  LANGUAGE plpgsql;
SELECT centroides();
SELECT * FROM paginas_tc_patron