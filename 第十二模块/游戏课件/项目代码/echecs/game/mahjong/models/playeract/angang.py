# coding=utf-8

__author__ = 'jamon'

from share.espoirlog import logger
from share.messageids import *
from base_player_act import BasePlayerAct
from game.mahjong.constants.gamedefine import Act
from game.mahjong.models.actrecord import ActRecord
from game.mahjong.models.card.card import Card
from game.mahjong.models.timermanager import timer_manager_ins


class AnGang(BasePlayerAct):
    def __init__(self, game_data):
        super(AnGang, self).__init__(game_data=game_data)
        self.step_handlers = {
            "param_check": self.param_check,            # 参数验证
            "clear_other_act": self.clear_other_act,    # 清除该玩家其他动作
            "set_data": self.set_data,                  # 设置相应数据
            "record": self.record,                      # 记录玩家动作
            "notify_other_player": self.notify_other_player,  # 记录玩家动作
            "clear_lou_hu": self.clear_lou_hu,          # 清除漏胡数据
            "draw_gang_card": self.draw_gang_card       # 杠后摸牌
        }

        self.seat_id = -1  # 执行出牌的玩家位置
        self.used_card = -1  # 玩家选择的执行杠牌的牌值

    def execute(self, act_params={}):
        """
        执行暗杠
        :param act_params:
        :return:
        """
        logger.debug(u"暗杠: %s", str(act_params))
        for step in self.game_config.player_act_step.get(Act.AN_GANG):
            for name, cfg in step.items():
                ret = self.step_handlers.get(name)(act_params=act_params, config_params=cfg)
                if not ret:
                    logger.error("an_gang step:%s", step)
                    return
        return 1

    def param_check(self, **kwargs):      # 参数验证
        act_params = kwargs.get("act_params")
        if 1 != len(act_params):
            # 同时只允许有一个玩家发生暗杠操作
            logger.debug(u"act_an_gang_error:%s", str(act_params))
            return

        seat_id = act_params.keys()[0]
        params = act_params[seat_id]
        # TODO 此处需要接受参数 用户选择暗杠牌值
        used_card = params.get("used_card")[0]
        # card_val = self.game_data.last_chu_card_val

        if not used_card:
            logger.error("an_gang params error: %s", str([seat_id, params]))
            return

        hand_card = self.players[seat_id].hand_card
        if 4 != hand_card.hand_card_info[Card.cal_card_type(used_card)][Card.cal_card_digit(used_card)]:
            logger.error("an_gang params error: %s", str([seat_id, params]))
            return

        self.seat_id = seat_id
        self.used_card = used_card
        return 1

    def clear_other_act(self, **kwargs):  # 清除该玩家其他动作
        timer_manager_ins.kill_timer(self.desk_id, self.seat_id, is_force=True)
        return 1

    def set_data(self, **kwargs):         # 设置相应数据
        card_val = self.used_card
        self.players[self.seat_id].hand_card.del_hand_card_by_val_list([card_val, card_val, card_val, card_val])
        return 1

    def record(self, **kwargs):           # 记录玩家动作
        card_val = self.used_card
        cards = [card_val]
        act_record = ActRecord(self.seat_id, Act.AN_GANG, cards)
        self.game_data.act_record_list.append(act_record)
        self.players[self.seat_id].hand_card.record_an_gang_card(card_val)
        return 1

    def notify_other_player(self, **kwargs):  # 记录玩家动作
        act_info = {"seat_id": self.seat_id, "act_type": Act.AN_GANG, "card_list": [self.used_card]}
        self.notify_other_player_act_an_gang(self.seat_id,
                                              act_info=act_info,
                                              max_player_num=self.game_data.max_player_num)
        return 1

    def clear_lou_hu(self, **kwargs):     # 清除漏胡数据
        return 1

    def draw_gang_card(self, **kwargs):   # 杠后摸牌
        self.draw_card(self.seat_id, is_last=True)
        return 1
