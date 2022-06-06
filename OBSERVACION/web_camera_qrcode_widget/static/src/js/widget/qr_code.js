odoo.define('web.web_camera_qrcode_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var utils = require('web.utils');
    var config = require('web.config');
    var fieldRegistry = require('web.field_registry');
    var FieldChar = require('web.basic_fields').FieldChar;
    var Dialog = require('web.Dialog');
    var _t = core._t;
    var QWeb = core.qweb;
    var WEB_CAMERA_QRCODE_WIDGET_COOKIE = 'web_camera_qrcode_widget_default_camera';
    var audio = new Audio('/web_camera_qrcode_widget/static/audio/beep.mp3');

    function Q(el) {
        if (typeof el === "string") {
            var els = document.querySelectorAll(el);
            return typeof els === "undefined" ? undefined : els.length > 1 ? els : els[0];
        }
        return el;
    }

    var QRCode = FieldChar.extend({
        template: 'QRCode',
        className: 'o_field_qr_code',
        jsLibs: [
            '/web_camera_qrcode_widget/static/lib/ZXing/ZXing.js'
        ],
        init: function (parent) {
            var self = this;
            this._super.apply(this, arguments);
            this.need_confirm = self.convertBoolean(self.nodeOptions.need_confirm); //需要确认扫码结果，默认为true
            // this.allow_select = self.convertBoolean(self.nodeOptions.allow_select);
            this.autoplay = self.convertBoolean(self.nodeOptions.autoplay);
            this.scanResult = null;

            this.barcode_parser = parent.barcode_parser;
            core.bus.on('barcode_scanned', this, function (barcode) {
                this.use_scanner(barcode);
            });
        },

        convertBoolean: function (value) {
            switch (value) {
                case false:
                    return false;
                    break;
                case undefined:
                    return true;
                    break;
                case null:
                    return true;
                    break;
                case 0:
                    return false;
                    break;
                case -0:
                    return false;
                    break;
                case NaN:
                    return true;
                    break;
                case "":
                    return true;
                    break;
                default:
                    return true;
            }
        },
        isEnterprise: function () {
            // 判断是否企业版
            if (_.last(odoo.session_info.server_version_info) === 'e') {
                return true;
            } else {
                return false;
            }
        },
        //#region 浏览器
        //****************************
        // 浏览器
        //****************************

        checkBrowserType() {
            var self = this;
            // 判断是否手机设备
            if (!config.device.isMobile) {
                // 非手机设备
                this.browserType = _("PC browser");
            } else {
                // 手机设备
                this.browserType = _("Mobile browser");
            }

        },
        //#endregion

        //#region 使用扫描枪
        set_barcode_parser: function (barcode_parser) {
            this.barcode_parser = barcode_parser;
        },
        use_scanner: function (code) {
            var self = this;

            if (!code) {
                return;
            }

            if (self.need_confirm) {
                self.scan_result_value.textContent = code;
                self.scanResult = code;
            } else {
                //不需要确认扫码结果
                this.$el.find('input').val(code);
                // self.updateResult();
            }

            core.bus.off('barcode_scanned', this, this.use_scanner);
        },
        //#endregion

        //#region 启动
        //****************************
        // 启动
        //****************************
        start_scan: function () {
            var self = this;
            if (self.isEnterprise()) {
                self.start_web_scan();
            } else {
                self.start_web_scan();
            }
        },
        start_web_scan: function () {
            // 启动浏览器扫码
            // 判断浏览器 的版本
            var self = this;
            if (!config.device.isMobile) {
                // 非手机设备启动PC浏览器扫码
                this.isApp = false;
                self.open_scan_dialog();
            } else {
                // 手机设备启动手机浏览器扫码
                self.start_mobile_web_sacn();
            }
        },
        start_mobile_web_sacn: function () {
            // 启动
            var self = this;
            //移动浏览器
            self.open_scan_dialog();
        },

        // #endregion

        //#region dialog
        //****************************
        // dialog
        //****************************
        open_scan_dialog: function () {
            var self = this;
            self.$el.find("button[class*='o_show_camera_button']").prop('disabled', true); //禁用 --变灰，且不能调用点击事件
            self.$el.find(".loading").removeClass("o_hidden");

            self.checkBrowserType();
            var dialog_title = this.browserType;
            // var dialog_title = this.browserType + ": " + _t("QR code and Bar code Scanning");
            this.dialog = new Dialog(self, {
                size: 'medium', //'extra-large', 'large', 'medium', 'small'
                dialogClass: 'o_act_window',
                title: dialog_title,
                buttons: self.getButtons(),
                renderHeader: false,
                onForceClose: function () {
                    //使用键盘ESC按键时，关闭摄像头
                    self.closeDialog();
                },
                $content: QWeb.render('QRCode.camera', {
                    browser_type: this.browserType,
                    isApp: this.isApp,
                    // active: this.activeCameraId,
                    // error: res.msg,
                })
            });
            this.dialog.opened().then(function (res) {
                self.initScanDialog();
            });
            self.dialog.open();
        },
        initScanDialog: function () {
            var self = this;

            this.modal_body = this.dialog.$modal.find(".modal-body");
            this.scan_result_value = this.modal_body.find(".scan_result_value")[0];

            this.dialog.$modal.find("footer").css({
                "padding": "4px 16px"
            });


            this.footer_last_button = this.dialog.$modal.find("footer").find("button:last");

            self.footer_last_button.after("<span class='scan_info text-right font-weight-bold' style='flex:1;'></span>");
            this.scan_info = this.dialog.$modal.find("footer").find(".scan_info");

            // 启动浏览器摄像头
            this.initWebScanner();
        },
        initWebScanner: function () {
            var self = this;
            var header_button = this.dialog.$modal.find("header").find("button");
            header_button.click(function () {
                self.closeDialog();
            });

            var camera_widget_options_panel = this.dialog.$modal.find("#camera_widget_options");

            var options_button = this.modal_body.find(".show_or_hide_options_panel");
            var options_button_icon = options_button.find("i");
            var options_button_text = options_button.find("span");

            $(camera_widget_options_panel).on('show.bs.collapse', function () {
                options_button_icon.addClass("fa-angle-double-up").removeClass("fa-angle-double-down");
                options_button_text.html(_t("Hide"));
            })
            $(camera_widget_options_panel).on('hide.bs.collapse', function () {
                options_button_icon.addClass("fa-angle-double-down").removeClass("fa-angle-double-up");
                options_button_text.html(_t("Show"));
            })

            if (this.getCameraCookie() == "") {
                self.vertical = false;
                self.horizontal = false;
            } else {
                self.vertical = JSON.parse(this.getCameraCookie())["vertical"];
                self.horizontal = JSON.parse(this.getCameraCookie())["horizontal"];
            }


            this.flip_vertical_checkbox = self.modal_body.find("#flip_vertical");
            $(self.flip_vertical_checkbox).change(function () {
                self.vertical = self.flip_vertical_checkbox.prop("checked");
                self.set_flip();
                self.setDefaultCookie();
            });
            this.flip_horizontal_checkbox = self.modal_body.find("#flip_horizontal");
            $(self.flip_horizontal_checkbox).change(function () {
                self.horizontal = self.flip_horizontal_checkbox.prop("checked");
                self.set_flip();
                self.setDefaultCookie();
            });
            self.set_flip();

            this.scan_info.text(_t("The camera is being initialized. . .")).addClass("text-info").removeClass("text-danger").removeClass("text-success");

            self.initCodeReader();
        },
        set_flip: function () {
            //设置翻转
            var self = this;

            if (self.horizontal && self.vertical) {
                self.dialog.$modal.find("#scancode-video").attr("class", "").addClass("video-flip-both");
            } else if (self.horizontal) {
                self.dialog.$modal.find("#scancode-video").attr("class", "").addClass("video-flip-horizontal");
            } else if (self.vertical) {
                self.dialog.$modal.find("#scancode-video").attr("class", "").addClass("video-flip-vertically");
            } else {
                self.dialog.$modal.find("#scancode-video").attr("class", "").addClass("video-no-flip");
            }
        },
        getButtons: function () {
            var self = this;
            var buttons = [];
            if (this.need_confirm) {
                buttons = [{
                    text: _t("Confirm"),
                    classes: 'btn-info',
                    close: false,
                    click: function () {
                        if (self.scanResult === null) {
                            self.scan_info.removeClass("text-success").addClass(
                                "text-warning");
                            self.scan_info.text(_t(
                                "Scan has not been performed, please scan."));
                        } else {
                            self.scan_info.removeClass("text-warning").addClass(
                                "text-success");
                            self.updateResult();
                            self.closeDialog();
                        }
                    }
                }, {
                    text: _t("Cancel"),
                    classes: 'btn-dark',
                    close: true,
                    click: function () {
                        self.closeDialog();
                    }
                }];
            } else if (!this.nodeOptions.confirm) {
                buttons = [{
                    text: _t("Cancel"),
                    classes: 'btn-dark',
                    close: true,
                    click: function () {
                        self.closeDialog();
                    }
                }]
            }
            return buttons;
        },
        updateResult: function () {
            var self = this;
            this.$el.find('input').val(self.scanResult);
            this._setValue(); //设置值
        },
        closeDialog: function () {
            var self = this;
            if (self.codeReader) {
                self.stopCodeReader();
            }
            // self.$input.find(".loading").addClass("o_hidden");
            // self.$input.find("button[class*='o_show_camera_button']").prop('disabled', false); //启用
            self.$el.find(".loading").addClass("o_hidden");
            self.$el.find("button[class*='o_show_camera_button']").prop('disabled', false); //启用

            this.dialog.$modal.modal('hide');
        },
        //#endregion

        //#region ZXing
        //****************************
        //multi-format 1D/2D barcode image processing library
        //****************************

        initCodeReader: function () {
            this.camera_source = this.modal_body.find(".camera-select");
            this.start_button = this.modal_body.find(".scancode_start");
            this.stop_button = this.modal_body.find(".scancode_stop");
            this.show_options_button = this.modal_body.find(".show_or_hide_options_panel");
            this.scannerLaser = this.modal_body.find(".scanner-laser");

            var self = this;
            self.scannerLaser.addClass("o_hidden");
            this.codeReader = new ZXing.BrowserMultiFormatReader();

            self.codeReader.listVideoInputDevices()
                .then((videoInputDevices) => {
                    // 判断本地设备数量;
                    if (videoInputDevices.length >= 1) {
                        //设置按钮事件
                        self.start_button.click(function () {
                            self.startCodeReader();
                        });
                        self.stop_button.click(function () {
                            self.stopCodeReader();
                        });

                        // 本地设备数量大于等于1;
                        this.localDevices = videoInputDevices;
                        //判断COOKIE是否有数据
                        if (self.getCameraCookie() === undefined || self.getCameraCookie() === null || self.getCameraCookie() === "") {
                            // COOKIE无数据，设置COOKIE
                            if (videoInputDevices.length > 1) {
                                //如果摄像头数量大于1，默认为第二个摄像头
                                self.defaultCameraId = videoInputDevices[1].deviceId;
                                self.defaultCameraName = videoInputDevices[1].label;
                            } else {
                                self.defaultCameraId = videoInputDevices[0].deviceId;
                                self.defaultCameraName = videoInputDevices[0].label;
                            }
                            self.vertical = false;
                            self.horizontal = false;

                            self.setDefaultCookie();
                        } else {
                            // COOKIE有数据
                            // 判断COOKIE中的默认摄像头是否在本地设备列表中

                            self.flip_vertical_checkbox.prop("checked", self.vertical);
                            self.flip_horizontal_checkbox.prop("checked", self.horizontal);

                            if (!self.cookieDefaultIsExistInLocalDevices()) {
                                // COOKIE中的默认摄像头 不在本地设备列表中
                                // 重新设置 缓存中的默认摄像头
                                self.defaultCameraId = videoInputDevices[0].deviceId;
                                self.defaultCameraName = videoInputDevices[0].label;
                                self.setDefaultCookie();
                            } else {
                                // COOKIE中的默认摄像头 在本地设备列表中
                                // 设置默认摄像头为 cookie中的数据
                                self.defaultCameraId = JSON.parse(self.getCameraCookie())["defaultCamera"]["id"];
                            }
                            //设置下拉菜单
                            videoInputDevices.forEach((element) => {
                                var option;
                                if (element.deviceId === self.defaultCameraId) {
                                    option = new Option(element.label, element.deviceId, true, true);
                                } else {
                                    option = new Option(element.label, element.deviceId);
                                }
                                self.camera_source.append(option);
                            })
                            self.camera_source.change(function () {
                                self.defaultCameraId = $(this).children('option:selected').val();
                                self.defaultCameraName = $(this).children('option:selected').text();
                                self.setDefaultCookie();
                                self.toggleCodeReader();
                            });
                        }

                        this.scan_info.text(_t("The camera is initialized successfully!")).addClass("text-info").removeClass("text-danger").removeClass("text-success");
                        if (self.autoplay) {
                            self.start_button.prop('disabled', true); //禁用 --变灰，且不能调用事件
                            self.stop_button.prop('disabled', false); //启用

                            self.startCodeReader();
                        } else {
                            self.start_button.prop('disabled', false); //启用
                            self.stop_button.prop('disabled', true); //禁用 --变灰，且不能调用事件
                            self.scan_info.text(_("The camera has not started yet. Please click the start button.")).addClass("text-warning").removeClass("text-info").removeClass("text-success");
                        }
                    } else {
                        // 无本地设备数量;
                        self.scan_info.text(_t("Startup failed: no cameras were found.")).removeClass("text-info").addClass("text-danger").removeClass("text-success");
                        self.scannerLaser.addClass("o_hidden");
                        self.camera_source.prop('disabled', true); //禁用 --变灰，且不能调用事件
                        self.start_button.prop('disabled', true); //禁用 --变灰，且不能调用事件
                        self.stop_button.prop('disabled', true); //禁用 --变灰，且不能调用
                    }
                })
                .catch(function (err) {
                    if (err.TypeError === undefined) {
                        self.scan_info.text(_t("Startup failed: no cameras were found.")).removeClass("text-info").addClass("text-danger").removeClass("text-success");
                        self.camera_source.prop('disabled', true); //禁用 --变灰，且不能调用事件
                        self.start_button.prop('disabled', true); //禁用 --变灰，且不能调用事件
                        self.stop_button.prop('disabled', true); //禁用 --变灰，且不能调用事件

                        self.scannerLaser.addClass("o_hidden");
                    }
                    console.log(err);
                });
        },
        // this.scan_info.text(_t("Scanning...")).addClass("text-info").removeClass("text-danger").removeClass("text-success");
        startCodeReader: function () {
            var self = this;
            self.scan_info.text(_t("Start camera...")).addClass("text-info").removeClass("text-danger").removeClass("text-success");

            self.codeReader.decodeFromVideoDevice(self.defaultCameraId, 'scancode-video', (result, err) => {

                self.start_button.prop('disabled', true); //禁用 --变灰，且不能调用点击事件
                self.stop_button.prop('disabled', false); //启用
                self.camera_source.prop('disabled', false); //启用
                self.scannerLaser.removeClass("o_hidden");

                if (result) {
                    audio.play();
                    self.scan_result_value.textContent = result.text;
                    self.scanResult = result.text;

                    self.scan_info.text(_t("Scan the code successfully, Format:") + self.getZXingFormat(result.format)).addClass("text-success").removeClass("text-danger").removeClass("text-warning");


                    self.scannerLaser.fadeOut(0.5);
                    setTimeout(function () {
                        self.scannerLaser.fadeIn(0.5);
                    });

                    if (self.need_confirm) {
                        //需要确认扫码结果
                    } else {
                        //不需要确认扫码结果
                        self.updateResult();
                        self.closeDialog();
                    }
                }
                if (err && !(err instanceof ZXing.NotFoundException)) {
                    console.error(err);
                    self.scan_result_value.textContent = err;

                    self.scan_info.text(_t("Startup failed:" + err)).removeClass("text-info").addClass("text-danger").removeClass("text-success");
                    self.scannerLaser.addClass("o_hidden");
                }
            });
            self.scan_info.text(_t("Started successfully. Please scan the code...")).removeClass("text-info").removeClass("text-danger").removeClass("text-warning").addClass("text-success");
        },
        stopCodeReader: function () {
            var self = this;
            self.codeReader.reset();
            self.scan_result_value.textContent = '';
            self.scannerLaser.hide();

            self.start_button.prop('disabled', false); //启用 
            self.scan_info.text(_("The camera stops working.")).addClass("text-warning").removeClass("text-info").removeClass("text-success");
        },
        toggleCodeReader: function () {
            var self = this;
            self.stopCodeReader();
            self.startCodeReader();
        },

        getZXingFormat: function (value) {
            switch (value) {
                case 0:
                    return "AZTEC";
                    break;
                case 1:
                    return "CODABAR";
                    break;
                case 2:
                    return "CODE_39";
                    break;
                case 3:
                    return "CODE_93";
                    break;
                case 4:
                    return "CODE_128";
                    break;
                case 5:
                    return "DATA_MATRIX";
                    break;
                case 6:
                    return "PDF_417";
                    break;
                case 7:
                    return "EAN_13";
                    break;
                case 8:
                    return "ITF";
                    break;
                case 9:
                    return "MAXICODE";
                    break;
                case 10:
                    return "PDF_417";
                    break;
                case 11:
                    return "QR_CODE";
                    break;
                case 12:
                    return "RSS_14";
                    break;
                case 13:
                    return "RSS_EXPANDED";
                    break;
                case 14:
                    return "UPC_A";
                    break;
                case 15:
                    return "UPC_E";
                    break;
                case 16:
                    return "UPC_EAN_EXTENSION";
                    break;
                default:
                    return _("unknown");
            }
        },
        getCameraCookie: function () {
            // 获取cookie中的默认摄像头
            return utils.get_cookie(WEB_CAMERA_QRCODE_WIDGET_COOKIE);
        },
        setDefaultCookie: function () {
            // 设置cookie中的默认摄像头
            this.devices = {
                "defaultCamera": {
                    "id": this.defaultCameraId,
                    "name": this.defaultCameraName,
                },
                "list": this.localDevices,
                "vertical": JSON.parse(this.vertical),
                "horizontal": JSON.parse(this.horizontal),
            }
            utils.set_cookie(WEB_CAMERA_QRCODE_WIDGET_COOKIE, JSON.stringify(this.devices), 60 * 60 * 24 * 30); // 30 day cookie
        },
        cookieDefaultIsExistInLocalDevices: function () {
            //判断缓存的defaultCameraId是否存在当前设备本地连接的摄像头列表中
            var self = this;
            var list = JSON.parse(self.getCameraCookie())["list"];
            return JSON.stringify(list).indexOf(JSON.parse(self.getCameraCookie())["defaultCamera"]["id"]) !== -1;
        },
        //#endregion

        //#region widget
        //****************************
        // widget
        //****************************
        _renderEdit: function () {
            var $input = this.$el.find('input');
            setTimeout(function () {
                //设置焦点
                $input.focus();
            }, 1000)
            // this.$loading = this.$el.find('.loading');

            if (this.value === null || this.value === "" || this.value === false) {
                return this._super($input.val(""));
            } else {
                return this._super($input.val(this.value));
            }
        },
        _prepareInput: function ($input) {
            var self = this;

            var $button = this.$el.find("button.o_show_camera_button");
            $button.click(function () {
                self.start_scan();
            })

            return $.when($input, this._super.apply(this, arguments));
        },
        _setValue: function () {
            var $input = this.$el.find('input');
            return this._super($input.val());
        },
        //#endregion
    });

    fieldRegistry.add('qr_code', QRCode);
    return {
        QRCode: QRCode
    };
});