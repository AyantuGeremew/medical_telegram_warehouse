SELECT
    message_id,

    c.channel_key,
    DATE(m.message_date) AS date_key,

    m.message_text,
    m.message_length,
    m.views,
    m.forwards,
    m.has_image

FROM {{ ref('stg_telegram_messages') }} m
LEFT JOIN {{ ref('dim_channels') }} c
    ON m.channel_name = c.channel_name
    