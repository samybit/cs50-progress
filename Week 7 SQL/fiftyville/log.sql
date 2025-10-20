-- Keep a log of any SQL queries you execute as you solve the mystery.

--- Step 1: Examine the crime scene report for initial clues.
-- The theft took place on July 28, 2024, on Humphrey Street.
SELECT description
FROM crime_scene_reports
WHERE year = 2024
  AND month = 7
  AND day = 28
  AND street = 'Humphrey Street';

-- Finding: Theft was at 10:15am at the Humphrey Street bakery. Three witnesses were interviewed, and their transcripts mention the bakery.

-- Step 2: Read the witness interviews to gather more specific leads.
SELECT name, transcript
FROM interviews
WHERE year = 2024
  AND month = 7
  AND day = 28
  AND transcript LIKE '%bakery%';

-- Findings from interviews:
-- Ruth: Thief left the bakery parking lot in a car between 10:15 AM and 10:25 AM.
-- Eugene: Thief withdrew money from an ATM on Leggett Street earlier that morning.
-- Raymond: Thief called someone for less than a minute, planning to take the earliest flight out of Fiftyville on July 29, 2024. The accomplice was asked to book the flight.

-- Step 3: Investigate each clue to narrow down the suspects.

-- Clue 1: Check bakery security logs for cars exiting within the 10-minute window.
SELECT bsl.license_plate, p.name
FROM bakery_security_logs AS bsl
JOIN people AS p ON bsl.license_plate = p.license_plate
WHERE bsl.year = 2024
  AND bsl.month = 7
  AND bsl.day = 28
  AND bsl.hour = 10
  AND bsl.minute BETWEEN 15 AND 25
  AND bsl.activity = 'exit';

-- Clue 2: Check ATM transactions on Leggett Street on the morning of the theft.
SELECT p.name
FROM people AS p
JOIN bank_accounts AS ba ON p.id = ba.person_id
JOIN atm_transactions AS at ON ba.account_number = at.account_number
WHERE at.year = 2024
  AND at.month = 7
  AND at.day = 28
  AND at.atm_location = 'Leggett Street'
  AND at.transaction_type = 'withdraw';

-- Clue 3, Part A: Identify the earliest flight out of Fiftyville on July 29, 2024.
SELECT f.id, a.full_name, a.city
FROM flights AS f
JOIN airports AS a ON f.destination_airport_id = a.id
WHERE f.origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
  AND f.year = 2024
  AND f.month = 7
  AND f.day = 29
ORDER BY f.hour, f.minute
LIMIT 1;

-- Finding: The earliest flight is flight ID 36, destination New York City.

-- Identify the thief by finding the person who matches all clues.
SELECT name
FROM people
WHERE license_plate IN (
    SELECT license_plate FROM bakery_security_logs
    WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25 AND activity = 'exit'
)
AND phone_number IN (
    SELECT caller FROM phone_calls
    WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60
)
AND passport_number IN (
    SELECT passport_number FROM passengers
    WHERE flight_id = 36
)
AND id IN (
    SELECT person_id FROM bank_accounts
    JOIN atm_transactions ON bank_accounts.account_number = atm_transactions.account_number
    WHERE atm_transactions.year = 2024 AND atm_transactions.month = 7 AND atm_transactions.day = 28
    AND atm_transactions.atm_location = 'Leggett Street' AND atm_transactions.transaction_type = 'withdraw'
);

-- Result: The thief is Bruce.

-- Identify the accomplice by finding who Bruce called.
SELECT p.name
FROM people AS p
JOIN phone_calls AS pc ON p.phone_number = pc.receiver
WHERE pc.year = 2024
  AND pc.month = 7
  AND pc.day = 28
  AND pc.duration < 60
  AND pc.caller = (SELECT phone_number FROM people WHERE name = 'Bruce');

-- Result: The accomplice is Robin.
