from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import os
import uuid
from typing import Dict, List, Any


class ReportGenerator:
    """Generate PDF reports for disaster response scenarios"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Define custom styles
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkred
        ))
        
        # Subsection header style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.darkgreen
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_LEFT
        ))
        
        # Highlight style
        self.styles.add(ParagraphStyle(
            name='Highlight',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_LEFT,
            textColor=colors.darkblue,
            backColor=colors.lightblue
        ))
    
    def generate_report(self, scenario_data: Dict[str, Any], prediction_result: Dict[str, Any], 
                       allocation_result: Dict[str, Any], narrative: str) -> str:
        """Generate a comprehensive PDF report"""
        
        # Generate unique filename
        report_id = str(uuid.uuid4())
        filename = f"disaster_response_report_{report_id}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=A4, rightMargin=72, leftMargin=72, 
                              topMargin=72, bottomMargin=18)
        
        # Build story (content)
        story = []
        
        # Add title page
        story.extend(self._create_title_page(scenario_data))
        story.append(PageBreak())
        
        # Add executive summary
        story.extend(self._create_executive_summary(scenario_data, prediction_result, allocation_result))
        story.append(PageBreak())
        
        # Add scenario details
        story.extend(self._create_scenario_details(scenario_data))
        story.append(PageBreak())
        
        # Add resource predictions
        story.extend(self._create_resource_predictions(prediction_result))
        story.append(PageBreak())
        
        # Add allocation plan
        story.extend(self._create_allocation_plan(allocation_result))
        story.append(PageBreak())
        
        # Add narrative analysis
        story.extend(self._create_narrative_analysis(narrative))
        story.append(PageBreak())
        
        # Add recommendations
        story.extend(self._create_recommendations(prediction_result, allocation_result))
        
        # Build PDF
        doc.build(story)
        
        return filepath
    
    def _create_title_page(self, scenario_data: Dict[str, Any]) -> List:
        """Create the title page"""
        elements = []
        
        # Title
        title = Paragraph("RapidRelief Disaster Response Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 30))
        
        # Subtitle
        subtitle = Paragraph(f"{scenario_data['disaster_type'].title()} - {scenario_data['severity'].title()} Severity", 
                           self.styles['SectionHeader'])
        elements.append(subtitle)
        elements.append(Spacer(1, 20))
        
        # Location
        location = Paragraph(f"Location: {scenario_data['location']['city']}, {scenario_data['location']['state']}, {scenario_data['location']['country']}", 
                           self.styles['BodyText'])
        elements.append(location)
        elements.append(Spacer(1, 10))
        
        # Date
        date_str = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        date_para = Paragraph(f"Report Generated: {date_str}", self.styles['BodyText'])
        elements.append(date_para)
        elements.append(Spacer(1, 20))
        
        # AI Generated notice
        ai_notice = Paragraph("This report was generated using IBM Granite AI models and the IBM Agent Development Kit for automated disaster response planning.", 
                            self.styles['Highlight'])
        elements.append(ai_notice)
        
        return elements
    
    def _create_executive_summary(self, scenario_data: Dict[str, Any], 
                                prediction_result: Dict[str, Any], 
                                allocation_result: Dict[str, Any]) -> List:
        """Create executive summary section"""
        elements = []
        
        # Section header
        header = Paragraph("Executive Summary", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 12))
        
        # Key metrics table
        metrics_data = [
            ['Metric', 'Value'],
            ['Disaster Type', scenario_data['disaster_type'].title()],
            ['Severity Level', scenario_data['severity'].title()],
            ['Affected Population', f"{scenario_data['location']['population']:,}"],
            ['Affected Area', f"{scenario_data['affected_area_km2']} km²"],
            ['Estimated Casualties', f"{scenario_data['estimated_casualties']:,}"],
            ['Prediction Confidence', f"{prediction_result.get('confidence_score', 0):.1%}"],
            ['Response Time', f"{prediction_result.get('estimated_response_time_hours', 0)} hours"],
            ['Total Cost', f"${allocation_result.get('total_cost', 0):,.2f}"],
            ['Plan Efficiency', f"{allocation_result.get('efficiency_score', 0):.1%}"]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2*inch, 3*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 20))
        
        # Summary text
        summary_text = f"""
        This report presents a comprehensive analysis of the {scenario_data['disaster_type']} disaster 
        affecting {scenario_data['location']['city']}, {scenario_data['location']['country']}. 
        The AI-powered analysis indicates a {scenario_data['severity']} severity event requiring 
        immediate response coordination.
        
        Key findings include a predicted response time of {prediction_result.get('estimated_response_time_hours', 0)} hours 
        with {prediction_result.get('confidence_score', 0):.1%} confidence. The optimized allocation plan 
        achieves {allocation_result.get('efficiency_score', 0):.1%} efficiency with a total estimated cost 
        of ${allocation_result.get('total_cost', 0):,.2f}.
        """
        
        summary_para = Paragraph(summary_text, self.styles['BodyText'])
        elements.append(summary_para)
        
        return elements
    
    def _create_scenario_details(self, scenario_data: Dict[str, Any]) -> List:
        """Create scenario details section"""
        elements = []
        
        # Section header
        header = Paragraph("Disaster Scenario Details", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 12))
        
        # Scenario table
        scenario_data_table = [
            ['Detail', 'Value'],
            ['Disaster Type', scenario_data['disaster_type'].title()],
            ['Severity Level', scenario_data['severity'].title()],
            ['City', scenario_data['location']['city']],
            ['State/Province', scenario_data['location']['state']],
            ['Country', scenario_data['location']['country']],
            ['Population', f"{scenario_data['location']['population']:,}"],
            ['Affected Area', f"{scenario_data['affected_area_km2']} km²"],
            ['Estimated Casualties', f"{scenario_data['estimated_casualties']:,}"],
            ['Available Volunteers', f"{scenario_data['available_volunteers']:,}"],
            ['Infrastructure Damage', scenario_data['infrastructure_damage']],
            ['Weather Conditions', scenario_data['weather_conditions']]
        ]
        
        scenario_table = Table(scenario_data_table, colWidths=[2*inch, 4*inch])
        scenario_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(scenario_table)
        elements.append(Spacer(1, 20))
        
        # Description
        desc_header = Paragraph("Scenario Description", self.styles['SubsectionHeader'])
        elements.append(desc_header)
        elements.append(Spacer(1, 8))
        
        desc_para = Paragraph(scenario_data['description'], self.styles['BodyText'])
        elements.append(desc_para)
        
        return elements
    
    def _create_resource_predictions(self, prediction_result: Dict[str, Any]) -> List:
        """Create resource predictions section"""
        elements = []
        
        # Section header
        header = Paragraph("AI-Powered Resource Predictions", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 12))
        
        # Prediction metrics
        metrics_text = f"""
        <b>Prediction Confidence:</b> {prediction_result.get('confidence_score', 0):.1%}<br/>
        <b>Estimated Response Time:</b> {prediction_result.get('estimated_response_time_hours', 0)} hours<br/>
        <b>Key Risk Factors:</b> {', '.join(prediction_result.get('risk_factors', []))}
        """
        
        metrics_para = Paragraph(metrics_text, self.styles['BodyText'])
        elements.append(metrics_para)
        elements.append(Spacer(1, 15))
        
        # Resource needs table
        predicted_needs = prediction_result.get('predicted_needs', [])
        if predicted_needs:
            needs_header = Paragraph("Predicted Resource Needs", self.styles['SubsectionHeader'])
            elements.append(needs_header)
            elements.append(Spacer(1, 8))
            
            needs_data = [['Resource Type', 'Quantity', 'Priority', 'Cost', 'Delivery Time']]
            for need in predicted_needs:
                needs_data.append([
                    need.get('resource_type', ''),
                    str(need.get('quantity', 0)),
                    need.get('priority', ''),
                    f"${need.get('estimated_cost', 0):,.2f}",
                    f"{need.get('delivery_time_hours', 0)} hours"
                ])
            
            needs_table = Table(needs_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 1*inch, 1*inch])
            needs_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(needs_table)
        
        return elements
    
    def _create_allocation_plan(self, allocation_result: Dict[str, Any]) -> List:
        """Create allocation plan section"""
        elements = []
        
        # Section header
        header = Paragraph("Optimized Resource Allocation Plan", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 12))
        
        # Plan metrics
        metrics_text = f"""
        <b>Plan Efficiency:</b> {allocation_result.get('efficiency_score', 0):.1%}<br/>
        <b>Total Cost:</b> ${allocation_result.get('total_cost', 0):,.2f}<br/>
        <b>Timeline:</b> {allocation_result.get('timeline_hours', 0)} hours
        """
        
        metrics_para = Paragraph(metrics_text, self.styles['BodyText'])
        elements.append(metrics_para)
        elements.append(Spacer(1, 15))
        
        # Resource allocations
        resource_allocations = allocation_result.get('resource_allocations', [])
        if resource_allocations:
            alloc_header = Paragraph("Resource Allocations", self.styles['SubsectionHeader'])
            elements.append(alloc_header)
            elements.append(Spacer(1, 8))
            
            alloc_data = [['Resource Type', 'Quantity', 'Priority', 'Cost', 'Delivery Time']]
            for alloc in resource_allocations:
                alloc_data.append([
                    alloc.get('resource_type', ''),
                    str(alloc.get('quantity', 0)),
                    alloc.get('priority', ''),
                    f"${alloc.get('estimated_cost', 0):,.2f}",
                    f"{alloc.get('delivery_time_hours', 0)} hours"
                ])
            
            alloc_table = Table(alloc_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 1*inch, 1*inch])
            alloc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(alloc_table)
            elements.append(Spacer(1, 15))
        
        # Volunteer assignments
        volunteer_assignments = allocation_result.get('volunteer_assignments', {})
        if volunteer_assignments:
            vol_header = Paragraph("Volunteer Assignments", self.styles['SubsectionHeader'])
            elements.append(vol_header)
            elements.append(Spacer(1, 8))
            
            vol_data = [['Task Category', 'Assigned Teams']]
            for task, teams in volunteer_assignments.items():
                vol_data.append([task.replace('_', ' ').title(), ', '.join(teams)])
            
            vol_table = Table(vol_data, colWidths=[2*inch, 3*inch])
            vol_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(vol_table)
        
        return elements
    
    def _create_narrative_analysis(self, narrative: str) -> List:
        """Create narrative analysis section"""
        elements = []
        
        # Section header
        header = Paragraph("AI-Generated Narrative Analysis", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 12))
        
        # Narrative text
        narrative_para = Paragraph(narrative, self.styles['BodyText'])
        elements.append(narrative_para)
        
        return elements
    
    def _create_recommendations(self, prediction_result: Dict[str, Any], 
                              allocation_result: Dict[str, Any]) -> List:
        """Create recommendations section"""
        elements = []
        
        # Section header
        header = Paragraph("Key Recommendations", self.styles['SectionHeader'])
        elements.append(header)
        elements.append(Spacer(1, 12))
        
        # Recommendations list
        recommendations = [
            "Immediate medical response deployment to affected areas",
            "Establish emergency communication channels",
            "Coordinate with local authorities and emergency services",
            "Monitor weather conditions and adjust plans accordingly",
            "Deploy volunteer teams according to the allocation plan",
            "Establish supply chain coordination for resource delivery",
            "Implement regular status reporting and progress tracking",
            "Prepare for potential escalation scenarios"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            rec_text = f"{i}. {rec}"
            rec_para = Paragraph(rec_text, self.styles['BodyText'])
            elements.append(rec_para)
            elements.append(Spacer(1, 6))
        
        elements.append(Spacer(1, 15))
        
        # Risk assessment
        risk_header = Paragraph("Risk Assessment", self.styles['SubsectionHeader'])
        elements.append(risk_header)
        elements.append(Spacer(1, 8))
        
        risk_factors = prediction_result.get('risk_factors', [])
        if risk_factors:
            risk_text = f"<b>Key Risk Factors:</b><br/>"
            for factor in risk_factors:
                risk_text += f"• {factor}<br/>"
        else:
            risk_text = "No specific risk factors identified in the current analysis."
        
        risk_para = Paragraph(risk_text, self.styles['BodyText'])
        elements.append(risk_para)
        
        return elements
