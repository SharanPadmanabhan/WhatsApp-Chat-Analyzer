# Whatsapp Chat Analyzer

### Introduction

<p align="justify">
The advent of smartphones in recent years has altered the definition of mobile phones. The phone is no longer just a communication tool; it has become an integral part of people's communication and daily lives. Various applications made people's lives more enjoyable and made it easier and more efficient to communicate urgent information among people. For example, if there is a meeting or a family gathering, people can communicate that information with the invitation and send detailed information with links and directions using the various applications.

With over 2 billion registered users, WhatsApp is one of the most popular social media services. As a communication tool, WhatsApp is indispensable in people's lives. People use WhatsApp to express their feelings through text messaging. Such communications are inundating them. As a consequence, many of them end the day by spending more time using WhatsApp, and they won't be aware of anything like how many chats they have sent and how much media content they have shared. So, suppose a user wanted to know about the analysis of what they are doing. In that case, he/she could easily just upload the exported chat in this site and view the result which will consist of a detailed report of the user's chats by running a strategic analysis on the chat.

The project's goal is to create a system that analyses text messages and emojis from WhatsApp chats and displays the results, allowing the user to comprehend the actions on their own by simply entering the text data into the website.

</p>

### Steps To Run The Code

> Note: Make sure you have python v3.6 or above installed on your system.

-   Create The virtual environment.

```powershell
    > cd WhatsAppTextAnalyser
    > python -m venv env --prompt 'whatsapp-text-analyser'
```

-   Activate the virtual environment.

```bash
    # Linux / MacOS Users
    $ source ./env/Scripts/activate
```

```powershell
    # Windows Users
    > .\env\Scripts\activate
```

-   Install The Dependencies
```powershell
    > python -m pip install -U -r requirements.txt
```


-   Run The Application

```bash
    # Linux / MacOS Users
    $ streamlit run ./src/app.py
```

```powershell
    # Windows Users
    > streamlit run .\src\app.py
```
