
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  SELECT *
FROM "medical_db"."analytics"."stg_telegram_messages"
WHERE message_date > CURRENT_TIMESTAMP
  
  
      
    ) dbt_internal_test