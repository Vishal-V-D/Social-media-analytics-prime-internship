# Social Media Analytics Platform 📈

An internship project for social media analytics, built with FastAPI and SQLAlchemy. This platform provides key insights into social media data, including trending hashtags, engagement depth analysis, and post-level metrics.

---

## 🚀 Key Features
- **FastAPI Backend**: High-performance, asynchronous web server built with Python to serve all analytics endpoints efficiently.
- **SQLAlchemy ORM**: Handles database interactions with clean, maintainable data models for users, posts, and comments.
- **Database Seeding**: Built-in script to populate the database with realistic sample data for testing locally.
- **Hashtag Analysis Engine**: Identifies trending hashtags within a specified timeframe for insights into popular topics.
- **Recursive Comment Parser**: Analyzes comment threads to determine engagement depth, giving insights beyond simple comment counts.

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **FastAPI**: Modern, fast (high-performance) web framework for building APIs.
- **SQLAlchemy**: Python SQL toolkit and Object-Relational Mapper.
- **MySQL**: Relational database to store all social media data.
- **python-dotenv**: For secure management of environment variables.

## 📂 Project Structure
All core components are consolidated into a single-file architecture for simplicity:
```bash
week-1-task/
│
├── src/
│   ├── main.py              # FastAPI entrypoint
│   ├── db_layer.py          # DB connection helpers
│   ├── hashtag_engine.py    # Trending hashtag queries
│   ├── comment_parser.py    # Recursive comment depth
│   ├── cache.py             # Caching helpers and retry logic
│   └── utils.py             # Utility functions for analytics
│
├── db/
│   ├── seed.py              # Seed script for users, posts, hashtags
│   └── schema.py            # SQLAlchemy models
│
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── README.md                # Project docs

```
## ⚙️ Setup & Installation

### Clone the Repository
```bash
git clone https://github.com/Vishal-V-D/Social-media-analytics-prime-internship.git
cd Social-media-analytics-prime-internship
```

3. Install Dependencies
Install all required Python packages using the requirements.txt file.
```bash
pip install -r requirements.txt
```
4. Configure the Database
   
Create a MySQL database and a .env file in the root directory with your credentials.
```bash
# .env file
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=social_media_analytics
```
5. Run the Application
   
The app.py file handles both database setup and API serving.

First, seed the database by running the file as a script:
```bash
python -m  db.seed 
```
This will create the necessary tables and populate them with sample data.

Next, start the FastAPI server:
```bash
uvicorn app:app --reload
````
The API will now be live at http://localhost:8000. You can access the interactive documentation at http://localhost:8000/docs.

## 🌐 API Endpoints

Explore the analytics by interacting with the following API endpoints:

| Endpoint                 | Method | Description |
|--------------------------|--------|-------------|
| `/trending-hashtags`     | GET    | Returns a list of the top 10 trending hashtags based on recent posts. |
| `/post-metrics/{post_id}`| GET    | Provides engagement insights for a specific post, including comment count. |
| `/comment-tree/{post_id}`| GET    | Displays the full comment tree for a given post, showing nested replies and depth. |

🤝 Contribution
Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute.

✒️ Author
Vishal V D

GitHub: @Vishal-V-D

📄 License
This project is open source and available under the MIT License.
