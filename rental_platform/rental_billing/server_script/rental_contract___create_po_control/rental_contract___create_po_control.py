if not doc.po_required or not doc.po_number:
    pass
else:
    existing = frappe.get_all(
        "PO Control",
        filters={"po_number": doc.po_number, "rental_contract": doc.name},
        fields=["name"]
    )
    if not existing:
        po_control = frappe.new_doc("PO Control")
        po_control.po_number = doc.po_number
        po_control.customer = doc.customer
        po_control.rental_contract = doc.name
        po_control.po_total_value = doc.po_total_value
        po_control.po_expiry_date = doc.contract_end_date
        po_control.amount_utilised = 0
        po_control.remaining_balance = doc.po_total_value
        po_control.utilisation = 0
        po_control.status = "Active"
        po_control.alert_sent_80 = 0
        po_control.alert_sent_90 = 0
        po_control.insert(ignore_permissions=True)
