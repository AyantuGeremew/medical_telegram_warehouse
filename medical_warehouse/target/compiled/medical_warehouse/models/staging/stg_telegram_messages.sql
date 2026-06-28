WITH source AS (
    SELECT * FROM raw.telegram_messages
)

SELECT
    message_id,
    channel_name,

    message_date::timestamp AS message_date,

    text AS message_text,

    COALESCE(views, 0) AS views,
    COALESCE(forwards, 0) AS forwards,

    media_type,

    CASE
        WHEN image_path IS NOT NULL THEN TRUE
        ELSE FALSE
    END AS has_image,

    LENGTH(text) AS message_length

FROM source
WHERE text IS NOT NULL
  AND text <> ''