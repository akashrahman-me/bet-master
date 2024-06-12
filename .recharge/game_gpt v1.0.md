Let's play a game together.

## Game description.

-  You've 500 coins.
-  I'll tell you a number
-  You'll try to guess the next number.
-  I'll tell you the acutal next number later.
-  If you see you prediction/guess next number is below or equal to the actual number, you get guess_number \* 100 coins. If not you just lose 100 coins.
-  Again you'll try to predict next number.
-  And so on.

If you think that you can not predict the next number, just predict 1

## Game example and how you should response.

Here's I show you will response, as I know you're just a conversional AI agent.

-  Make sure, you don't include any further explanation in your response.
-  Response by follow the format below.
-  Do not response in a code block, just plain text.

Examples:

```
You:  - Current coins: 500
      - Next Prediction: 3.28

Me:   - Next number: 4

You:  - Congrats! You get 328 coins.
      - Current coins: 828
      - Next Prediction: 2.18

Me:   - Next number: 8

You:  - Congrats! You get 218 coins.
      - Current coins: 1046
      - Next Prediction: 4.73

Me:   - Next number: 1.06

You:  - Bad luck! You loss 100 coins.
      - Current coins: 946
      - Next Prediction: 3.88

Me:   - Next number: 5.64

You:  - Congrats! You loss 388 coins.
      - Current coins: 1334
      - Next Prediction: 2.56

And so on...
```

## Your main goal.

You should try to increase your coins as much as possible by predict the squeence of numbers.

## Game rules.

-  Again remeber, if you think that you can not predict just predict 1.
-  Make sure, your calculation formula is correct.
   -  If win multiply the 100 and prediction number and add it to your current coins
   -  If not win remove 100 from your current coins.

## How to play.

1. Initial Analysis
   Look at the recent sequence of numbers to identify any obvious patterns or trends.
2. Prediction Strategy
   Use a combination of average values and recent trends to make informed guesses.
   Adjust the predictions based on the outcomes of previous rounds.
3. Continuous Adjustment
   Continuously refine the prediction approach based on new numbers provided.
   Given the constraints of this conversation, I would start with a simple heuristic-based approach:

Alright, here's my first turn

-  Next number: 1.77

-  Next number: 1.71
-  Next number: 2.49
-  Next number: 2.77
-  Next number: 1.49
-  Next number: 2.3
-  Next number: 2.7
-  Next number: 7.72
-  Next number: 3.58
-  Next number: 3.86
-  Next number: 3.09
-  Next number: 2.93
-  Next number: 1.5
-  Next number: 7.0
-  Next number: 1.29
-  Next number: 1.03
-  Next number: 1.58
-  Next number: 2.18
-  Next number: 1.69
-  Next number: 4.73
-  Next number: 3.49
-  Next number: 1.12
-  Next number: 1.06
-  Next number: 1.45
-  Next number: 2.52
-  Next number: 19.71
-  Next number: 1.89
-  Next number: 1.38
-  Next number: 1.16
-  Next number: 1.08
-  Next number: 2.38
-  Next number: 2.35

```json
[
   3.28, 3.42, 8.2, 6.59, 11.92, 18.0, 1.01, 1.32, 1.06, 1.4, 1.91, 1.12, 4.63, 22.71, 1.06, 1.16,
   20.8, 11.77, 1.71, 2.49, 2.77, 1.49, 2.3, 2.7, 7.72, 3.58, 3.86, 3.09, 2.93, 1.5, 3.62, 7.0,
   1.29, 1.03, 1.58, 2.18, 1.69, 4.73, 3.49, 1.12, 1.06, 1.45, 2.52, 19.71, 1.89, 1.18, 1.38, 1.16,
   1.08, 2.38, 2.35, 12.5, 3.63, 6.99, 1.0, 1.84, 4.92
]
```
