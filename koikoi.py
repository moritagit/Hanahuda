#! usr/bin/env python3
# -*-coding: utf-8 -*-



## modules -------------------------------------------------------------------------------------------------------------
import random



## variables -----------------------------------------------------------------------------------------------------------

# lists
lights = ["鶴", "幕", "月", "小野道風", "鳳凰"]
seeds = ["鶯", "不如帰", "八橋", "蝶", "猪", "雁", "盃", "鹿", "燕"]
strips = ["短冊", "赤短", "青短"]

priority2flower_list = [["菊"], ["桜", "芒"], ["松"], ["桐"], ["牡丹", "紅葉"], ["柳"], ["梅", "萩"], ["藤", "菖蒲"]]
priority2role_list = ["盃", "幕", "月", "鶴", "鳳凰", "赤短", "青短", "小野道風", "鹿", "蝶", "猪"]
priority2month_list = [9, 3, 8, 1, 12, 6, 10, 11, 2, 7]

# dictionaries
month2flower =\
    {
        1 : "松", 2 : "梅", 3 : "桜", 4 : "藤", 5 : "菖蒲", 6 : "牡丹",
        7 : "萩", 8 : "芒", 9 : "菊", 10 : "紅葉", 11 : "柳", 12 : "桐"
    }

flower2month = \
    {
        "松" : 1, "梅" : 2, "桜" : 3, "藤" : 4, "菖蒲" : 5, "牡丹" : 6,
        "萩" : 7, "芒" : 8, "菊" : 9, "紅葉" : 10, "柳" : 11, "桐" : 12
    }

month2role =\
    {
         1 : ["鶴",                  "赤短", "カス", "カス"],
         2 : [              "鶯",    "赤短", "カス", "カス"],
         3 : ["幕",                  "赤短", "カス", "カス"],
         4 : [              "不如帰","短冊", "カス", "カス"],
         5 : [              "八橋",  "短冊", "カス", "カス"],
         6 : [              "蝶",    "青短", "カス", "カス"],
         7 : [              "猪",    "短冊", "カス", "カス"],
         8 : ["月",         "雁",            "カス", "カス"],
         9 : [              "盃",    "青短", "カス", "カス"],
        10 : [              "鹿",    "青短", "カス", "カス"],
        11 : ["小野道風",   "燕",    "短冊", "カス"],
        12 : ["鳳凰",                         "カス", "カス", "カス"]
    }

month2primeroles =\
    {
        1 : ["鶴", "赤短"], 2 : ["赤短"], 3 : ["幕", "赤短"], 4 : [], 5 : [], 6 : ["蝶", "青短"],
        7 : ["猪"], 8 : ["月"], 9 : ["盃", "青短"], 10 : ["鹿", "青短"], 11 : ["小野道風"], 12 : ["鳳凰"]
    }

role2num = {}
for role in lights:
    role2num[role] = 1
for role in seeds:
    role2num[role] = 2
for role in strips:
    role2num[role] = 3
role2num["カス"] = 4

yaku2point =\
    {
        "五光" : 10, "四光" : 8, "雨四光" : 7, "三光" : 5,
        "花見酒" : 5, "月見酒" : 5,
        "猪鹿蝶" : 5, "赤短" : 5, "青短" : 5,
        "たね" : 1, "たん" : 1, "かす" : 1
    }



## functions -----------------------------------------------------------------------------------------------------------

def make_carddict():
    """
    This is a function to make month-to-card list dictionary.
    """
    month2card = {}
    for month in range(1, 13):
        list_temp = []
        for role in month2primeroles[month]:
            card = Card(month, role)
            list_temp.append(card)
        month2card[month] = list_temp
    return month2card


def make_primecard_list():
    """
    This is a function to make a list of cards which have priority.
    """
    priority_list = []
    for flowerlist in priority2flower_list:
        for flower in flowerlist:
            month = flower2month[flower]
            for role in month2role[month]:
                priority_list.append(Card(month, role))
    return priority_list


def make_deck():
    """
    This is a function to make a deck
    by making a list including all cards,
    and shuffle it.
    This function assumes that a deck is drawn by sequence, not randomly.
    """
    deck = []
    for month in range(1, 13):
        for role in month2role[month]:
            card = Card(month, role)
            deck.append(card)
    random.shuffle(deck)
    return deck


def draw_card_from(cards):
    """
    This is a function to draw a card (mainly from the deck).
    """
    drawn_card = cards.pop(0)
    return drawn_card


def pickup_card_from(cards):
    """
    This is a function to chose a card
    from a set of cards (argument) by inputting the card name.
    """
    mistaken = False
    chosen_name = input("札の名前を入力してください：")
    print()

    chosen = None
    for card in cards:
        if chosen_name == card.name:
            chosen = card
            break

    if chosen is None:
        print("あるものの名前を入れてください")
        chosen = pickup_card_from(cards)
        mistaken = True

    if not mistaken:
        cards.remove(chosen)
    return chosen


def classify(man, cards):
    """
    This is a function to classify the cards by their role
    """
    for card in cards:
        if card.role in lights:
            man.hikari.append(card)
        elif card.role == "盃":
            man.tane.append(card)
            man.kasu.append(card)
        elif card.role in seeds:
            man.tane.append(card)
        elif card.role in strips:
            man.tan.append(card)
        else:
            man.kasu.append(card)


def make_month2cards(cards):
    """
    This is a function to make a dictionary
    (key = month, value = list of cards which month is same).
    """
    month2cards = {}
    for month in range(1, 13):
        month2cards[month] = []
    for card in cards:
        month2cards[card.month].append(card)
    return month2cards


def choose_from(cards, reverse=False):
    """
    This is a function to choose a card from 2 cards.
    """
    sorted_cards = sorted(cards)
    if reverse == False:
        return sorted_cards[0]
    else:
        return sorted_cards[-1]



## classes -------------------------------------------------------------------------------------------------------------

class Card(object):
    """
    This is a class to represent a card.
    This class takes 2 arguments, month and role.
    The type of month may be int or str, which represents the month.
    The type of role is str, which is included in month2role dict.
    Parameters, i.e. month, flower, and role(light, seed, strip, or kasu) can be accessed.
    """
    def __init__(self, month, role):
        if type(month) == int:
            self.month = month
            self.flower = month2flower[self.month]
        elif type(month) == str:
            self.flower = month
            for i in range(1, 13):
                if month2flower[i] == self.flower:
                    self.month = i
        self.role = role
        self.name = "{flower}の{role}".format(flower=self.flower, role=self.role)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if type(other) == str:
            return self.name == other
        elif type(other) == Card:
            return self.name == other.name

    def __ne__(self, other):
        if type(other) == str:
            return self.name != other
        elif type(other) == Card:
            return self.name != other.name

    def __lt__(self, other):
        if self.month < other.month:
            return self.month < other.month
        elif self.month == other.month:
            return role2num[self.role] < role2num[other.role]

    def __gt__(self, other):
        if self.month > other.month:
            return self.month > other.month
        elif self.month == other.month:
            return role2num[self.role] > role2num[other.role]


class Player:
    """
    This is a class to represent a player.
    The parameters are lists for saving his hand, share (got cards), and point.
    """
    def __init__(self):
        self.hand = []
        self.share = []
        self.share_temp = []
        self.yaku = []
        self.hikari = []
        self.tane = []
        self.tan = []
        self.kasu = []
        self.hold = [self.hikari, self.tane, self.tan, self.kasu]          # a list for storing sorted cards
        self.point = 0



class Koikoi:
    """
    This is the main class to play koikoi.
    """
    def __init__(self):
        self.player = Player()
        self.cp = Player()
        self.field = []

        self.month_priority = []

        self.winner = None
        self.winpoint = 0
        self.agari = False


    def start(self):
        """
        Start a Koikoi game,
        i.e. make deck, make hands and a field,
        and display player's hand and the field.
        """
        self.deck = make_deck()
        self.month2card = make_carddict()
        self.prime_cards = make_primecard_list()

        for i in range(8):
            self.player.hand.append(draw_card_from(self.deck))
            self.cp.hand.append(draw_card_from(self.deck))
            self.field.append(draw_card_from(self.deck))
        self.display_now()

        # when 4 cards in same month are on the field, restart the game
        months = []
        for card in self.field:
            months.append(card.month)
        for i in range(1, 13):
            if months.count(i) == 4:
                print("同じ月の札が四枚場に出てしまったのでやり直します")
                self.start()


    def display_now(self):
        print("相手の取り札")
        print(self.cp.hold)
        print()

        print("相手の手札")
        print(self.cp.hand)
        print()

        print("場")
        print(self.field)
        print()
        print("手札")
        print(self.player.hand)
        print()
        print("自分の取り札")
        print(self.player.hold)
        print()


    def draw_display(self, turn):
        """
        This is a method to draw a card and put it on the field,
        and then display the field.
        """
        print("山札から1枚引きます")
        drawn_card = draw_card_from(self.deck)
        print("{card}が引かれました\n".format(card=drawn_card))
        self.put(drawn_card, turn)
        self.display_now()


    def put(self, chosen, turn):
        """
        This is a method to put a card (argument) in the field.
        """
        man = turn
        man.share_temp = []
        chosen_card = chosen

        match_list = []      # create a list to store cards, which month matches chosen one's
        for card in self.field:
            if card.month == chosen_card.month:
                match_list.append(card)

        counter = len(match_list)
        if counter == 0:
            man.share_temp = []
            self.field.append(chosen_card)
        elif counter == 1:
            man.share_temp = [chosen_card, match_list[0]]
            man.share.append(chosen_card)
            man.share.append(match_list[0])
            self.field.remove(match_list[0])
        elif counter == 2:
            print("場に出た札と同じ月の札が2枚あります")
            if man == self.player:
                appended = pickup_card_from(match_list)
            else:
                appended = choose_from(match_list)
                print("{card}を選びました".format(card=appended))
            man.share_temp = [chosen_card, appended]
            man.share.append(chosen_card)
            man.share.append(appended)
            self.field.remove(appended)
        elif counter == 3:
            man.share_temp = [chosen_card]
            man.share.append(chosen_card)
            for i in range(3):
                man.share_temp.append(match_list[i])
                man.share.append(match_list[i])
                self.field.remove(match_list[i])

        classify(man, man.share_temp)


    def choose(self):           #なんか死んでる
        """
        This is a method for cp to choose a card from his hand, to put it on the field.
        """
        hand_dict = make_month2cards(self.cp.hand)
        field_dict = make_month2cards(self.field)
        self.make_priority_list()

        remain = self.deck
        remain += self.player.hand
        month2remaining = make_month2cards(remain)

        chosen = None

        matched_month = []
        for month in range(1, 13):
            if (hand_dict[month] != []) and (field_dict[month] != []):
                matched_month.append(month)

        # frags and lists for searching cp's hand
        have4 = False
        have4month = []
        have3remain1 = False
        have3remain1month = []
        have2remain2 = False
        have2remain2month = []
        have2remain0 = False
        have2remain0month = []
        have1remain1 = False
        have1remain1month = []
        have1remain23 = False
        have1remain23month = []

        have3thereis1 = False
        have3thereis1month = []
        have2thereis2 = False
        have2thereis2month = []
        have2thereis1 = False
        have2thereis1month = []
        have1thereis3 = False
        have1thereis3month = []
        have1thereis2 = False
        have1thereis2month = []
        have1thereis1remain2 = False
        have1thereis1remain2month = []
        have1thereis1remain0 = False
        have1thereis1remain0month = []

        # recognize the circumstance
        for month in range(1, 13):
            if len(hand_dict[month]) == 0:
                continue
            elif len(hand_dict[month]) == 4:
                have4 = True
                have4month.append(month)
            elif len(hand_dict[month]) == 3:
                have3remain1 = True
                have3remain1month.append(month)
            elif len(hand_dict[month]) == 2:
                if len(month2remaining) == 2:
                    have2remain2 = True
                    have2remain2month.append(month)
                elif len(month2remaining) == 0:
                    have2remain0 = True
                    have2remain0month.append(month)
            elif (len(hand_dict[month]) == 1) and (len(month2remaining) == 1):
                have1remain1 = True
                have1remain1month.append(month)
            else:  # that is, have1remain2 or have1remain3
                have1remain23 = True
                have1remain23month.append(month)

        # when cp can take nothing from the field
        if len(matched_month) == 0:
            if have4:
                chosen = random.choice(hand_dict[have4month[0]])
            elif have2remain0:
                chosen = random.choice(hand_dict[have2remain0month])
            elif have3remain1:                                              #ここに複雑な論理を入れる？
                for flowerlist in priority2flower_list[::-1]:
                    for flower in flowerlist:
                        month = flower2month[flower]
                        if month in have3remain1month:
                            chosen = Card(month, "カス")
            elif have1remain23:
                for flowerlist in priority2flower_list[::-1]:
                    for flower in flowerlist:
                        month = flower2month[flower]
                        if month in have1remain23month:
                            chosen_temp = hand_dict[month][0]
                            if chosen_temp not in self.prime_cards:
                                chosen = chosen_temp
            elif have2remain2:
                for flowerlist in priority2flower_list[::-1]:
                    for flower in flowerlist:
                        month = flower2month[flower]
                        if month in have2remain2month:
                            chosen_temp = choose_from(hand_dict[month], reverse=True)
                            if chosen_temp not in self.prime_cards:
                                chosen = chosen_temp
            else:   #have1remain1
                for flowerlist in priority2flower_list[::-1]:
                    for flower in flowerlist:
                        month = flower2month[flower]
                        if month in have1remain1month:
                            chosen_temp = hand_dict[month][0]
                            if chosen_temp not in self.prime_cards:
                                chosen = chosen_temp

            if chosen == None:
                for card in self.prime_cards[::-1]:
                    if card in self.cp.hand:
                        chosen = card

        # when cp can take anything from the field
        else:
            # recognize the circumstance
            for month in matched_month:
                if len(hand_dict[month]) == 3:
                    have3thereis1 = True
                    have3thereis1month.append(month)
                elif len(hand_dict[month]) == 2:
                    if len(field_dict[month]) == 2:
                        have2thereis2 = True
                        have2thereis2month.append(month)
                    elif len(field_dict[month]) == 1:
                        have2thereis1 = True
                        have2thereis1month.append(month)
                elif len(hand_dict[month]) == 1:
                    if len(field_dict[month]) == 3:
                        have1thereis3 = True
                        have1thereis3month.append(month)
                    elif len(field_dict[month]) == 2:
                        have1thereis2 = True
                        have1thereis2month.append(month)
                    elif len(field_dict[month]) == 1:
                        if len(month2remaining[month]) == 2:
                            have1thereis1remain2 = True
                            have1thereis1remain2month.append(month)
                        elif len(month2remaining[month]) == 0:
                            have1thereis1remain0 = True
                            have1thereis1remain0month.append(month)

            # choose from cards which are not confirmed to be taken
            if have2thereis1 or have1thereis1remain2 or have1thereis2:
                cantake = have2thereis1month
                cantake += have1thereis1remain2month
                cantake += have1thereis2month
                if "菊の盃" in cantake:
                    chosen = choose_from(hand_dict[9])
                elif "桜の幕" in cantake:
                    chosen = choose_from(hand_dict[3])
                elif "芒の月" in cantake:
                    chosen = choose_from(hand_dict[8])

            if not chosen:
                if have2thereis1:
                    for month in priority2month_list:
                        if month in have2thereis1month:
                            chosen = choose_from(hand_dict[month])
                            break
                elif have1thereis1remain2:
                    for month in priority2month_list:
                        if month in have1thereis1remain2month:
                            chosen_temp = choose_from(hand_dict[month])
                            if chosen_temp in self.prime_cards:
                                chosen = chosen_temp
                                break
                elif have1thereis2:
                    for month in priority2month_list:
                        if month in have1thereis2month:
                            chosen_temp = choose_from(hand_dict[month])
                            if chosen_temp in self.prime_cards:
                                chosen = chosen_temp
                                break

            if not chosen:
                if have2thereis1:
                    chosen = choose_from(hand_dict[have2thereis1month[0]])
                elif have1thereis2:
                    chosen = hand_dict[have1thereis2month[0]][0]
                elif have1thereis1remain2:
                    chosen = hand_dict[have1thereis1remain2month[0]][0]

            # put a card which is confirmed to be taken
            if not chosen:
                if have4:
                    chosen = random.choice(hand_dict[have4month[0]])
                elif have2remain0:
                    chosen = random.choice(hand_dict[have2remain0month[0]])

            # 中間処理
            if not chosen:
                if have2thereis2:
                    chosen = choose_from(hand_dict[have2thereis2month[0]], reverse=True)
                elif have3remain1:  # ここに複雑な論理を入れる？
                    for flowerlist in priority2flower_list[::-1]:
                        for flower in flowerlist:
                            month = flower2month[flower]
                            if month in have3remain1month:
                                chosen = Card(month, "カス")
                elif have1remain23:
                    for flowerlist in priority2flower_list[::-1]:
                        for flower in flowerlist:
                            month = flower2month[flower]
                            if month in have1remain23month:
                                chosen_temp = hand_dict[month][0]
                                if chosen_temp not in self.prime_cards:
                                    chosen = chosen_temp
                elif have2remain2:
                    for flowerlist in priority2flower_list[::-1]:
                        for flower in flowerlist:
                            month = flower2month[flower]
                            if month in have2remain2month:
                                chosen_temp = hand_dict[month][-1]
                                if chosen_temp not in self.prime_cards:
                                    chosen = chosen_temp

            # choose from cards which are confirmed to be taken
            if not chosen:
                if have3thereis1:
                    chosen = choose_from(hand_dict[have3thereis1month[0]], reverse=True)
                elif have1thereis3:
                    chosen = hand_dict[have1thereis3month[0]][0]
                elif have1thereis1remain0:
                    chosen = hand_dict[have1thereis1remain0month[0]][0]

        print(chosen)
        self.cp.hand.remove(chosen)
        return chosen


    def make_priority_list(self):       #要アップデート
        """
        This is a method to make a priority list of cards for cp.
        """
        hand_dict = make_month2cards(self.cp.hand)
        month2count = {}
        for month in range(1, 13):
            if hand_dict[month] is not []:
                month2count[month] = month2count.get(month, 0) + 1

        remain = self.deck
        remain += self.player.hand
        month2remain = make_month2cards(remain)

        self.month_priority = []
        months_in_hand = list(month2count.keys())
        for i in range(len(priority2flower_list)):
            for flower in priority2flower_list[i]:
                if flower2month[flower] in months_in_hand:
                    self.month_priority.append(flower2month[flower])


    def myturn(self):
        """
        This is a method to implement player's turn once.
        """
        # chose a card from my hand and put it in the field
        print("あなたの番です")
        chosen_card = pickup_card_from(self.player.hand)
        print("{chosen}を出しました\n".format(chosen=chosen_card))
        self.put(chosen_card, self.player)

        # draw a card from the deck and put it in the field
        self.draw_display(self.player)


    def cpturn(self):
        """
        This is a method to implement cp's turn once.
        """
        print("CPの番です")
        chosen_card = self.choose()
        print("{chosen}を出しました\n".format(chosen=chosen_card))
        self.put(chosen_card, self.cp)
        self.draw_display(self.cp)


    def calc_point(self, turn):
        """
        This is a method to calculate the point (mon).
        """
        man = turn
        point_temp = 0
        gokou = False
        sikou = False
        amesikou = False
        sankou = False
        inosikatyou = False
        akatan = False
        aotan = False
        hanamizake = False
        tsukimizake = False
        tane = False
        tan = False
        kasu = False

        # about hikari cards
        if len(man.hikari) == 5:
            man.yaku.append("五光")
            point_temp += yaku2point["五光"]
            if gokou == False:
                print("五光です")
                gokou = True
        elif len(man.hikari) == 4:
            if "柳の小野道風" in man.hikari:
                man.yaku.append("雨四光")
                point_temp += yaku2point["雨四光"]
                if amesikou == False:
                    print("雨四光です")
                    amesikou = True
            else:
                man.yaku.append("四光")
                point_temp += yaku2point["四光"]
                if sikou == False:
                    print("四光です")
                    sikou = True
        elif (len(man.hikari) == 3) and ("柳の小野道風" not in man.hikari):
            man.yaku.append("三光")
            point_temp += yaku2point["三光"]
            if sankou == False:
                print("三光です")
                sankou = True

        # about sake
        if "菊の盃" in man.tane:
            if "桜の幕" in man.hikari:
                man.yaku.append("花見酒")
                point_temp += yaku2point["花見酒"]
                if hanamizake == False:
                    print("花見酒です")
            elif "芒の月" in man.hikari:
                man.yaku.append("月見酒")
                point_temp += yaku2point["月見酒"]
                if tsukimizake == False:
                    print("月見酒です")

        # about tane cards
        if len(man.tane) >= 5:
            man.yaku.append("たね")
            point_temp += yaku2point["たね"] * (len(man.tane) - 4)
            print("たねです")
        if ("萩の猪" in man.tane) and ("紅葉の鹿" in man.tane) and ("牡丹の蝶" in man.tane):
            man.yaku.append("猪鹿蝶")
            point_temp += yaku2point["猪鹿蝶"]
            if inosikatyou == False:
                print("猪鹿蝶です")
                inosikatyou = True

        # about tanzaku cards
        if man.tan.count("赤短") == 3:
            man.yaku.append("赤短")
            point_temp += yaku2point["赤短"]
            if akatan == False:
                print("赤短です")
                akatan = True
        if man.tan.count("青短") == 3:
            man.yaku.append("青短")
            point_temp += yaku2point["青短"]
            if aotan == False:
                print("青短")
                aotan = True
        if ("赤短" in man.yaku) or ("青短" in man.yaku):    #ここ違う
            point_temp += yaku2point["短冊"] * (man.tan.count("短冊") - 3)
            print("たんです")
        elif len(man.tan) >= 5:
            man.yaku.append("たん")
            point_temp += yaku2point["たん"] * (len(man.tan) - 4)
            print("たんです")

        # about kasu cards
        if len(man.kasu) >= 10:
            man.yaku.append("かす")
            point_temp += yaku2point["かす"] * (len(man.kasu) - 9)
            print("かすです")

        return point_temp


    def play(self):
        """
        This is a method to actually play the game koikoi.
        You can play koikoi by making an instance of Koikoi class (like k = Koikoi()),
        and using this method (like k.play()).
        """
        self.start()
        while self.player.hand != [] and self.cp.hand != []:
            self.myturn()

            point_temp = self.calc_point(self.player)
            if point_temp > self.player.point:
                self.player.point = point_temp
                print("playerさんが点を獲得しました")
                if self.player.hand != []:
                    message = input("こいこいですか？ 上がりですか？")
                    print()
                    if message == "こいこい":
                        pass
                    elif message == "上がり":
                        self.winner = "player"
                        self.winpoint = self.player.point
                        self.agari = True
                        break
                    else:
                        print("どっちだよ。こいこいにすっからな")
                else:
                    self.winner = "player"
                    self.winpoint = self.player.point
                    self.agari = True
                    break

            self.cpturn()
            point_temp = self.calc_point(self.cp)
            if point_temp > self.cp.point:
                self.cp.point = point_temp
                print("cpさんが点を獲得しました")
                if self.cp.hand is not []:
                    message = input("こいこいですか？ 上がりですか？")
                    print()
                    if message == "こいこい":
                        pass
                    elif message == "上がり":
                        self.winner = "cp"
                        self.winpoint = self.cp.point
                        self.agari = True
                        break
                    else:
                        print("どっちだよ。こいこいにすっからな")
                else:
                    self.winner = "cp"
                    self.winpoint = self.cp.point
                    self.agari = True
                    break

        if self.agari:
            print("{point}文で{winner}の勝ちです".format(point=self.winpoint, winner=self.winner))
        else:
            print("流れです")




## execution -----------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    k = Koikoi()
    k.play()
