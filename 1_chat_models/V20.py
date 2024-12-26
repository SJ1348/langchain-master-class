from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import json
import { z } from "zod";

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o", temperature=0)

# SystemMessage:
#   Message for priming AI behavior, usually passed in as the first of a sequence of input messages.
# HumanMessage:
#   Message from a human to the AI model.

from typing import Optional
from langchain_core.pydantic_v1 import BaseModel, Field


const zodSchema = z.object({
  name: z.string().describe("Company name"),
  buy_price: z.number().describe("buy_price"),
  sell_price: z.number().describe("sell_price"),
  
})



Prompt = """
Structure of the Data:
Company-Level: Each entry in the dataset represents a company, identified by its Company name.
Stock Prices: For each company, there is an array of daily stock price records (StockPrices), each with the following attributes:
Day: The day number (from 1 to 10) within the time frame.
High: The highest price of the stock on that day.
Low: The lowest price of the stock on that day.
Open: The price at which the stock started trading on that day.
Close: The price at which the stock closed trading on that day.

Context : 
Green Candle = The day where the open price is lower than the close price.
Red Candle = The day where the close price is higher than the open price.

Operation :
I want to filter out some of the companies from this list which satisfy my buying criteria : 
1. Continuous all green candles without a red candle in between. This is the day range for which the below criteria should meet.
2. From the lowest price of Low of the green candles to the highest price of high of the green candles the difference should be more than 20%.
3. The last day price of the stock should be below the lowest level from point 2.

Output : 
Company Name, Buy Price (day 10 close price), Sell Price (highest price of high calculated in point 2)

Input Dataset : 
data = [
    {
        "Company": "Avyaya",
        "StockPrices": [
            {"Day": 1, "High": 120.0, "Low": 115.0, "Open": 116.5, "Close": 118.0},
            {"Day": 2, "High": 130.0, "Low": 121.0, "Open": 122.0, "Close": 129.5},
            {"Day": 3, "High": 140.0, "Low": 131.5, "Open": 132.0, "Close": 139.0},
            {"Day": 4, "High": 150.5, "Low": 141.0, "Open": 142.5, "Close": 149.0},
            {"Day": 5, "High": 160.0, "Low": 151.0, "Open": 152.5, "Close": 159.0},
            {"Day": 6, "High": 155.5, "Low": 148.5, "Open": 145.0, "Close": 140.0},
            {"Day": 7, "High": 140.0, "Low": 130.0, "Open": 139.5, "Close": 131.5},
            {"Day": 8, "High": 135.5, "Low": 132.5, "Open": 133.0, "Close": 134.0},
            {"Day": 9, "High": 130.0, "Low": 110.5, "Open": 112.5, "Close": 129.5},
            {"Day": 10, "High": 130.5, "Low": 127.5, "Open": 128.0, "Close": 129.0}
        ]
    },
    {
        "Company": "EduTech",
        "StockPrices": [
            {"Day": 1, "High": 120.0, "Low": 115.0, "Open": 116.5, "Close": 118.0},
            {"Day": 2, "High": 122.5, "Low": 116.5, "Open": 118.0, "Close": 119.5},
            {"Day": 3, "High": 124.0, "Low": 117.5, "Open": 119.0, "Close": 121.0},
            {"Day": 4, "High": 125.5, "Low": 119.0, "Open": 120.5, "Close": 122.0},
            {"Day": 5, "High": 127.0, "Low": 120.0, "Open": 122.5, "Close": 124.0},
            {"Day": 6, "High": 128.5, "Low": 121.5, "Open": 123.0, "Close": 125.0},
            {"Day": 7, "High": 130.0, "Low": 123.0, "Open": 124.5, "Close": 126.5},
            {"Day": 8, "High": 131.5, "Low": 124.5, "Open": 126.0, "Close": 128.0},
            {"Day": 9, "High": 133.0, "Low": 126.0, "Open": 127.5, "Close": 129.5},
            {"Day": 10, "High": 134.5, "Low": 127.5, "Open": 129.0, "Close": 131.0}
        ]
    },
    {
        "Company": "TIMKEN",
        "StockPrices": [
            {"Day": 1, "High": 3502.95, "Low": 3351.15, "Open": 3472.0, "Close": 3400.65},
            {"Day": 2, "High": 3519.0, "Low": 3393.85, "Open": 3420.0, "Close": 3500.25},
            {"Day": 3, "High": 3760.0, "Low": 3510.0, "Open": 3510.0, "Close": 3732.70},
            {"Day": 4, "High": 4019.95, "Low": 3676.35, "Open": 3699.0, "Close": 3972.45},
            {"Day": 5, "High": 4288.80, "Low": 4010.0, "Open": 4010.0, "Close": 4201.60},
            {"Day": 6, "High": 4288.0, "Low": 4122.65, "Open": 4209.95, "Close": 4215.40},
            {"Day": 7, "High": 4267.45, "Low": 4151.00, "Open": 4227.0, "Close": 4157.25},
            {"Day": 8, "High": 4817.90, "Low": 4625.1, "Open": 4650.40, "Close": 4712.65},
            {"Day": 9, "High": 3487.95, "Low": 3401.15, "Open": 3474.25, "Close": 3469.85},
            {"Day": 10, "High": 3230.0, "Low": 3162.0, "Open": 3198.80, "Close": 3218.70}
        ]
    },
    {
        "Company": "AKZOINDIA",
        "StockPrices": [
            {"Day": 1, "High": 3925.0, "Low": 3766.60, "Open": 3840.70, "Close": 3800.60},
            {"Day": 2, "High": 4166.95, "Low": 3692.70, "Open": 3817.05, "Close": 3919.35},
            {"Day": 3, "High": 4649.00, "Low": 3875.10, "Open": 3915.90, "Close": 4338.85},
            {"Day": 4, "High": 4349.90, "Low": 41400.00, "Open": 4299.05, "Close": 4212.20},
            {"Day": 5, "High": 3734.90, "Low": 3655.10, "Open": 3734.95, "Close": 3684.65},
            {"Day": 6, "High": 3829.90, "Low": 3740.05, "Open": 3740.05, "Close": 3802.70},
            {"Day": 7, "High": 4559.00, "Low": 3849.00, "Open": 3849.00, "Close": 4402.30},
            {"Day": 8, "High": 4674.00, "Low": 4400.00, "Open": 4405.00, "Close": 4518.50},
            {"Day": 9, "High": 3760.00, "Low": 3630.80, "Open": 3750.00, "Close": 3762.05},
            {"Day": 10, "High": 3550.00, "Low": 3451.55, "Open": 3451.55, "Close": 3484.40}
        ]
    }
]
"""

# Convert the data into a JSON string
messages = [
    # SystemMessage(content=prompt),
    # HumanMessage(content=f"{data_str}"),
    HumanMessage(content=Prompt)
]


const chain = createStructuredOutputChainFromZod(zodSchema, {
  prompt,
  model,
})

# Invoke the model with messages
response = chain.invoke(messages)
print(JSON.stringify(response, null, 2))