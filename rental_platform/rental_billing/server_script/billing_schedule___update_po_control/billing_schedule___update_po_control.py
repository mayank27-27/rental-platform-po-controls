if doc.status != "Invoiced":
    pass
else:
    po_controls = frappe.get_all(
        "PO Control",
        filters={"rental_contract": doc.rental_contract, "status": "Active"},
        fields=["name", "po_total_value", "amount_utilised",
                "remaining_balance", "alert_sent_80", "alert_sent_90"]
    )
    if not po_controls:
        pass
    else:
        po_control = frappe.get_doc("PO Control", po_controls[0]["name"])
        new_utilised = po_control.amount_utilised + doc.billing_amount
        new_balance = po_control.po_total_value - new_utilised
        new_percent = (new_utilised / po_control.po_total_value) * 100
        po_control.amount_utilised = new_utilised
        po_control.remaining_balance = new_balance
        po_control.utilisation = new_percent
        if new_balance <= 0:
            po_control.status = "Exhausted"
        if new_percent >= 90 and not po_control.alert_sent_90:
            frappe.msgprint(
                f"Alert: PO {po_control.po_number} has reached {new_percent:.1f}% utilisation. Remaining balance: {new_balance:.2f}",
                indicator="red", alert=True
            )
            po_control.alert_sent_90 = 1
        elif new_percent >= 80 and not po_control.alert_sent_80:
            frappe.msgprint(
                f"Warning: PO {po_control.po_number} has reached {new_percent:.1f}% utilisation. Remaining balance: {new_balance:.2f}",
                indicator="orange", alert=True
            )
            po_control.alert_sent_80 = 1
        po_control.save(ignore_permissions=True)
