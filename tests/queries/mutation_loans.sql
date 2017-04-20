Select * from loaners.debit_policy_daily_snapshot
where snapshot_date = current_date  and transfer_flag = 'yes'