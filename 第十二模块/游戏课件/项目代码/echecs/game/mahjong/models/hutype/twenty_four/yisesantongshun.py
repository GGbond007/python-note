# coding=utf-8
import copy
import time

from game.mahjong.models.hutype.basetype import BaseType
from game.mahjong.constants.carddefine import CardType
from game.mahjong.models.hutype.basetype import BaseType
from game.mahjong.constants.carddefine import CardType, CARD_SIZE
from game.mahjong.models.card.hand_card import HandCard
from game.mahjong.models.utils.cardanalyse import CardAnalyse


class YiSeSanTongShun(BaseType):
    """
    3)	一色三同顺 : 胡牌时，牌里有一种花色且序数相同的3副顺子
    不记番： 一色三节高、一般高
    """
    def __init__(self):
        super(YiSeSanTongShun, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        # 不是清一色则返 False
        union_card = hand_card.union_card_info
        print "union_card = ", union_card
        # 4,5,6 至少有一张
        for i, count in enumerate(union_card[CardType.WAN]):
            if i == 0 and count != 14:
                return False

        chi_card_vals = hand_card.chi_card_vals
        ret = card_analyse.get_jiang_ke_shun_plus(hand_card.hand_card_vals)
        for index in xrange(len(ret)):

            s = ret[index]["s"]
            s.extend(chi_card_vals)
            if len(s) < 3:
                continue
            shun_count = 1
            while len(s) > 0:
                t = s.pop()
                if t in s:
                    shun_count += 1
                    if shun_count == 3:
                        return True
                else:
                    shun_count = 0

            print s

        return False


if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0, None)
    hand_card.hand_card_info = {
        1: [14, 3, 3, 3, 1, 1, 1, 0, 0, 2],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [0, 0, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }
    # hand_card.hand_card_info = {
    #     1: [12, 1, 1, 3, 3, 3, 1, 0, 0, 2],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [0, 0, 0, 0, 0],                 # 风
    #     5: [0, 0, 0, 0],                    # 箭
    # }

    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print "hand_card =", hand_card.hand_card_vals
    test_type = YiSeSanTongShun()
    start_time = time.time()
    print test_type.is_this_type(hand_card, card_analyse)
    print "time = ", time.time() - start_time