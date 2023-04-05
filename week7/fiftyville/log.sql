-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Select a crime scene report that matches the date and the location.
SELECT description
FROM crime_scene_reports
WHERE year = 2021
    AND month = 7
    AND day = 28
    AND street = 'Humphrey Street';

-- Select interviews about crime.
SELECT transcript
FROM interviews
WHERE year = 2021
    AND month = 7
    AND day = 28;

-- The crime took place at 10:15 am and within 10 mins, the thief took off from the bakery parking lot.
-- Select people who left bakery parking lot around 10:15 am.
SELECT DISTINCT (people.name)
FROM people
JOIN bakery_security_logs
ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
    AND bakery_security_logs.month = 7
    AND bakery_security_logs.day = 28
    AND bakery_security_logs.hour = 10
    AND bakery_security_logs.minute > 15
    AND bakery_security_logs.minute <= 25
    AND bakery_security_logs.activity = 'exit'
ORDER BY people.name;

-- | Barry   |
-- | Bruce   |
-- | Diana   |
-- | Iman    |
-- | Kelsey  |
-- | Luca    |
-- | Sofia   |
-- | Vanessa |

-- Select people who withdrew money from ATM at Leggett Street.
SELECT DISTINCT (people.name)
FROM people
JOIN bank_accounts
ON bank_accounts.person_id = people.id
JOIN atm_transactions
ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.year = 2021
     AND atm_transactions.month = 7
     AND atm_transactions.day = 28
     AND atm_transactions.atm_location = 'Leggett Street'
     AND atm_transactions.transaction_type = 'withdraw'
ORDER BY people.name;

-- | Bruce   |
-- | Diana   |
-- | Iman    |
-- | Luca    |

-- The thief called someone and purchase the earliest flight for tomorrow.
-- Select people who purchase the earliest flight for tomorrow.
SELECT DISTINCT (people.name)
FROM people
JOIN passengers
ON passengers.passport_number = people.passport_number
JOIN flights
ON flights.id = passengers.flight_id
WHERE flights.id = (SELECT flights.id
    FROM flights
    JOIN airports
    ON airports.id = flights.origin_airport_id
    WHERE flights.year = 2021
        AND flights.month = 7
        AND flights.day = 29
        AND airports.city = 'Fiftyville'
        ORDER BY flights.hour
        LIMIT 1)
ORDER BY people.name;

-- | Bruce   |
-- | Luca    |

-- Select phone calls that match the date, time, and duration.
SELECT DISTINCT (people.name)
FROM people
JOIN phone_calls
ON phone_calls.caller = people.phone_number
WHERE phone_calls.year = 2021
     AND phone_calls.month = 7
     AND phone_calls.day = 28
     AND phone_calls.duration < 60
ORDER BY people.name;

-- | Bruce   |

-- Thief’s accomplice
SELECT people.name
FROM people
JOIN phone_calls
ON phone_calls.receiver = people.phone_number
WHERE phone_calls.year = 2021
    AND phone_calls.month = 7
    AND phone_calls.day = 28
    AND phone_calls.duration < 60
    AND phone_calls.caller = (SELECT phone_number
    FROM people
    WHERE name = 'Bruce');

-- | Robin   |

-- City thief escaped to
SELECT airports.city
FROM airports
JOIN flights
ON flights.destination_airport_id = airports.id
JOIN passengers
ON passengers.flight_id = flights.id
JOIN people
ON people.passport_number = passengers.passport_number
WHERE people.name = 'Bruce';

-- | New York City   |