module Tpm {
    export class SingleClass {

        /**
         * 获取一个单例
         */
        public static getInstance(): any {
            var Class: any = this;
            if (Class.instance == null) {
                Class.instance = new Class();
            }
            return Class.instance;
        }
    }
}
