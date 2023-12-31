module Tpm {
    export class ClientSocket {
        public name:string = "";                 //socket名字，用于判断push和game

        private socket: egret.WebSocket;          //socket
        private callBackList = {};               //回调列表
        private objList = {};                    //执行对象列表

        private reconnecting: boolean = false;    //是否断线重连中，重连中时不派发连接错误事件
        private reconInvalTime: number = 3000;    //断线重连时间间隔
        private curReconnectCount: number = 0;    //当前断线重连次数
        private reconnenctLimit: number = 5;      //断线重连限制次数
        private bAllowReconnnect: boolean = false;//是否允许断线重连

        public protoBuffer: string = "";          //断线时，协议缓存
        public dataBuffer = null;                //断线时，数据缓存

        private url: string = "";                 //IP地址

        private headSize: number = 12              //头大小

        private getMessage: number = 0; //返回心跳次数
        private timer: egret.Timer = new egret.Timer(5000, 0);
        private timeId: number;

        /**
         * 注册通讯回调
         * @param proto 协议
         * @param callBack 回调函数
         * @param thisObject 回调函数绑定对象
         */
        public register(proto: string, callBack: Function, thisObject) {
            this.callBackList[proto] = callBack;
            this.objList[proto] = thisObject;
        }

        /**
         * 取消注册
         * @param proto 协议
         */
        public unRegister(proto: string) {
            delete this.callBackList[proto];
            delete this.objList[proto];
        }

        /**
         * 开始连接socket
         * @url IP地址
         * @bAllowReconnnect 是否允许断线重连
         */
        public startConnect(url: string, bAllowReconnnect: boolean = false): void {
            console.log("开始连接" + ":" + url);
            App.LoadingLock.addLock("网络连接中...");
            this.url = url;
            this.bAllowReconnnect = bAllowReconnnect;
            this.createSocket();
            this.socket.connectByUrl(url);
            this.getMessage = 0;
            //连接超时处理
            this.timeId = egret.setTimeout(this.netError, this, 4500);
        }

        /**
         * 连接超时
         */
        private netError() {
            if (!this.isConnected()) {
                App.EventManager.sendEvent(EventConst.SocketClose, this);
            }
        }

        //创建socket; egret引擎bug，不重新创建socket就不派发事件。
        private createSocket() {
            if (this.socket) {
                this.socket.removeEventListener(egret.Event.CONNECT, this.onConnect, this);
                this.socket.removeEventListener(egret.Event.CLOSE, this.onClose, this);
                this.socket.removeEventListener(egret.IOErrorEvent.IO_ERROR, this.onError, this);
                this.socket.removeEventListener(egret.ProgressEvent.SOCKET_DATA, this.onRecieve, this);
                this.socket.connected && this.socket.close();
            }

            this.socket = new egret.WebSocket();
            this.socket.type = egret.WebSocket.TYPE_BINARY;
            this.socket.addEventListener(egret.Event.CONNECT, this.onConnect, this);
            this.socket.addEventListener(egret.Event.CLOSE, this.onClose, this);
            this.socket.addEventListener(egret.IOErrorEvent.IO_ERROR, this.onError, this);
            this.socket.addEventListener(egret.ProgressEvent.SOCKET_DATA, this.onRecieve, this);
        }

        //连接成功
        private onConnect(e: egret.Event): void {
            egret.log(" connect success");
            App.LoadingLock.minusLock();
            this.resetReconnenct();
            App.EventManager.sendEvent(EventConst.SocketConnect, this);
            this.sendHeart();
        }

        //连接关闭
        private onClose(e: egret.Event): void {
            egret.log("socket close");
            App.LoadingLock.minusLock();
            //socket断开，派发事件，重启游戏
            App.EventManager.sendEvent(EventConst.SocketClose, this);
            this.timer.stop();
            // //如果无重连动作，派发关闭事件,并重置重连
            // if(this.bAllowReconnnect == false || (this.bAllowReconnnect && (this.curReconnectCount > this.reconnenctLimit))){
            //     this.resetReconnenct();
            //     App.EventManager.sendEvent(EventConst.SocketClose, this);
            // }
        }

        //连接错误
        private onError(e: egret.IOErrorEvent): void {
            egret.log("socket error");
            this.timer.stop();
            if (this.tryReconnect() == false) {
                App.EventManager.sendEvent(EventConst.SocketIOError, this);
            }
        }

        /**
         * 尝试断线重连
         * @return 是否进行重连
         */
        private tryReconnect() {
            //不允许断线重连
            if (this.bAllowReconnnect == false) {
                return false;
            }
            //断线重连
            this.curReconnectCount++;
            if (this.curReconnectCount <= this.reconnenctLimit) {
                //如果第一次重连，则派发事件
                if (this.curReconnectCount == 1) {
                    App.EventManager.sendEvent(EventConst.StartReconnect, this);
                }
                //开始断线重连
                egret.setTimeout(this.startConnect, this, this.reconInvalTime, this.url, true);
                return true;
            }
            return false;
        }

        //主动关闭Socket，不派发事件
        public close(): void {
            this.timer.stop();
            egret.clearTimeout(this.timeId);
            if (this.socket) {
                this.socket.removeEventListener(egret.Event.CONNECT, this.onConnect, this);
                this.socket.removeEventListener(egret.Event.CLOSE, this.onClose, this);
                this.socket.removeEventListener(egret.IOErrorEvent.IO_ERROR, this.onError, this);
                this.socket.removeEventListener(egret.ProgressEvent.SOCKET_DATA, this.onRecieve, this);
                this.socket.connected && this.socket.close();
            }
            this.resetReconnenct();
            this.dataBuffer = null;
            this.protoBuffer = null;
        }

        //重置重连
        private resetReconnenct() {
            this.reconnecting = false;
            this.curReconnectCount = 0;
        }

        /**是否已连接*/
        public isConnected() {
            if (this.socket && this.socket.connected) {
                return true;
            }
            return false;
        }

        /**
         * 发送数据
         * @param data 待发送json数据
         * @param d1 协议号1
         * @param d2 协议号2
         */
        public send(proto: string, data: any = {}) {
            if (this.socket && this.socket.connected) {

                var sendDataByte: egret.ByteArray = new egret.ByteArray();
                var sendJson = JSON.stringify(data)
                sendDataByte.writeUTFBytes(sendJson)
                var size: number = this.headSize + sendDataByte.length;
                var protoList = proto.split("_");
                var head: egret.ByteArray = this.getHead(size, protoList[0]);
                head.writeBytes(sendDataByte);
                this.socket.writeBytes(head);
                this.socket.flush();
                console.log("send:", proto, JSON.stringify(data));

            } else {
                egret.log("socket is not connected");
                this.dataBuffer = data;
                this.protoBuffer = proto;
                App.EventManager.sendEvent(EventConst.SocketNotConnect, this);
                App.EventManager.sendEvent(EventConst.SocketClose, this);
            }
        }

        //接收数据
        private onRecieve(e: egret.ProgressEvent): void {
            // console.log("--------------------------------------")
            this.getMessage = 0;
            var b: egret.ByteArray = new egret.ByteArray();
            b.endian = egret.Endian.LITTLE_ENDIAN;
            this.socket.readBytes(b);
            this.process(b);
        }

        /**
         * 解析数据
         * @param b 待解析数据
         */
        public process(b: egret.ByteArray): void {
            var size = b.readInt();
            if (size != b.length) {
                console.error("data error!!")
                return
            }
            var id1 = b.readInt();
            var reserve2 = b.readInt();
            var str = b.readUTFBytes(b.length - this.headSize);
            var data;
            if ("" != str) {
                data = JSON.parse(str);
            }
            var proto: string = id1 + "";
            var callBack: Function = this.callBackList[proto];
            var thisObject = this.objList[proto];
            // if (proto != "10101") {
            console.log("rev:", proto, data);
            // }
            if (callBack && thisObject) {
                callBack.call(thisObject, data);

            } else {
                console.log("no receive callback:", proto);
            }
        }

        /**
         * 消息头部
         * @param size 数据长度
         * @param id1 
         * @param id2
         */
        private getHead(size, id1): egret.ByteArray {
            var a: egret.ByteArray = new egret.ByteArray();
            a.endian = egret.Endian.LITTLE_ENDIAN;
            a.writeInt(size);
            a.writeInt(id1);
            a.writeInt(0);
            return a;
        }

        /**
         * 发送心跳
         */
        private sendHeart() {
            // this.timer.start();
            // this.timer.addEventListener(egret.TimerEvent.TIMER, this.timerLisener, this);
        }

        private timerLisener() {

            if (this.getMessage == 0) {
                this.send("", "");
                this.getMessage++
            } else {
                this.socket.close();
            }
        }
    }
}

