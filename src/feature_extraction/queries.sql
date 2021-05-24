/*
 * Data Export
 */

(SELECT 'uuid', 'key_event', 'key_code', 'key_char', 'alt_key', 'ctrl_key', 'shift_key', 'is_bot', 'timestamp')
UNION
(SELECT uuid, key_event, key_code, key_char, alt_key, ctrl_key, shift_key, is_bot, timestamp
INTO OUTFILE '/var/lib/mysql-files/keylog.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM production.KEYSTROKE_METRICS
WHERE key_code NOT IN (8, 9, 13, 17, 18, 20, 37, 38, 39, 40, 46, 49, 59, 91, 173, 186, 187, 191, 219)
ORDER BY uuid, timestamp, key_char);

/*
 * View all characters/counts
 */

 SELECT DISTINCT key_code, key_char, count(key_code) 
 FROM production.KEYSTROKE_METRICS 
 GROUP BY key_code, key_char 
 ORDER BY key_code;