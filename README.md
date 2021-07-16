# HomeSystem

This repo includes the code for the RPi Server that holds all of the HomeSystem data and is also used as a home page for the whole project with links to the other project repos.

## To-Do's
- [x] Telegram bot to send notifications to users.
- [x] Telegram Bot to receive and respond to messages from users.
- [x] Flask Server to receive HTTP POST requests.
- [ ] Flask Server to receive HTTP GET requests.
- [ ] All incoming requests from Flask and Telegram are sent to a main file for processing.
- [ ] All outgoing requests and messages are sent from main.py. Example Scenario: HS_Bot.py file recieves a command request for the time, it then sends a request via the Data Interchange including the chat id that the request came from. main.py acts opon the request (Gets the date and time) and sends a message to the chat id obtained earlier. (This is an alternative to sending a request back to HS_Bot.py and that file sending a response.)
- [ ] Ability to make HTTP requests.
- [ ] Ability to save files to a directory tree.

## Other Project Repositories
(Coming in near future)