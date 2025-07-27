"""
CuranData Health Analysis Framework
Based on functional medicine principles
"""

import re
from typing import Dict, List, Optional, Tuple
import json

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

class HealthAnalyzer:

    def __init__(self):
        # your setup code
        self.abcde_protocol = {
            'A': '25,000 IU daily...',
            ...
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
        context_start = max(0, start - 20)
        context_end = min(len(text), end + 20)
        context = text[context_start:context_end]
        
        if biomarker == 'vitamin_d':
            if 'nmol/l' in context:
                return 'nmol/L'
            else:
                return 'ng/mL'
        
        elif biomarker in ['neutrophils', 'lymphocytes']:
            if any(x in context for x in ['x10³/µl', 'x10^3/ul', '10³/µl', '10^3/ul', 'k/ul']):
                return 'x10³/µL'
            elif '%' in context or 'percent' in context:
                return '%'
            else:
                value = float(re.search(r'(\d+\.?\d*)', context).group(1))
                if value < 20:
                    return 'x10³/µL'
                else:
                    return '%'
        
        return 'unknown'

#VItamin D

    def analyze_vitamin_d(self, value):
        """Analyze vitamin D using your framework"""
        if value < 30:
            return {
                'status': 'Deficient',
                'recommendation': 'Start 5000 IU D3 daily',
                'priority': 'HIGH',
                'explanation': 'Below lab normal - critical for cognitive function',
                'retest': '8-12 weeks'
            }
        elif value < 50:
            return {
                'status': 'Suboptimal',
                'recommendation': 'Continue 5000 IU D3 daily',
                'priority': 'MEDIUM',
                'explanation': 'Lab normal but below YOUR optimal for cognitive health',
                'retest': '8-12 weeks'
            }
        else:
            return {
                'status': 'Optimal',
                'recommendation': 'Maintain current intake',
                'priority': 'LOW',
                'explanation': 'Excellent level for cognitive function',
                'retest': '6 months'
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
            if biomarker == 'vitamin_d':
                analysis = self.analyze_vitamin_d(value)
                results['analysis'][biomarker] = analysis
                
                # Update summary
                if analysis['priority'] == 'CRITICAL':
                    results['summary']['critical_findings'].append(f"{biomarker}: {analysis['status']}")
                elif analysis['priority'] == 'HIGH':
                    results['summary']['high_priority'].append(f"{biomarker}: {analysis['status']}")
                
                if analysis['priority'] in ['CRITICAL', 'HIGH']:
                    results['summary']['recommendations'].append(analysis['recommendation'])
        
        return results
      
