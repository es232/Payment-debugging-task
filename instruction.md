# Payment Payout API Debugging Task

## Background

Our backend service provides an API endpoint that calculates merchant payouts based on a list of financial transactions. Recently, several issues have been reported in production, including incorrect payout calculations, missing input validation, and inaccurate monetary calculations.

Your task is to investigate the application, identify the issues, and implement the necessary fixes.

## Problem Statement

The endpoint:

/api/payouts/calculate

is currently not behaving as expected. The implementation contains logic bugs and validation gaps that cause multiple test cases to fail.

You are expected to debug the application and make the endpoint comply with the business requirements described below.

## Business Requirements

### Transaction Handling

The system supports the following transaction types:

* PAYMENT → Add the transaction amount to the merchant payout.
* REFUND → Subtract the transaction amount from the merchant payout.
* DISPUTE → Subtract the transaction amount and apply an additional dispute fee of $15.00.

The dispute fee should also be included in the total fees charged.

### Input Validation

The API should reject invalid requests in the following situations:

* Transaction amount is zero.
* Transaction amount is negative.
* Transactions list is empty.
* Merchant ID does not start with `MERCH_`.

In all of the above cases, the API should return HTTP 400.

### Monetary Precision

Financial calculations must be accurate.

The current implementation uses floating-point arithmetic, which may produce precision errors during payout calculations.

Example:

0.1 + 0.2 = 0.30000000000000004

The application should perform calculations accurately and return values rounded to two decimal places.

## Constraints

* Do not modify the endpoint path.
* Do not change the response keys.
* Do not modify the provided tests.
* Implement all fixes inside `environment/app.py`.

## Success Criteria

Your solution will be considered correct when all provided tests pass successfully.

To run the tests:

```bash
bash tests/test.sh
```

Focus on correctness, validation, and accurate payout calculations.
