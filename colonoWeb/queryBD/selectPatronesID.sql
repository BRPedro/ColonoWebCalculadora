CREATE OR REPLACE FUNCTION consultaCoo(f integer,c integer) 
RETURNS SETOF record AS
$BODY$
declare
tabla record;
BEGIN

	for tabla in 
	select  pat.idtablapatron_id, count(pat.idtablapatron_id) from
	(select idtablapatron_id from paginas_tc_coordenada where 
	(filac=f-1 and columnac=c-1) or
	(filac=f-1 and columnac=c) or 
	(filac=f-1 and columnac=c+1) or 
	(filac=f and columnac=c-1) or 
	(filac=f and columnac=c+1) or 
	(filac=f+1 and columnac=c-1) or 
	(filac=f+1 and columnac=c) or 
	(filac=f+1 and columnac=c+1)) as coo1,
	paginas_tc_coordenada as pat where (coo1.idtablapatron_id=pat.idtablapatron_id )
	group by pat.idcoordenada
	 loop
	return next tabla;
	end loop;
return;
end;
$BODY$
  LANGUAGE plpgsql
  
select consultaCoo(5,5)