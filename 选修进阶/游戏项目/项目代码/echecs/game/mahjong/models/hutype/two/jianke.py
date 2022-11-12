# coding=utf-8
import time

from game.mahjong.models.hutype.basetype import BaseType
from game.mahjong.constants.carddefine import CardType, CARD_SIZE
from game.mahjong.models.card.hand_card import HandCard
from game.mahjong.models.utils.cardanalyse import CardAnalyse


class JianKe(BaseType):
    """
    1)	箭刻：由中、发、白3张相同的牌组成的刻子或者杠。胡牌时，手牌中有一个箭刻。
    """

    def __init__(self):
        super(JianKe, self).__init__()

    def is_this_type(self, hand_card, card_analyse):
        used_card_type = [CardType.WAN]  # 此游戏中使用的花色
        union_card = hand_card.union_card_info
        print "union_card = ", union_card
        # 4,5,6 至少有一张
        jiang_ke_count = 0
        for i,count in enumerate(union_card[CardType.JIAN]):
            if i == 0 and count < 3:
                return False
            if count == 3:
                jiang_ke_count += 1
        return jiang_ke_count == 1


if __name__ == "__main__":
    pass
    card_analyse = CardAnalyse()
    hand_card = HandCard(0)
    # hand_card.hand_card_info = {
    #     1: [9, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 万
    #     2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
    #     3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
    #     4: [2, 2, 0, 0, 0],                 # 风
    #     5: [3, 3, 0, 0],                    # 箭
    # }
    hand_card.hand_card_info = {
        1: [9, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 万
        2: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 条
        3: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 饼
        4: [2, 2, 0, 0, 0],                 # 风
        5: [0, 0, 0, 0],                    # 箭
    }
    hand_card.chi_card_vals=[[23,24,25]]
    hand_card.handle_hand_card_for_settle_show()
    hand_card.union_hand_card()
    print "hand_card =", hand_card.hand_card_vals
    test_type = JianKe()
    start_time = time.time()
    print test_type.is_this_type(hand_card, card_analyse)
    print "time = ", time.time() - start_time