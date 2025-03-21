from transformers import BertForQuestionAnswering, BertTokenizer
import torch
import os
import json
import urllib.request
import ssl
from dotenv import load_dotenv

load_dotenv()

rest_url = os.getenv("REST_URL")
api_key = os.getenv("API_KEY")

if not rest_url:
    rest_url = 'https://ai-test-run-promptflow-test.eastus.inference.ml.azure.com/score'

if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


headers = {'Content-Type':'application/json', 'Accept': 'application/json', 'Authorization':('Bearer '+ api_key)}

context = "1. How can I contact customer service? - You can contact customer service via phone, email, or live chat on our website. Our support team is available 24/7. 2. What are your customer service hours? - Our customer service team is available Monday to Friday from 8 AM to 8 PM (EST) and Saturday to Sunday from 9 AM to 6 PM (EST). 3. How long does it take to receive a response from customer service? - We aim to respond to all inquiries within 24 hours. Live chat and phone support provide immediate assistance. 4. How can I track my order? - You can track your order by logging into your account and clicking on \"Order History.\" A tracking number will be provided for shipped items. 5. What should I do if my order hasn’t arrived? - If your order hasn’t arrived within the expected timeframe, check your tracking number. If there is an issue, contact customer service for assistance. 6. Can I cancel or modify my order after placing it? - Orders can be modified or canceled within 24 hours of placement. After this period, changes may not be possible. 7. What is your return policy? - You can return items within 30 days of purchase if they are in their original condition. Some items, such as final sale items, may not be eligible for return. 8. How do I request a refund? - Refunds can be requested by contacting customer service. Once approved, refunds are processed within 5-7 business days. 9. What payment methods do you accept? - We accept credit cards, debit cards, PayPal, Apple Pay, and Google Pay. 10. How do I change my account details? - You can update your account details by logging into your account and navigating to \"Account Settings.\" 11. How do I reset my password? - Click on \"Forgot Password\" on the login page and follow the instructions sent to your email. 12. Do you offer price matching? - We offer price matching for identical items from authorized retailers within 14 days of purchase. 13. What should I do if I receive a damaged or defective product? - If you receive a damaged or defective product, contact customer service within 7 days to request a replacement or refund. 14. Can I speak to a live agent? - Yes! Our live agents are available via phone and chat during business hours. 15. How do I subscribe or unsubscribe from promotional emails? - You can manage your email preferences in your account settings or by clicking \"Unsubscribe\" at the bottom of any promotional email."
data = {}
data["context"] = context

choice_set = ("yes", "no")

while True:
    choice = input("Do you want to ask a question?").strip()
    if choice.lower() == "yes":
        question = input("What question do you want to ask?").strip()

        data["question"]=question
        body = str.encode(json.dumps(data))

        req = urllib.request.Request(rest_url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            print(result)
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))



    elif choice.lower() == "no":
        break

    else:
        print("Please enter a valid response")

print("Exiting app...")