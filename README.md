# Twitter News

**Twitter News** is an application that gets the most popular tweets of the moment and makes news based on them.


## Client-Server

This application is divided in 2 parts:
- Client: the responsable of gathering the necessary information to generate the news and then create them.
- Server: the responsable of showing up the created news in a pretty way.


## How does it works? (the technical part)

The client uses **[Selenium](https://www.seleniumhq.org/)** to go through the trending topics of Twitter. Then, using web scrapping, it obtains all the information of each tweet of each trending topic. This information is processed, the hashtags, links and other relevant things are extracted to have a pure text that can be used to generate the news.
After the text analysis is done, the creation of the news starts. The text of the tweets of each trending topic are joined to create a big text that will be used as the base from where the program will create the news. Using the **[Markovify](https://github.com/jsvine/markovify)**'s implementation of **Markov Chains** and **[spaCy](https://spacy.io/)** a **N**atural **L**anguage **P**rocessing software, sentences are created and putted together to form the news.
Finally, a JSON file is created with the news of each trending topic.

The server gets the JSON and using [React](https://reactjs.org/) with [Semantic UI](https://react.semantic-ui.com/) it shows the news in a web page in a _pretty_ way.

## Configuring the application before start using it

After download the application you have to install the necessaries things to run it.

For the Client:
1. Download the chrome driver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads) and set an environment variable for it
2. Install Python 3
3. Install [pip](https://pypi.org/project/pip/) (probably it's already installed because of the instalation of Python)
4. Install virtualenv: `pip install virtualenv`
5. **Go into the _client_ folder of the project** and run:
..* `virtualenv venv`
..* `source venv/bin/activate`
6. Install the necessary dependencies running: `pip install -r requirements.txt`

For the Server:
1. Install Node JS
2. **Inside the server folder** run: `npm install`

## How to use the app

**Requirement**: A Twitter account

Client:
To run the client go into the _src_ folder inside the _client_ folder and run

```python
python3 start.py username password
```
> **Note:** The **username** and the **password** are the username (or mail) and password of the Twitter account.

Server:
To run the server go to the _server_ folder and run
```javascript
npm start
```
