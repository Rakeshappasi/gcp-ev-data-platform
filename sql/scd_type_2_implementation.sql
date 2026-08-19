create or replace table silver_ds.users_scd_source as
with source_data as(
    select 
    cast(id as Int) as user_id,
    trim(name) as name,
    trim(username) as username,
    lower(trim(email)) as email,
    trim(phone) as phone,
    trim(website) as websitr
    from silver_ds.users_clean
)

select user_id,
name,username,email,phone,website,
to_hex(MD5(concat(
    coalesce(name,''),'|',
    coalesce(username,''),'|',
    coalesce(email,''),'|',
    coalesce(phone,''),'|',
    coalesce(website,''),'|',
)))as row_hash from source_data;