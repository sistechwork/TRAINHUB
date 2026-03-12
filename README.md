# Student Portal Application

A comprehensive Student Management Portal featuring a Flask backend and an Angular frontend. The application facilitates student tracking, performance monitoring, and admin management.

## Project Structure

- `server.py`: Flask backend serving the API.
- `students.db`: SQLite database for student records.
- `portal-frontend/`: Angular application source code.
- `static/`: Static assets for the backend.

---

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.x**
- **Node.js** (v18 or higher recommended)
- **npm** (comes with Node.js)

### 2. Backend Setup (Flask)
From the root directory:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask server:**
   ```bash
   python server.py
   ```
   The backend will start on `http://localhost:5000`.

### 3. Frontend Setup (Angular)
Navigate to the `portal-frontend` directory:

1. **Install npm dependencies:**
   ```bash
   cd portal-frontend
   npm install
   ```

2. **Run the Angular development server:**
   ```bash
   npm start
   ```
   The application will be available at `http://localhost:4200`.

---

## 🛠️ Features
- **Student Dashboard**: Overview of personal info, attendance, and performance.
- **Admin Management**: Full control over student data, including bulk imports and detailed editing.
- **Modern UI**: Polished "Blue-White" premium theme with Poppins typography and high-visibility black text.
- **Responsive Design**: Fully optimized for both desktop and mobile devices.

## 🔑 Admin Credentials
- **Email**: `erpvcodez@gmail.com`
- **Password**: `Vcodez@123`

---

## 🏗️ Building for Production
To build the Angular application for production:
```bash
cd portal-frontend
npm run build
```
The output will be in `portal-frontend/dist/`.
