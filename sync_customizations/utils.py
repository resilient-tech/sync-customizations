import os

import frappe
from frappe.modules.export_file import strip_default_fields
from frappe.utils import get_bench_path

from sync_customizations.constants import EXPORT_DIR_NAME


def write_document_file(doc):
    doc_export = doc.as_dict(no_nulls=True)
    for key in ("idx", "__unsaved"):
        doc_export.pop(key, None)

    doc.run_method("before_export", doc_export)
    doc_export = strip_default_fields(doc, doc_export)

    with open(get_file_path(doc), "w+") as txtfile:
        txtfile.write(frappe.as_json(doc_export))


def get_filters(doctype):
    return {"is_system_generated": 0} if doctype == "Custom Field" else {}


def get_doctype_field(doctype):
    return "dt" if doctype == "Custom Field" else "doc_type"


def delete_document_file(doc):
    try:
        os.remove(get_file_path(doc))
    except OSError:
        pass


def get_export_dir_path():
    if frappe.conf.customizations_dir:
        return os.path.join(get_bench_path(), frappe.conf.customizations_dir)

    return frappe.get_site_path(EXPORT_DIR_NAME)

def get_folder(doctype):
    folder_path = os.path.join(get_export_dir_path(), frappe.scrub(doctype))
    frappe.create_folder(folder_path)
    return folder_path


def get_file_path(doc):
    return os.path.join(get_folder(doc.doctype), get_file_name(doc.name))


def get_file_name(docname):
    return f"{docname}.json"
