import random

from kivy.app import App


class Monster:
    """
    A class used as template for every Monster.

    Methods
    -------
    attack(player_hp)
        Returns the players health after attacking.

    defend(player_attack)
        Returns the 
    """

    def __init__(self, hp, attack, lvl, loot):
        """
        :param hp: The health of the monster
        :type hp: int

        :param attack: The attack strength of the monster
        :type attack: int

        :param lvl: The level of the monster
        :type lvl: int

        :param loot: A 5 string long dictionary with items that the monster can drop
        :type loot: list

        :rtype: object
        """
        self.hp = hp
        self.attack = attack
        self.lvl = lvl
        self.loot = loot

    def strong_attack_m(self, player_hp):
        """ Takes the players health and removes the strong attack strength of
        the monster.

        :param player_hp: The players health
        :type player_hp: int

        :return player_hp: The players new health.
        :rtype: int
        """
        player_hp = player_hp - self.attack
        return player_hp

    def weak_attack_m(self, player_hp):
        """ Takes the players health and removes the weak attack strength of
        the monster.

        :param player_hp: The players health
        :type player_hp: int

        :return player_hp: The players new health.
        :rtype: int
        """

        player_hp = player_hp - self.attack * 0.5
        return round(player_hp)

    def check_dead(self):
        """ This function checks if the monster is killed if so the monster will
        drop 1 of its 5 lootable items and some xp.

        :return output: A list made form the loot and xp
        :rtype: list[str, int]
        """
        output = []
        if self.hp <= 0:
            output = [self.loot[random.randint(0, 4)], round(self.lvl * 0.6)]
            return output
        return output


class Player:
    def __init__(self, hp, attack, lvl, xp, right_hand=None, left_hand=None):
        self.hp = hp
        self.attack = attack
        self.lvl = lvl
        self.xp = xp
        self.right_hand = right_hand
        self.left_hand = left_hand

    def strong_attack_p(self, monster_hp):
        """ Takes the monster's health and removes the strong attack strength of
        the player.

        :param monster_hp: The monster's health
        :type monster_hp: int

        :return monster_hp: The monster's new health.
        :rtype: int
        """

        monster_hp = monster_hp - self.attack
        return monster_hp

    def weak_attack_p(self, monster_hp):
        """ Takes the monster's health and removes the weak attack strength of
        the player.

        :param monster_hp: The monster's health
        :type monster_hp: int

        :return monster_hp: The monster's new health.
        :rtype: int
        """

        monster_hp = monster_hp - self.attack * 0.5
        return round(monster_hp)

    def run(self):
        """ Run from the monster

        :return succeed: If the player escaped
        :rtype succeed: bool
        """

        random_int = random.randint(1, 10)
        if random_int > 8:
            succeed = False
        else:
            succeed = True
        return succeed

    def check_dead(self):
        """ This function checks if the player is killed if so return True

        :rtype: bool
        """

        if self.hp <= 0:
            App.get_running_app().config.set('game', 'health', self.hp)
            App.get_running_app().config.set('game', 'attack', self.attack)
            App.get_running_app().config.set('game', 'xp', self.xp)
            App.get_running_app().config.set('game', 'level', self.lvl)
            App.get_running_app().config.set('game', 'inventory',
                                             self.inventory())
            App.get_running_app().config.set('game', 'left', self.left_hand)
            App.get_running_app().config.set('game', 'right', self.right_hand)
            return True
        return False

    def inventory(self):
        """" 
        :return list(App.get_running_app().config.get('game', 'inventory')): the players inventory
        :rtype list
        """
        inventory = str(App.get_running_app().config.get('game', 'inventory'))
        inventory = inventory.split(' ')
        return list(inventory)

    def inventory_add(self, loot):
        """ Add the loot to the current inventory.
        
        :param loot: The new loot for in the inventory
        :type loot: str

        :rtype: bool
        """
        inventory = self.inventory()
        inventory.append(loot)
        inventory = ' '.join(inventory)

        App.get_running_app().config.set('game', 'inventory', str(inventory))
        return True

    def inventory_check(self):
        """"Check what is in the inventory that can be used"""
        inventory = self.inventory()
        potion = 0
        dust = 0
        bone = 0
        gold_nugget = 0
        flesh = 0
        for item in inventory:
            if item == "Potion":
                potion += 1
            elif item == "Flesh":
                flesh += 1
            elif item == "Gold nugget":
                gold_nugget += 1
            elif item == "Bone":
                bone += 1
            elif item == "Dust":
                dust += 1
        return [potion, flesh, gold_nugget, bone, dust]
