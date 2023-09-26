from sync_customizations.constants import DOCTYPES_TO_SYNC

app_name = "sync_customizations"
app_title = "Sync Customizations"
app_publisher = "Resilient Tech"
app_description = (
    "Automatically sync Custom Fields and Property Setters in Frappe sites"
)
app_email = "admin@resilient.tech"
app_license = "mit"

before_migrate = "sync_customizations.api.import_customizations"

doc_events = {
    DOCTYPES_TO_SYNC: {
        "on_update": "sync_customizations.api.export_doc",
        "on_trash": "sync_customizations.api.delete_doc",
    },
    "Customize Form": {
        "save_customization": "sync_customizations.api.on_save_customization",
    },
}
