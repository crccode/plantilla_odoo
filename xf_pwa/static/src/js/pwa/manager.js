odoo.define("xf_pwa.PWAManager", function (require) {
    "use strict";

    let UserMenu = require("web.UserMenu");

    let deferredInstallPrompt = null;
    UserMenu.include({
        start: function () {
            window.addEventListener("beforeinstallprompt", this.saveBeforeInstallPromptEvent.bind(this));
            return this._super.apply(this, arguments);
        },
        saveBeforeInstallPromptEvent: function (event) {
            deferredInstallPrompt = event;
            this.$el.find('a[data-menu="install_pwa"]').removeClass('o_hidden');
        },
        _onMenuInstall_pwa: function () {
            deferredInstallPrompt.prompt();
            // Hide the install button, it can't be called twice.
            this.el.setAttribute("hidden", true);
            // Log user response to prompt.
            deferredInstallPrompt.userChoice.then(function (choice) {
                if (choice.outcome === "accepted") {
                    console.log("User accepted the A2HS prompt", choice);
                } else {
                    console.log("User dismissed the A2HS prompt", choice);
                }
                deferredInstallPrompt = null;
            });
        },
    });
});
