select count(*) as total_records from silver_ds.users_clean union all 
select count(*) as total_records from bronze_ds.users;