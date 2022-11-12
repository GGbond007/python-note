# coding=utf-8

from share import messageids
from game.mahjong.constants.gamedefine import GameStatus
from game.mahjong.controls.notifybridge import notify_all_desk_player, notify_desk_game_over
from base_system_act import BaseSystemAct
from share.espoirlog import logger
from config.globalconfig import GlobalConfig

class GameOver(BaseSystemAct):
    """
    游戏结束
    """
    def __init__(self, game_data):
        super(GameOver, self).__init__(game_data=game_data)

    def execute(self):
        """
        游戏结束
        :return:
        """
        logger.debug(u"游戏结束: %s", str([]))
        self.game_data.game_status = GameStatus.OVER

        # 重置状态机
        self.game_data.state_machine.reset_data()
        #

        # 通知玩家游戏结束
        data = {"player_info": {}}

        for x in xrange(self.game_data.max_player_num):
            data["player_info"][x] = {}
            data["player_info"][x]["hand_card"] = self.game_data.players[x].hand_card.hand_card_for_settle_show

        notify_all_desk_player(self.desk_id, messageids.PUSH_GAME_OVER, data=data)
        notify_desk_game_over(self.desk_id)

        GlobalConfig().reset_test_data()
