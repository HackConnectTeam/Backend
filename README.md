
# 🚀 Hack Connect - A funny and engaging social network for all kind of people

**Hack Connect** is a social network designed to connect people through events, activities, and shared interests.
The platform allows users to create and join events, share experiences, and make new friends. With a focus on fun and
engagement, Hack Connect aims to foster a vibrant community where users can connect with like-minded individuals.
From event creation to funny avatars generation, Hack Connect provides a seamless experience for users to interact and engage
because of common stuff such as favorite programming languages, countries, and hobbies.
---
## Why choose Hack Connect?
Hack Connect is not just another social network. It stands out with its unique features:
- 🎉 **Event Creation**: Users can create and manage events, making it easy to organize meetups and activities.
- 💬 **User Engagement**: The platform encourages user interaction through events and shared interests, making it a lively space for socializing.
- 🤝 **Community Focus**: Hack Connect is designed to foster a sense of community, allowing users to connect with others who share their interests.
- 😄 **Funny Avatars**: Users can generate funny avatars based on their photos, adding a fun twist to their profiles.

---
## 🛠️ How can I use Hack Connect?

Well, it is easy! Just follow these steps:
1. 🧭 **Clone the Repository**.
You have to clone both repositories:
- Backend: https://github.com/HackConnectTeam/Backend.
- Frontend: https://github.com/HackConnectTeam/Frontend.
2. 🧠 **Set Up the Environment**.
   - Install Docker and Docker Compose.
   - Run a Cloudflare container to expose the application to the internet by tunelling:
     ```bash
     docker run --network host cloudflare/cloudflared:latest tunnel --no-autoupdate run --token
     eyJhIjoiNmMxN2NlMTM1ZDY4NTc0MGJmYmE4NjUxODAzNDA0NTciLCJ0IjoiYjQ3Mzc1OTYtZmU0MS00NDIwLWEyODQtY
     mFhYjczZGE4YTI4IiwicyI6Ill6RmpaamxoWlRrdE1qRmxNeTAwWkRjMUxUazVNak10WlRsbVkyVXdaVFJqWVdWbSJ9
     ```
   - Run these commands in the Frontend folder:
     ```bash
     npm install
     npm run dev
     ```
   - Create a `.env` file with the necessary environment variables. More information can be found in the [Environment Variables](#-environment-variables) section.
   - Run the Docker containers using Docker Compose:
     ```bash
     docker-compose up -f devops/docker-compose.yml up --build
     ```
3. 🚀 **Access the Application**.
   - Navigate to https://hackconnect.lamelas24.com and enjoy!
---

## 🧰 Tech Stack

- **FastAPI** – Web framework for building APIs
- **PostgreSQL** – Relational database for storing users, events, and related data
- **MinIO** – S3-compatible object storage for profile pictures
- **MLServer** – Model serving for deep learning-based avatar generation
- **Docker & Docker Compose** – Containerized development and deployment
- **pre-commit** – Automated checks on staged Git files
- **Conventional Commits** – Git commit standardization

---
## ⚙️ Environment Variables

You can configure your environment in a `.env` file. Example:

```env
MOUNT_PATH=${PWD}:/opt/project
PROJECT_NAME=hackupc
STAGE=pro
PYTHONPATH=/opt/project:/opt/project/src:/opt/project/app

POSTGRES_USER=app_user
POSTGRES_DB=app_db
POSTGRES_PASSWORD=secret
POSTGRES_HOST=host

MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123

PY_BACKEND_GEMINI_API=apikey
PY_BACKEND_DATABASE_URL==postgresql+asyncpg://app_user:secret@db/app_db
```
---
## 📄 License

MIT License. See [LICENSE](./LICENSE) for more information.

---

## 🙌 Acknowledgements

Special thanks to:
