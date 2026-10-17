"""
AI Explanation & Recommendation Engine
Generates clear, contextual, legal-grade explanations and actionable SMB recommendations
for detected risk clauses.
"""

EXPLANATION_TEMPLATES = {
    'Automatic Renewal': {
        'High': {
            'explanation': "The contract automatically renews on an evergreen basis with an onerous lock-in, narrow non-renewal notification window, or substantial exit penalties. This traps SMBs into unintended recurring multi-year financial commitments.",
            'recommendation': "Negotiate to remove evergreen automatic renewal. Require mutual written consent prior to any extension, or extend the non-renewal notice window to 60–90 days with zero exit fees."
        },
        'Medium': {
            'explanation': "The agreement automatically renews unless written notice is served 30 days prior. Annual price escalation may apply.",
            'recommendation': "Set automated calendar reminders 60 days before the contract anniversary to evaluate renewal and review price revision indices."
        },
        'Low': {
            'explanation': "The contract has a fixed term and strictly requires mutual written agreement for renewal, protecting the SMB's flexibility.",
            'recommendation': "Standard term structure. Ensure timely discussion 30 days prior to expiry if continuation of services is desired."
        }
    },
    'Payment Terms': {
        'High': {
            'explanation': "Payment terms are excessively delayed (Net 90–120+ days) or grant the client unilateral rights to withhold payments without interest or independent dispute mechanisms, posing severe cash-flow risks to SMBs.",
            'recommendation': "Insist on standard Net 30 or Net 45 payment terms. Add a clause entitling the SMB to statutory interest (e.g. 12-18% under MSMED Act, 2006) and right to suspend work upon non-payment exceeding 45 days."
        },
        'Medium': {
            'explanation': "Invoices are payable within 45 days with milestone sign-off conditions. Delayed payments attract moderate interest.",
            'recommendation': "Define clear milestone acceptance criteria (e.g. deemed approval if no feedback is provided within 7 business days)."
        },
        'Low': {
            'explanation': "Favorable payment terms (Net 15–30 days) with milestone payments and clear invoice dispute protocols.",
            'recommendation': "Maintain prompt invoicing with GST compliance and maintain Form 16A TDS certificates."
        }
    },
    'Liability Clauses': {
        'High': {
            'explanation': "The SMB assumes unlimited, uncapped liability and broad indemnity covering indirect, punitive, and consequential damages, while the opposing party enjoys limited or zero reciprocal exposure.",
            'recommendation': "CRITICAL: Introduce an aggregate liability cap equal to 100% of the total fees paid in the preceding 12 months. Expressly exclude indirect, special, punitive, and consequential damages."
        },
        'Medium': {
            'explanation': "Liability is capped at 2x or 3x the contract value, with mutual indemnification for gross negligence and willful misconduct.",
            'recommendation': "Ensure professional indemnity / errors & omissions insurance coverage is aligned with the stipulated liability ceiling."
        },
        'Low': {
            'explanation': "Mutual, balanced liability strictly capped at fees paid under the specific Statement of Work, with standard consequential damage exclusions.",
            'recommendation': "Well-balanced provision. Standard commercial protection in place."
        }
    },
    'Penalty Clauses': {
        'High': {
            'explanation': "Disproportionate liquidated damages (e.g., 2% per day of delay) and immediate forfeiture of security deposits/bank guarantees without reasonable cure periods, exceeding allowable standards under Section 74 of the Indian Contract Act.",
            'recommendation': "Cap total liquidated damages at a maximum of 5–10% of the affected milestone value. Require a mandatory 14 to 30-day written cure period before any penalties or deductions apply."
        },
        'Medium': {
            'explanation': "Liquidated damages are capped at 5–10% of the purchase order value with service credits applicable as credit notes.",
            'recommendation': "Ensure project delivery schedules include realistic buffer periods to avoid triggering SLA penalty thresholds."
        },
        'Low': {
            'explanation': "No punitive liquidated damages. Remedies are limited to reasonable cure periods and direct proven damages.",
            'recommendation': "Standard balanced terms. Maintain detailed documentation of all deliverables and dependency handovers."
        }
    },
    'Termination Clauses': {
        'High': {
            'explanation': "The client possesses unilateral rights to terminate immediately on 24 hours notice without cause or payment for work-in-progress, while the SMB is locked in with no right to terminate for convenience.",
            'recommendation': "Demand bilateral termination rights with at least 30–60 days prior written notice. Ensure the contract mandates full payment for all completed milestones and non-cancelable commitments upon early termination."
        },
        'Medium': {
            'explanation': "Either party may terminate for convenience with 30–60 days written notice or for material breach with a 30-day cure period.",
            'recommendation': "Ensure orderly handover protocols and establish clear timelines for pro-rata payment settlement upon termination."
        },
        'Low': {
            'explanation': "Balanced mutual termination for convenience with 60–90 days notice and full compensation for work-in-progress.",
            'recommendation': "Provides excellent operational security and fair wind-down time."
        }
    },
    'Confidentiality Clauses': {
        'High': {
            'explanation': "Perpetual non-disclosure obligations extending indefinitely with unilateral indemnity and overly broad trade secret definitions that restrict the SMB's residual general skills and future industry work.",
            'recommendation': "Limit confidentiality duration to a standard 2 to 3 years post-termination. Include standard carve-outs for publicly known information, independent development, and legally required disclosures."
        },
        'Medium': {
            'explanation': "Confidentiality obligations survive for 3–5 years post-termination with standard reasonable care and return-of-materials protocols.",
            'recommendation': "Maintain secure document handling procedures and ensure sub-contractors are bound by equivalent non-disclosure terms."
        },
        'Low': {
            'explanation': "Mutual 2-year confidentiality period with standard industry exceptions and balanced reciprocal protections.",
            'recommendation': "Standard bilateral protection. No changes necessary."
        }
    },
    'Non-Compete Clauses': {
        'High': {
            'explanation': "Broad non-compete covenant prohibiting the SMB from operating in its industry or offering services across India or globally for 2–3 years post-contract. Under Section 27 of the Indian Contract Act, 1872, post-contract non-compete covenants are generally void as agreements in restraint of trade.",
            'recommendation': "Reject or remove post-termination non-compete clauses. Replace with a reasonable, narrowly tailored non-solicitation clause limited to direct project team members for 6–12 months."
        },
        'Medium': {
            'explanation': "12-month non-solicitation of active project personnel and named clients introduced during the engagement.",
            'recommendation': "Acceptable commercial practice. Ensure the restriction applies strictly to personnel directly assigned to the project."
        },
        'Low': {
            'explanation': "No non-compete restrictions. The agreement expressly acknowledges the SMB's right to conduct commercial trade freely.",
            'recommendation': "Ideal terms preserving full commercial and professional freedom."
        }
    },
    'Restrictive Clauses': {
        'High': {
            'explanation': "Complete assignment of all SMB background IP, reusable code libraries, and future inventions to the client, coupled with 24/7 unannounced audit intrusion rights.",
            'recommendation': "Explicitly state that the SMB retains full ownership of its pre-existing background IP, tools, and general know-how. Grant the client a non-exclusive license for project deliverables only."
        },
        'Medium': {
            'explanation': "Client owns bespoke deliverables upon full payment; SMB grants license to embedded background utilities. Audits require 15 business days advance notice.",
            'recommendation': "Clearly enumerate proprietary background components in an Annexure to prevent future IP ownership disputes."
        },
        'Low': {
            'explanation': "Clear separation of custom deliverables (owned by Client upon full payment) and vendor core frameworks (retained by SMB).",
            'recommendation': "Optimal intellectual property framework. Standard commercial protection."
        }
    }
}


def generate_clause_explanation(category: str, risk_level: str, custom_clause_text: str = None) -> dict:
    """
    Retrieves or synthesizes legal explanation and recommendation for a clause.
    """
    cat_data = EXPLANATION_TEMPLATES.get(category, EXPLANATION_TEMPLATES['Restrictive Clauses'])
    level_data = cat_data.get(risk_level, cat_data.get('Medium'))

    explanation = level_data['explanation']
    recommendation = level_data['recommendation']

    # Contextual tailoring
    if custom_clause_text:
        text_lower = custom_clause_text.lower()
        if 'inr' in text_lower or '₹' in text_lower or 'rs.' in text_lower:
            recommendation += " Verify that all stated financial penalties conform with statutory ceilings."
        if 'arbitration' in text_lower:
            explanation += " Contains formal arbitration provisions under the Arbitration and Conciliation Act, 1996."

    return {
        'clause_category': category,
        'risk_level': risk_level,
        'explanation': explanation,
        'recommendation': recommendation
    }


def generate_contract_recommendations(analyzed_clauses: list[dict], overall_score: int) -> list[str]:
    """
    Compiles an executive summary list of top SMB actionable recommendations.
    """
    recommendations = []
    high_risks = [c for c in analyzed_clauses if c.get('risk_level') == 'High']

    if not high_risks and overall_score < 40:
        return [
            "Contract presents a low risk profile with balanced bilateral rights.",
            "Confirm operational timelines, milestone sign-off windows, and tax compliance (GST & TDS).",
            "Proceed with execution following standard management review."
        ]

    for c in high_risks:
        cat = c.get('clause_category', 'General')
        rec = generate_clause_explanation(cat, 'High')['recommendation']
        if rec not in recommendations:
            recommendations.append(f"[{cat}]: {rec}")

    if overall_score >= 70:
        recommendations.append("Obtain formal legal review from specialized commercial counsel before signing this agreement.")

    return recommendations[:6]
