from openai import OpenAI
from trade_analyzer import total_deposits, get_most_profitable_trade, calculate_oexp_loss_percentage, get_all_trades
from data_loader import load_trading_data
from dotenv import load_dotenv
import os

load_dotenv()

class TextSummarizer:
    openai_model = "gpt-3.5-turbo"

    def __init__(self):
        self.apikey = os.environ.get("OPENAI_API_KEY")

    def fetch_api_key(self):
        pass

    def average_sentences(self, list_of_sentences):
        client = OpenAI(api_key=self.apikey)
        prompt = "Here is a list of multiple sentences that I want you to summarize and rewrite as a single sentence. The sentences are separated by newline characters:\n{sentences}"
        formatted_prompt = prompt.format(sentences="\n".join(list_of_sentences))

        completion = client.chat.completions.create(
            model=self.openai_model,
            messages=[
                {"role": "system", "content": "You are an assistant that is able to read several sentences and then combine them into a single summarized sentence. The sentences will be sent to you with a new line character \\n separating them. You will return a single sentence."},
                {"role": "user", "content": formatted_prompt}
            ],
            max_tokens=150
        )

        summarized_sentence = completion.choices[0].message.content
        client.close()

        return summarized_sentence

df = load_trading_data("../data/Trades_sample.csv")
trades = get_all_trades(df)

def ask_openai(question, context=""):
    prompt = f"Context: {context}\n\nQuestion: {question}\nAnswer:"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[
            {"role": "system", "content": "You are an AI trading assistant who helps summarize trade data and provide insights."},
            {"role": "user", "content": question}
        ],
        max_tokens=150
    )
    
    return response.choices[0].message.content.strip()

def chatbot(question):
    question = question.strip().lower()

    if "most profitable" in question:
        most_profitable_trade = get_most_profitable_trade(trades)
        
        instrument = most_profitable_trade['instrument']
        net_profit = most_profitable_trade['net_profit']
        description = most_profitable_trade['description']
        date = most_profitable_trade['date']
        quantity = most_profitable_trade['quantity']
        
        list_of_sentences = [
            f"The most profitable trade was made on {date}.",
            f"The instrument traded was {instrument}.",
            f"The trade description is: {description}.",
            f"The net profit from this trade was ${net_profit:.2f}.",
            f"The quantity of trades executed was {quantity}."
        ]
        
        summarizer = TextSummarizer()
        summarized_trade = summarizer.average_sentences(list_of_sentences)
        
        return f"Summary: {summarized_trade}"

    elif "deposit" in question:
        total_deposit_amount, deposit_list = total_deposits(df)

        list_of_sentences = [
            f"The Total Deposit amount for the month was ${total_deposit_amount:.2f}.",
            f"There were {len(deposit_list)} deposit transactions recorded."
        ]

        summarizer = TextSummarizer()
        summarized_deposit_info = summarizer.average_sentences(list_of_sentences)

        return f"Deposit Summary: {summarized_deposit_info}\nDetails: {deposit_list.to_string(index=False)}"

    elif "loss percentage" in question:

        oexp_loss_percentage, oexp_loss_trades = calculate_oexp_loss_percentage(trades)

        if oexp_loss_trades:
            summaries = []  
            
            for trade in oexp_loss_trades:
                
                instrument = trade['instrument']
                description = trade['description']
                quantity = trade['quantity']

                list_of_sentences = [
                    f"The instrument for this OEXP loss trade was {instrument}.",
                    f"The trade description is: {description}.",
                    f"The quantity of trades executed was {quantity}."
                    f"The Percentage of loss from OEXP is {oexp_loss_percentage:.2f}"
                ]

                summarizer = TextSummarizer()
                summarized_trade = summarizer.average_sentences(list_of_sentences)

                summaries.append(summarized_trade)

            all_summaries = "\n".join(summaries)
            return f"Summary of OEXP Loss Trades:\n{all_summaries}"

        else:
            return f"No OEXP loss trades found. Percentage of Losses from OEXP: {oexp_loss_percentage:.2f}%"

    elif "advice" in question:

        advice = ask_openai(question)
        return f"Risk Management Advice: {advice}"

    else:
        return "Sorry, I didn't understand that question. Please ask about deposits, profitable trades, loss percentages, or risk advice."

def main():
    print("Welcome to the Trading AI Chatbot!")
    print("You can ask questions about deposits, most profitable trades, loss percentages, or risk advice.")
    
    while True:
        question = input("Ask a question: ").strip()
        if question.lower() == "exit":
            break
        
        answer = chatbot(question)
        print(answer)

if __name__ == "__main__":
    main()
