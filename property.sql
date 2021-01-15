SELECT count(*) FROM uk_property.property;

SET SQL_SAFE_UPDATES=0;

DELETE p1 FROM property p1
INNER JOIN property p2
WHERE
    p1.id > p2.id AND 
    p1.property_id = p2.property_id;