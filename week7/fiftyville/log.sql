-- Fiftyville Mystery - July 28, 2025
-- Duck stolen on Humphrey Street
-- Need to find: thief, where they went, who helped them

-- Okay first let's see what we're working with
.schema

-- Look for the crime report from that day on Humphrey Street
SELECT description
FROM crime_scene_reports
WHERE year = 2025
AND month = 7
AND day = 28
AND street = 'Humphrey Street';

-- Check if anyone was interviewed that day
SELECT name, transcript
FROM interviews
WHERE year = 2025
AND month = 7
AND day = 28;

-- Witnesses said the thief left the bakery around 10:15-10:25 AM
-- Let's check who left during that time
SELECT license_plate, activity, hour, minute
FROM bakery_security_logs
WHERE year = 2025
AND month = 7
AND day = 28
AND hour = 10
AND minute >= 15
AND minute <= 25;

-- Someone mentioned the thief hit up an ATM on Leggett Street that morning
SELECT account_number, amount
FROM atm_transactions
WHERE year = 2025
AND month = 7
AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

-- Witness heard thief on the phone for less than a minute
-- Thief was buying a plane ticket from whoever they called
SELECT caller, receiver, duration
FROM phone_calls
WHERE year = 2025
AND month = 7
AND day = 28
AND duration < 60;

-- Thief took earliest flight out on July 29
-- Let's find that flight
SELECT id, destination_airport_id, hour, minute
FROM flights
WHERE origin_airport_id = (
    SELECT id FROM airports WHERE city = 'Fiftyville'
)
AND year = 2025
AND month = 7
AND day = 29
ORDER BY hour, minute
LIMIT 1;

-- What city is that?
SELECT city
FROM airports
WHERE id = (
    SELECT destination_airport_id
    FROM flights
    WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
    AND year = 2025
    AND month = 7
    AND day = 29
    ORDER BY hour, minute
    LIMIT 1
);

-- Now let's find who was on that flight
SELECT passport_number
FROM passengers
WHERE flight_id = (
    SELECT id
    FROM flights
    WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
    AND year = 2025
    AND month = 7
    AND day = 29
    ORDER BY hour, minute
    LIMIT 1
);

-- Alright, putting it together
-- Need someone who:
-- - withdrew from Leggett Street ATM
-- - left bakery parking lot between 10:15-10:25
-- - made a call under 60 seconds
-- - was on that early flight

SELECT DISTINCT people.name
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2025
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = 'Leggett Street'
AND atm_transactions.transaction_type = 'withdraw'
AND people.license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2025
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute >= 15
    AND minute <= 25
    AND activity = 'exit'
)
AND people.phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE year = 2025
    AND month = 7
    AND day = 28
    AND duration < 60
)
AND people.passport_number IN (
    SELECT passport_number
    FROM passengers
    WHERE flight_id = (
        SELECT id
        FROM flights
        WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
        AND year = 2025
        AND month = 7
        AND day = 29
        ORDER BY hour, minute
        LIMIT 1
    )
);

-- Who did the thief call? That's the accomplice
-- First get the thief's phone number
SELECT phone_number
FROM people
JOIN bank_accounts ON people.id = bank_accounts.person_id
JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2025
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = 'Leggett Street'
AND atm_transactions.transaction_type = 'withdraw'
AND people.license_plate IN (
    SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2025
    AND month = 7
    AND day = 28
    AND hour = 10
    AND minute >= 15
    AND minute <= 25
    AND activity = 'exit'
)
AND people.phone_number IN (
    SELECT caller
    FROM phone_calls
    WHERE year = 2025
    AND month = 7
    AND day = 28
    AND duration < 60
)
AND people.passport_number IN (
    SELECT passport_number
    FROM passengers
    WHERE flight_id = (
        SELECT id
        FROM flights
        WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
        AND year = 2025
        AND month = 7
        AND day = 29
        ORDER BY hour, minute
        LIMIT 1
    )
);

-- Now find who they called
SELECT name
FROM people
WHERE phone_number = (
    SELECT receiver
    FROM phone_calls
    WHERE year = 2025
    AND month = 7
    AND day = 28
    AND duration < 60
    AND caller = (
        SELECT phone_number
        FROM people
        JOIN bank_accounts ON people.id = bank_accounts.person_id
        JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
        WHERE atm_transactions.year = 2025
        AND atm_transactions.month = 7
        AND atm_transactions.day = 28
        AND atm_transactions.atm_location = 'Leggett Street'
        AND atm_transactions.transaction_type = 'withdraw'
        AND people.license_plate IN (
            SELECT license_plate
            FROM bakery_security_logs
            WHERE year = 2025
            AND month = 7
            AND day = 28
            AND hour = 10
            AND minute >= 15
            AND minute <= 25
            AND activity = 'exit'
        )
        AND people.phone_number IN (
            SELECT caller
            FROM phone_calls
            WHERE year = 2025
            AND month = 7
            AND day = 28
            AND duration < 60
        )
        AND people.passport_number IN (
            SELECT passport_number
            FROM passengers
            WHERE flight_id = (
                SELECT id
                FROM flights
                WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
                AND year = 2025
                AND month = 7
                AND day = 29
                ORDER BY hour, minute
                LIMIT 1
            )
        )
    )
);
