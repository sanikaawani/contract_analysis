import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_pdf_report(analysis_result: dict) -> io.BytesIO:
    """
    Generate an executive Contract Risk Audit PDF Report using ReportLab.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        alignment=0
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748b'),
        alignment=0
    )
    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )
    bold_style = ParagraphStyle(
        'BoldDark',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0f172a')
    )
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0f172a')
    )
    counter_style = ParagraphStyle(
        'CounterClause',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#047857')
    )
    
    story = []
    
    # Header Banner
    story.append(Paragraph("AI-BASED CONTRACT RISK AUDIT REPORT", title_style))
    story.append(Paragraph(f"SMB Legal Intelligence & Natural Language Processing Engine | Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3b82f6'), spaceAfter=12))
    
    # Summary Box Table
    risk_score = analysis_result.get("overall_risk_score", 0)
    risk_grade = analysis_result.get("overall_risk_grade", "N/A")
    contract_title = analysis_result.get("contract_title", "Contract Analysis")
    contract_type = analysis_result.get("contract_type", "Standard Agreement")
    
    score_bg = colors.HexColor('#fee2e2') if risk_score >= 65 else (colors.HexColor('#fef3c7') if risk_score >= 40 else colors.HexColor('#dcfce7'))
    score_color = colors.HexColor('#b91c1c') if risk_score >= 65 else (colors.HexColor('#b45309') if risk_score >= 40 else colors.HexColor('#15803d'))
    
    score_display = Paragraph(f"<b>RISK SCORE</b><br/><font size=24 color='{score_color.hexval()}'><b>{risk_score}/100</b></font><br/><b>{risk_grade}</b>", ParagraphStyle('ScoreCell', parent=styles['Normal'], alignment=1))
    
    metadata_text = f"""
    <b>Contract Title:</b> {contract_title}<br/>
    <b>Contract Type:</b> {contract_type}<br/>
    <b>Total Clauses Analyzed:</b> {analysis_result.get('clause_counts', {}).get('total', 0)}<br/>
    <b>High Risk Flags:</b> <font color='#b91c1c'><b>{analysis_result.get('clause_counts', {}).get('high_risk', 0)} High</b></font> | 
    <font color='#b45309'><b>{analysis_result.get('clause_counts', {}).get('medium_risk', 0)} Medium</b></font> | 
    <font color='#15803d'><b>{analysis_result.get('clause_counts', {}).get('low_risk', 0)} Low</b></font>
    """
    metadata_display = Paragraph(metadata_text, body_style)
    
    meta_table = Table([[metadata_display, score_display]], colWidths=[360, 170])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (1, 0), (1, 0), score_bg),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))
    
    # Executive Summary
    story.append(Paragraph("Executive Risk Assessment", h2_style))
    summary_msg = analysis_result.get("risk_summary_text", "No critical summary available.")
    story.append(Paragraph(summary_msg, body_style))
    story.append(Spacer(1, 10))
    
    # Extracted Legal Entities Table
    entities = analysis_result.get("entities", {})
    orgs = ", ".join(entities.get("organizations", [])) or "None identified"
    dates = ", ".join(entities.get("dates", [])) or "None identified"
    money = ", ".join(entities.get("money_amounts", [])) or "None identified"
    durations = ", ".join(entities.get("contract_durations", [])) or "None identified"
    persons = ", ".join(entities.get("person_names", [])) or "None identified"
    
    story.append(Paragraph("Extracted Contract Metadata (NLP NER Analysis)", h2_style))
    entity_data = [
        [Paragraph("<b>Identified Parties / Organizations:</b>", bold_style), Paragraph(orgs, body_style)],
        [Paragraph("<b>Financial Terms / Amounts:</b>", bold_style), Paragraph(money, body_style)],
        [Paragraph("<b>Key Dates:</b>", bold_style), Paragraph(dates, body_style)],
        [Paragraph("<b>Durations & Notice Periods:</b>", bold_style), Paragraph(durations, body_style)],
        [Paragraph("<b>Signatories / Key Persons:</b>", bold_style), Paragraph(persons, body_style)]
    ]
    entity_table = Table(entity_data, colWidths=[180, 350])
    entity_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(entity_table)
    story.append(Spacer(1, 12))
    
    # Risk Category Breakdown Table
    story.append(Paragraph("Risk Category Exposure Breakdown", h2_style))
    cat_headers = [Paragraph("<b>Risk Category</b>", bold_style), Paragraph("<b>Clause Count</b>", bold_style), Paragraph("<b>Risk Score</b>", bold_style), Paragraph("<b>Severity</b>", bold_style)]
    cat_rows = [cat_headers]
    
    for c in analysis_result.get("category_breakdown", []):
        sev_color = "#b91c1c" if c["severity"] == "High" else ("#b45309" if c["severity"] == "Medium" else "#15803d")
        cat_rows.append([
            Paragraph(c["category"], body_style),
            Paragraph(str(c["clause_count"]), body_style),
            Paragraph(f"{c['risk_score']}/100", body_style),
            Paragraph(f"<font color='{sev_color}'><b>{c['severity']}</b></font>", body_style)
        ])
        
    cat_table = Table(cat_rows, colWidths=[200, 100, 110, 120])
    cat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e2e8f0')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(cat_table)
    story.append(Spacer(1, 14))
    
    # Detailed High-Risk Clause Explanations & Counter-Clauses
    story.append(Paragraph("Detailed High & Medium Risk Clause Analysis & Legal Counter-Measures", h2_style))
    
    risk_clauses = [cl for cl in analysis_result.get("clauses", []) if cl.get("risk_level") in ["High", "Medium"]]
    if not risk_clauses:
        story.append(Paragraph("No significant high or medium risk clauses were detected in this agreement.", body_style))
    else:
        for idx, cl in enumerate(risk_clauses[:6]):
            badge_color = "#b91c1c" if cl["risk_level"] == "High" else "#b45309"
            clause_card = [
                [Paragraph(f"<b>Clause #{cl['clause_id']}: {cl['category']}</b> (<font color='{badge_color}'><b>{cl['risk_level']} Risk - {cl['risk_score']}/100</b></font>)", bold_style)],
                [Paragraph(f"<b>Original Text:</b> \"{cl['clause_text']}\"", callout_style)],
                [Paragraph(f"<b>Indian Law Reference:</b> <b>{cl['statute']}</b> - {cl['legal_principle']}", body_style)],
                [Paragraph(f"<b>SMB Impact:</b> {cl['sme_impact']}", body_style)],
                [Paragraph(f"<b>Recommended Amendment / Counter-Clause:</b><br/>{cl['recommended_counter_clause']}", counter_style)]
            ]
            c_table = Table(clause_card, colWidths=[530])
            c_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#f8fafc')),
                ('BACKGROUND', (0, 1), (0, 1), colors.HexColor('#ffffff')),
                ('BACKGROUND', (0, 2), (0, -1), colors.HexColor('#f8fafc')),
                ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#cbd5e1')),
                ('LINEBELOW', (0, 0), (0, -2), 0.5, colors.HexColor('#e2e8f0')),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(KeepTogether([c_table, Spacer(1, 8)]))
            
    # Legal Disclaimer Footer
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#cbd5e1'), spaceAfter=8))
    disclaimer_text = "<b>DISCLAIMER:</b> This report is generated by an automated Natural Language Processing and Machine Learning research system. It is designed for informational risk-screening purposes for Small and Medium Businesses and does not constitute formal legal counsel. Users should consult a qualified legal advocate prior to executing binding commercial agreements."
    story.append(Paragraph(disclaimer_text, ParagraphStyle('Disc', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.HexColor('#94a3b8'))))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
