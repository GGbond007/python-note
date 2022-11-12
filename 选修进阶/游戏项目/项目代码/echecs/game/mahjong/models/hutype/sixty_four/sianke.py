# coding=utf-8
import time

from game.mahjong.models.hutype.basetype import BaseType
from game.mahjong.constants.carddefine import CardType, CARD_SIZE
from game.mahjong.models.card.hand_card import HandCard
from game.mahjong.models.utils.cardanalyse import CardAnalyse


class SiAnKe(BaseType):
    """
    3)	四暗刻: 胡牌时，牌里有4个暗刻（暗杠）。
    不记番： 门前清、碰碰和、三暗刻、双暗刻、不求人。
    """

    def __init__(self):
        super(SiAnKe, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        ret = card_analyse.get_jiang_ke_shun_plus(hand_card.hand_card_vals)
        for index in xrange(len(ret)):
            k = ret[index]["k"]
            if len(k) == 4:
                return True
        return False


if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0, None)
    hand_card.hand_card_info = {
        1: [8, 3, 3, 0, 0, 0, 0, 0, 2, 0],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [3, 3, 0, 0, 0],                 # 风
        5: [3, 3, 0, 0],                    # 箭
    }
    # hand_card.hand_card_info = {
    #     1: [9, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [2, 2, 0, 0, 0],                 # 风
    #     5: [0, 0, 0, 0],                    # 箭
    # }

    hand_card.record_an_gang_card(17)
    hand_card.record_an_gang_card(18)
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print "hand_card =", hand_card.hand_card_vals
    test_type = SiAnKe()
    start_time = time.time()
    print test_type.is_this_type(hand_card, card_analyse)
    print "time = ", time.time() - start_time