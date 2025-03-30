# intelligent_resume_analyzer_simple/scoring.py
def normalize_score(score):
    """Normalizes a score to a percentage (0-100)."""
    return max(0, min(100, score))