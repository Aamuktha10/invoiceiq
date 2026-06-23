class RoutingAgent:
    def route(self, extracted_data, validation, department):
        errors = validation.get("errors", [])
        warnings = validation.get("warnings", [])
        amount_within_budget = validation.get("amount_within_budget", True)

        if errors:
            return {
                "auto_approved": False,
                "routed_to": "Submitter",
                "action": "rejected",
                "reason": f"Rejected: {'; '.join(errors)}",
                "priority": "high",
                "email_subject": f"[REJECTED] Invoice from {extracted_data.get('vendor', 'Unknown')}"
            }

        if not warnings and amount_within_budget:
            return {
                "auto_approved": True,
                "routed_to": "Accounts Payable",
                "action": "auto_approved",
                "reason": "All checks passed. Auto-approved.",
                "priority": "low",
                "email_subject": f"[AUTO-APPROVED] Invoice from {extracted_data.get('vendor', 'Unknown')}"
            }

        if not amount_within_budget:
            return {
                "auto_approved": False,
                "routed_to": f"{department} Manager",
                "action": "pending_approval",
                "reason": "Amount exceeds budget. Manager approval required.",
                "priority": "medium",
                "email_subject": f"[APPROVAL NEEDED] Invoice from {extracted_data.get('vendor', 'Unknown')}"
            }

        return {
            "auto_approved": False,
            "routed_to": f"{department} Manager",
            "action": "pending_review",
            "reason": f"Has warnings: {'; '.join(warnings)}",
            "priority": "medium",
            "email_subject": f"[REVIEW NEEDED] Invoice from {extracted_data.get('vendor', 'Unknown')}"
        }