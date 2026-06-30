{{ config(materialized='table') }}

SELECT

    fm.message_id,

    fm.channel_key,

    fm.date_key,

    yd.detected_objects AS detected_class,

    yd.confidence_score,

    yd.image_category

FROM {{ ref('fct_messages') }} fm

LEFT JOIN {{ ref('yolo_detections') }} yd

ON fm.message_id = yd.message_id