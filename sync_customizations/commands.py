import click

import frappe
from frappe.commands import get_site, pass_context


@click.command("sc-export")
@pass_context
def export_customizations(context):
    """Export supported customizations to JSON files"""

    from sync_customizations.api import export_customizations

    site = get_site(context)
    frappe.init(site=site)
    frappe.connect()

    export_customizations()
    print("Customizations exported successfully!")


commands = [export_customizations]
