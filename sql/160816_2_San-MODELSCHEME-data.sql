execute block
as
declare variable id type of column scheme_modelstack.id;
declare variable x_pdiff type of column scheme_modelstack.x_pdiff;
declare variable y_pdiff type of column scheme_modelstack.y_pdiff;
declare variable z_pdiff type of column scheme_modelstack.z_pdiff;
begin
    for
        select s.id, s.x_pdiff, s.y_pdiff, s.z_pdiff
          from scheme_modelstack s
         where s.modelid <> 1
          into :id, :x_pdiff, :y_pdiff, :z_pdiff
    do
        update scheme_modelstack s
           set s.y_pdiff = :z_pdiff,
               s.x_pdiff = :y_pdiff,
               s.z_pdiff = :x_pdiff
         where s.id = :id;

end
