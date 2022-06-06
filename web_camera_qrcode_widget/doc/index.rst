==============================================
Web Camera QRCode Widget
==============================================

Features:
----------------------------------------------
* Use web camera recognition.
* SupportSupport QR code and barcode.
* Automatically set focus, support barcode scanner.
* Use `zxing-js <https://github.com/zxing-js/library/>`_ .

----

Supported Formats:
----------------------------------------------
+------------------------+------------------------+----------------------+
| 1D product             | 1D industrial          |         2D           |
+========================+========================+======================+
| EAN-8                  | Code 39                | QR Code              |
+------------------------+------------------------+----------------------+
| EAN-13                 | Code 128               | Data Matrix          |
+------------------------+------------------------+----------------------+
|                        | ITF                    | PDF 417              |
+------------------------+------------------------+----------------------+
|                        | RSS-14                 |                      |
+------------------------+------------------------+----------------------+


Note:
----------------------------------------------
* When using the WebRTC API, the browser requires HTTPS. Any page that uses this library should be served via HTTPS.  
* Chrome is recommended.

----



How to install:
----------------------------------------------
1) Click on the menu "Apps".
2) Select "Extra" in the filter popup menu.
3) Enter "Web QRCode Widget" in the search input box.
4) Please install the module "Web QRCode Widget" in the search results.

----

How to use in form view:
----------------------------------------------
* You can directly modify the form view in odoo debug mode.
* You can inherit the view and use position="attributes" to add widget="qr_code" to the field.

**Example1:Modify the form view in debug mode**

::

    <field name="arch" type="xml">
        <form string="View name">
            <field name="barcode" widget="qr_code" options="{'need_confirm': true, 'autoplay':true}" />
        </form>
    </field>

**Example2:Inherit the view to add attributes to the field**

::

    <xpath expr="//field[@name='barcode']" position="attributes">
        <attribute name="widget">qr_code</attribute>
        <attribute name="options">{'need_confirm': true, 'autoplay':true}</attribute>
    </xpath>

----

Options description:
----------------------------------------------

-need_confirm           Do you need to confirm after scanning,
                        Default true
-autoplay               Automatically start the camera,
                        Default true



**need_confirm:**

* default need_confirm= true .
* need_confirm:true,The scan result is displayed in the dialog box. Click the OK button to return.
* need_confirm:false,The scan result is not displayed in the dialog box, and the dialog box is closed directly when the scan is successful.

**select:**

* default select= true .
* select:true,Can select multiple cameras.
* select:false,Only cameras with device serial number 0 can be used.



Bugs and requirements:
----------------------------------------------

You can send an email to rain.wen@outlook.com to submit bugs and requirements to me.

如果你是汉语使用者，直接使用中文吧。我在武汉，愿世界安详，世道够艰难的。