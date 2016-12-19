create or replace function borradoTotal() 
returns boolean as
$BODY$
begin
	delete from paginas_tc_coordenada;
	delete from paginas_tc_patron;
end;
$BODY$
language plpgsql;
