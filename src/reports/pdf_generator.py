"""
PDF Report Generation Module
Generates a formal, professional Legal-Tech Contract Risk Report using ReportLab.
Includes executive score badge, metadata, entity breakdown, flagged clauses, and SMB advice.
"""

import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


def generate_pdf_report(analysis_result: dict, output_path: str = None) -> bytes:
    """
    Generates a PDF Risk Report from analysis results dictionary.
    Returns bytes or writes to output_path.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor('#1E293B')   # Dark Slate
    secondary_color = colors.HexColor('#2563EB') # Royal Blue
    danger_color = colors.HexColor('#DC2626')    # Crimson Red
    warning_color = colors.HexColor('#D97706')   # Amber
    success_color = colors.HexColor('#16A34A')   # Emerald Green
    light_bg = colors.HexColor('#F8FAFC')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=TA_LEFT
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#64748B'),
        alignment=TA_LEFT
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=secondary_color,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        alignment=TA_JUSTIFY
    )

    clause_text_style = ParagraphStyle(
        'ClauseText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#475569')
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("AI-BASED CONTRACT RISK ASSESSMENT REPORT", title_style))
    story.append(Paragraph("Automated Legal Clause Detection & Risk Diagnostics for SMBs", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=secondary_color, spaceAfter=12))

    # Metadata & Score Row
    metadata = analysis_result.get('metadata', {})
    score_info = analysis_result.get('risk_score', {})
    overall_score = score_info.get('overall_score', 0)
    risk_level = score_info.get('risk_level', 'Medium')
    
    score_bg = danger_color if overall_score >= 70 else (warning_color if overall_score >= 36 else success_color)

    meta_text = f"""
    <b>Contract Document:</b> {metadata.get('filename', 'Contract Document')}<br/>
    <b>Detected Title:</b> {metadata.get('detected_title', 'Commercial Agreement')}<br/>
    <b>Contract Type:</b> {analysis_result.get('contract_type', 'Service Agreement')}<br/>
    <b>Word Count:</b> {metadata.get('word_count', 0):,} words | <b>Est. Pages:</b> {metadata.get('page_count', 1)}<br/>
    <b>Date Analyzed:</b> {datetime.now().strftime('%d %B %Y, %I:%M %p')}
    """

    score_box_content = [
        [Paragraph(f"RISK SCORE", ParagraphStyle('Sc1', fontName='Helvetica-Bold', fontSize=10, textColor=colors.white, alignment=TA_CENTER))],
        [Paragraph(f"<b>{overall_score}/100</b>", badge_style)],
        [Paragraph(f"{risk_level.upper()} RISK", ParagraphStyle('Sc2', fontName='Helvetica-Bold', fontSize=11, textColor=colors.white, alignment=TA_CENTER))]
    ]
    score_table = Table(score_box_content, colWidths=[130])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), score_bg),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('CORNER_RADIUS', (0, 0), (-1, -1), 6)
    ]))

    meta_table = Table([
        [Paragraph(meta_text, body_style), score_table]
    ], colWidths=[390, 150])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (0, 0), light_bg),
        ('PADDING', (0, 0), (0, 0), 8)
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # 2. Executive Summary & Distribution
    story.append(Paragraph("1. Executive Risk Summary", h2_style))
    summary_headline = score_info.get('recommendation_headline', 'Review clauses before signing.')
    story.append(Paragraph(f"<b>Summary Finding:</b> {summary_headline}", body_style))
    story.append(Spacer(1, 6))

    dist_table_data = [
        ["Total Clauses", "High Risk Clauses", "Medium Risk Clauses", "Low Risk Clauses"],
        [
            str(score_info.get('total_clauses', 0)),
            f"{score_info.get('high_count', 0)} ({score_info.get('risk_percentage_breakdown', {}).get('High', 0)}%)",
            f"{score_info.get('medium_count', 0)} ({score_info.get('risk_percentage_breakdown', {}).get('Medium', 0)}%)",
            f"{score_info.get('low_count', 0)} ({score_info.get('risk_percentage_breakdown', {}).get('Low', 0)}%)"
        ]
    ]
    dist_table = Table(dist_table_data, colWidths=[135, 135, 135, 135])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (1, 1), (1, 1), colors.HexColor('#FEE2E2')),
        ('BACKGROUND', (2, 1), (2, 1), colors.HexColor('#FEF3C7')),
        ('BACKGROUND', (3, 1), (3, 1), colors.HexColor('#DCFCE7')),
        ('PADDING', (0, 0), (-1, -1), 6)
    ]))
    story.append(dist_table)
    story.append(Spacer(1, 14))

    # 3. Key Extracted Entities (NER)
    entities = analysis_result.get('entities', {})
    story.append(Paragraph("2. Key Extracted Legal Entities & Commercial Terms", h2_style))
    
    orgs_str = ", ".join(entities.get('organizations', [])[:4]) or "Not explicitly identified"
    persons_str = ", ".join(entities.get('persons', [])[:4]) or "Not explicitly identified"
    dates_str = ", ".join(entities.get('dates', [])[:4]) or "None extracted"
    money_str = ", ".join(entities.get('money_amounts', [])[:4]) or "None extracted"
    durs_str = ", ".join(entities.get('durations', [])[:4]) or "None extracted"
    acts_str = ", ".join(entities.get('governing_acts', [])[:4]) or "Indian Contract Act, 1872"

    entity_table_data = [
        [Paragraph("<b>Identified Parties:</b>", body_style), Paragraph(orgs_str, body_style)],
        [Paragraph("<b>Signatories / Persons:</b>", body_style), Paragraph(persons_str, body_style)],
        [Paragraph("<b>Key Dates:</b>", body_style), Paragraph(dates_str, body_style)],
        [Paragraph("<b>Financial / Penal Sums:</b>", body_style), Paragraph(money_str, body_style)],
        [Paragraph("<b>Durations / Periods:</b>", body_style), Paragraph(durs_str, body_style)],
        [Paragraph("<b>Governing Acts & Laws:</b>", body_style), Paragraph(acts_str, body_style)]
    ]
    entity_table = Table(entity_table_data, colWidths=[160, 380])
    entity_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0, 0), (0, -1), light_bg),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('PADDING', (0, 0), (-1, -1), 5)
    ]))
    story.append(entity_table)
    story.append(Spacer(1, 14))

    # 4. Detailed Clause-by-Clause Risk Breakdown
    story.append(Paragraph("3. Detailed Clause Risk Analysis & AI Recommendations", h2_style))
    
    clauses = analysis_result.get('clauses', [])
    for c in clauses:
        c_level = c.get('risk_level', 'Medium')
        c_cat = c.get('clause_category', 'General Clause')
        c_title = c.get('clause_title', c.get('clause_number', 'Clause'))
        c_score = c.get('risk_score', 50)
        c_text = c.get('clause_text', '')
        c_exp = c.get('explanation', '')
        c_rec = c.get('recommendation', '')

        level_color = danger_color if c_level == 'High' else (warning_color if c_level == 'Medium' else success_color)

        clause_header_text = f"<b>{c_title}</b> — <font color='{level_color.hexval()}'><b>[{c_level.upper()} RISK | Category: {c_cat}]</b></font>"
        
        clause_content = [
            [Paragraph(clause_header_text, body_style)],
            [Paragraph(f"<b>Contract Text:</b> \"{c_text[:350]}...\"", clause_text_style)],
            [Paragraph(f"<b>AI Legal Explanation:</b> {c_exp}", body_style)],
            [Paragraph(f"<b>Actionable SMB Recommendation:</b> <font color='{secondary_color.hexval()}'><b>{c_rec}</b></font>", body_style)]
        ]

        c_table = Table(clause_content, colWidths=[540])
        c_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), light_bg),
            ('BOX', (0, 0), (-1, -1), 1, level_color),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(KeepTogether([c_table, Spacer(1, 8)]))

    # 5. Top SMB Actionable Negotiation Strategy
    story.append(Spacer(1, 10))
    story.append(Paragraph("4. Recommended Negotiation Strategy for Small Businesses", h2_style))
    
    recs = analysis_result.get('recommendations', [])
    rec_items = []
    for idx, r in enumerate(recs, 1):
        rec_items.append(Paragraph(f"<b>{idx}.</b> {r}", body_style))
        rec_items.append(Spacer(1, 4))
    
    story.append(KeepTogether(rec_items))
    story.append(Spacer(1, 14))

    # Disclaimer
    disclaimer_text = """
    <b>DISCLAIMER:</b> This report is generated by an automated Natural Language Processing (NLP) and Machine Learning system for informational and risk triage purposes only. It does not constitute formal legal advice. Small and medium-sized businesses are advised to consult a qualified legal practitioner or advocate for binding contractual negotiations.
    """
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#94A3B8'), spaceBefore=8, spaceAfter=8))
    story.append(Paragraph(disclaimer_text, ParagraphStyle('Disc', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=10, textColor=colors.HexColor('#64748B'))))

    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(pdf_bytes)

    return pdf_bytes
