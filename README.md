# Construction Project Quotation System

This Django-based web application was created to help construction companies streamline the quotation process for their clients. The application enables administrators and users to handle project quotations, project aspects, and resources, thereby replacing spreadsheets with a more efficient and structured method. The software, created using Django and Bootstrap, has a clean, responsive UI, user account management, project tracking, and real-time quotation updates.

---

## Table of Contents

1. Project Overview
2. Features
3. Project Packages
4. Getting Started
5. Setup and Usage
6. Final Notes

---

## Project Overview

The construction company traditionally used Google Sheets to calculate costs, apply markups, and generate summaries for customer projects. This web application enhances this process by allowing:

- **Admins** to create and manage projects, elements, and materials.
- **Users** to register, request project quotations, and view their project statuses.

Admins can add specific project elements and materials, set markups, and generate dynamic, real-time cost calculations that are instantly visible across the app.

---

## Features

### Admin Functionality
- Full project management.
- Control over project elements and materials, with options to add, remove, or edit.
- Dynamic markup updates on materials with real-time calculations using JavaScript (AJAX/jQuery).
- Ability to approve, decline, or mark projects as completed.

### User Functionality
- Registration, login, and account management.
- Request project quotations by specifying area size, project elements, and materials.
- Access a dashboard displaying their project quotations and statuses.
- Approve or decline quotations once reviewed.

### Project Cycle
- **Pending** – Initial status after request.
- **Approved** – Both admin and user have approved.
- **Declined** – User or admin declines.
- **Completed** – Only settable by admin after user approval.

### Public Functionality
- **Register** – User registration page.
- **Login** – Both User and Admin login page.
- **Logout** – Both User and Admin can logout.

---

## Project Packages

The following packages are used in this project:

- **Django**: Web framework
- **Bootstrap**: Front-end framework for responsive design
- **AJAX (jQuery)**: Used for real-time project cost updates on the admin panel

Install all packages via the `requirements.txt` file, which can be found in the project root.

---

## Getting Started

### Prerequisites

Ensure you have Python and Django installed. 

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/eayerishz/cpqs.git>
   cd <cpqs>

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Environment Variables:**
   - Create a `.env` file for sensitive data.
   - Set up database configurations, secret keys, etc., in this file.

4. **Database Migration:**
   ```bash
   python manage.py migrate

5. **Create a Superuser:**
   ```bash
   python manage.py createsuperuser

6. **Start the Development Server:**
   ```bash
   python manage.py runserver

Access the application at `http://127.0.0.1:8000/`

---

## Setup and Usage

### Admin Workflow
1. Login: Access the admin dashboard by logging in with your superuser credentials.
2. Project Management:
   - Go to Pending Quotations to view new user requests.
   - Visit each request’s detailed view to adjust elements, materials, or markup as needed.
   - Approve or decline quotations as appropriate.
3. Real-Time Cost Calculations:
   - Use the detailed view to modify project elements, materials, or markups.
   - Updates reflect instantly through AJAX.
4. Quotation Approval:
   - Once a quotation meets your requirements, approve it to enable user access to the final cost.

### User Workflow
1. Register/Login: Register a new account or login.
2. Request a Quote:
   - Navigate to Request a Quote to start a new quotation.
   - Specify area size, select project elements, and materials.
   - Approve or decline quotations as appropriate.
3. View Quotation Status:
   - Return to the dashboard to see all requested quotations and their statuses.
   - Approve or decline quotations based on admin input.
   
---

## Final Notes
  - Dynamic Calculations: Real-time updates require JavaScript (AJAX/jQuery) to reflect changes instantly for admins.
  - Customization: You may further customize elements and materials in the admin dashboard.
  - Bootstrap Integration: The UI is styled using Bootstrap, ensuring a responsive layout across devices.


This README gives a detailed guide to understanding, configuring, and using this construction quotation application, which streamlines the process of generating and approving quotations for construction projects.
