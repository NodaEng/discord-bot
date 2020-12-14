import json
from distutils.command.config import config


class Player:
    def __init__(self, name, server, age=None, height=None, weight=None, strength=None, dexterity=None,
                 constitution=None, intelligence=None, wisdom=None, charisma=None, sanity=None, skills=None):
        self.name = name
        self.server = server
        self.age = age
        self.height = height
        self.weight = weight
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma
        self.sanity = sanity
        self.skills = skills

    