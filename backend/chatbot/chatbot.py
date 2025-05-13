import numpy as np
from openai import OpenAI
from trade_analyzer import total_deposits, get_most_profitable_trade, calculate_oexp_loss_percentage, get_all_trades
from data_loader import load_trading_data
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load trading data
df = load_trading_data("../data/Trades_sample.csv")
trades = get_all_trades(df)

# Define intent examples for embedding comparison
intent_examples = {
    "most_profitable": "What was the most profitable trade?",
    "deposits": "How much money was deposited this month?",
    "oexp_loss": "What percent of losses came from options expiring?",
    "advice": "What advice would you give to improve trading performance?"
}

# Embedding + similarity functions
def get_embedding(text, client):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Main chatbot logic
def chatbot(question):
    question = question.strip()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Embed user's question
    question_embedding = get_embedding(question, client)

    # Find best matching intent
    best_intent = None
    highest_score = -1
    for key, sample in intent_examples.items():
        intent_embedding = get_embedding(sample, client)
        score = cosine_similarity(question_embedding, intent_embedding)
        if score > highest_score:
            highest_score = score
            best_intent = key

    # Reject unclear questions
    MIN_SIMILARITY_THRESHOLD = 0.80
    if highest_score < MIN_SIMILARITY_THRESHOLD:
        return "Sorry, I couldn't understand your question. Please try asking about trades, deposits, or losses."

    # Intent-based routing
    if best_intent == "most_profitable":
        trade = get_most_profitable_trade(trades)
        return (
            f"Most Profitable Trade:\n"
            f"Date: {trade['date']}\n"
            f"Instrument: {trade['instrument']}\n"
            f"Description: {trade['description']}\n"
            f"Net Profit: ${trade['net_profit']:.2f}\n"
            f"Quantity: {trade['quantity']}"
        )

    elif best_intent == "deposits":
        total, deposit_list = total_deposits(df)
        deposit_info = deposit_list.to_string(index=False)
        return (
            f"Total Deposits for the Month: ${total:.2f}\n"
            f"Number of Deposits: {len(deposit_list)}\n\n"
            f"Deposit Details:\n{deposit_info}"
        )

    elif best_intent == "oexp_loss":
        percent, oexp_trades = calculate_oexp_loss_percentage(trades)
        if not oexp_trades:
            return f"No OEXP loss trades found. Percentage: {percent:.2f}%"

        summary_lines = [
            f"{trade['instrument']} | {trade['description']} | Qty: {trade['quantity']} | "
            f"Date: {trade['date']} | Loss: ${abs(trade['net_profit']):.2f}"
            for trade in oexp_trades
        ]
        return (
            f"Percentage of Losses from OEXP: {percent:.2f}%\n"
            f"Summary of OEXP Loss Trades:\n" + "\n".join(summary_lines)
        )

    elif best_intent == "advice":
        # Convert trade summaries into text chunks
        trade_summaries = []
        for trade in trades:
            line = (
                f"{trade['date']} | {trade['instrument']} | {trade['description']} | "
                f"Qty: {trade['quantity']} | Net: ${trade['net_profit']:.2f}"
            )
            trade_summaries.append(line)

        # Join them into a single context block
        trade_context = "\n".join(trade_summaries)

        # Prompt GPT to generate advice
        prompt = (
            "Here is a summary of a trader's activity. "
            "Based on this, give 2–3 clear and constructive suggestions to improve trading performance, "
            "such as reducing risk, timing trades better, or avoiding common mistakes.\n\n"
            f"{trade_context}"
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a financial trading assistant who gives advice."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )

        return "Trading Advice:\n" + response.choices[0].message.content.strip()

    return "Sorry, I didn't understand that question. Please ask about deposits, profitable trades, or loss percentages."

# Run chatbot
def main():
    print("Welcome to the Trading AI Chatbot!")
    print("You can ask questions like:\n- Most profitable trade\n- How much was deposited?\n- Losses from expiry?")
    while True:
        question = input("\nAsk a question (or type 'exit'): ").strip()
        if question.lower() == "exit":
            break
        print(chatbot(question))

if __name__ == "__main__":
    main()
