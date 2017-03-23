

SET TERM ^ ;

CREATE OR ALTER procedure FG_GET_PRODLINES
returns (
    ID_PRODLINE type of R_ID,
    NUMBER type of R_NUMBER,
    NAME type of R_NAME,
    CHGDATE type of R_FLAG,
    PRODUCERS type of R_VARCHAR255)
AS
begin
  for select id_prodline,
             number,
             name,
             coalesce(chgdate,'0'),
             listproducers
      from fg_prodlines pl
      where pl.generatorname is not null
      order by pl.number
      into :id_prodline,
           :number,
           :name,
           :chgdate,
           :producers
  do
    suspend;
end^

SET TERM ; ^

