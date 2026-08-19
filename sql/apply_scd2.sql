update gold_ds.dim_users_scd2 t
SET
effective_end_ts = cureent_timestamp(),
update_ts= cureent_timestamp(),
is_current =FALSE
Where t.is_current =TRUE
and exists(
    select 1 from silver_ds.users_scd_source s
    where s.user_id = t.user_id
    and s.row_hash<>t.row_hash<>
);

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
    left join `gold_ds.dim_users_scd2` t on
    s.user_id= t.user_id
    and t.is_current =TRUE
    where t.user_id is null;