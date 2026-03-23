expired_pos = frappe.get_all(
    "PO Control",
    filters={"status": "Active", "po_expiry_date": ["<", frappe.utils.nowdate()]},
    fields=["name", "po_number", "rental_contract"]
)
for po in expired_pos:
    frappe.db.set_value("PO Control", po["name"], "status", "Expired")
    pending_schedules = frappe.get_all(
        "Billing Schedule",
        filters={"rental_contract": po["rental_contract"], "status": "Pending"},
        fields=["name"]
    )
    for schedule in pending_schedules:
        frappe.db.set_value("Billing Schedule", schedule["name"], "status", "Cancelled")
    frappe.msgprint(
        f"PO {po['po_number']} has expired. {len(pending_schedules)} pending billing schedule(s) cancelled.",
        indicator="red", alert=True
    )
