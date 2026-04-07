from app.rag.retriever import DocumentRetriever


def test_lexical_score_boosts_overlap():
    retriever = DocumentRetriever.__new__(DocumentRetriever)
    query_terms = ["expense", "approval", "cfo"]

    high = retriever._lexical_score(query_terms, "Expense approval requires CFO sign-off.")
    low = retriever._lexical_score(query_terms, "Holiday calendar and onboarding guidance.")

    assert high > low
    assert 0.0 <= high <= 1.0
    assert 0.0 <= low <= 1.0
