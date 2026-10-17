"""
Legal Knowledge Base for Indian Contract Law & SME Risk Evaluation
Grounding rules: Indian Contract Act 1872, MSMED Act 2006, Arbitration Act 1996
"""

LEGAL_STATUTES = {
    "Non-Compete Clauses": {
        "statute": "Section 27, Indian Contract Act, 1872",
        "legal_principle": "Every agreement by which anyone is restrained from exercising a lawful profession, trade, or business of any kind is to that extent VOID.",
        "case_law": "Niranjan Shankar Golikari v. Century Spg. & Mfg. Co. Ltd. (1967) / Percept D'Mark v. Zaheer Khan (2006)",
        "sme_impact": "Post-contractual non-competes are legally void in India. However, counterparties use them to intimidate SMB founders and suppress talent.",
        "counter_clause": "The parties acknowledge that no post-termination non-compete restriction shall apply. Restraints shall be strictly confined to protecting bona fide trade secrets without restricting lawful trade or employment."
    },
    "Payment Terms": {
        "statute": "Section 15 & 16, Micro, Small and Medium Enterprises Development (MSMED) Act, 2006",
        "legal_principle": "Mandates buyer payment within agreed period (maximum 45 days). Overdue amounts attract compound interest with monthly rests at 3 times the RBI Bank Rate.",
        "case_law": "Silpi Industries v. Kerala State Road Transport Corporation (Supreme Court of India, 2021)",
        "sme_impact": "Payment terms exceeding 45 days or unilateral right to withhold undisputed invoices threaten SMB cash flow and working capital survival.",
        "counter_clause": "Payment shall be made within 30 days of undisputed invoice submission. Overdue amounts beyond 45 days shall accrue interest as mandated under the MSMED Act, 2006. Disputed items must be notified within 7 days."
    },
    "Penalty Clauses": {
        "statute": "Section 74, Indian Contract Act, 1872",
        "legal_principle": "Liquidated damages must represent a genuine pre-estimate of loss. Disproportionate or punitive forfeiture is treated as a penalty and disallowed.",
        "case_law": "Kailash Nath Associates v. Delhi Development Authority (2015) 4 SCC 136",
        "sme_impact": "Severe daily penalties (e.g., 5% per day) can wipe out SMB profit margins for minor or client-induced delays.",
        "counter_clause": "In the event of unexcused delay attributable solely to Service Provider, liquidated damages shall be 0.5% per week of the delayed deliverable, capped at an aggregate maximum of 5% of the applicable Statement of Work."
    },
    "Liability Clauses": {
        "statute": "Section 73, Indian Contract Act, 1872",
        "legal_principle": "Compensation is recoverable only for direct natural losses arising in usual course, not for remote or indirect damage.",
        "case_law": "Hadley v. Baxendale principle codified in Section 73",
        "sme_impact": "Uncapped liability and indemnity for indirect/consequential damages exposes the SMB to ruinous multi-million claims.",
        "counter_clause": "Neither party shall be liable for indirect, incidental, or consequential damages. Each party's total aggregate liability arising out of this Agreement shall be capped at the total fees paid or payable in the preceding 6 months."
    },
    "Automatic Renewal": {
        "statute": "Doctrine of Unfair Terms / Consumer & Commercial Equity",
        "legal_principle": "Evergreen clauses with punitive notice windows (e.g. 180 days) lock SMBs into unwanted multi-year recurring obligations.",
        "case_law": "Central Inland Water Transport Corp v. Brojo Nath Ganguly (1986)",
        "sme_impact": "Automatic multi-year renewal without clear reminders forces SMBs to pay recurring license or service fees they no longer need.",
        "counter_clause": "This Agreement shall expire at the end of the Initial Term and may only be renewed upon mutual written agreement of both parties at least 30 days prior to expiry."
    },
    "Termination Clauses": {
        "statute": "Section 14 & 39, Specific Relief Act & Indian Contract Act",
        "legal_principle": "Asymmetric termination rights (client exits immediately with zero compensation while SMB is locked in) create unconscionable contractual inequality.",
        "case_law": "Indian Oil Corporation Ltd v. Amritsar Gas Service (1991)",
        "sme_impact": "SMB risks sudden revenue loss after investing upfront resources without being paid for completed work or work-in-progress.",
        "counter_clause": "Either party may terminate for convenience with 30 days written notice, provided Client pays for all deliverables completed and unavoidable commitments incurred prior to the termination date."
    },
    "Confidentiality Clauses": {
        "statute": "Common Law Breach of Confidence & Trade Secret Jurisprudence",
        "legal_principle": "Perpetual confidentiality without standard exclusions for public information or legal compliance creates unending legal risk.",
        "case_law": "Zee Telefilms Ltd. v. Sundial Communications Pvt. Ltd. (2003)",
        "sme_impact": "Perpetual non-disclosure prevents SMB employees and founders from utilizing generalized industry know-how in future projects.",
        "counter_clause": "Confidentiality obligations shall survive for a period of 2 (two) years post-termination, with standard exclusions for publicly known information and independently developed technology."
    },
    "Restrictive Clauses": {
        "statute": "Section 27, Indian Contract Act, 1872",
        "legal_principle": "Overbroad non-solicitation of clients or employees across long timeframes (5 years) or territory functions as illegal restraint of trade.",
        "case_law": "Wipro Ltd. v. Beckman Coulter International S.A. (2006)",
        "sme_impact": "Expropriation of SMB's background IP and extreme non-solicitation restricts hiring and destroys commercial competitiveness.",
        "counter_clause": "Each party retains ownership of its preexisting background IP. Non-solicitation of key project staff shall be limited to a mutual 6-month period following project completion."
    }
}

RISK_HEURISTIC_RULES = [
    {
        "pattern": r"(?:uncapped|without any monetary limitation|without limitation|unlimited liability)",
        "category": "Liability Clauses",
        "boost_risk": "High",
        "reason": "Explicit uncapped liability detected."
    },
    {
        "pattern": r"(?:restrained|not.*engage in.*compet|non-compete.*(?:2|3|5)\s*years|anywhere in India)",
        "category": "Non-Compete Clauses",
        "boost_risk": "High",
        "reason": "Post-contractual non-compete is void under Section 27 Indian Contract Act."
    },
    {
        "pattern": r"(?:withhold 100%|within (?:90|120|180) days|non-refundable under any circumstance)",
        "category": "Payment Terms",
        "boost_risk": "High",
        "reason": "Payment window exceeds MSMED Act statutory limit of 45 days or unilateral withholding detected."
    },
    {
        "pattern": r"(?:5% per (?:calendar\s+)?day|penalty sum of (?:INR|₹)\s*[0-9,]+|forfeiture of 100%)",
        "category": "Penalty Clauses",
        "boost_risk": "High",
        "reason": "Disproportionate liquidated damages violating Section 74 Indian Contract Act principles."
    },
    {
        "pattern": r"(?:terminate.*immediately.*without cause|sole and absolute discretion.*terminate)",
        "category": "Termination Clauses",
        "boost_risk": "High",
        "reason": "Unilateral immediate termination without compensation for work completed."
    },
    {
        "pattern": r"(?:survive perpetually and indefinitely|all.*communications.*including information already known)",
        "category": "Confidentiality Clauses",
        "boost_risk": "High",
        "reason": "Perpetual confidentiality without standard exclusions."
    },
    {
        "pattern": r"(?:preexisting frameworks.*sole and exclusive property|prohibited from hiring.*5 years)",
        "category": "Restrictive Clauses",
        "boost_risk": "High",
        "reason": "Loss of background IP ownership or overbroad non-solicitation."
    },
    {
        "pattern": r"(?:automatically renew for successive terms of (?:2|3|5)\s*years|at least 180 days prior)",
        "category": "Automatic Renewal",
        "boost_risk": "High",
        "reason": "Multi-year evergreen lock-in with onerous notice requirement."
    }
]
