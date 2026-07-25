from report_store import ReportStore


def load_report(store: ReportStore, tenant_id: str, report_id: str) -> str | None:
    return store.get(tenant_id=tenant_id, report_id=report_id)
