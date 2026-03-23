if doc.status != "Invoiced":
    pass
else:
    po_controls = frappe.get_all(
        "PO Control",
        filters={"rental_contract": doc.rental_contract},
        fields=["name", "status", "remaining_balance", "po_number"]
    )
    if po_controls:
        po_control = frappe.get_doc("PO Control", po_controls[0]["name"])
        if po_control.status == "Expired":
            frappe.throw(f"Cannot invoice. PO {po_control.po_number} has expired.")
        if po_control.status == "Exhausted":
            frappe.throw(f"Cannot invoice. PO {po_control.po_number} balance is exhausted.")
        if po_control.remaining_balance < doc.billing_amount:
            frappe.throw(
                f"Cannot invoice. Insufficient PO balance. "
                f"Required: {doc.billing_amount:.2f}, Available: {po_control.remaining_balance:.2f}"
            )
