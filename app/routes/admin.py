from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.vendor import Vendor
from app.models.assessment import Assessment
from app.utils.pdf_generator import PDFGenerator
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def dashboard():
    # Get all assessments with their vendors
    assessments = Assessment.query.order_by(Assessment.created_at.desc()).all()
    
    # Calculate statistics
    total_assessments = len(assessments)
    high_risk = sum(1 for a in assessments if a.risk_classification == 'High Risk')
    medium_risk = sum(1 for a in assessments if a.risk_classification == 'Medium Risk')
    low_risk = sum(1 for a in assessments if a.risk_classification == 'Low Risk')
    
    # Get recent assessments
    recent_assessments = assessments[:5]
    
    # Calculate industry distribution
    industry_counts = {}
    industry_colors = {
        'tech': '#0d6efd',
        'healthcare': '#198754',
        'finance': '#dc3545',
        'retail': '#ffc107',
        'other': '#6c757d'
    }
    
    for assessment in assessments:
        industry = assessment.vendor.industry
        industry_counts[industry] = industry_counts.get(industry, 0) + 1
    
    # Format industry labels and colors
    industry_labels = []
    industry_counts_list = []
    industry_colors_list = []
    
    for industry, count in industry_counts.items():
        industry_labels.append(industry.title())
        industry_counts_list.append(count)
        industry_colors_list.append(industry_colors.get(industry.lower(), '#6c757d'))
    
    # Calculate risk score trend (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_assessments_30d = [a for a in assessments if a.created_at >= thirty_days_ago]
    
    # Create a date range for the last 30 days
    date_range = []
    current_date = thirty_days_ago
    while current_date <= datetime.utcnow():
        date_range.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    # Initialize trend data with zeros
    trend_data = {date: [] for date in date_range}
    
    # Fill in actual assessment data
    for assessment in recent_assessments_30d:
        date_str = assessment.created_at.strftime('%Y-%m-%d')
        if date_str in trend_data:
            trend_data[date_str].append(assessment.total_risk_score)
    
    # Calculate averages and handle empty days
    trend_dates = []
    trend_scores = []
    for date in date_range:
        scores = trend_data[date]
        if scores:  # Only include dates with assessments
            trend_dates.append(date)
            trend_scores.append(sum(scores) / len(scores))
    
    # Get vendor data for the vendor list
    vendors = Vendor.query.all()
    vendor_data = []
    
    for vendor in vendors:
        latest_assessment = Assessment.query.filter_by(vendor_id=vendor.id)\
            .order_by(Assessment.created_at.desc()).first()
        
        vendor_data.append({
            'vendor': vendor,
            'latest_assessment': latest_assessment
        })
    
    return render_template('admin/dashboard.html',
                         assessments=assessments,
                         total_assessments=total_assessments,
                         high_risk=high_risk,
                         medium_risk=medium_risk,
                         low_risk=low_risk,
                         recent_assessments=recent_assessments,
                         industry_labels=industry_labels,
                         industry_counts=industry_counts_list,
                         industry_colors=industry_colors_list,
                         trend_dates=trend_dates,
                         trend_scores=trend_scores,
                         vendor_data=vendor_data)

@admin_bp.route('/vendor/<int:vendor_id>')
def vendor_details(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    assessments = Assessment.query.filter_by(vendor_id=vendor_id)\
        .order_by(Assessment.created_at.desc()).all()
    
    return render_template('admin/vendor_details.html',
                         vendor=vendor,
                         assessments=assessments)

@admin_bp.route('/assessment/<int:assessment_id>')
def assessment_details(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    vendor = Vendor.query.get_or_404(assessment.vendor_id)
    
    return render_template('admin/assessment_details.html',
                         assessment=assessment,
                         vendor=vendor)

@admin_bp.route('/assessment/<int:assessment_id>/regenerate-pdf')
def regenerate_pdf(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    PDFGenerator.generate_assessment_report(assessment_id)
    flash('PDF report has been regenerated successfully.', 'success')
    
    return redirect(url_for('admin.assessment_details', assessment_id=assessment_id))

@admin_bp.route('/search')
def search():
    query = request.args.get('q', '')
    risk_level = request.args.get('risk_level', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    # Build query
    assessments = Assessment.query
    
    if risk_level:
        assessments = assessments.filter_by(risk_classification=risk_level)
    
    if date_from:
        assessments = assessments.filter(Assessment.created_at >= date_from)
    
    if date_to:
        assessments = assessments.filter(Assessment.created_at <= date_to)
    
    if query:
        vendors = Vendor.query.filter(Vendor.name.ilike(f'%{query}%')).all()
        vendor_ids = [v.id for v in vendors]
        assessments = assessments.filter(Assessment.vendor_id.in_(vendor_ids))
    
    assessments = assessments.order_by(Assessment.created_at.desc()).all()
    
    return render_template('admin/search_results.html',
                         assessments=assessments,
                         query=query,
                         risk_level=risk_level,
                         date_from=date_from,
                         date_to=date_to) 