from ai_assistant import generate_ai_explanation

response = generate_ai_explanation(

    pair="BTCINR",

    signal="SHORT",

    rsi=34,

    market_state="BEARISH",

    price=6870000
)

print("\n")
print(response)
print("\n")