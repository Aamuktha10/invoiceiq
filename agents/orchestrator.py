from agents.extraction_agent import ExtractionAgent
from agents.validation_agent import ValidationAgent
from agents.routing_agent import RoutingAgent

class OrchestratorAgent:
    def __init__(self):
        self.extractor = ExtractionAgent()
        self.validator = ValidationAgent()
        self.router = RoutingAgent()
        self._report_log = []

    def run(self, filepath, budget_limit, department):
        print("[Orchestrator] Step 1: Extracting...")
        extracted = self.extractor.extract(filepath)

        print("[Orchestrator] Step 2: Validating...")
        validation = self.validator.validate(
            extracted_data=extracted,
            budget_limit=budget_limit,
            existing_invoices=self._report_log
        )

        print("[Orchestrator] Step 3: Routing...")
        routing = self.router.route(
            extracted_data=extracted,
            validation=validation,
            department=department
        )

        result = {
            "extracted": extracted,
            "validation": validation,
            "routing": routing,
            "status": "approved" if routing["auto_approved"] else "pending_review"
        }

        self._report_log.append({
            "vendor": extracted.get("vendor", "Unknown"),
            "amount": extracted.get("amount", 0),
            "date": extracted.get("date", "Unknown"),
            "status": result["status"],
            "flags": validation.get("flags", []),
            "routed_to": routing.get("routed_to", "Unknown")
        })

        return result

    def get_report_log(self):
        return self._report_log

    def clear_report_log(self):
        self._report_log = []
