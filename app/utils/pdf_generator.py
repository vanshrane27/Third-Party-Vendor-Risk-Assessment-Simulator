import os
from datetime import datetime
from weasyprint import HTML
from flask import render_template, current_app
from app.models.vendor import Vendor
from app.models.assessment import Assessment
from app import db

class PDFGenerator:
    @staticmethod
    def generate_assessment_report(assessment_id):
        """
        Generate a PDF report for an assessment.
        
        Args:
            assessment_id (int): ID of the assessment
            
        Returns:
            str: Path to the generated PDF file
        """
        # Get assessment data
        assessment = Assessment.query.get_or_404(assessment_id)
        vendor = Vendor.query.get_or_404(assessment.vendor_id)
        
        # Generate HTML content
        html_content = render_template(
            'pdf/assessment_report.html',
            assessment=assessment,
            vendor=vendor,
            generated_date=datetime.utcnow()
        )
        
        # Create PDF filename
        filename = f'assessment_{assessment_id}_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}.pdf'
        pdf_path = os.path.join(current_app.config['PDF_FOLDER'], filename)
        
        # Ensure PDF directory exists
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
        
        # Generate PDF
        HTML(string=html_content).write_pdf(pdf_path)
        
        # Update assessment with PDF path
        assessment.pdf_report_path = filename
        db.session.commit()
        
        return pdf_path
    
    @staticmethod
    def get_report_template_data(assessment):
        """
        Prepare data for the report template.
        
        Args:
            assessment (Assessment): Assessment object
            
        Returns:
            dict: Template data
        """
        return {
            'assessment': assessment,
            'vendor': assessment.vendor,
            'responses': assessment.responses,
            'risk_score': assessment.total_risk_score,
            'risk_classification': assessment.risk_classification,
            'nist_controls': assessment.nist_controls,
            'iso_controls': assessment.iso_controls,
            'pci_controls': assessment.pci_controls,
            'generated_date': datetime.utcnow()
        } 