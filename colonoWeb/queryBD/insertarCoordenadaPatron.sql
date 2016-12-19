create or replace function insercionCoordenasas(f integer, c integer)
RETURNS integer  as
$BODY$
declare 
contador integer;
id integer;
vcursor refcursor;
vprospecto BIGINT;
begin 
	CREATE TEMP TABLE IF NOT EXISTS temp_table AS
		select temporal.id,temporal.contador from (
		select  pat.idpatron as id, pat.contadorp as contador from
		(select idtablapatron_id from paginas_tc_coordenada where 
		(filac=f-1 and columnac= c-1) or
		(filac=f-1 and columnac=c) or 
		(filac=f-1 and columnac=c+1) or 
		(filac=f and columnac=c-1) or 
		(filac=f and columnac=c+1) or 
		(filac=f+1 and columnac=c-1) or 
		(filac=f+1 and columnac=c) or 
		(filac=f+1 and columnac=c+1)) as coo1,
		paginas_tc_patron as pat where (coo1.idtablapatron_id=pat.idpatron )
		group by pat.idpatron
		order by pat.contadorp desc) as temporal;
	
	contador = (select count(*) from temp_table);
	if (contador=0) then
		insert into paginas_tc_patron(filap,columnap,contadorp) values (0,0,1) 
		RETURNING idpatron into id;
		insert into paginas_tc_coordenada(filac,columnac,idtablapatron_id) values (f,c,id);
		DROP TABLE temp_table;
		return 0;
	elsif(contador=1) then 
		id = (select temp_table.id from temp_table limit(1));
		insert into paginas_tc_coordenada(filac,columnac,idtablapatron_id) values (f,c,id);
		update paginas_tc_patron set contadorp=contadorp+1
		where (idpatron=id);    
		DROP TABLE temp_table;
		return 1;
	else
		id = (select temp_table.id from temp_table limit(1));
		OPEN vcursor for  select temp_table.id from temp_table;
		loop
		FETCH vcursor INTO vprospecto;
		EXIT WHEN NOT FOUND;
		if (vprospecto <> id) then
			UPDATE paginas_tc_coordenada
			SET idtablapatron_id = id WHERE idtablapatron_id = vprospecto;
						
			delete from paginas_tc_patron
			where idpatron=vprospecto;
		end if;
		
		END loop;
		CLOSE vcursor;
		
		UPDATE paginas_tc_patron
		SET contadorp = (select sum(temp_table.contador)+1 from temp_table) WHERE idpatron = id;
		insert into paginas_tc_coordenada(filac,columnac,idtablapatron_id) values (f,c,id);
		DROP TABLE temp_table;
		return 100;
	end if;		
end;
$BODY$
  LANGUAGE plpgsql;
