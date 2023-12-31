var __reflect = (this && this.__reflect) || function (p, c, t) {
    p.__class__ = c, t ? t.push(c) : t = [c], p.__types__ = p.__types__ ? t.concat(p.__types__) : t;
};
var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var Tpm;
(function (Tpm) {
    var DeviceUtils = (function (_super) {
        __extends(DeviceUtils, _super);
        function DeviceUtils() {
            return _super !== null && _super.apply(this, arguments) || this;
        }
        Object.defineProperty(DeviceUtils.prototype, "IsWeb", {
            get: function () {
                return (egret.Capabilities.runtimeType == egret.RuntimeType.WEB);
            },
            enumerable: true,
            configurable: true
        });
        Object.defineProperty(DeviceUtils.prototype, "IsNative", {
            get: function () {
                return (egret.Capabilities.runtimeType == egret.RuntimeType.NATIVE);
            },
            enumerable: true,
            configurable: true
        });
        Object.defineProperty(DeviceUtils.prototype, "IsIos", {
            get: function () {
                return (egret.Capabilities.os == "iOS");
            },
            enumerable: true,
            configurable: true
        });
        Object.defineProperty(DeviceUtils.prototype, "IsAndroid", {
            get: function () {
                return (egret.Capabilities.os == "Android");
            },
            enumerable: true,
            configurable: true
        });
        return DeviceUtils;
    }(Tpm.SingleClass));
    Tpm.DeviceUtils = DeviceUtils;
    __reflect(DeviceUtils.prototype, "Tpm.DeviceUtils");
})(Tpm || (Tpm = {}));
//# sourceMappingURL=DeviceUtils.js.map