# dimensions presents on comments

select field as Field, count(distinct comment_commentid) as count
from (
    select o.comment_commentid, o.dimension_dimension_id, d.dimension_id, d.field
    from opinion o, dimension d
    where o.dimension_dimension_id = d.dimension_id
) as fi
group by field;


# u analysis
select concept, count(*) as count from dimension where field = 'Usability' group by concept

#ux
select concept, count(*) as total from dimension where field = 'UX' group by concept