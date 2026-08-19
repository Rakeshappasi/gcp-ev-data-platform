create or replace table silver_ds.users_clean as
select id, trim(name) as name , lower(email) as email , username , phone,website from bronze_ds.users;