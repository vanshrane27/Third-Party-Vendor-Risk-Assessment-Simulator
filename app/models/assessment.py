from datetime import datetime
from app import db

class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'), nullable=False)
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_risk_score = db.Column(db.Integer, nullable=False)
    risk_classification = db.Column(db.String(20), nullable=False)
    pdf_report_path = db.Column(db.String(255))
    
    # Assessment responses stored as JSON
    responses = db.Column(db.JSON, nullable=False)
    
    # Framework mappings
    nist_controls = db.Column(db.JSON)
    iso_controls = db.Column(db.JSON)
    pci_controls = db.Column(db.JSON)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Assessment {self.id} for Vendor {self.vendor_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'vendor_id': self.vendor_id,
            'assessment_date': self.assessment_date.isoformat(),
            'total_risk_score': self.total_risk_score,
            'risk_classification': self.risk_classification,
            'pdf_report_path': self.pdf_report_path,
            'responses': self.responses,
            'nist_controls': self.nist_controls,
            'iso_controls': self.iso_controls,
            'pci_controls': self.pci_controls,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 