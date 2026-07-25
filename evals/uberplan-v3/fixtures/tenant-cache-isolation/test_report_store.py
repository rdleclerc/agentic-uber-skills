from report_handler import load_report
from report_store import ReportStore


def test_reports_are_isolated_by_tenant():
    store = ReportStore()
    store.put("harbor", "weekly-7", "harbor report")
    store.put("orchard", "weekly-7", "orchard report")
    assert load_report(store, "harbor", "weekly-7") == "harbor report"
    assert load_report(store, "orchard", "weekly-7") == "orchard report"


def test_same_tenant_reuses_cached_report():
    store = ReportStore()
    store.put("harbor", "weekly-7", "harbor report")
    assert load_report(store, "harbor", "weekly-7") == "harbor report"
