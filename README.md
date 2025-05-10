# Trading AI Chatbot

This project implements a **proactive AI chatbot** that interacts with a sample trading data file and provides insights like the most profitable trade, total deposits, and loss percentages. The chatbot uses OpenAI's API to process and summarize the trading data.

## Table of Contents

- Requirements
- Setup Instructions
- Running the Project
- How to Use
- Notes

## Requirements

Before you can run the project, you'll need to install the required dependencies. The required libraries are listed below:

- **pandas**: Used for data manipulation and analysis.
- **openai**: The OpenAI API client, used to interact with the GPT model.
- **python-dotenv**: Used to load environment variables, including the OpenAI API key, from the `.env` file.

The requirements.txt file includes all the required libraries.

Setup Instructions


## 1. Unzip the Folder
   You should receive the full project folder. Unzip it and navigate into the folder directory that you named when cloning.

## 2. Install Dependencies
   Once you're inside the project folder, and navigate to the folder named backend open your terminal and install the required dependencies using the command:
   cd ooln-chatbot

```bash
cd backend
pip install -r requirements.txt
```

## 3. Create and Configure .env
   You will need to create an .env file to store your OpenAI API key.
   Inside the chatbot folder, create a file named .env.

   Inside the .env file, add the following:
   ```bash
   OPENAI_API_KEY=your-openai-api-key
   ```

   Replace your-openai-api-key with your actual OpenAI API key. You can get your API key by signing up on the OpenAI platform.

## 4. Prepare Trading Data
   Make sure the Trades_sample.csv file is present inside the backend/data folder. This file contains the trading data that the chatbot will process.

## 5. Verify Folder Structure
   Ensure that your folder structure looks like this:

<img width="196" alt="image" src="https://github.com/user-attachments/assets/64096dd4-952b-4710-9b50-a1f576c75a21" />
 
## Running the Project
Once everything is set up, you can run the chatbot by executing the following command from the ooln-chatbot folder:

```bash
python3 backend/chatbot/chatbot.py
```

OR

```bash
python backend/chatbot/chatbot.py
```

This will start a terminal-based interactive session where you can ask the chatbot questions about your trading data. Simply type a question, and the chatbot will provide a response.

Sample Questions You Can Ask:
"What was my most profitable trade?"

"How much was deposited into the account during the month?"

"What percentage of losses came from options expiring?"

"Can you summarize my most profitable trade?"

To exit the chatbot, simply type exit and press Enter.

How to Use
After running the project, you can interact with the chatbot by typing questions about your trading data.

For example:

"What was my most profitable trade?"
The chatbot will look at the trade data and summarize the most profitable trade based on your inputs.

"How much was deposited into the account during the month?"
The chatbot will give you the total deposit amount for the month.

Notes
The chatbot currently handles basic if-elif cases for questions like "deposit", "most profitable", and "loss percentage".

The chatbot uses OpenAI's API to summarize and respond with insights about your trading data.

Net profit calculations: There is currently a small issue with calculating net profits in cases where there are multiple "Sell to Close" (STC) transactions for a single "Buy to Open" (BTO). This issue needs further investigation.

If you want to expand the chatbot to handle additional queries, you can add more if-elif cases to the chatbot() function.

```

```
