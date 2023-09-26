import os

import frappe
from frappe.modules.import_file import import_file_by_path

from sync_customizations.utils import (
    write_document_file,
    delete_document_file,
    get_folder,
    get_filters,
    get_doctype_field,
    get_file_name,
)
from sync_customizations.constants import DOCTYPES_TO_SYNC


IMPORT_FLAG = "sc_importing_customizations"


def export_doc(doc, method=None):
    if (
        doc.doctype == "Custom Field" and doc.is_system_generated
    ) or frappe.local.flags.get(IMPORT_FLAG, False):
        return

    frappe.db.after_commit.add(lambda: write_document_file(doc))


def delete_doc(doc, method=None):
    frappe.db.after_commit.add(lambda: delete_document_file(doc))


def on_save_customization(doc, method=None):
    frappe.db.after_commit.add(
        lambda: export_customizations(filter_by_doctype=doc.doc_type)
    )


def export_customizations(filter_by_doctype=None):
    for doctype in DOCTYPES_TO_SYNC:
        folder = get_folder(doctype)
        filters = get_filters(doctype)
        files_to_keep = set(
            get_file_name(doc.name) for doc in frappe.get_all(doctype, filters=filters)
        )
        files_to_delete = [
            fname for fname in os.listdir(folder) if fname not in files_to_keep
        ]

        for file_name in files_to_delete:
            os.remove(os.path.join(folder, file_name))

        if filter_by_doctype:
            doctype_field = get_doctype_field(doctype)
            filters[doctype_field] = filter_by_doctype

        for doc in frappe.get_all(doctype, filters=filters, fields="*"):
            doc = frappe.get_doc({"doctype": doctype, **doc})
            write_document_file(doc)


def import_customizations():
    flags = frappe.local.flags
    try:
        flags[IMPORT_FLAG] = True
        _import_customizations()

    finally:
        flags.pop(IMPORT_FLAG, None)


def _import_customizations():
    for doctype in DOCTYPES_TO_SYNC:
        docnames = set()

        folder = get_folder(doctype)

        for doc_filename in os.listdir(folder):
            if not doc_filename.endswith(".json"):
                continue

            import_file_by_path(os.path.join(folder, doc_filename))
            docnames.add(os.path.splitext(doc_filename)[0])

        frappe.db.commit()
        print(f"{doctype}s imported successfully...")

        docs_to_delete = frappe.get_all(
            doctype,
            filters={"name": ("not in", docnames), **get_filters(doctype)},
            pluck="name",
        )
        if docs_to_delete:
            print(f"Detected stale {doctype}s:\n{', '.join(docs_to_delete)}")
            print("\nDeleting...", end=" ")

            frappe.db.delete(doctype, {"name": ("in", docs_to_delete)})
            frappe.db.commit()
            print("Done!\n")

    frappe.clear_cache()
