CREATE table if not exists gold_ds.dim_users_scd2(
    user_sk string,
    user_id int64,
    name string,
    username string,
    email string,
    phone string,
    website string,
    row_hash string,
    effective_start_date timestamp,
    effective_end_date timestamp,
    is_current bool,
    created_ts timestamp,
    update_ts timestamp,

);