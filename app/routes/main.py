from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email
from app import db
from app.models.vendor import Vendor
from app.models.assessment import Assessment
from app.utils.risk_scoring import RiskScoring
from app.utils.pdf_generator import PDFGenerator

main_bp = Blueprint('main', __name__)

# Assessment questions with their respective controls
ASSESSMENT_QUESTIONS = {
    'q1': {
        'text': 'Does your organization implement Multi-Factor Authentication (MFA) for all remote access?',
        'control_id': 'NIST AC-2',
        'weight': 'critical',
        'description': 'Remote access authentication controls',
        'improvement_suggestion': 'Implement MFA for all remote access methods.'
    },
    'q2': {
        'text': 'Do you maintain an up-to-date inventory of all systems and software?',
        'control_id': 'NIST CM-8',
        'weight': 'high',
        'description': 'System inventory management',
        'improvement_suggestion': 'Implement and maintain a comprehensive system inventory.'
    },
    'q3': {
        'text': 'Do you have a formal incident response plan that is tested annually?',
        'control_id': 'NIST IR-1',
        'weight': 'critical',
        'description': 'Incident response planning',
        'improvement_suggestion': 'Develop and test an incident response plan annually.'
    },
    'q4': {
        'text': 'Do you encrypt sensitive data both in transit and at rest?',
        'control_id': 'NIST SC-28',
        'weight': 'critical',
        'description': 'Data encryption controls',
        'improvement_suggestion': 'Implement encryption for sensitive data in transit and at rest.'
    },
    'q5': {
        'text': 'Do you perform regular vulnerability assessments and penetration testing?',
        'control_id': 'NIST RA-5',
        'weight': 'high',
        'description': 'Vulnerability management',
        'improvement_suggestion': 'Conduct regular vulnerability assessments and penetration testing.'
    },
    'q6': {
        'text': 'Do you have a formal patch management process?',
        'control_id': 'NIST SI-2',
        'weight': 'high',
        'description': 'Patch management',
        'improvement_suggestion': 'Implement a formal patch management process.'
    },
    'q7': {
        'text': 'Do you maintain logs of all security events and review them regularly?',
        'control_id': 'NIST AU-6',
        'weight': 'high',
        'description': 'Audit log management',
        'improvement_suggestion': 'Implement comprehensive logging and regular log review.'
    },
    'q8': {
        'text': 'Do you have a formal backup and recovery process?',
        'control_id': 'NIST CP-9',
        'weight': 'critical',
        'description': 'Backup and recovery',
        'improvement_suggestion': 'Develop and test a formal backup and recovery process.'
    },
    'q9': {
        'text': 'Do you conduct regular security awareness training for employees?',
        'control_id': 'NIST AT-2',
        'weight': 'high',
        'description': 'Security awareness training',
        'improvement_suggestion': 'Implement regular security awareness training program.'
    },
    'q10': {
        'text': 'Do you have a formal vendor management process?',
        'control_id': 'NIST PS-7',
        'weight': 'high',
        'description': 'Vendor management',
        'improvement_suggestion': 'Develop a formal vendor management process.'
    },
    'q11': {
        'text': 'Do you have a formal change management process?',
        'control_id': 'NIST CM-3',
        'weight': 'high',
        'description': 'Change management',
        'improvement_suggestion': 'Implement a formal change management process.'
    },
    'q12': {
        'text': 'Do you have a formal access control policy?',
        'control_id': 'NIST AC-1',
        'weight': 'critical',
        'description': 'Access control policy',
        'improvement_suggestion': 'Develop and implement a formal access control policy.'
    }
}

class VendorForm(FlaskForm):
    name = StringField('Vendor Name', validators=[DataRequired()])
    industry = SelectField('Industry', choices=[
        ('tech', 'Technology'),
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('retail', 'Retail'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Start Assessment')

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/assessment/new', methods=['GET', 'POST'])
def new_assessment():
    form = VendorForm()
    if form.validate_on_submit():
        # Check if vendor already exists
        existing_vendor = Vendor.query.filter_by(email=form.email.data).first()
        
        if existing_vendor:
            # Update existing vendor's information
            existing_vendor.name = form.name.data
            existing_vendor.industry = form.industry.data
            db.session.commit()
            return redirect(url_for('main.assessment_form', vendor_id=existing_vendor.id))
        
        # Create new vendor if doesn't exist
        vendor = Vendor(
            name=form.name.data,
            industry=form.industry.data,
            email=form.email.data
        )
        db.session.add(vendor)
        db.session.commit()
        
        return redirect(url_for('main.assessment_form', vendor_id=vendor.id))
    
    return render_template('assessment/new.html', form=form)

@main_bp.route('/assessment/<int:vendor_id>', methods=['GET', 'POST'])
def assessment_form(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    
    if request.method == 'POST':
        responses = {}
        for question_id, question_data in ASSESSMENT_QUESTIONS.items():
            response = request.form.get(question_id)
            responses[question_id] = {
                'answer': response,
                'question_data': question_data
            }
        
        # Calculate risk score
        total_score, risk_classification = RiskScoring.calculate_risk_score(responses)
        
        # Create assessment
        assessment = Assessment(
            vendor_id=vendor.id,
            total_risk_score=total_score,
            risk_classification=risk_classification,
            responses=responses
        )
        db.session.add(assessment)
        db.session.commit()
        
        # Generate PDF report
        PDFGenerator.generate_assessment_report(assessment.id)
        
        return redirect(url_for('main.assessment_result', assessment_id=assessment.id))
    
    return render_template('assessment/form.html', vendor=vendor, questions=ASSESSMENT_QUESTIONS)

@main_bp.route('/assessment/result/<int:assessment_id>')
def assessment_result(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    vendor = Vendor.query.get_or_404(assessment.vendor_id)
    
    return render_template('assessment/result.html',
                         assessment=assessment,
                         vendor=vendor)

@main_bp.route('/assessment/pdf/<int:assessment_id>')
def download_pdf(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    if not assessment.pdf_report_path:
        PDFGenerator.generate_assessment_report(assessment_id)
    
    return redirect(url_for('static', filename=f'pdfs/{assessment.pdf_report_path}'))

@main_bp.route('/admin/assessments')
def admin_assessments():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get filter parameters
    search_query = request.args.get('q', '')
    risk_level = request.args.get('risk_level', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Start with base query
    query = Assessment.query
    
    # Apply search filter if provided
    if search_query:
        query = query.join(Vendor).filter(
            Vendor.name.ilike(f'%{search_query}%')
        )
    
    # Apply risk level filter if provided
    if risk_level:
        query = query.filter(Assessment.risk_classification == risk_level)
    
    # Apply date range filters if provided
    if date_from:
        query = query.filter(Assessment.created_at >= date_from)
    if date_to:
        query = query.filter(Assessment.created_at <= date_to)
    
    # Get paginated assessments with filters applied
    assessments = query.order_by(Assessment.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/assessments.html', assessments=assessments)

@main_bp.route('/admin/vendors')
def admin_vendors():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Get paginated vendors
    vendors = Vendor.query.order_by(Vendor.name).paginate(
        page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/vendors.html', vendors=vendors) 