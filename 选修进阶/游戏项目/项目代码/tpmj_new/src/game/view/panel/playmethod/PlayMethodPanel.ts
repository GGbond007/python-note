module Tpm {
	export class PlayMethodPanel extends BasePanel {
		private closeBtn: eui.Button;
		private playMethodtabBar: eui.TabBar;
		private contentGroup:eui.Group;
		private baseRuleScroller: eui.Scroller;
		private baseTypeScroller: eui.Scroller;
		private tsRuleScroller: eui.Scroller;
		private resultRuleScroller: eui.Scroller;
		private baseRuleText: eui.Label;    //基本规则富文本
		private tsRuleText: eui.Label;      //特殊规则富文本
		private resultRuleText: eui.Label;  //结算富文本
		private fanTypeIsInt: boolean;  //番型已初始化
		private textIsInt: boolean;  //文本已初始化
		private contentList:eui.Label[]=[];  //文本组件列表
		private styleList=[];  //文本格式列表


		public constructor() {
			super();
			this.skinName =TpmSkin.PlayMethodPanelSkin;
		}
		/**添加到场景中*/
		protected onEnable() {
			// this.playMethodtabBar.selectedIndex
			this.showTargetScroller(0,true);
			this.setContenTex();
			this.setFanType();
			this.playMethodtabBar.addEventListener(egret.TouchEvent.TOUCH_TAP, this.showPlayMethod, this);
			this.closeBtn.addEventListener(egret.TouchEvent.TOUCH_TAP, this.hide, this);
		}

		/**从场景中移除*/
		protected onRemove() {
			this.playMethodtabBar.removeEventListener(egret.TouchEvent.TOUCH_TAP, this.showPlayMethod, this);
			this.closeBtn.removeEventListener(egret.TouchEvent.TOUCH_TAP, this.hide, this);
		}
		/**销毁*/
		protected onDestory() {
			this.removeChildren();
		}
		private showPlayMethod(e: egret.TouchEvent) {
			this.showTargetScroller(this.playMethodtabBar.selectedIndex);
		}
		/**
  		* 格式化内容文本
   		*/
		private setContenTex() {
			if(this.textIsInt)return;
			//"fontFamily":"楷体"
			var tetleTextStyleJson = { "size": 27.2, "textColor": 0x370b00, "fontFamily": "SimHei","bold":"true"}
			var contentTextStyleJson = { "size": 26.2, "textColor": 0x370b00, "fontFamily": "SimHei" }
			this.contentList=[this.baseRuleText,this.tsRuleText,this.resultRuleText];
			this.styleList=[tetleTextStyleJson,contentTextStyleJson];
			this.setAllTextContent();
			this.textIsInt=true;
		}
		/**
		 * 添加分割线
		 */
		private addLine(x,y)
		{
			var line:eui.Image=new eui.Image();
			line.source=RES.getRes("tpm_line_png");
			line.x=x;
			line.y=y;
			line.width=this.baseRuleText.width;
			line.height=1;
			(this.baseRuleScroller.viewport as eui.Group).addChild(line);
		}
		private setAllTextContent() {
			var baseRuleConf = RES.getRes("tpm_baseRuleConf_json");
			var len = baseRuleConf.content.length;
			var clen = this.contentGroup.numChildren;
			for (var i = 0; i < len; i++) {
				this.setTextContent(this.contentList[i], baseRuleConf.content[i]);
			}
			this.addLine(40,90);
			this.addLine(40,310);
		}
		private setTextContent(target: eui.Label, src) {
			var len = src.length;
			var arr: egret.ITextElement[] = [];
			for (var i = 0; i < len; i++) {
				var textItem: egret.ITextElement = {} as egret.ITextElement;
				textItem.text = src[i].text;
				textItem.style = this.styleList[Number(src[i].style)];
				arr.push(textItem);
			}
			target.textFlow = arr;
		}

		/**
		 * 设置番型
		 */
		private setFanType() {
			if(this.fanTypeIsInt)return;
			var typeConf = RES.getRes("tpm_fanTypeConf_json");
			var len = typeConf.content.length;
			var viewport = (<eui.Group>this.baseTypeScroller.viewport);
			var titleWidth=this.baseTypeScroller.width;
			for (var i = len-1; i>0; i--) {
				var flen = typeConf.content[i].length;
				for (var j = 0; j < flen; j++) {
					var data = typeConf.content[i][j];
					if (j == 0) {
						var title: eui.Label = new eui.Label(data.fanNum);
						title.size = 27.2;
						title.width = titleWidth;
						title.textColor = 0x370b00;
						title.fontFamily = "SimHei";
						title.textAlign = "left";
						viewport.addChild(title);
						j = 1;
						data = typeConf.content[i][j];
					}
					var item: FanTypeItem = new FanTypeItem();
					// item.setName(data.name);
					item.setDescripe(data.name+"："+data.descripe);
					item.setCardList(data.cardList);
					viewport.addChild(item);
				}
			}
			this.fanTypeIsInt=true;
		}

		/**
		 * 显示选择的滑动组件
		 */
		private showTargetScroller(index: number=0,isreset:boolean=false) {
			this.playMethodtabBar.selectedIndex=index;
			var len = this.contentGroup.numChildren;
			for (var i = 0; i < len; i++) {
				var target=this.contentGroup.getChildAt(i) as eui.Scroller;
				if (i == index) target.visible = true;
				else target.visible = false;
				if (isreset)target.viewport.scrollV=0;
			}
		}
	}
}