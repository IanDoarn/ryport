--s0-1 gets kit standard for all kits in Centralized Inventory
--s2 gets loose pieces in Southaven Warehouse R-Bin location
--s3-4 gets the kit percent invalid in G locations in SH
--s5 gets the components available
--s6 gets qty in E01 and available
--s7 gets unique Kit Serial of stock in g SH
--s8 gets kit_bin locations (g locations only)

With s0 as (  
SELECT DISTINCT
  s.product_id,
  pc.component_product_id,
  pc.quantity
FROM
  sms.stock s
    LEFT JOIN sms.product_component pc ON s.product_id = pc.product_id
WHERE
  stock_type in (3, 4)
  AND inventory_type = 3),

s1 as (  --7292 lines no issues
SELECT
  p.product_number as kit_product_number, 
  p.edi_number as kit_edi,  
  p.description as kit_description,
  p2.product_number as component_product_number,
  p2.edi_number as component_prod_id,
  p2.description as component_description,
  s0.quantity as component_quantity_in_kit
FROM 
  s0
    LEFT JOIN sms.product p ON s0.product_id = p.id
    LEFT JOIN sms.product p2 ON s0.component_product_id = p2.id
WHERE 
  p.product_number not like 'ZPB%'
),

s2 as (
SELECT
  p.product_number,
  p.edi_number,
  b.zone || '-' || b.position || '-' || b.shelf as component_bin,
  sum (s.quantity_available) as Qty_avail_SH
FROM
  sms.stock s
    LEFT JOIN sms.product p ON p.id = s.product_id
    LEFT JOIN sms.bin b ON b.id = s.container_id and s.container_type = 1
WHERE
  s.stock_type = 1
  and s.inventory_type = 3
  and s.location_type = 1
  and s.location_id = 370
  and s.container_type = 1
  and s.quantity_available > 0
  and b.zone like 'R%'
GROUP BY
  p.product_number,
  p.edi_number,
  b.zone || '-' || b.position || '-' || b.shelf),
  
s3 as (
SELECT 
  p.product_number, p.edi_number, p.description,
  case when stock_type = 3 then sum(s.quantity_on_hand) end as Valid,
  case when stock_type = 4 then sum(s.quantity_on_hand) end as Invalid
FROM 
  sms.stock s
    LEFT JOIN sms.product p ON s.product_id = p.id
    LEFT JOIN sms.bin b ON b.id = s.container_id and s.container_type = 1
WHERE
  s.inventory_type = 3
  and stock_type in (3,4)
  and s.location_id = 370 
  and s.location_type = 1
  and b.zone like 'G%'
  --and product_id = 688800
group by
  p.product_number,p.edi_number, p.description,
  s.stock_type),

s4 as (
Select
  s3.product_number as kit_prod_number, 
  s3.edi_number as kit_edi, 
  s3.description as kit_description, 
  coalesce(sum(s3.valid),0) as valid,
  coalesce(sum (s3.invalid),0) as invalid,
  case 
    when sum(s3.valid) is null then 1.0
    when sum(s3.invalid) is null then 0.0
      else sum (s3.invalid)/ (sum(s3.valid)+ sum (s3.invalid)) end as Percent_invalid
from
s3
Group by 
  product_number, edi_number, description),

s5 as (
SELECT 
  p2.product_number as kit_prod_number,
  p2.edi_number as kit_edi,
  p2.description as kit_description,
  ps.serial_number,
  b.zone || '-' || b.position || '-' || b.shelf as kit_bin,
  p.product_number as Component_product_number,
  p.edi_number as component_edi,
  p.description as component_description,
  sum (s.quantity_available) as quantity_available
FROM
  sms.stock s 
  LEFT JOIN sms.product p on s.product_id = p.id
  LEFT JOIN sms.stock s2 On s.container_id = s2.id and s.container_type = 2
  LEFT JOIN sms.product p2 on s2.product_id = p2.id
  left join sms.product_serial ps on s2.serial_id = ps.id
  LEFT JOIN sms.bin b on s2.container_id = b.id and s2.container_type = 1
where 
  s.location_type = 1
  and s.location_id = 370
  and s.stock_type = 2
  and s.container_type =2
  and p2.product_number is not null
GROUP BY
  p2.product_number ,
  p2.edi_number,
  p2.description,
  ps.serial_number,
  b.zone || '-' || b.position || '-' || b.shelf ,
  p.product_number ,
  p.edi_number ,
  p.description),

s6 as (
SELECT
  prod_id,
  sum (invntry_on_hand_qty - invntry_on_reserve_qty - invntry_unavailable_qty) as qty_avail_e01
FROM
  dcs.invntry_snpsht_dcs_daily
WHERE
  snapshot_dte = current_date
  and warehouse_id = 'E01'
GROUP BY
  prod_id),

s7 as (  --may pull this out, probably not needed
SELECT DISTINCT
    p.product_number as kit_product_number,
    p.edi_number as Kit_edi,
    ps.serial_number
FROM
  sms.stock s
    LEFT JOIN sms.product p ON s.product_id = p.id
    LEFT JOIN sms.product_serial ps ON ps.id = s.serial_id
    LEFT JOIN sms.bin b ON b.id = s.container_id and s.container_type = 1
WHERE
  s.inventory_type = 3
  and s.stock_type in (3,4)
  and s.location_type = 1
  and s.location_id = 370
  and b.zone like 'G%'),

s8 as (
SELECT Distinct
  p2.product_number as kit_prod_number,
  p2.edi_number as kit_edi,
  p2.description as kit_description,
  b.zone || '-' || b.position || '-' || b.shelf as kit_bin
FROM
  sms.stock s2 
  LEFT JOIN sms.product p2 on s2.product_id = p2.id
  LEFT JOIN sms.bin b on s2.container_id = b.id and s2.container_type = 1
where 
  s2.location_type = 1
  and s2.location_id = 370
  and s2.stock_type in (3,4)
  and p2.product_number is not null
  and b.zone like 'G%'),


s9 as (
SELECT
  s1.kit_product_number,
  s1.kit_edi,
  s1.kit_description,
  s7.serial_number,
  s1.component_product_number,
  s1.component_prod_id,
  s1.component_description,
  s1.component_quantity_in_kit  
FROM
  s1
    LEFT JOIN s7 ON s1.kit_product_number = s7.kit_product_number)

SELECT
  s9.kit_product_number,
  s9.kit_edi,
  s9.kit_description,
  s9.serial_number,
  s8.kit_bin,
  s9.component_product_number,
  s9.component_prod_id,
  s9.component_description,
  s9.component_quantity_in_kit as component_quantity_in_kit_std,
  coalesce (s5.quantity_available,0) as qty_in_kit,
  s2.qty_avail_sh,
  s2.component_bin,
  s6.qty_avail_e01,
  s4.percent_invalid,
  sum(s9.component_quantity_in_kit - coalesce (s5.quantity_available,0)) over (partition by s9.kit_product_number, s9.serial_number) as Pieces_missing
FROM
  s9
    LEFT JOIN s5 ON s9.kit_product_number = s5.kit_prod_number and s9.serial_number = s5.serial_number and s9.component_prod_id = s5.component_edi
    LEFT JOIN s4 ON s9.kit_product_number = s4.kit_prod_number and s9.kit_edi = s4.kit_edi
    LEFT JOIN s2 ON s9.component_product_number = s2.product_number and s9.component_prod_id = s2.edi_number
    LEFT JOIN s6 on s9.component_prod_id = s6.prod_id
    LEFT JOIN s8 ON s9.kit_product_number = s8.kit_prod_number
WHERE
  s8.kit_bin is not null
ORDER BY
  s4.percent_invalid DESC,
  s9.kit_product_number,
  s9.serial_number,
  s9.component_product_number

--Developed by PKS