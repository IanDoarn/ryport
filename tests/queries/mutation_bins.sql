with s1 as (
SELECT
    snapshot_date,
    dcs_warehouse,
    name,
    location_name,
    location_acct_number,
    bin, product_number,
    edi_number,
    description,
    lot_number,
    serial_number,
    bus_days_this_month,
    max_charge,
    container_type,
    container_id,
    row_number () over (partition by dcs_warehouse, location_acct_number, Location_name, product_number, lot_number, serial_number, bin order by snapshot_date desc) as record_number
FROM
    loaners.debit_bin_report_daily_snapshot),

s2 as (
SELECT
    snapshot_date,
    dcs_warehouse,
    name,
    location_name,
    location_acct_number,
    bin, product_number,
    edi_number,
    description,
    lot_number,
    serial_number,
    bus_days_this_month,
    max_charge,
    container_type,
    container_id,
    record_number,
    row_number () over (partition by dcs_warehouse, location_acct_number, Location_name, product_number, lot_number, serial_number, bin order by snapshot_date asc, record_number desc) as Days_in_bin
FROM
    s1),

s3 as (
SELECT
    snapshot_date,
    dcs_warehouse,
    name,
    location_name,
    location_acct_number,
    bin, product_number,
    edi_number,
    description,
    lot_number,
    serial_number,
    bus_days_this_month,
    max_charge,
    container_type,
    container_id,
    record_number,
    days_in_bin,
    days_in_bin * 25 as non_adjusted_total_charge,
    case
        when days_in_bin * 25 > max_charge then max_charge
            else days_in_bin * 25 end as adjusted_total_charge,
    case
        when days_in_bin > bus_days_this_month then bus_days_this_month * 25.0
            else days_in_bin * 25.0 end as Month_charge
FROM
    s2)

SELECT
    snapshot_date,
    dcs_warehouse,
    name,
    location_name,
    location_acct_number,
    bin, product_number,
    edi_number,
    description,
    lot_number,
    serial_number,
    bus_days_this_month,
    days_in_bin,
    max_charge,
    non_adjusted_total_charge,
    adjusted_total_charge,
    month_charge,
    case
        when days_in_bin > 9 and  adjusted_total_charge = max_charge then 'Yes'
            else 'No' end as transfer_flag
FROM
    s3
where
    record_number = 1 and snapshot_date = current_date
    and Case
        when days_in_bin > 9 and  adjusted_total_charge = max_charge then 'Yes'
            else 'No' end = 'Yes'
ORDER BY
    dcs_warehouse