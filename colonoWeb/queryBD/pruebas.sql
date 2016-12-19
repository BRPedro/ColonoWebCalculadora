CREATE OR REPLACE FUNCTION consultaCoo(f integer,c integer) 
RETURNS table record AS
$BODY$
BEGIN

	create temp table tabla as(
	select  pat.idpatron, pat.contadorp from
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
	order by pat.contadorp desc);
	FOR resultado IN SELECT *  FROM tabla LOOP
          RETURN NEXT resultado;
      END LOOP;
      RETURN;
end;
$BODY$
  LANGUAGE plpgsql

select  consultaCoo(5,5)

UPDATE paginas_tc_patron
SET contadorp = (contadorp+1)
WHERE idpatron =1

select * from paginas_tc_patron
select * from paginas_tc_coordenada
insert into paginas_tc_patron(contadorp) values (1)

insert into paginas_tc_coordenada(filac,columnac, idtablapatron_id) values (4,5,1)
insert into paginas_tc_coordenada(filac,columnac, idtablapatron_id) values (4,6,1)
insert into paginas_tc_coordenada(filac,columnac, idtablapatron_id) values (5,6,2)


select  pat.idpatron, pat.contadorp from
	(select idtablapatron_id from paginas_tc_coordenada where 
	(filac=5-1 and columnac= 5-1) or
	(filac=5-1 and columnac=5) or 
	(filac=5-1 and columnac=5+1) or 
	(filac=5 and columnac=5-1) or 
	(filac=5 and columnac=5+1) or 
	(filac=5+1 and columnac=5-1) or 
	(filac=5+1 and columnac=5) or 
	(filac=5+1 and columnac=5+1)) as coo1,
	paginas_tc_patron as pat where (coo1.idtablapatron_id=pat.idpatron )
	group by pat.idpatron
	order by pat.contadorp desc;
