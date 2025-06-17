# Third-Party Vendor Risk Assessment Simulator

A comprehensive web application for conducting and managing third-party vendor cybersecurity assessments based on industry frameworks like NIST, ISO 27001, and PCI DSS. This tool helps organizations evaluate and monitor the security posture of their vendors through standardized assessments and risk scoring.

## Project Overview

The Third-Party Vendor Risk Assessment Simulator is designed to streamline the vendor security assessment process. It provides a structured approach to evaluating vendor security controls, calculating risk scores, and generating detailed reports. The system helps organizations:

- Standardize vendor security assessments
- Identify high-risk vendors
- Track vendor security improvements over time
- Generate compliance reports
- Maintain an audit trail of assessments

## Features

### Core Features
- Dynamic vendor assessment form with 12 key cybersecurity questions
- Risk scoring engine based on NIST controls and industry best practices
- PDF report generation with detailed findings and recommendations
- Vendor management dashboard
- Assessment history tracking
- Filterable assessment results by risk level, date, and vendor name

### Security Controls
The assessment covers critical security domains:
- Access Control (MFA, Access Policies)
- System Management (Inventory, Patch Management)
- Incident Response
- Data Protection (Encryption)
- Vulnerability Management
- Security Monitoring
- Backup and Recovery
- Security Awareness
- Vendor Management
- Change Management

### Risk Scoring
The risk scoring system uses a weighted approach:
- Critical controls: 3 points each
- High priority controls: 2 points each
- Each "No" answer contributes to the risk score
- Risk Classification:
  - Low Risk: 0-10 points
  - Medium Risk: 11-20 points
  - High Risk: 21+ points

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Forms**: Flask-WTF with CSRF protection
- **PDF Generation**: WeasyPrint
- **Authentication**: Flask-Login

### Frontend
- **Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS for form validation
- **CSS**: Custom styling with Bootstrap utilities
- **Icons**: Font Awesome

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd third-party-vendor-assessment
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
third-party-vendor-assessment/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── vendor.py
│   │   └── assessment.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── assessment/
│   │   └── admin/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── utils/
│       ├── __init__.py
│       ├── risk_scoring.py
│       └── pdf_generator.py
├── instance/
├── migrations/
├── requirements.txt
├── config.py
└── run.py
```

## Usage Guide

### Starting a New Assessment
1. Navigate to `/assessment/new`
2. Enter vendor information:
   - Vendor Name
   - Industry
   - Contact Email
3. Complete the security assessment questionnaire
4. Submit the form to generate the risk assessment

### Viewing Results
1. Access the assessment results page
2. Review the risk score and classification
3. Download the PDF report
4. View detailed findings and recommendations

### Admin Dashboard
1. Access the admin dashboard at `/admin`
2. View all assessments with filtering options:
   - Search by vendor name
   - Filter by risk level
   - Filter by date range
3. Generate PDF reports
4. Track vendor security improvements

## Security Considerations

- All form submissions are validated server-side
- Email addresses are verified
- Risk scores are calculated based on industry standards
- PDF reports are generated securely
- CSRF protection on all forms
- Input sanitization and validation
- Secure session management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For support, please open an issue in the repository or contact the development team. 

![Screenshot 2025-06-17 105801](https://github.com/user-attachments/assets/e6856215-3ddd-45aa-a2a8-0a45036087b5)

![Screenshot 2025-06-17 105814](https://github.com/user-attachments/assets/f45ace0a-4017-406f-9ace-cb612f1a5f8a)

![Screenshot 2025-06-17 105911](https://github.com/user-attachments/assets/51511053-0d90-4b43-bea0-3ba561604782)

![Screenshot 2025-06-17 105925](https://github.com/user-attachments/assets/0330b550-5b4a-4b20-8a59-fabba288c42b)

![Screenshot 2025-06-17 105839](https://github.com/user-attachments/assets/ccfe417c-2b15-41b5-ab95-8ed8c6b29251)

![Screenshot 2025-06-17 105855](https://github.com/user-attachments/assets/00c6acba-cb42-4f6b-a625-f54009bdba76)
