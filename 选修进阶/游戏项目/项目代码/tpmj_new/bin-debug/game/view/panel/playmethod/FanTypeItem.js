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
    var FanTypeItem = (function (_super) {
        __extends(FanTypeItem, _super);
        function FanTypeItem() {
            var _this = _super.call(this) || this;
            _this.skinName = "TpmSkin.FanTypeItemSkin";
            return _this;
        }
        FanTypeItem.prototype.setName = function (fanName) {
            this.nameLabel.text = fanName;
        };
        FanTypeItem.prototype.setDescripe = function (des) {
            this.descripeLabel.text = des;
            //描述超过两行时，牌容器下移和Item高度增加
            if (this.descripeLabel.numLines >= 2) {
                var offerY = this.descripeLabel.size * (this.descripeLabel.numLines - 1);
                this.cardGroup.y += offerY;
                this.height += offerY;
            }
        };
        FanTypeItem.prototype.setCardList = function (cardList) {
            var len = cardList.length;
            var card;
            var cardFactory = Tpm.CardFactory.getInstance();
            for (var i = 0; i < len; i++) {
                card = cardFactory.getOutCard(cardList[i], Tpm.UserPosition.Down);
                card.scaleX = 0.9;
                card.scaleY = 0.9;
                card.x = 0.8 * 58 * i;
                card.y = 0;
                this.cardGroup.addChild(card);
            }
            //牌数组为0时，Item高度减少
            if (len == 0) {
                this.height = this.height - this.cardGroup.height;
            }
        };
        return FanTypeItem;
    }(eui.Component));
    Tpm.FanTypeItem = FanTypeItem;
    __reflect(FanTypeItem.prototype, "Tpm.FanTypeItem");
})(Tpm || (Tpm = {}));
//# sourceMappingURL=FanTypeItem.js.map