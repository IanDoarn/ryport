with s1 as (
SELECT
	case
		when p.is_biomet = 1 then 'BIOMET'
		when p.is_biomet = 0 then 'ZIMMER'
	end as legacy_type,
	s.inventory_type,
	p.product_number,
	p.edi_number,
	p.description,
	p.id as item_id
FROM
	sms.stock s
		LEFT JOIN sms.product p ON p.id = s.product_id
WHERE
	s.stock_type = 2
	and s.inventory_type = 3
	and s.location_type = 1
GROUP BY
	p.id,
	p.product_number,
	p.edi_number,
	p.description,
	p.is_biomet,
	s.inventory_type
order by
	legacy_type desc,
	p.product_number desc
)

select
	s1.legacy_type,
	case
		when s1.inventory_type = 3 then 'CI'
	end as inv_type,
	s1.product_number,
	s1.edi_number,
	s1.description,
	s1.item_id
from
	s1

