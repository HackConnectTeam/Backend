# 🚀 Hack Connect – A fun and engaging app to connect hackers during a hackathon
Hack Connect is a social platform designed to bring hackathon participants together during the coding hours. Instead of just grinding code, users can take fun breaks, complete mini-challenges, and connect with other hackers based on shared interests and backgrounds.

Whether you're taking a break from debugging or just want to meet cool people, Hack Connect adds a social and creative twist to your hackathon experience.

## 🎯 What can you do with Hack Connect?
🧩 Complete Fun Challenges: Break the ice and beat boredom by completing quick, creative challenges. They're designed to help participants connect and stay energized throughout the event.

💻 Create Your Project: Register your hackathon project directly in the platform, making it easy to share what you're building with others.

🏆 Check the Scoreboard: See how you and others are doing! Earn points by solving challenges and climb the live scoreboard — a fun way to add friendly competition to the event.

😄 Generate Funny Avatars: Upload your photo and get a fun avatar created with AI-based diffusion models — a quirky way to show your personality!

🧠 Name Your Project with AI: Stuck on a project name? Let our AI suggest creative, memorable names tailored to your hack idea.

🌐 Meet Like-Minded Hackers: Get matched with people who share your programming languages, country, and hobbies — perfect for networking and collaboration.

## 💡 Why Hack Connect?
Hackathons are intense, but that doesn't mean they have to be isolating or boring. Hack Connect is built for:

🤝 Community Building: Make real connections during the hackathon, not just at the closing ceremony.

🕹️ Micro-Entertainment: Keep the energy high with fun features that offer lighthearted breaks without leaving the event context.

🧩 Enhanced Team Dynamics: Share laughs, ideas, and vibes with your team or new friends you meet on the platform.

## 🛠️ How can I use Hack Connect?

Well, it is easy! Just follow these steps:
1. 🧭 **Clone the Repository**.
You have to clone both repositories:
- Backend: https://github.com/HackConnectTeam/Backend.
- Frontend: https://github.com/HackConnectTeam/Frontend.
2. 🧠 **Set Up the Environment**.
   - Install Docker and Docker Compose.
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
POSTGRES_HOST

MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123

PY_BACKEND_GEMINI_API=
PY_BACKEND_DATABASE_URL==postgresql+asyncpg://app_user:secret@db/app_db
```
---
## 📄 License

MIT License. See [LICENSE](./LICENSE) for more information.

---

## 🙏 Special Thanks

A huge thank you to the HackUPC organizers for putting together such an amazing event.
