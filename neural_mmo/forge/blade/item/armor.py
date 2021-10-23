from neural_mmo.forge.blade.item import item


class NPC(item.Item):
   def __init__(self, armor_type, description):
      super().__init__(armor_type, description)
