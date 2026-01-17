# WhatsApp Bot Setup Guide

This guide will help you connect your local Insurance Agent to WhatsApp using **Twilio** and **ngrok**.

## Prerequisites
- **Twilio Account**: [Sign up here](https://www.twilio.com/try-twilio) (Free trial is fine).
- **ngrok**: [Download here](https://ngrok.com/download) (To expose your local server to the internet).

## Step 1: Set up Twilio Sandbox
1.  Log in to your Twilio Console.
2.  Go to **Messaging** > **Try it out** > **Send a WhatsApp message**.
3.  Follow the instructions to activate the Sandbox (usually sending a code like `join <word>` to a specific number).
4.  **Keep this page open**, you will need it for Step 3.

## Step 2: Start Your Local Server & ngrok
1.  **Start the Bot**:
    Make sure your FastAPI server is running.
    ```bash
    ./run_services.sh
    ```
    (This starts the API on port `8000`).

2.  **Expose with ngrok**:
    Open a *new* terminal window and run:
    ```bash
    ngrok http 8000
    ```
3.  **Copy the Forwarding URL**:
    Based on your screenshot, your URL is:
    `https://unspeakably-chordamesodermal-lesha.ngrok-free.dev`

## Step 3: Configure Twilio Webhook
1.  Go back to the **Twilio Console** > **Messaging** > **Settings** > **WhatsApp Sandbox Settings**.
2.  Find the **"When a message comes in"** field.
3.  Paste your ngrok URL and append `/webhook`:
    ```
    https://unspeakably-chordamesodermal-lesha.ngrok-free.dev/webhook
    ```
    *(Make sure it ends with `/webhook`)*.
4.  Set the method to **POST**.
5.  Click **Save**.

## Step 4: Configure Environment Variables
1.  Open your `.env` file in the project folder.
2.  Add your Twilio credentials:
    - **Go to the Twilio Console Dashboard** (the page in your screenshot).
    - **Scroll down** to the "Account Info" section.
    - Copy the **Account SID**.
    - Click "Show" to reveal and copy the **Auth Token**.
    
    Update your `.env` file:
    ```env
    TWILIO_ACCOUNT_SID=your_sid_here
    TWILIO_AUTH_TOKEN=your_token_here
    ```
3.  Restart your server (`Ctrl+C` and `./run_services.sh`) to load the new keys.

## Step 5: Test It!
1.  Open WhatsApp on your phone.
2.  Send a message (e.g., "Hi") to the Twilio Sandbox number.
3.  You should receive the "🙏 Namaste!" welcome message from your bot.
4.  Try sending a voice note!

## Troubleshooting
- **404 Error**: Did you forget to add `/webhook` to the end of the URL in Twilio?
- **500 Error**: Check your terminal logs for Python errors.
- **No Response**: Ensure ngrok is still running.
- **Fortinet / SSL Error in Browser**:
    - This is a local network restriction in your office.
    - **It DOES NOT affect Twilio.** Twilio is outside your network and can reach ngrok fine.
    - **DO NOT** try to open the link in your browser. It won't work.
    - **DO** paste the link into Twilio and send a message from your **phone**. That is the real test!
