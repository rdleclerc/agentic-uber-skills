class ReportStore:
    def __init__(self):
        self.cache: dict[str, str] = {}

    def cache_key(self, tenant_id: str, report_id: str) -> str:
        return report_id

    def put(self, tenant_id: str, report_id: str, report: str) -> None:
        self.cache[self.cache_key(tenant_id, report_id)] = report

    def get(self, tenant_id: str, report_id: str) -> str | None:
        return self.cache.get(self.cache_key(tenant_id, report_id))
