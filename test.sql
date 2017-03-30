with s1 as (
SELECT
	case
		when p.is_biomet = 1 then 'BIOMET'
		when p.is_biomet = 0 then 'ZIMMER'
	end as legacy_type,
	case
		when (s.stock_type = 3 or s.stock_type = 4) and s.product_type = 3 then 'TRAY'
		when (s.stock_type = 3 or s.stock_type = 4) and s.product_type = 1 then 'KIT'
		when s.stock_type = 1 then 'PIECE'
		when s.stock_type = 2 then 'COMPONENT'
	end as item_type,
	s.inventory_type,
	p.product_number,
	p.edi_number,
	p.description,
	b.zone || '-' || b.position || '-' || b.shelf as component_bin,
	sum (s.quantity_available) as qty_avail_sh,
	ps.serial_number
FROM
	sms.stock s
		LEFT JOIN sms.product p ON p.id = s.product_id
		LEFT JOIN sms.bin b ON b.id = s.container_id
		LEFT JOIN sms.product_serial ps on s.serial_id = ps.id
WHERE
	s.inventory_type = 3
	and s.location_type = 1
GROUP BY
	p.product_number,
	p.edi_number,
	p.description,
	p.is_biomet,
	s.inventory_type,
	s.stock_type,
	s.product_type,
	ps.serial_number,
	b.zone || '-' || b.position || '-' || b.shelf
order by
	legacy_type desc,
	p.product_number desc
)
select
	s1.legacy_type,
	case
		when s1.inventory_type = 3 then 'CI'
	end as inv_type,
	s1.item_type,
	s1.product_number,
	s1.edi_number,
	s1.description,
	s1.serial_number,
	s1.component_bin,
	s1.qty_avail_sh
from
	s1
order by
	s1.item_type,
	s1.product_number
