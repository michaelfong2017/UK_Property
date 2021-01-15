SELECT count(*) FROM uk_property.property;

SET SQL_SAFE_UPDATES=0;
ALTER TABLE uk_property.property AUTO_INCREMENT = 1;
-- step 1
CREATE TABLE uk_property.property_temp 
LIKE uk_property.property;

-- step 2
INSERT INTO uk_property.property_temp
SELECT * 
FROM uk_property.property 
GROUP BY property_id;

-- step 3
DROP TABLE uk_property.property;

ALTER TABLE uk_property.property_temp 
RENAME TO uk_property.property;


ALTER TABLE uk_property.property DROP id;
ALTER TABLE uk_property.property ADD id INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (id), AUTO_INCREMENT=1;