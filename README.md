# Masterblog 📝

A simple web-based blog system built with Flask – enables creating, editing, deleting, and liking posts in a local JSON store.

---

## 🔍 Project Description

Masterblog is a minimalist Flask web application that allows users to manage blog entries directly in the browser. Blog posts are stored locally in a JSON file and rendered through clean Jinja2-powered HTML templates. The project includes full CRUD functionality and an interactive like feature.

---

## ✨ Features

- 🗂 Create, Read, Update, and Delete (CRUD) blog posts
- ❤️ Like posts with a single click
- 📁 JSON-based data storage (`data/posts.json`)
- 🌐 HTML user interface rendered with Jinja2 templates
- 🧩 RESTful route structure
- 🛠️ Integrated error handling and logging
- 🔄 Auto-generated UUIDs for each blog post

---

## 🛠️ Tech Stack

- Python 3.11+
- Flask (web framework)
- HTML + Jinja2 templates
- JSON for data persistence

---

## 🧱 Project Structure

```
.
├── app.py                    # Main application logic and routes
├── requirements.txt          # Python dependencies
├── LICENSE                   # Project license
├── README.md                 # This documentation
├── data/
│   └── posts.json            # Local JSON file storing blog posts
├── static/                   # Static assets (CSS)
├── templates/
│   ├── index.html            # Main view listing all posts
│   ├── add.html              # Form to add a new post
│   └── update.html           # Form to edit an existing post
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ItsHarfer/Masterblog.git
cd Masterblog
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser to view the app.

---

## 🔧 Example Operations

- **✍️ Add a Post:** Fill out the form and submit
- **🛠 Edit a Post:** Modify content via pre-filled form
- **🗑 Delete a Post:** Remove with one click
- **❤️ Like a Post:** Click the like button to increase count

---

## 📋 Requirements

All required packages are listed in `requirements.txt`. Core dependencies:

- `Flask` – web routing and rendering
- `uuid` – ID generation
- `json` – for storing and loading posts

---

## 👤 Author

Martin Haferanke  
GitHub: [@ItsHarfer](https://github.com/ItsHarfer)  
Email: `martin.haferanke@gmail.com`

---

## 📄 License

Licensed under the MIT License.

This project is intended for educational and demonstrative purposes.