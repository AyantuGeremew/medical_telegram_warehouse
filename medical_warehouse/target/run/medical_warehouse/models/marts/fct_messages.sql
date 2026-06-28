
  
    

  create  table "medical_db"."analytics"."fct_messages__dbt_tmp"
  
  
    as
  
  (
    SELECT
    message_id,

    c.channel_key,
    DATE(m.message_date) AS date_key,

    m.message_text,
    m.message_length,
    m.views,
    m.forwards,
    m.has_image

FROM "medical_db"."analytics"."stg_telegram_messages" m
LEFT JOIN "medical_db"."analytics"."dim_channels" c
    ON m.channel_name = c.channel_name
  );
  