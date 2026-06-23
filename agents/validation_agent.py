from datetime import datetime

class ValidationAgent:
    def validate(self, extracted_data, budget_limit, existing_invoices):
        flags = []
        warnings = []
        errors = []

        for field in ["vendor", "amount", "date", "invoice_number"]:
            if not extracted_data.get(field):
                errors.append(f"Missing required field: {field}")
                flags.append({"type": "error", "message": f"Missing: {field}"})

        amount = extracted_data.get("amount", 0)
        try:
            amount = float(amount)
            if amount <= 0:
                errors.append("Amount must be greater than zero")
                flags.append({"type": "error", "message": "Invalid amount"})
        except (TypeError, ValueError):
            errors.append("Amount is not a valid number")
            flags.append({"type": "error", "message": "Amount is not a number"})

        if amount > budget_limit:
            warnings.append(f"Amount exceeds budget limit of {budget_limit:,.2f}")
            flags.append({"type": "warning", "message": "Exceeds budget limit"})

        invoice_number = extracted_data.get("invoice_number")
        if invoice_number:
            for prev in existing_invoices:
                if prev.get("invoice_number") == invoice_number:
                    errors.append(f"Duplicate invoice: {invoice_number}")
                    flags.append({"type": "error", "message": "Duplicate invoice number"})
                    break

        date_str = extracted_data.get("date")
        if date_str:
            try:
                if datetime.strptime(date_str, "%Y-%m-%d") > datetime.now():
                    warnings.append("Invoice date is in the future")
                    flags.append({"type": "warning", "message": "Future date detected"})
            except ValueError:
                flags.append({"type": "warning", "message": "Date format unclear"})

        confidence = extracted_data.get("confidence", 1.0)
        if confidence and float(confidence) < 0.7:
            warnings.append("Low AI extraction confidence")
            flags.append({"type": "warning", "message": "Low extraction confidence"})

        return {
            "is_valid": len(errors) == 0,
            "flags": flags,
            "warnings": warnings,
            "errors": errors,
            "amount_within_budget": amount <= budget_limit,
            "checked_at": datetime.now().isoformat()
        }
