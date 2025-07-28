"""
CuranData Health Analysis Framework
Based on functional medicine principles
"""

import re
from typing import Dict, List, Optional, Tuple
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class HealthAnalyzer:
    def __init__(self):
        """Initialize with your home healer framework"""
        self.optimal_ranges = {
            'vitamin_d': {'optimal': 50, 'lab_normal': 30},
            'cholesterol_female': 200,
            'cholesterol_male': 300,
            'glucose': 90,
            'hba1c': 5.0,
            'wbc': 6,
            'neutrophils': 60,
            'lymphocytes': 30,
            'monocytes_min': 4,
            'monocytes_max': 7,
            'basophils_max': 1
        }
        
        # Biomarker name variations for NLP
        self.biomarker_aliases = {
            'vitamin_d': [
                'vitamin d', 'vit d', '25-oh-d', '25(oh)d', '25-hydroxyvitamin d',
                '25 oh vitamin d', 'calcidiol', 'vitamin d total', 'd3', 'vit d3'
            ],
            'neutrophils': [
                'neutrophil', 'neutrophils', 'neut', 'polys', 'pmns', 
                'segmented neutrophils', 'segs', 'neutrophil count'
            ],
            'lymphocytes': [
                'lymphocyte', 'lymphocytes', 'lymph', 'lymphs',
                'lymphocyte count', 'total lymphocytes'
            ]
        }

        self.abcde_protocol = {
            'A': '25,000 IU daily (75,000 when sick) - for eyes/vision',
            'B': 'B50 Complex 2/day + B12 sublingual - all B vitamins',
            'C': '1 tsp ascorbic acid in water - for immunity',
            'D': '5000 IU D3 daily - for cognitive function',
            'E': '400 IU mixed tocopherols'
        }

    def extract_biomarkers_from_text(self, text: str) -> Dict[str, List[Dict]]:
        """Extract biomarker values from lab report text using NLP"""
        text = text.lower()
        extracted_data = {}
        
        # Pattern to match various number formats with units
        value_pattern = r'(\d+\.?\d*)\s*(?:x\s*10[³3⁹⁹]?/[µu]l|ng/ml|nmol/l|%|percent)?'
        
        for biomarker, aliases in self.biomarker_aliases.items():
            findings = []
            
            for alias in aliases:
                # Look for the biomarker name followed by a value
                patterns = [
                    rf'{alias}\s*:?\s*{value_pattern}',
                    rf'{alias}\s*=\s*{value_pattern}',
                    rf'{value_pattern}\s*{alias}',
                    rf'{alias}\s*\(\s*{value_pattern}\s*\)',
                    rf'{alias}\s*-\s*{value_pattern}'
                ]
                
                for pattern in patterns:
                    matches = re.finditer(pattern, text)
                    for match in matches:
                        value = float(match.group(1))
                        unit = self._determine_unit(text, match.start(), match.end(), biomarker)
                        
                        findings.append({
                            'value': value,
                            'unit': unit,
                            'position': match.start(),
                            'raw_match': match.group(0)
                        })
            
            if findings:
                # Remove duplicates based on position
                unique_findings = []
                seen_positions = set()
                for finding in findings:
                    if finding['position'] not in seen_positions:
                        unique_findings.append(finding)
                        seen_positions.add(finding['position'])
                
                extracted_data[biomarker] = unique_findings
        
        return extracted_data

    def _determine_unit(self, text: str, start: int, end: int, biomarker: str) -> str:
        """Determine the unit for a biomarker value based on context"""
        # Default units for known biomarkers
        default_units = {
            'vitamin_d': 'ng/ml',
            'neutrophils': '%',
            'lymphocytes': '%',
            'wbc': 'x10³/μL',
            'glucose': 'mg/dL',
            'hba1c': '%',
            'cholesterol': 'mg/dL'
        }
        
        # Check if there's a unit in the text near the match
        context = text[max(0, start-10):min(len(text), end+10)]
        
        # Look for common units
        if 'mg/dl' in context or 'mg/dL' in context:
            return 'mg/dL'
        elif 'ng/ml' in context or 'ng/mL' in context:
            return 'ng/mL'
        elif 'nmol/l' in context or 'nmol/L' in context:
            return 'nmol/L'
        elif '%' in context:
            return '%'
        
        # Return default unit for this biomarker if known
        return default_units.get(biomarker, '')

    def analyze_vitamin_d(self, value: float) -> Dict:
        """Analyze vitamin D levels"""
        if value < 20:
            return {
                'status': 'Severely Deficient',
                'priority': 'CRITICAL',
                'recommendation': 'High-dose vitamin D supplementation needed',
                'explanation': 'Severe deficiency can lead to bone disorders and immune dysfunction'
            }
        elif value < 30:
            return {
                'status': 'Deficient',
                'priority': 'HIGH',
                'recommendation': 'Vitamin D supplementation recommended',
                'explanation': 'Below optimal range for immune function and bone health'
            }
        elif value <= 80:
            return {
                'status': 'Optimal',
                'priority': 'NORMAL',
                'recommendation': 'Maintain current vitamin D levels',
                'explanation': 'Within optimal range for health'
            }
        else:
            return {
                'status': 'Potentially Toxic',
                'priority': 'HIGH',
                'recommendation': 'Consult healthcare provider',
                'explanation': 'Vitamin D levels above 80 ng/mL may be toxic'
            }

    def analyze_neutrophils(self, value: float) -> Dict:
        """Analyze neutrophils percentage"""
        if value < 40:
            return {
                'status': 'Low Neutrophils',
                'priority': 'HIGH',
                'recommendation': 'May indicate infection or bone marrow issue',
                'explanation': 'Below normal range (40-75%)'
            }
        elif value <= 75:
            return {
                'status': 'Normal Neutrophils',
                'priority': 'NORMAL',
                'recommendation': 'No action needed',
                'explanation': 'Within normal range (40-75%)'
            }
        else:
            return {
                'status': 'High Neutrophils',
                'priority': 'HIGH',
                'recommendation': 'May indicate infection or inflammation',
                'explanation': 'Above normal range (40-75%)'
            }

    def analyze_lymphocytes(self, value: float) -> Dict:
        """Analyze lymphocytes percentage"""
        if value < 20:
            return {
                'status': 'Low Lymphocytes',
                'priority': 'HIGH',
                'recommendation': 'May indicate immune system issue',
                'explanation': 'Below normal range (20-40%)'
            }
        elif value <= 40:
            return {
                'status': 'Normal Lymphocytes',
                'priority': 'NORMAL',
                'recommendation': 'No action needed',
                'explanation': 'Within normal range (20-40%)'
            }
        else:
            return {
                'status': 'High Lymphocytes',
                'priority': 'HIGH',
                'recommendation': 'May indicate viral infection or other condition',
                'explanation': 'Above normal range (20-40%)'
            }

    def analyze_lab_report(self, text: str) -> Dict:
        """Main function to analyze a complete lab report"""
        # Extract biomarkers from text
        extracted_data = self.extract_biomarkers_from_text(text)
        
        results = {
            'extracted_biomarkers': {},
            'analysis': {},
            'summary': {
                'critical_findings': [],
                'high_priority': [],
                'recommendations': []
            }
        }
        
        # Analyze each extracted biomarker
        for biomarker, findings in extracted_data.items():
            if not findings:
                continue
                
            # Use the first finding
            finding = findings[0]
            value = finding['value']
            unit = finding['unit']
            
            results['extracted_biomarkers'][biomarker] = {
                'value': value,
                'unit': unit,
                'raw_match': finding['raw_match']
            }
            
            # Perform analysis based on biomarker type
            analysis = {}
            if biomarker == 'vitamin_d':
                analysis = self.analyze_vitamin_d(value)
            elif biomarker == 'neutrophils':
                analysis = self.analyze_neutrophils(value)
            elif biomarker == 'lymphocytes':
                analysis = self.analyze_lymphocytes(value)
            
            # Only process if we have analysis results
            if analysis:
                results['analysis'][biomarker] = analysis
                
                # Update summary
                if analysis['priority'] == 'CRITICAL':
                    results['summary']['critical_findings'].append(f"{biomarker}: {analysis['status']}")
                elif analysis['priority'] == 'HIGH':
                    results['summary']['high_priority'].append(f"{biomarker}: {analysis['status']}")
                
                if analysis['priority'] in ['CRITICAL', 'HIGH']:
                    results['summary']['recommendations'].append(analysis['recommendation'])
        
        return results

# API Endpoints
@app.route("/api/analyze", methods=["POST"])
def handle_analysis_request():
    """Handle analysis requests from the frontend"""
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400
    
    data = request.get_json()
    lab_text = data.get('lab_text', '')
    
    if not lab_text:
        return jsonify({"error": "No lab text provided"}), 400
    
    try:
        analyzer = HealthAnalyzer()
        results = analyzer.analyze_lab_report(lab_text)
        
        return jsonify({
            'success': True,
            'extracted_values': results.get('extracted_biomarkers', {}),
            'detailed_analysis': results.get('analysis', {}),
            'summary': results.get('summary', {})
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# This block runs ONLY when you execute `python health_analyzer.py` on your local machine.
# It is NOT used by Render's production server (Gunicorn).
if __name__ == "__main__":
    app.run(debug=True, port=5001)
