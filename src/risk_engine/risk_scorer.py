"""
Composite Risk Scoring Module
Computes overall contract risk score (0-100), risk distribution,
and risk badge status from evaluated clauses.
"""

def compute_contract_risk_score(analyzed_clauses: list[dict]) -> dict:
    """
    Computes weighted composite contract risk score (0 to 100).
    High Risk Clause: 25-30 weight
    Medium Risk Clause: 12-15 weight
    Low Risk Clause: 3-5 weight
    """
    if not analyzed_clauses:
        return {
            'overall_score': 0,
            'risk_level': 'Low',
            'badge_color': 'green',
            'high_count': 0,
            'medium_count': 0,
            'low_count': 0,
            'total_clauses': 0,
            'category_distribution': {},
            'risk_percentage_breakdown': {'High': 0, 'Medium': 0, 'Low': 0}
        }

    high_clauses = [c for c in analyzed_clauses if c.get('risk_level') == 'High']
    medium_clauses = [c for c in analyzed_clauses if c.get('risk_level') == 'Medium']
    low_clauses = [c for c in analyzed_clauses if c.get('risk_level') == 'Low']

    n_total = len(analyzed_clauses)
    n_high = len(high_clauses)
    n_medium = len(medium_clauses)
    n_low = len(low_clauses)

    # Category distribution
    cat_dist = {}
    for c in analyzed_clauses:
        cat = c.get('clause_category', 'Other')
        cat_dist[cat] = cat_dist.get(cat, 0) + 1

    # Base weighted sum
    # Formula emphasizes high severity risks typical in legal contracts
    raw_score = (n_high * 28.0) + (n_medium * 12.0) + (n_low * 3.0)
    
    # Normalization factor based on clause count
    if n_total <= 4:
        normalized_score = min(100, (n_high * 32) + (n_medium * 15) + 10)
    else:
        # Scale to max 100
        normalized_score = min(100, (raw_score / max(1, n_total * 20)) * 100)

    # If 3 or more high risk clauses are present, minimum risk score is 75
    if n_high >= 3:
        normalized_score = max(75, normalized_score)
    elif n_high >= 1:
        normalized_score = max(55, normalized_score)

    final_score = int(round(min(100, max(5, normalized_score))))

    # Risk level classification
    if final_score >= 71:
        overall_risk_level = 'High'
        badge_color = 'danger'  # Red
        recommendation_headline = "High Risk: Review and renegotiate critical clauses prior to signing."
    elif final_score >= 36:
        overall_risk_level = 'Medium'
        badge_color = 'warning'  # Amber
        recommendation_headline = "Moderate Risk: Several commercial terms require clarification."
    else:
        overall_risk_level = 'Low'
        badge_color = 'success'  # Green
        recommendation_headline = "Low Risk: Contract contains standard, balanced commercial terms."

    pct_high = round((n_high / n_total) * 100, 1)
    pct_med = round((n_medium / n_total) * 100, 1)
    pct_low = round((n_low / n_total) * 100, 1)

    return {
        'overall_score': final_score,
        'risk_level': overall_risk_level,
        'badge_color': badge_color,
        'recommendation_headline': recommendation_headline,
        'high_count': n_high,
        'medium_count': n_medium,
        'low_count': n_low,
        'total_clauses': n_total,
        'category_distribution': cat_dist,
        'risk_percentage_breakdown': {
            'High': pct_high,
            'Medium': pct_med,
            'Low': pct_low
        }
    }
