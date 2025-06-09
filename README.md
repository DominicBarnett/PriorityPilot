## PriorityPilot

**PriorityPilot** is a Flask-based task manager that helps users organize, prioritize, and complete tasks efficiently. It features user authentication, task prioritization, achievement tracking, and a modern, user-friendly interface.

---

### Features

- **User Authentication**: Register and log in with username or email.
- **Task Management**: Add, update, delete, and mark tasks as complete.
- **Task Prioritization**: Assign priorities to tasks and earn points for completing high-priority items.
- **Achievements & Streaks**: Unlock achievements and track your productivity streaks.
- **Calendar View**: Visualize your tasks on a calendar.
- **Profile & Progress**: View your profile, achievements, and progress.
- **Password Reset**: Secure password reset via email.
- **Responsive UI**: Modern interface with themed graphics and icons.

---

### Screenshots

You can add screenshots or reference images from `static/images/` here, e.g.:

![PriorityPilot Dashboard](static/images/plane-bullet-points.png)

---

### Getting Started

#### Prerequisites

- Python 3.11+
- MongoDB (local or via Docker)
- (Optional) Docker & Docker Compose

#### Installation

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd PriorityPilot
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in your secrets (Mongo URI, mail credentials, etc).

4. **Run the app:**
   ```sh
   python app.py
   ```
   The app will be available at [http://localhost:5000](http://localhost:5000).

---

### Using Docker

You can run the app and MongoDB together using Docker Compose:

```sh
docker-compose up --build
```

---

### Project Structure

- `app.py` - Main Flask application with routes and logic
- `models.py` - Data models for users, tasks, and priorities
- `templates/` - HTML templates for the UI
- `static/` - Static assets (CSS, JS, images)
- `seeds.py` - (Optional) Script to seed the database
- `Dockerfile` & `docker-compose.yml` - For containerized deployment

---

### Configuration

- **Environment Variables**: Set in `.env` (see `.env.example`)
  - `SECRET_KEY`
  - `MONGO_URI`
  - `MAIL_USERNAME`
  - `MAIL_PASSWORD`

---

### Achievements

- First Task Completed
- Task Master (10+ tasks)
- Streak Starter (3+ days)
- Weekend Warrior (tasks on weekends)
- High Priority Hero (5+ high-priority tasks)

---

### Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

### License

[MIT](LICENSE) (or specify your license)

```sh
pip install -r requirements.txt
python app.py
```