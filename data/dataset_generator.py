"""
Dataset Generator and Kaggle Dataset Ingestion Module
for Indian Legal Contract Clauses Dataset.
Generates balanced, realistic contract clauses across 5 contract types,
8 risk categories, and 3 risk levels (Low, Medium, High).
"""

import os
import json
import random
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')
SAMPLE_DIR = os.path.join(DATA_DIR, 'sample_contracts')

CONTRACT_TYPES = [
    'Service Agreement',
    'Vendor Agreement',
    'Employment Agreement',
    'Non-Disclosure Agreement (NDA)',
    'Supply Agreement'
]

RISK_CATEGORIES = [
    'Automatic Renewal',
    'Payment Terms',
    'Liability Clauses',
    'Penalty Clauses',
    'Termination Clauses',
    'Confidentiality Clauses',
    'Non-Compete Clauses',
    'Restrictive Clauses'
]

RISK_LEVELS = ['Low', 'Medium', 'High']

# Comprehensive Clause Seed Bank for Indian Commercial Contracts
CLAUSE_TEMPLATES = {
    'Automatic Renewal': {
        'High': [
            "This Agreement shall automatically renew for successive terms of two (2) years each unless the Client provides written notice of non-renewal at least ninety (90) days prior to the expiration date. In the event of non-renewal by Vendor, Vendor shall pay an administrative exit fee of INR 1,50,000.",
            "Upon expiration of the Initial Term, this Agreement shall automatically renew on an evergreen basis for indefinite consecutive periods of twelve (12) months. Notice of non-renewal must be delivered within a strict 5-day window exactly 60 days before the renewal date.",
            "The term of this Contract shall automatically extend for additional three (3) year terms without requiring further execution or consent from either party. Fees for each renewed term shall escalate automatically by 25% over the preceding term.",
            "This Service Agreement will renew automatically on an annual basis. The Service Provider shall have no right to cancel or prevent automatic renewal if any outstanding service ticket remains open on the anniversary date.",
            "Unless cancelled by the Customer in writing strictly via registered post forty-five (45) days prior to expiry, this Supply Contract automatically rolls over for another two years with minimum order commitments binding upon the Supplier.",
            "The subscription and license shall automatically renew for additional twenty-four (24) month cycles. Failure to send notice before 120 days prior to expiry shall deem the Contractor bound for the complete renewed billing cycle without refund.",
            "This Agreement shall perpetuate automatically year after year unless terminated by the Company. The Vendor agrees to a mandatory automatic price discount of 15% for each automatic extension term.",
            "Automatic renewal of this Master Services Agreement shall occur on the anniversary date without limitation, and any attempt to terminate upon renewal shall trigger a liquidated renewal compensation charge of INR 2,00,000."
        ],
        'Medium': [
            "This Agreement shall automatically renew for additional periods of one (1) year unless either party gives written notice of termination at least thirty (30) days prior to the end of the then-current term.",
            "Upon completion of the Initial Term, the contract shall be extended for successive six (6) month periods unless thirty (30) days prior written notice is served by either party.",
            "The Agreement shall automatically renew for an additional 12-month period, subject to an annual rate revision not exceeding the prevailing Reserve Bank of India (RBI) CPI inflation index plus 3%.",
            "Unless either party provides sixty (60) days written notice before the end of the term, this Vendor Contract will renew for a one-year period under identical terms and conditions.",
            "This NDA will automatically renew for one additional year unless either party delivers a written notice of non-renewal at least fifteen (15) business days before the expiration date.",
            "The Supply Agreement shall renew automatically for six (6) months unless disputed in writing 30 days in advance by either party with mutual acknowledgment.",
            "Automatic renewal for a one-year term will take effect unless written objection is received 45 days prior to the scheduled expiration date.",
            "This Service Agreement shall renew for successive 12-month terms unless written notice is given 30 days prior, with pricing adjustments capped at 5% per annum."
        ],
        'Low': [
            "This Agreement shall terminate on the Expiration Date and shall only be renewed upon the mutual written agreement and execution of a formal renewal addendum signed by authorized representatives of both parties.",
            "There shall be no automatic renewal of this Agreement. Any continuation of services beyond the Initial Term shall require a separate, mutually negotiated Statement of Work.",
            "The term of this Contract is strictly twelve (12) months from the Effective Date. Any extension shall be subject to prior mutual written consent at least thirty (30) days prior to expiration.",
            "This Agreement will expire automatically at the conclusion of the Term unless both parties mutually agree in writing to extend the term on mutually agreed commercial terms.",
            "No tacit or automatic renewal shall apply to this Supply Agreement. Renewal may occur solely upon execution of a written extension agreement.",
            "Upon the expiration of the term, this Agreement shall terminate without notice unless explicitly renewed in writing by both the Client and the Service Provider.",
            "This Non-Disclosure Agreement shall expire after three (3) years from the Effective Date without automatic rollover or unilateral extension.",
            "The contract concludes on the specified completion date. Any further engagement requires a new purchase order and signed mutual extension."
        ]
    },
    'Payment Terms': {
        'High': [
            "The Client shall make payment within ninety (90) to one hundred twenty (120) days following receipt of an undisputed invoice. The Client reserves the right to withhold any payment at its sole discretion without incurring interest or liability.",
            "Invoices shall be payable within 120 days of delivery. Late payments by the Vendor for any incidental charges shall accrue penal interest at the rate of 24% per annum compounded monthly.",
            "Payment shall be conditional upon the final customer paying the Client. If the Client does not receive payment from its end-customer, the Subcontractor shall waive all rights to compensation for services rendered.",
            "The Company retains the unilateral right to set off, deduct, or withhold up to 50% of the invoice amount for any alleged defect or delay without prior notice or independent audit.",
            "Payment terms are Net 90 days. The Vendor shall have no right to suspend services or deliveries in the event of non-payment or delayed disbursements by the Buyer.",
            "The Buyer shall pay the Supplier within 180 days from receipt of goods. Any dispute regarding invoice amounts must be notified by the Buyer at any time within 2 years, with immediate refund obligations on the Supplier.",
            "Compensation is subject to milestone approval at the sole, unappealable discretion of the Client, and no progress payments shall be issued for completed intermediate deliverables.",
            "All payments are deferred until complete project handover and final acceptance by third-party auditors, with no liability for interest or interim cash flow compensation to the SMB."
        ],
        'Medium': [
            "Payment shall be made by the Client within forty-five (45) days of receipt of a valid and correct Goods and Services Tax (GST) compliant tax invoice.",
            "Invoices shall be due Net 45 days. Any undisputed amount not paid within the due date shall bear simple interest at the rate of 12% per annum until settled.",
            "The Purchaser shall pay invoices within 30 days of submission. In case of any invoice dispute, the Purchaser may withhold only the disputed portion while releasing the balance.",
            "Payment milestone releases are contingent on Client sign-off, which shall not be unreasonably withheld or delayed beyond fourteen (14) calendar days.",
            "The Vendor shall submit monthly invoices, and the Customer shall process payment within thirty (30) to forty-five (45) business days upon verification of deliverables.",
            "Late payments shall attract interest at the Reserve Bank of India repo rate plus 2% per annum, calculated from the 46th day following invoice receipt.",
            "Payment shall be released Net 30 days after physical inspection of delivered goods at the designated warehouse location in Mumbai.",
            "Taxes including GST shall be shown separately on all invoices and paid by the Client within forty-five (45) days of invoice date."
        ],
        'Low': [
            "The Client shall pay all undisputed invoices within thirty (30) days from the date of receipt of the invoice. Advance mobilization fee of 20% shall be paid upon contract signing.",
            "Payment terms are strictly Net 15 to Net 30 days. Payments shall be remitted via NEFT/RTGS to the designated bank account of the Service Provider.",
            "The Buyer shall process payments within 30 days of invoice receipt. Both parties agree to a transparent milestone payment schedule with prompt sign-offs within 5 business days.",
            "All undisputed payments shall be disbursed within thirty (30) calendar days. Any payment dispute must be raised in writing with detailed reasons within ten (10) business days.",
            "The Service Provider shall be compensated on a monthly retainer basis, payable within fifteen (15) days of each calendar month-end.",
            "Invoices are payable within 30 days. In the event of non-payment exceeding 45 days, the Service Provider reserves the right to suspend services upon 7 days written notice.",
            "Clear payment terms of Net 30 days apply to all deliverables, with statutory GST and TDS deductions documented via valid Form 16A certificates.",
            "Payment for supplies shall be released within 21 days of delivery and acceptance, with zero deductions other than legally mandated TDS under Indian Income Tax Act."
        ]
    },
    'Liability Clauses': {
        'High': [
            "The Service Provider agrees to indemnify, defend, and hold harmless the Client, its affiliates, directors, and agents from any and all claims, losses, damages, liabilities, costs, and expenses without any monetary cap or limitation of liability whatsoever.",
            "The Vendor's total liability under or in connection with this Agreement shall be unlimited, and Vendor shall be liable for all direct, indirect, special, incidental, punitive, and consequential damages, including loss of profits and business interruption.",
            "In no event shall the Client be liable to the Contractor for any damages exceeding INR 1,000, while the Contractor's liability to the Client shall remain fully uncapped and unlimited.",
            "The Supplier assumes full, unlimited liability for any third-party claims arising out of the use of the goods, including consequential losses, patent infringements, and economic damages.",
            "The Consultant shall hold the Company harmless against all losses, whether foreseeable or unforeseeable, without right of contribution, and with no reciprocal indemnity from the Company.",
            "The Vendor agrees to unlimited indemnification for any breach of confidentiality, data protection, intellectual property, or regulatory compliance without any liability ceiling or carve-out.",
            "The Service Provider assumes sole responsibility for all consequential, reputational, and indirect losses suffered by the Client, regardless of negligence or fault.",
            "The Contractor waives all statutory limitations of liability and agrees to unlimited personal and corporate liability for all deliverables provided under this Contract."
        ],
        'Medium': [
            "Each party's aggregate liability under this Agreement shall be capped at three times (3x) the total fees paid or payable by the Client during the twelve (12) months preceding the claim.",
            "The Supplier's total liability for direct damages shall not exceed the total contract value, except in cases of gross negligence, fraud, or willful misconduct.",
            "Except for indemnification obligations relating to intellectual property infringement, neither party shall be liable for indirect, incidental, or consequential damages.",
            "The aggregate liability of either party for all claims arising out of this Agreement shall be limited to an amount equal to two times (2x) the total fees paid under the applicable Statement of Work.",
            "The Service Provider's liability for data security incidents shall be capped at INR 25,00,000 or the total fees paid under this Agreement, whichever is greater.",
            "Each party agrees to indemnify the other for third-party claims arising directly from gross negligence, capped at the insurance policy limit of INR 50,00,000.",
            "Total cumulative liability of the Vendor for breach of performance warranties is capped at 150% of the total purchase order amount.",
            "Liability for breach of contractual obligations is limited to direct proven damages not exceeding twice the annual contract compensation."
        ],
        'Low': [
            "To the maximum extent permitted by applicable law, each party's total aggregate liability arising out of or related to this Agreement shall be strictly limited to the total fees actually paid by the Client in the twelve (12) months preceding the incident.",
            "Neither party shall be liable to the other for any indirect, incidental, special, punitive, exemplary, or consequential damages, including loss of profits, revenue, data, or business opportunities.",
            "Both parties agree to a mutual cap on liability equal to 100% of the total fees paid under this Agreement during the preceding six (6) months.",
            "The parties mutually agree that direct damages capped at the total contract value shall be the sole and exclusive remedy for any breach of this Agreement.",
            "Liability is strictly bilateral and capped at the amount paid by the Customer to the Vendor under the specific Statement of Work giving rise to the claim.",
            "Each party's maximum cumulative liability for any and all claims shall not exceed the total contract consideration received by the Service Provider.",
            "Mutual exclusion of all consequential, indirect, and punitive damages, with aggregate liability capped at the actual invoice value of the affected milestone.",
            "Neither party shall have liability exceeding the sums paid under this Service Agreement in the three (3) months prior to the event causing liability."
        ]
    },
    'Penalty Clauses': {
        'High': [
            "In the event of any delay in deliverable submission, the Vendor shall pay liquidated damages of 2% of the total contract value for each day of delay, without any maximum cap, and the Client may immediately forfeit the entire Security Deposit and Bank Guarantee.",
            "Any defect in materials shall result in an immediate penalty of INR 5,00,000 per occurrence, and the Buyer reserves the right to confiscate all supplier equipment on site without judicial recourse.",
            "Failure to meet agreed service levels (SLA) for two consecutive months will trigger an automatic penalty of 50% of the annual contract value as predetermined liquidated damages under Section 74 of the Indian Contract Act.",
            "The Contractor shall be subject to a penalty of INR 25,000 per hour for system downtime, which shall be deducted directly from pending invoices without right of audit or dispute.",
            "If the Vendor terminates this Agreement early, the Vendor shall pay a punitive penalty equal to the entire remaining value of the contract term plus legal costs.",
            "Delayed delivery of supply batches shall incur liquidated damages of 5% per week up to 100% of the total consignment value, alongside immediate blacklisting of the Supplier.",
            "Failure to achieve 100% performance criteria on day one shall entitle the Customer to forfeit the earnest money deposit and impose a penalty of INR 10,00,000.",
            "The Employee/Consultant shall pay a penalty of INR 10,00,000 if they fail to serve the complete 6-month notice period or commit any procedural breach."
        ],
        'Medium': [
            "For delays attributable solely to the Service Provider, liquidated damages shall accrue at the rate of 0.5% per week of delay, subject to an aggregate maximum cap of 10% of the affected milestone value.",
            "Failure to meet defined SLAs shall result in service credits capped at 15% of the monthly retainer fee for the affected month as the sole remedy.",
            "In case of delayed shipment, the Supplier shall be liable to pay liquidated damages of 1% per week, up to a maximum ceiling of 5% of the purchase order value.",
            "If the Vendor fails to rectify a critical defect within 48 hours, a penalty of INR 5,000 per day shall apply, capped at a maximum of INR 50,000 per incident.",
            "Failure to provide designated personnel will attract a replacement delay penalty of INR 2,000 per day after a mandatory 14-day grace period.",
            "Late delivery penalties shall be calculated at 0.5% per completed week of delay, not to exceed 7.5% of the total order value.",
            "Service level penalties shall be adjusted against future invoices as credit notes, not exceeding 10% of the quarterly billing amount.",
            "Penalty for delivery default is capped at 5% of invoice value after granting a written 7-day cure period."
        ],
        'Low': [
            "The parties agree that in the event of performance delays, the defaulting party shall be granted a reasonable cure period of thirty (30) days following written notice before any remedies or liquidated damages are assessed.",
            "No punitive damages or arbitrary penalty deductions shall apply. Remedies for delays shall be limited to actual, documented direct damages proven by the non-breaching party.",
            "If a milestone is delayed due to force majeure or client dependency, schedules shall be extended day-for-day without any financial penalties or deductions.",
            "Penalties are replaced by mutual good-faith SLA service credits capped at 3% of the monthly fee, applicable solely towards future billing.",
            "Neither party shall be subject to liquidated damages, and any breach shall be addressed through standard cure mechanisms and mutual dispute resolution.",
            "In the event of a quality defect, the Supplier's sole obligation is to repair, replace, or re-perform the defective deliverable within 15 days at no additional charge.",
            "Zero penalty clauses apply; the contract relies on milestone completion sign-offs and mutually agreed rectification windows.",
            "The Service Provider shall have 30 business days to remediate any identified non-conformity without penalty or financial withholding."
        ]
    },
    'Termination Clauses': {
        'High': [
            "The Client may terminate this Agreement at any time, with or without cause, immediately upon 24 hours written notice. The Vendor shall have no right to terminate for convenience and is locked into a mandatory three (3) year term.",
            "The Company reserves the right to terminate this contract immediately without cause, notice, or compensation for work-in-progress, while the Contractor is barred from terminating under any circumstances.",
            "In the event of termination by the Client for any reason, the Service Provider shall immediately refund all fees received during the preceding six (6) months and surrender all work product without payment.",
            "The Buyer may unilaterally cancel this purchase order at any time prior to delivery without compensating the Supplier for customized raw materials or tooling investments.",
            "Immediate termination without cure period shall occur upon any alleged minor breach determined solely by the Client's internal compliance officer.",
            "The Client may terminate this contract for convenience on 3 days notice, with full forfeiture of all pending retainers and accrued billing due to the SMB.",
            "The Contractor is bound to complete the 5-year term and shall pay a unilateral exit penalty of INR 5,00,000 if it seeks early termination for any reason.",
            "Unilateral immediate termination rights are vested solely in the Employer/Client, with zero severance or transition reimbursement payable to the Service Provider."
        ],
        'Medium': [
            "Either party may terminate this Agreement for convenience by providing sixty (60) days prior written notice to the other party.",
            "Either party may terminate this Agreement immediately upon written notice if the other party commits a material breach and fails to cure such breach within thirty (30) days of receiving written notice.",
            "The Client may terminate this Agreement on thirty (30) days notice, provided it pays the Service Provider for all services satisfactorily rendered up to the date of termination.",
            "In the event of termination for convenience by the Customer, the Customer shall reimburse the Vendor for reasonable, unavoidable wind-down costs capped at 15% of the remaining contract value.",
            "Either party may terminate if the other party enters into insolvency, bankruptcy, or liquidation under the Insolvency and Bankruptcy Code (IBC) 2016.",
            "Termination for cause requires a written 21-day notice detailing the breach, with right to cure before formal termination takes effect.",
            "Contract may be terminated with 45 days written notice, with mutual transition assistance provided for up to 30 days at standard hourly rates.",
            "Upon termination, the Client shall pay for all approved deliverables and work-in-progress on a pro-rata basis within 30 days."
        ],
        'Low': [
            "Either party may terminate this Agreement for convenience upon ninety (90) days prior written notice, ensuring sufficient transition and planning time for both parties.",
            "Both parties have equal, bilateral rights to terminate this Agreement for cause upon forty-five (45) days written notice and failure to cure the specified material breach.",
            "Upon any termination, the Client shall promptly pay the Service Provider for all completed work, approved deliverables, and non-cancelable third-party commitments incurred up to the effective termination date.",
            "Mutual termination rights with a 60-day notice period apply equally to both parties, with orderly handover protocols and fair pro-rata fee settlement.",
            "Neither party may terminate for convenience during an active SOW without mutual consent, protecting project continuity and resource investments.",
            "Termination requires bilateral written agreement or an uncured 45-day material breach, with full compensation for all accrued work-in-progress.",
            "Balanced termination provisions grant each party 60 days advance notice, with all IP rights to completed paid work transferring smoothly upon final settlement.",
            "Equal rights to terminate for convenience with 90 days notice, ensuring fair wind-down and zero exit penalties for either party."
        ]
    },
    'Confidentiality Clauses': {
        'High': [
            "The Receiving Party's confidentiality obligations under this Agreement shall survive perpetually and indefinitely in perpetuity. The Receiving Party shall hold all information, ideas, concepts, and residual business knowledge confidential forever and agrees to unlimited liquidated damages of INR 50,00,000 for any alleged disclosure.",
            "The Vendor agrees that all business contacts, client lists, methodologies, and general industry experience acquired during this engagement constitute proprietary trade secrets of the Client and may never be utilized in any future engagement.",
            "Confidentiality obligations are strictly unilateral on the Service Provider, with the Client bearing zero duty of confidentiality regarding the Service Provider's proprietary code, tools, or pricing models.",
            "The Disclosing Party may seek immediate ex-parte injunctions and confiscate the Receiving Party's computing devices upon suspicion of any confidentiality breach without requiring proof of actual damage.",
            "All employee discussions, emails, and technical workflows are deemed strictly confidential for 20 years, with personal liability attached to the SMB directors.",
            "Perpetual non-disclosure applies to all data without standard carve-outs for publicly available information or judicial subpoenas.",
            "The Contractor agrees to a perpetual gag clause preventing any disclosure of the business relationship or general technical work in public portfolios forever.",
            "Unilateral perpetual confidentiality with immediate punitive indemnity of INR 25,00,000 for any inadvertent disclosure."
        ],
        'Medium': [
            "The obligations of confidentiality under this Agreement shall survive for a period of five (5) years following the expiration or termination of this Agreement.",
            "Confidential Information shall be protected with the same degree of care as the Receiving Party uses for its own confidential information, but not less than reasonable care, for three (3) years post-termination.",
            "Confidential Information does not include information that is publicly known, already in the recipient's possession, or required to be disclosed by applicable law or regulatory authority.",
            "Upon termination, each party shall either return or certify the secure destruction of all Confidential Information within thirty (30) days, except for statutory backup archives.",
            "Confidentiality terms shall bind both parties for four (4) years, with standard carve-outs for legally mandated disclosures and independent development.",
            "The receiving party shall restrict disclosure of Confidential Information strictly to employees and contractors with a need-to-know, bound by written NDAs.",
            "Mutual confidentiality obligations shall endure for three (3) years from the date of disclosure, governed by standard commercial trade secret protections.",
            "Non-disclosure obligations continue for 5 years after agreement termination, excluding information disclosed under order of an Indian court."
        ],
        'Low': [
            "The confidentiality obligations under this Agreement shall remain in effect for a reasonable period of two (2) years from the date of disclosure, after which all obligations shall expire.",
            "Mutual confidentiality protections apply equally to both parties, with comprehensive standard exclusions for public domain information, independent development, and third-party lawful disclosures.",
            "Each party agrees to protect the other's confidential data using standard reasonable care for twenty-four (24) months post-termination, with express rights to retain one copy for legal compliance records.",
            "Confidentiality duration is bilateral and capped at eighteen (18) months following contract completion, with zero restriction on generic residual skills and knowledge.",
            "Mutual non-disclosure terms for two (2) years with clear, balanced definitions, allowing standard publicity mentions in client lists upon prior written consent.",
            "Standard 2-year mutual confidentiality agreement with clear exceptions for disclosures required by regulatory or tax authorities under Indian Law.",
            "Bilateral confidentiality obligations terminate two years after project delivery, with mutual return or deletion of digital assets.",
            "Reasonable 24-month confidentiality window with complete bilateral reciprocity and standard industry carve-outs."
        ]
    },
    'Non-Compete Clauses': {
        'High': [
            "The Service Provider and its employees agree not to engage in any competing business, provide similar services, or work for any entity in the same industry anywhere in India or globally for a period of three (3) years following the termination of this Agreement (in potential contravention of Section 27 of the Indian Contract Act 1872).",
            "The Consultant is strictly prohibited from offering consulting services to any technology firm in Asia for twenty-four (24) months post-contract, on penalty of INR 20,00,000.",
            "The Vendor covenants that it will not develop, market, or sell any software related to fintech or enterprise operations to any competitor of the Client for a duration of five (5) years.",
            "The Employee/Contractor shall not accept employment or independent advisory roles with any client, vendor, or competitor of the Company worldwide for 2 years post-departure.",
            "Extensive post-termination non-compete restricts the SMB from operating in its core domain across Maharashtra, Karnataka, and Delhi NCR for three years.",
            "The Supplier is barred from selling similar manufactured components to any other buyer within the Indian territory for forty-eight (48) months.",
            "Total geographic and industry non-compete for 36 months, enforceable through immediate injunctive relief and liquidated damages of INR 30,00,000.",
            "The Service Provider is prohibited from bidding on any public or private tender in the client's sector for two years following contract cessation."
        ],
        'Medium': [
            "The Vendor agrees not to solicit or hire any employee or contractor of the Client directly involved in this project for a period of twelve (12) months following the termination of this Agreement.",
            "The Consultant agrees not to directly solicit business from the named clients introduced by the Company for a period of one (1) year post-termination within the city of Mumbai.",
            "Non-solicitation of clients and staff shall be limited to a 12-month period post-termination and restricted strictly to direct project collaborators.",
            "The Service Provider agrees not to provide identical customized software to direct named competitors of the Client for six (6) months post-delivery.",
            "Vendor shall not solicit the Client's active accounts identified in Schedule A for a period of nine (9) months from contract termination.",
            "Mutual non-solicitation of key project personnel for twelve (12) months post-completion, with liquidated buyout fee equal to 3 months salary.",
            "Restricted non-solicitation clause applying strictly to active project team members for one year following SOW closure.",
            "Non-solicitation of direct client contacts within the specific territory of Bengaluru for a duration of 12 months."
        ],
        'Low': [
            "Nothing in this Agreement shall restrict the Service Provider from providing identical or similar services to any third party or competitor, provided the Service Provider does not breach its confidentiality obligations.",
            "The parties agree that there are no non-compete restrictions, and the Service Provider remains entirely free to practice its trade, profession, and business in accordance with Section 27 of the Indian Contract Act, 1872.",
            "No non-compete restrictions apply. The Vendor is free to conduct commercial business with any third party globally without restriction.",
            "Non-solicitation is mutual and limited strictly to direct project team members for a period not exceeding six (6) months post-completion.",
            "The Agreement explicitly recognizes the Service Provider's right to develop similar solutions for other customers using general know-how and independent open-source tools.",
            "Zero post-termination non-compete covenants; the Service Provider retains full freedom to engage with market competitors.",
            "Mutual acknowledgment that general industry competition is unrestricted, preserving both parties' commercial independence.",
            "No geographical or industry non-compete covenant; engagement is non-exclusive for both parties."
        ]
    },
    'Restrictive Clauses': {
        'High': [
            "All intellectual property rights, pre-existing background code, proprietary tools, frameworks, and future inventions developed by the Vendor during the term shall become the sole and exclusive property of the Client as a work-made-for-hire, with Vendor waiving all moral rights.",
            "The Client shall have the unrestricted right to enter and audit the Vendor's physical premises, source code repositories, and financial books at any time without prior notice.",
            "The Vendor shall not use the Client's name, logo, or engagement details in any portfolio, case study, marketing material, or investor presentation under any circumstances.",
            "The Service Provider assigns all worldwide rights in any proprietary methodology, software library, or trade secret utilized during the project to the Customer exclusively without additional compensation.",
            "The Supplier is restricted from making any changes to its management, corporate structure, or ownership without prior written approval from the Buyer.",
            "The Contractor agrees to a complete negative covenant barring it from publishing technical research or speaking at conferences regarding general technologies used in the project.",
            "Unconditional assignment of all past, present, and future background IP of the SMB to the Client upon signature of this Contract.",
            "The Vendor shall be subject to 24/7 unannounced compliance audits with full liability for third-party auditor fees incurred by the Client."
        ],
        'Medium': [
            "Custom deliverables created specifically for the Client shall belong to the Client upon full payment, while the Service Provider retains all rights to its pre-existing tools and background IP.",
            "The Client may conduct an annual audit of project-related records upon at least fifteen (15) business days prior written notice during normal business hours.",
            "The Vendor may include the Client's name and generic logo in its client roster and marketing materials, subject to the Client's standard trademark usage guidelines.",
            "The Service Provider grants the Client a perpetual, royalty-free, non-exclusive license to use background IP embedded within the final project deliverables.",
            "Audit rights are limited to once per calendar year, conducted by an independent certified auditor at the requesting party's sole expense.",
            "Use of company brand assets for press releases or public case studies requires prior written approval from the other party, not to be unreasonably withheld.",
            "Custom code transfers to Client upon receipt of final invoice payment, with Vendor granting license to standard utility libraries.",
            "Audit inspections require twenty (20) business days advance notification and are limited to direct project-related compliance documentation."
        ],
        'Low': [
            "The Service Provider retains all right, title, and interest in its pre-existing intellectual property, reusable software libraries, generic know-how, and proprietary frameworks.",
            "Custom project deliverables transfer to the Client upon full and final payment of all corresponding milestone invoices.",
            "The Service Provider may reference the Client as a customer and publish a brief high-level case study with mutual approval on text and branding.",
            "No audit rights into internal financials or proprietary code repositories; compliance reviews are limited to mutual deliverable verification meetings.",
            "The Client receives a non-exclusive, worldwide, perpetual license to use the delivered custom software for its internal business operations.",
            "Both parties retain full ownership of their respective background intellectual property and trademark assets.",
            "Standard balanced IP terms: Client owns bespoke deliverables, Service Provider retains core development accelerators and generic utilities.",
            "Freedom to use general skills, techniques, and public domain technologies without restrictive covenants or audit intrusion."
        ]
    }
}


def generate_augmented_dataset(target_rows=1200):
    """
    Generates a balanced, rich dataset of annotated contract clauses.
    Returns a pandas DataFrame.
    """
    records = []
    clause_id = 1
    
    # Generate variations using legal phrasing patterns
    modifiers = [
        ("Furthermore, ", "in accordance with applicable statutory rules, "),
        ("Notwithstanding anything to the contrary contained herein, ", "subject to the provisions hereof, "),
        ("It is expressly agreed that ", "under all circumstances and conditions, "),
        ("Pursuant to the terms of this Agreement, ", "as stipulated by the governing board, "),
        ("Provided always that ", "subject to compliance with Indian laws, "),
        ("", ""),
        ("In addition to the foregoing, ", "without prejudice to any other remedies, "),
        ("For the avoidance of doubt, ", "as mutually acknowledged by the parties, ")
    ]
    
    cities = ["Mumbai", "Bengaluru", "New Delhi", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad", "Gurugram", "Noida"]
    acts = [
        "Indian Contract Act, 1872",
        "Arbitration and Conciliation Act, 1996",
        "Information Technology Act, 2000",
        "Insolvency and Bankruptcy Code, 2016",
        "Specific Relief Act, 1963",
        "Companies Act, 2013"
    ]
    
    # 1. Base seed clauses
    for category, levels in CLAUSE_TEMPLATES.items():
        for risk_level, clauses in levels.items():
            for clause in clauses:
                contract_type = random.choice(CONTRACT_TYPES)
                city = random.choice(cities)
                act = random.choice(acts)
                
                records.append({
                    'clause_id': f"IND-CLS-{clause_id:05d}",
                    'contract_type': contract_type,
                    'clause_category': category,
                    'risk_level': risk_level,
                    'clause_text': clause,
                    'governing_act': act,
                    'jurisdiction_city': city,
                    'is_synthetic': False
                })
                clause_id += 1
                
    # 2. Augmented Variations to reach target_rows
    while len(records) < target_rows:
        category = random.choice(RISK_CATEGORIES)
        risk_level = random.choice(RISK_LEVELS)
        base_clause = random.choice(CLAUSE_TEMPLATES[category][risk_level])
        prefix, infix = random.choice(modifiers)
        contract_type = random.choice(CONTRACT_TYPES)
        city = random.choice(cities)
        act = random.choice(acts)
        
        # Apply synthetic contextual variation
        modified_clause = f"{prefix}{base_clause}"
        if infix and infix not in modified_clause:
            words = modified_clause.split(' ')
            if len(words) > 6:
                insert_pos = random.randint(3, len(words) - 3)
                words.insert(insert_pos, infix)
                modified_clause = ' '.join(words)
                
        records.append({
            'clause_id': f"IND-CLS-{clause_id:05d}",
            'contract_type': contract_type,
            'clause_category': category,
            'risk_level': risk_level,
            'clause_text': modified_clause.strip(),
            'governing_act': act,
            'jurisdiction_city': city,
            'is_synthetic': True
        })
        clause_id += 1
        
    df = pd.DataFrame(records)
    return df


def create_sample_contracts():
    """
    Creates 5 full, authentic sample Indian contracts in data/sample_contracts/
    """
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    
    samples = {
        'service_agreement.txt': """MASTER SERVICE AGREEMENT

This Master Service Agreement ("Agreement") is made and entered into on this 15th day of January, 2026 ("Effective Date") at Bengaluru, Karnataka, India by and between:

ALPHA TECH ENTERPRISES PVT. LTD., a private limited company incorporated under the Companies Act, 2013, having its registered office at 4th Floor, Tech Park, Outer Ring Road, Bengaluru 560103, Karnataka (hereinafter referred to as the "Client" or "Company");

AND

FASTGROWTH SOLUTIONS LLP, a limited liability partnership having its registered office at Suite 202, MG Road, Pune 411001, Maharashtra, represented by its Designated Partner Rajesh Sharma (hereinafter referred to as the "Service Provider" or "Vendor").

RECITALS:
WHEREAS, the Client is engaged in the business of digital payments and financial technology;
WHEREAS, the Service Provider possesses specialized technical expertise in cloud infrastructure management, software development, and AI systems maintenance;
WHEREAS, the Client desires to engage the Service Provider, and the Service Provider agrees to deliver services under the following terms:

NOW, THEREFORE, IT IS AGREED AS FOLLOWS:

1. SCOPE OF SERVICES
1.1 The Service Provider shall perform software engineering, bug fixes, API integrations, and cloud maintenance services as specified in Statements of Work (SOWs) executed from time to time.
1.2 Time is of the essence in the execution of all deliverables under this Agreement.

2. PAYMENT TERMS
2.1 Invoices shall be submitted monthly upon completion of milestones. The Client shall make payment within ninety (90) to one hundred twenty (120) days following receipt of an undisputed invoice. The Client reserves the right to withhold any payment at its sole discretion without incurring interest or liability.
2.2 All fees are exclusive of Goods and Services Tax (GST) at 18%, and Tax Deducted at Source (TDS) shall be deducted under Section 194J of the Income Tax Act, 1961.

3. TERM AND AUTOMATIC RENEWAL
3.1 The Initial Term of this Agreement shall be twelve (12) months from the Effective Date.
3.2 This Agreement shall automatically renew for successive terms of two (2) years each unless the Client provides written notice of non-renewal at least ninety (90) days prior to the expiration date. In the event of non-renewal by Vendor, Vendor shall pay an administrative exit fee of INR 1,50,000.

4. LIMITATION OF LIABILITY AND INDEMNITY
4.1 The Service Provider agrees to indemnify, defend, and hold harmless the Client, its affiliates, directors, and agents from any and all claims, losses, damages, liabilities, costs, and expenses without any monetary cap or limitation of liability whatsoever.
4.2 The Vendor's total liability under or in connection with this Agreement shall be unlimited, and Vendor shall be liable for all direct, indirect, special, incidental, punitive, and consequential damages, including loss of profits and business interruption.

5. PENALTIES AND LIQUIDATED DAMAGES
5.1 In the event of any delay in deliverable submission, the Vendor shall pay liquidated damages of 2% of the total contract value for each day of delay, without any maximum cap, and the Client may immediately forfeit the entire Security Deposit and Bank Guarantee.
5.2 Failure to meet agreed service levels (SLA) for two consecutive months will trigger an automatic penalty of 50% of the annual contract value as predetermined liquidated damages under Section 74 of the Indian Contract Act.

6. TERMINATION
6.1 The Client may terminate this Agreement at any time, with or without cause, immediately upon 24 hours written notice. The Vendor shall have no right to terminate for convenience and is locked into a mandatory three (3) year term.
6.2 In the event of termination by the Client for any reason, the Service Provider shall immediately refund all fees received during the preceding six (6) months and surrender all work product without payment.

7. CONFIDENTIALITY
7.1 The obligations of confidentiality under this Agreement shall survive for a period of five (5) years following the expiration or termination of this Agreement.
7.2 Confidential Information does not include information that is publicly known, already in the recipient's possession, or required to be disclosed by applicable law or regulatory authority under Indian statutes.

8. NON-COMPETE AND RESTRICTIVE COVENANTS
8.1 The Service Provider and its employees agree not to engage in any competing business, provide similar services, or work for any entity in the same industry anywhere in India or globally for a period of three (3) years following the termination of this Agreement (in potential contravention of Section 27 of the Indian Contract Act 1872).
8.2 All intellectual property rights, pre-existing background code, proprietary tools, frameworks, and future inventions developed by the Vendor during the term shall become the sole and exclusive property of the Client as a work-made-for-hire, with Vendor waiving all moral rights.

9. GOVERNING LAW AND DISPUTE RESOLUTION
9.1 This Agreement shall be governed by and construed in accordance with the laws of India.
9.2 Any dispute arising out of this Agreement shall be referred to arbitration in Bengaluru under the Arbitration and Conciliation Act, 1996 before a sole arbitrator appointed by the Client.

IN WITNESS WHEREOF, the Parties have executed this Agreement by their duly authorized representatives.

For ALPHA TECH ENTERPRISES PVT. LTD.      For FASTGROWTH SOLUTIONS LLP
Authorized Signatory: Vikram Verma        Authorized Signatory: Rajesh Sharma
Designation: Managing Director             Designation: Designated Partner
""",

        'vendor_agreement.txt': """COMMERCIAL VENDOR SUPPLY AGREEMENT

This Vendor Agreement ("Agreement") is executed on 1st March 2026 at Mumbai, Maharashtra between:

RELIABLE INDUSTRIAL CORP LTD., Mumbai (hereinafter called the "Purchaser");
AND
MAHARASHTRA METAL CRAFTS PVT LTD., Pune (hereinafter called the "Vendor").

1. SUPPLY OF GOODS
1.1 The Vendor shall manufacture and supply industrial precision components as per Purchase Orders issued by the Purchaser.

2. PAYMENT TERMS
2.1 Payment shall be made by the Purchaser within forty-five (45) days of receipt of a valid and correct Goods and Services Tax (GST) compliant tax invoice.
2.2 Any undisputed amount not paid within the due date shall bear simple interest at the rate of 12% per annum until settled.

3. TERM AND EXTENSION
3.1 Upon completion of the Initial Term, the contract shall be extended for successive six (6) month periods unless thirty (30) days prior written notice is served by either party.

4. LIABILITY AND WARRANTY
4.1 The Supplier's total liability for direct damages shall not exceed the total contract value, except in cases of gross negligence, fraud, or willful misconduct.
4.2 Except for indemnification obligations relating to intellectual property infringement, neither party shall be liable for indirect, incidental, or consequential damages.

5. PENALTY FOR DELAYS
5.1 For delays attributable solely to the Vendor, liquidated damages shall accrue at the rate of 0.5% per week of delay, subject to an aggregate maximum cap of 10% of the affected milestone value.

6. TERMINATION
6.1 Either party may terminate this Agreement for convenience by providing sixty (60) days prior written notice to the other party.
6.2 Either party may terminate this Agreement immediately upon written notice if the other party commits a material breach and fails to cure such breach within thirty (30) days.

7. CONFIDENTIALITY
7.1 Confidential Information shall be protected with the same degree of care as the Receiving Party uses for its own confidential information, but not less than reasonable care, for three (3) years post-termination.

8. NON-SOLICITATION AND IP
8.1 The Vendor agrees not to solicit or hire any employee or contractor of the Client directly involved in this project for a period of twelve (12) months following the termination of this Agreement.
8.2 Custom deliverables created specifically for the Client shall belong to the Client upon full payment, while the Service Provider retains all rights to its pre-existing tools and background IP.

9. JURISDICTION
Governed by laws of India with exclusive jurisdiction of courts at Mumbai.
""",

        'employment_agreement.txt': """EXECUTIVE EMPLOYMENT AGREEMENT

This Employment Agreement is entered into on 1st February 2026 at Gurugram, Haryana between:

APEX CLOUD SERVICES INDIA PVT. LTD. ("Employer" or "Company");
AND
AMIT K. SHARMA ("Employee").

1. POSITION AND DUTIES
1.1 The Employee is appointed as Principal AI Engineer and shall perform technical research and architectural design duties.

2. COMPENSATION AND EXPENSES
2.1 Annual CTC of INR 32,00,000 payable monthly via direct bank deposit on the 1st of each month subject to statutory TDS and Provident Fund (PF) deductions.

3. NOTICE PERIOD AND TERMINATION
3.1 Either party may terminate employment with sixty (60) days written notice or payment of basic salary in lieu thereof.
3.2 The Employee shall not be entitled to severance if terminated for cause (fraud, embezzlement, criminal misconduct).

4. CONFIDENTIALITY
4.1 The Employee agrees to keep all proprietary source code, algorithms, and customer data confidential for a period of three (3) years following cessation of employment.

5. NON-COMPETE AND NON-SOLICIT
5.1 The Employee/Contractor shall not accept employment or independent advisory roles with any client, vendor, or competitor of the Company worldwide for 2 years post-departure. (Note: Subject to Section 27 of the Indian Contract Act 1872).
5.2 The Employee agrees not to solicit any company colleagues for a period of twelve (12) months following resignation.

6. INTELLECTUAL PROPERTY ASSIGNMENT
6.1 All inventions, patents, software, and trade secrets created by the Employee during the course of employment shall constitute work-for-hire and belong exclusively to the Company.

7. GOVERNING LAW
Governed by Indian Law; Courts at Gurugram shall have exclusive jurisdiction.
""",

        'nda_agreement.txt': """MUTUAL NON-DISCLOSURE AGREEMENT

This Mutual Non-Disclosure Agreement ("NDA") is made on 10th February 2026 at Hyderabad, Telangana between:

QUANTUM DATA LABS PVT. LTD., Hyderabad ("Party A");
AND
NEXUS CONSULTING SERVICES LLP, Chennai ("Party B").

1. PURPOSE
The parties wish to explore a potential joint business partnership regarding AI analytics for legal and enterprise data ("Purpose").

2. CONFIDENTIAL INFORMATION
Confidential Information includes all technical, financial, and business data disclosed by one Party to the other.

3. TERM AND CONFIDENTIALITY OBLIGATION
3.1 The confidentiality obligations under this Agreement shall remain in effect for a reasonable period of two (2) years from the date of disclosure, after which all obligations shall expire.
3.2 This Agreement shall terminate on the Expiration Date and shall only be renewed upon the mutual written agreement of both parties.

4. EXCLUSIONS
Confidential Information does not include info in the public domain, already known to recipient, or required by court order under Indian law.

5. LIMITATION OF LIABILITY
5.1 To the maximum extent permitted by applicable law, each party's total aggregate liability arising out of or related to this Agreement shall be strictly limited to direct proven damages not exceeding INR 10,00,000.
5.2 Neither party shall be liable for indirect, punitive, or consequential damages.

6. RETURN OF MATERIALS
Within 15 days of written request, each party shall return or destroy all physical and electronic confidential files.

7. GOVERNING LAW
Governed by the laws of India, subject to the jurisdiction of courts in Hyderabad.
""",

        'supply_agreement.txt': """ANNUAL RAW MATERIAL SUPPLY AGREEMENT

This Supply Agreement is made on 20th January 2026 at New Delhi between:

BHARAT AGRO PROCESSING LTD., New Delhi ("Buyer");
AND
KAVERI AGRI SUPPLIES CO., Chandigarh ("Supplier").

1. PURCHASE COMMITMENT AND ORDERS
1.1 Buyer agrees to purchase Grade-A processed grains as per quarterly Purchase Orders.

2. PRICING AND PAYMENT TERMS
2.1 The Buyer shall process payments within thirty (30) days of invoice receipt. Both parties agree to a transparent milestone payment schedule.
2.2 Statutory GST shall be charged at 5% and paid promptly.

3. TERM AND RENEWAL
3.1 The term of this Contract is strictly twelve (12) months from the Effective Date. Any extension shall be subject to prior mutual written consent at least thirty (30) days prior to expiration.

4. QUALITY AND PENALTIES
4.1 If a shipment fails quality testing, Supplier's sole obligation is to replace the defective batch within 7 days at Supplier's cost. No punitive damages shall apply.

5. TERMINATION
5.1 Either party may terminate for convenience upon ninety (90) days prior written notice, ensuring fair wind-down and zero exit penalties for either party.

6. GOVERNING LAW
Governed by Indian Law; Arbitration in New Delhi under the Arbitration and Conciliation Act, 1996.
"""
    }
    
    for filename, content in samples.items():
        filepath = os.path.join(SAMPLE_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"Sample contract created: {filepath}")


def ingest_kaggle_dataset(kaggle_csv_path):
    """
    Ingests and standardizes a Kaggle Legal Indian Contract Clauses Dataset CSV file.
    Maps arbitrary column names to standard schema:
    [clause_id, contract_type, clause_category, risk_level, clause_text, governing_act, jurisdiction_city]
    """
    if not os.path.exists(kaggle_csv_path):
        print(f"File not found: {kaggle_csv_path}")
        return None
        
    df_raw = pd.read_csv(kaggle_csv_path)
    print(f"Raw Kaggle dataset shape: {df_raw.shape}")
    
    # Column mapping heuristic
    col_map = {}
    for col in df_raw.columns:
        c_lower = col.lower()
        if 'clause' in c_lower and ('text' in c_lower or 'content' in c_lower or 'sentence' in c_lower):
            col_map[col] = 'clause_text'
        elif 'category' in c_lower or 'type' in c_lower or 'label' in c_lower:
            col_map[col] = 'clause_category'
        elif 'risk' in c_lower or 'severity' in c_lower:
            col_map[col] = 'risk_level'
        elif 'contract' in c_lower:
            col_map[col] = 'contract_type'
            
    df_clean = df_raw.rename(columns=col_map)
    return df_clean


def main():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(SAMPLE_DIR, exist_ok=True)
    
    print("Generating enriched Indian Legal Contract Clauses Dataset...")
    df = generate_augmented_dataset(target_rows=1500)
    
    csv_path = os.path.join(PROCESSED_DIR, 'clauses_dataset.csv')
    json_path = os.path.join(PROCESSED_DIR, 'clauses_dataset.json')
    
    df.to_csv(csv_path, index=False, encoding='utf-8')
    df.to_json(json_path, orient='records', indent=2)
    
    print(f"Dataset generated successfully! Total rows: {len(df)}")
    print(f"Saved to: {csv_path} and {json_path}")
    print(f"Clause Categories: {df['clause_category'].value_counts().to_dict()}")
    print(f"Risk Levels: {df['risk_level'].value_counts().to_dict()}")
    
    print("\nCreating 5 authentic Indian sample contracts...")
    create_sample_contracts()
    print("Sample contracts ready in data/sample_contracts/")


if __name__ == '__main__':
    main()
