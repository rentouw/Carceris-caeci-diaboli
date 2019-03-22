"""Carceris caeci diaboli.
------------------------
This is a text based game. Where you fight monsters or people in a dungeon.

The app widget structure (layout) is found in main.kv
The mosnter and player class you will find in the game_class.py file
The app launcher used for debugging only supportes up to version 1.9.1
"""
import gettext
import random
from os.path import join, dirname
from time import sleep

import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Observable
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout

import game_classes

kivy.require('1.9.1')  # Used version of kivy for this project.


# Language class
class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('base', locale_dir, languages=[lang])
        self.ugettext = locales.gettext

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)


tr = Lang("en")  # The tr stands for translate

# class Pointer(Widget):
#     # text = "itohrsjgpoetrkhpotrdhktroijkhtrpojtmpo"
#     # id = StringProperty("point")
#     """3=0.18:0.178    4=0.16:0.12    x= x:y"""
#
#     # pos_hint = DictProperty({'x': 0.16, 'y': 0.278})
#
#     def enable(self):
#         self.text = "<--"
#
#     def disable(self):
#         self.text = ""


class RootWidget(FloatLayout):
    """This is the main class where the hole GUI is build and cconfigured"""
    # Connect the widget objects to the python program
    output_box = ObjectProperty(None)
    info = ObjectProperty(None)
    button_a = ObjectProperty(None)
    button_b = ObjectProperty(None)
    button_c = ObjectProperty(None)
    button_d = ObjectProperty(None)
    monster = ObjectProperty(None)
    player = ObjectProperty(None)
    game_text = "Placeholder"
    game_text_clear = ""
    first_text = ""
    backup = "backup text"

    first = 1  # 1 = Game first start, 0 = Game already started, 2 = placeholder
    move = 0b101  # 0b100 = can go left. 0b010 = can go forward. 0b001 = can go right
    waiting = 0  # 1 if waiting for input for moving/fighting
    random_int = 0
    dead = False
    teller = 0
    inventory = 1

    def first_run(self):
        """Sets up all the standard texts for the buttons and labels"""
        self.player = game_classes.Player(
            int(App.get_running_app().config.getint('game', 'health')),
            int(App.get_running_app().config.getint('game', 'attack')),
            int(App.get_running_app().config.getint('game', 'level')),
            int(App.get_running_app().config.getint('game', 'xp')),
            str(App.get_running_app().config.get('game', 'right')),
            str(App.get_running_app().config.get('game', 'left')))
        self.button_a.text = tr._("left")
        self.button_b.text = tr._("right")
        self.button_c.text = tr._("forward")
        self.button_d.text = tr._("inventory")
        self.game_text = tr._("""Welcome to Carceris caeci diaboli.
=======================================================

This is a text based game. Where you are in a dungeon and fight monsters.
You move around in the dungeon by pressing the buttons and when you encounter a monster you fight it.
You can use items in your inventory to heal or level up faster.


Press forward enter the dungeon.
""")
        Clock.schedule_interval(self.update, 0.5)

    def update(self, dt):
        """This updates the game every 0.5 second.
        
        Updates the label and screen and check if the player is dead. 
        """
        del dt  # Unused
        # Update buttons
        tr.switch_lang(str(App.get_running_app().config.get('main', 'lang')))
        if self.waiting == 1:
            self.button_a.text = tr._("left")
            self.button_b.text = tr._("right")
            self.button_c.text = tr._("forward")
            self.button_d.text = tr._("inventory")
        elif self.waiting == 2:
            self.button_a.text = tr._("weak attack")
            self.button_b.text = tr._("strong attack")
            self.button_c.text = tr._("run")
            self.button_d.text = tr._("inventory")
        elif self.waiting == 3:
            self.button_a.text = tr._("up")
            self.button_b.text = tr._("use")
            self.button_c.text = tr._("down")
            self.button_d.text = tr._("exit")
        # Update Label
        self.info.text = tr._(
            "Username: %s\n    Health: %s\n    Attack: %s\n    Level: %s\n    Xp: %s"
        ) % (str(App.get_running_app().config.get('main', 'username')),
             str(self.player.hp), str(self.player.attack), str(
                 self.player.lvl), str(self.player.xp))
        # Update screen.
        self.output_box.text = self.game_text

        if self.dead:
            Clock.unschedule(self.update)
            sleep(1)
            self.game_text = tr._("""You have died.
            
Your level was %s

Thanks for playing

:Authors: rentouw
:Version: 0.2V 10/02/2019""") % (str(self.player.lvl))
            # For the last update of the screen.
            self.output_box.text = self.game_text
            self.waiting = 0
            self.first = App.get_running_app().config.set(
                'main', 'first_run', 0)

    def update_text(self, text):
        """This updates the Label attribute."""
        # TODO: Make everything new jump out
        self.teller += 1
        if self.teller >= 9:
            self.teller = 0
            self.game_text_clear = ""
        self.game_text_clear = self.game_text_clear + "\n" + self.first_text + "\n"
        self.first_text = text
        self.game_text = self.game_text_clear + "\n**" + self.first_text + "**"
        return True

    def crossroad(self, random_int):
        """ Check what sort of crossroad is found."""
        template_text = tr._("You have found a crossroad where you can go ")
        if random_int == 0b111:
            self.update_text(template_text + tr._("left, right, or forwards."))
        elif random_int == 0b011:
            self.update_text(template_text + tr._("forward or right."))
        elif random_int == 0b101:
            self.update_text(template_text + tr._("left or right."))
        elif random_int == 0b110:
            self.update_text(template_text + tr._("left or forwards."))
        elif random_int == 0b001:
            self.update_text(tr._("You can only go right."))
        elif random_int == 0b100:
            self.update_text(tr._("You can only go left."))
        else:
            self.random_int = random.randint(1, 7)
            # This needs to go back to move to update it.
            random_int = self.crossroad(self.random_int)
        return random_int

    def monster_turn(self):
        """"The monster's turn."""
        random_int = random.randint(1, 10)
        if random_int > 8:
            self.update_text(
                tr._("The monster tries to attack you but misses."))
        else:
            if random_int > 4:
                self.player.hp = self.monster.strong_attack_m(self.player.hp)
                self.update_text(
                    tr._("The monster used a strong attack against you."))
            else:
                self.player.hp = self.monster.weak_attack_m(self.player.hp)
                self.update_text(
                    tr._("The monster used a weak attack against you."))
            self.dead = self.player.check_dead()

    def check_monster_kill(self):
        """" Check if the monster is dead."""
        loot = self.monster.check_dead()
        if len(loot) == 2:
            self.update_text(tr._("You killed the monster."))
            self.update_text(
                tr._("The monster dropped %s and %s XP.") % (str(loot[0]),
                                                             str(loot[1])))
            self.player.inventory_add(loot[0])
            self.player.xp = self.player.xp + int(loot[1])
            self.monster = False

            return True
        else:
            return False

    def monster_encounter(self, random_int):
        hp_m = round(2 * random_int + self.player.lvl * 0.8)
        attack_m = round(random_int + self.player.lvl * 0.8)
        lvl_m = round(random_int + self.player.lvl * 0.8)
        loot_m = ['Bone', 'Flesh', 'Gold nugget', 'Dust', 'Potion']
        self.monster = game_classes.Monster(hp_m, attack_m, lvl_m, loot_m)
        self.update_text(
            tr._("There is a monster around the corner which jumps you."))
        self.monster_turn()

    def pointer_pos(self, pos):
        if pos == 1:
            self.ids['point'].pos_hint = {'x': 0.13, 'y': 0.274}
        elif pos == 2:
            self.ids['point'].pos_hint = {'x': 0.12, 'y': 0.225}
        elif pos == 3:
            self.ids['point'].pos_hint = {'x': 0.17, 'y': 0.1786}
        elif pos == 4:
            self.ids['point'].pos_hint = {'x': 0.12, 'y': 0.130}
        elif pos == 5:
            self.ids['point'].pos_hint = {'x': 0.12, 'y': 0.080}

    def buttona(self):
        """This is for the Left/weak/up attack button"""
        if self.waiting == 1:  # Move Mode
            if self.move & 0b100:
                self.update_text(tr._("You enter the hallway to your left."))
                self.random_int = random.randint(
                    1, 10)  # random int to check encounter
                if self.random_int > 6:  # No monster
                    self.random_int = random.randint(1, 7)
                    self.move = self.crossroad(self.random_int)
                else:
                    self.waiting = 2
                    self.button_a.text = tr._("weak attack")
                    self.button_b.text = tr._("strong attack")
                    self.button_c.text = tr._("run")
                    self.monster_encounter(self.random_int)

        elif self.waiting == 2:  # Attack Mode
            random_int = random.randint(1, 10)
            if random_int > 8:
                self.update_text(
                    tr._("You tried to attack the monster but failed."))
            else:
                self.monster.hp = self.player.weak_attack_p(self.monster.hp)
                self.update_text(tr._("You attack the monster"))
                self.update_text(
                    tr._("The monsters health is %s now.") % (str(
                        self.monster.hp)))

            if self.check_monster_kill():
                self.button_a.text = tr._("left")
                self.button_b.text = tr._("right")
                self.button_c.text = tr._("forward")
                self.waiting = 1
                self.random_int = random.randint(1, 7)
                self.move = self.crossroad(self.random_int)
            else:
                self.monster_turn()

        elif self.waiting == 3:
            if self.inventory <= 1:
                self.inventory = 1
            elif self.inventory > 1:
                self.inventory -= 1
            self.pointer_pos(self.inventory)

    def buttonb(self):
        """This is for the right/strong/use attack button"""
        if self.waiting == 1:
            if self.move & 0b001:

                self.update_text(tr._("You enter the hallway to your right."))
                self.random_int = random.randint(
                    1, 10)  # random int to check encounter
                if self.random_int > 6:  # No monster
                    self.random_int = random.randint(1, 7)
                    self.move = self.crossroad(self.random_int)
                else:
                    self.waiting = 2
                    self.button_a.text = tr._("weak attack")
                    self.button_b.text = tr._("strong attack")
                    self.button_c.text = tr._("run")

                    self.monster_encounter(self.random_int)

        elif self.waiting == 2:
            random_int = random.randint(1, 10)
            if random_int > 8:
                self.update_text(
                    tr._("You tried to attack the monster but failed."))
            else:
                self.monster.hp = self.player.strong_attack_p(self.monster.hp)
                self.update_text(tr._("You attack the monster"))
                self.update_text(
                    tr._("The monsters health is %s now.") % (str(
                        self.monster.hp)))

            if self.check_monster_kill():
                self.button_a.text = tr._("left")
                self.button_b.text = tr._("right")
                self.button_c.text = tr._("forward")
                self.waiting = 1
                self.random_int = random.randint(1, 7)
                self.move = self.crossroad(self.random_int)
            else:
                self.monster_turn()

        elif self.waiting == 3:
            if self.inventory == 1:
                # Potion
                pass
            elif self.inventory == 2:
                # Flesh
                pass
            elif self.inventory == 3:
                # Gold nugget
                pass
            elif self.inventory == 4:
                # Bone
                pass
            elif self.inventory == 5:
                # Dust
                pass
            pass

    def buttonc(self):
        """This is for the Move/run/down button"""
        if self.first == 1:
            self.game_text = ""
            App.get_running_app().config.set('main', 'first_run', 0)
            self.first = 0
            self.update_text(tr._("You enter the dungeon."))
            self.random_int = random.randint(1, 7)
            self.move = self.crossroad(self.random_int)
            self.waiting = 1

        elif self.waiting == 1:
            if self.move & 0b010:
                self.update_text(tr._("You keep walking forward."))
                self.random_int = random.randint(
                    1, 10)  # random int to check encounter
                if self.random_int > 6:  # No monster
                    self.random_int = random.randint(1, 7)
                    self.move = self.crossroad(self.random_int)
                else:
                    self.waiting = 2
                    self.button_a.text = tr._("weak attack")
                    self.button_b.text = tr._("strong attack")
                    self.button_c.text = tr._("run")

                    self.monster_encounter(self.random_int)

        elif self.waiting == 2:
            random_int = random.randint(1, 10)
            if random_int <= 3:
                self.update_text(
                    tr.
                    _("You successfully ran around the monster without it grabbing you."
                      ))
                self.random_int = random.randint(1, 7)
                self.move = self.crossroad(self.random_int)
                self.button_a.text = tr._("left")
                self.button_b.text = tr._("right")
                self.button_c.text = tr._("forward")
            else:
                self.update_text(
                    tr.
                    _("You tried to run around the monster but it garbed you and throws you against the wall."
                      ))
                self.player.hp = self.player.hp - 1
                self.dead = self.player.check_dead()

        elif self.waiting == 3:
            if self.inventory >= 5:
                self.inventory = 5
            elif self.inventory < 5:
                self.inventory += 1
            self.pointer_pos(self.inventory)

    def buttond(self):
        """This is for the Inventory/exit button"""
        if self.first != 1 and not self.dead:
            if self.waiting == 3:
                self.game_text = self.backup
                self.ids['point'].pos_hint = {'x': 1, 'y': 1}
                if self.monster:
                    self.waiting = 2
                else:
                    self.waiting = 1
            else:
                a = self.player.inventory_check()
                output_text = tr._("""Inventory
=================
Potion = %s

Flesh = %s

Gold nugget = %s

Bone = %s

Dust = %s""") % (a[0], a[1], a[2], a[3], a[4])
                self.backup = self.game_text
                self.game_text = output_text
                self.button_a.text = tr._("up")
                self.button_b.text = tr._("use")
                self.button_c.text = tr._("down")
                self.button_d.text = tr._("exit")
                self.waiting = 3
                self.ids['point'].pos_hint = {'x': 0.13, 'y': 0.273}


class MainApp(App):
    """This is the main class. Because this class is called MainApp the paired
    file is main.kv.
    """
    # This turns of the settings menu for kivy
    use_kivy_settings = False

    # # FOR ANDROID CONFIG ONLY
    # def get_application_config(self, defaultpath='/sdcard/.%(appname)s.ini'):
    #     return super(MainApp, self).get_application_config('/sdcard/.%(appname)s.ini')

    def build_settings(self, settings):  # Make settings menu

        settings.add_json_panel(
            'Main settings', self.config,
            'Main_settings.json')  # Settings menu for Main settings section
        settings.add_json_panel(
            'Game settings', self.config,
            'Game_settings.json')  # Settings menu for Game settings section

    def build_config(self, config):
        config.setdefaults(  # Configure the default setings
            'main',
            {
                'id': 1,  # User id
                'username': 'user',  # Username
                'lang': 'en',  # Language
                'first_run': 1  # first run 1 = yes 0 = no
            })
        config.setdefaults(
            'game',
            {
                'health': 10,  # health
                'attack': 10,  # attack power
                'xp': 0,  # expirience
                'level': 1,  # level
                'inventory': '',  # inventory
                'left': "None",  # left hand item
                'right': "None"  # right hand item
            })

    def build(self):
        game = RootWidget()
        # Update language
        global tr
        tr = Lang(str(App.get_running_app().config.get('main', 'lang')))

        game.first_run()
        return game

    # Language part
    lang = StringProperty('en')


if __name__ == '__main__':
    MainApp().run()  # Start the app by running the first class
