insert into gold_ds.dim_users_scd2(
    user_sk ,
    user_id ,
    name ,
    username ,
    email ,
    phone ,
    website ,
    row_hash ,
    effective_start_date ,
    effective_end_date ,
    is_current,
    created_ts ,
    update_ts 
)
select 
generate_uuid() as user_sk,
s.user_id ,
    s.name ,
    s.username ,
    s.email ,
    s.phone ,
    s.website ,
    s.row_hash ,
    current_timestamp() as effective_start_date,
    timestamp('9999-12-31 00:00:00') as effective_end_date,
    TRUE as is_current,
    current_timestamp() as created_ts,
    current_timestamp() as update_ts,
    from `silver_ds.users_scd_source` s
  where not exists(
    select 1 from gold_ds.dim_users_scd2 t
    where t.user_id = s.user_id
  );
  
