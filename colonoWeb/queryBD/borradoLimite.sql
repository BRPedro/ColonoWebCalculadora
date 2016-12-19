create or replace function borradoLimite(limite integer)
RETURNS integer  as
$BODY$
declare 
id integer;
vcursor refcursor;
vprospecto BIGINT;
begin 
	CREATE TEMP TABLE IF NOT EXISTS temp_table AS
		select temporal.id from (
		select  pat.idpatron as id, pat.contadorp as contador from
		paginas_tc_coordenada as coo1,
		paginas_tc_patron as pat where (coo1.idtablapatron_id=pat.idpatron and pat.contadorp<=limite)
		group by pat.idpatron) as temporal;	
		
		OPEN vcursor for  select temp_table.id from temp_table;
		loop
		FETCH vcursor INTO vprospecto;
		EXIT WHEN NOT FOUND;					
			delete from paginas_tc_coordenada
			where idtablapatron_id=vprospecto;
			delete from paginas_tc_patron
			where idpatron=vprospecto;
		END loop;
		CLOSE vcursor;
		DROP TABLE temp_table;
		return 100;
end;
$BODY$
  LANGUAGE plpgsql;

select * from paginas_tc_patron

select borradoLimite(2)
