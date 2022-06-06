# -*- coding: utf-8 -*-

{
    "name": "Web Camera QRCode Widget",
    "author": "RStudio",
    "category": "Hidden",
    "summary": "Odoo Community Edition QR code and barcode Camera widgit.",
    "version": "14.0.0.1",
    "description": """ 
Odoo Community Edition QR code and barcode Camera widgit.
======================================================
Please read the document carefully.
""",
    "depends": ["web", "barcodes",],
    "data": ["views/code_template.xml",],
    "qweb": ["static/src/xml/*.xml",],
    "images": ["images/main_screenshot.png"],
    "installable": True,
    "auto_install": False,
    "license": "OPL-1",
    "price": 25,
    "currency": "EUR",
}
