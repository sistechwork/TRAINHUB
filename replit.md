# Trainhub Systems Student Portal & Admin Dashboard

## Overview
This Flask-based web application provides a comprehensive student portal and an administrative dashboard for Trainhub Systems.

## Recent Changes (January 23, 2026)

### ✅ COMPLETE: BRANDING UPDATE - GradTwin to Trainhub Systems
- **Logo Replacement**: Updated GradTwin logo to the new Trainhub Systems logo (Geometric Train Icon)
- **New Logo Path**: /static/images/trainhub_logo.png
- **Login Page Redesign**: Implemented a sleek, professional black and white UI for the login dashboard
- **Copyright Update**: Updated copyright text to "2025 Trainhub Systems"
- **Page Titles Updated**: Changed from "GradTwin" to "Trainhub" in login page title
- **Theme Shift**: Transitioned from purple gradient to a high-contrast black and white professional aesthetic for the main login portal

## Recent Changes (November 24, 2025)

### ✅ COMPLETE: MENTOR FILTER REPLACED WITH STIPEND FILTER
- **Removed**: "Mentor" filter from admin dashboard search/filter section
- **Added**: New "Stipend" filter for searching students by stipend eligibility status
- **Filter Capabilities**:
  - ✓ Search by stipend status (e.g., "Yes", "No", "Eligible", etc.)
  - ✓ Works with other filters (Domain, Batch, Search term)
  - ✓ Partial matching support (e.g., typing "Eli" matches "Eligible")
  - ✓ Database joins attendance table for accurate stipend data
  - ✓ Enter key support for quick filtering
- **Filter Location**: Admin Dashboard → Search & Filter Section (4th filter field after Batch)

### ✅ COMPLETE: BULK IMPORT FEATURE (Excel-Ready) - FIXED
- **"Bulk Import" Button**: New purple button in admin dashboard (next to "Add Candidate")
- **Direct Excel Support**: Upload CSV or Excel files matching your Portal format (ML Portal.xlsx, DS Portal.xlsx, DA Portal.xlsx)
- **Multi-Sheet Excel Support**: Automatically reads and merges all three sheets (PERSONAL INFORMATION, ATTENDANCE, OVERALL PERFORMANCE)
- **Exact Column Mapping**:
  - **Personal Information**: Name, Email, Phone Number, Domain, COLLEGE, DEPT, Mode, Session Timings, Days, Session start Date, Session end date, TRAINER, Batch, Registration date
  - **Attendance**: Email, ATTENDNACE, STIPEND, REASON (column names preserved as-is)
  - **Overall Performance**: Email, Project title, Assesment 1, Assesment 2, Task, Project marks, Final validation, Total
- **Smart Duplicate Handling**:
  - ✓ Checks for all required columns (exact column names from Excel files)
  - ✓ Verifies no missing required fields (Name, Email, Phone Number, Domain)
  - ✓ Detects duplicate emails within the uploaded file
  - ✓ Detects duplicate emails in existing database
  - ✓ **Stores only NEW valid records for import**
  - ✓ **Imports only non-duplicate students to SQL**
  - ✓ Shows validation report with exact row numbers
- **Two-Step Process**:
  1. Upload file → System validates and shows valid row count
  2. Review report → Click "Import Data" (imports only new valid records, skips all duplicates)
- **Multi-Table Insert**: Data stored in all three tables (personal_info, attendance, performance)
- **Real-Time Dashboard Update**: New students automatically visible when they login
- **Column Name Preservation**: All original Excel column names preserved (including ATTENDNACE typo from source)
- **Bug Fix**: Validation now stores only valid records, so import always succeeds with correct count

### ✅ COMPLETE: ADD CANDIDATE FEATURE
- Single candidate addition via modal form with all three sheets' data

## User Preferences
I prefer clear and concise explanations. When making changes, prioritize iterative development and ask for confirmation before implementing major architectural shifts or significant code overhauls. Do not make changes to the file `server.py` unless explicitly instructed to.

## System Architecture

### UI/UX Decisions
The application features a unified login page, a detailed student dashboard with five distinct tabs (Personal Information, Project Information, Assessment Scores, Timeline, Attendance), and a comprehensive admin dashboard. The admin dashboard includes robust search and filter capabilities, along with modal forms for adding new candidates and an extensive editor for managing student data across all categories. The design emphasizes user-friendliness and real-time data presentation.

### Technical Implementations
The system is built using Flask. It uses a SQLite database (`students.db`) with three linked tables: `personal_info`, `attendance`, and `performance`. Data is fetched directly from the database for each page load to ensure real-time updates for students and administrators. The "Bulk Import" and "Add Candidate" features include comprehensive validation for data integrity, handling duplicates and ensuring all required fields are present. Search and filter functionalities on the admin dashboard are robust, allowing queries by name, email, phone, domain, batch, and mentor.

### Feature Specifications
- **Student Portal**: Secure login, personalized dashboard displaying personal, project, assessment, timeline, and attendance information with real-time data.
- **Admin Portal**: Secure login, dashboard to manage 1,857+ students with advanced search and filter options, bulk import via CSV/Excel, add new candidates through a comprehensive form, and a detailed student editor allowing modifications across all data categories.
- **Real-Time Data Updates**: All changes made by admins are immediately reflected in the student portal, ensuring data consistency across the application.
- **Data Integration**: Successfully integrates and manages data for ML, DS, and DA programs, encompassing personal, attendance, and performance metrics for each student.

### System Design Choices
- **Database**: SQLite with three normalized tables (`personal_info`, `attendance`, `performance`) linked by email for data integrity and efficient querying.
- **Backend**: Flask handles routing, authentication, and API endpoints for data retrieval and updates.
- **Data Flow**: Admin updates directly modify the database. Student dashboards query the database on every load, eliminating caching issues and guaranteeing fresh data.
- **Security**: Session-based authentication is implemented for both student and admin logins.
- **File Structure**: Organized `server.py` for backend logic, `templates/` for HTML, `static/` for assets, and `students.db` for the database.

## External Dependencies
- **Flask**: Web framework for the backend.
- **pandas**: Used for data manipulation, particularly for handling Excel/CSV imports.
- **openpyxl**: Required for reading and writing Excel files.
- **python-dotenv**: For managing environment variables (e.g., `SECRET_KEY`).
- **gunicorn**: Recommended for production deployment as a WSGI server.