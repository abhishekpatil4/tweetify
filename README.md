# Tweetify 
*Improve your Twitter game with Tweetify! Create posts, share permissions effortlessly, and let our AI generate engaging retweet content. Amplify your reach while you focus on what matters most*

## Demo
### Check it out on Replit
[![Open in Replit](https://img.shields.io/badge/Open%20in-Replit-blue?logo=replit&style=for-the-badge)](https://replit.com/@abishkpatil/tweetify?v=1)

### Live Demo ([Live Link](https://tweetify-three.vercel.app))
[![gmailgenius-demo](https://github.com/user-attachments/assets/abb24495-d242-42f3-8cff-599182f735f4)](https://drive.google.com/file/d/1hQSjQc0GdQj8kPrrIlqLJvPzUpphU5hc/preview)

## Description
Tweetify is an AI agent using which you can create posts easily, get authorisation from other users to repost tweets on their behalf, generate repost quote using AI

## Tech Stack
- Frontend: ReactJS, Vite, TailwindCSS
- Backend: Python, FastAPI
- AI Agent: CrewAI
- Composio tools: [Twitter](https://app.composio.dev/app/twitter)

## Run Locally
### Setup tutorial
[![gmailgenius-demo](https://github.com/user-attachments/assets/abb24495-d242-42f3-8cff-599182f735f4)](https://drive.google.com/file/d/1kC9oVSUatqQ6Tcs3u6CTsVsmczzG-F6k/preview)

Clone the project

```bash
  git clone https://github.com/ComposioHQ/cookbook.git
```

Go to the project directory

```bash
  cd gmail-assistant/gmail-assistant-firebase
```

### Backend

Go to backend dir & run setup script, this will create a virtual environment & download necessary libraries (Note: if you're unable to execute then grant permisson -> chmod +x setup.sh)
You'll then be prompted to login to **Composio**, link **Gmail** & **Google Sheets**. 
Add API keys in **.env file**

```bash
  cd backend && ./setup.sh
```

Start the server

```bash
  python main.py
```

Start the agent

```bash
  python agent.py
```

### Frontend

Install dependencies

```bash
  npm install
```

Start the server

```bash
  npm run dev
```

### Composio Login
If you're prompted to login & enter API key, run the below command to login

```bash
  composio login
```

You'll be redirected to composio website, login, get the API key and paste it

## 🛡️ License

Composio is licensed under the Elastic License - see the [LICENSE](https://github.com/composiodev/composio/blob/master/LICENSE) file for details.
  
