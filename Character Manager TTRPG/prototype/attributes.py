
# idk why this exists. im sure it'll be useful later 
#obso

class Attributes:
    def __init__(self, prowess=0, might=0, presence=0, power=0, armor_uses=1):
        self.basic_attributes = {'prowess': prowess, 'might': might, 'presence': presence}
        self.special_attributes = {'power': power, 'armor_uses': armor_uses}
        self.harm_tracks = {'physical': [4, 4], 'mental': [4, 4], 'spiritual': [3, 3]}
        self.wound_thresholds = {'minor': 5, 'major': 7, 'severe': 9}
        self.damage_dice = {'physical': '1d4', 'mental': '1d4', 'spiritual': '1d4'}
        self.resources = {
            'mana': {'current': 0, 'max': 10},
            'mercy': {'current': 0, 'max': 10},
            'wrath': {'current': 0, 'max': 10},
            'trickery_dice': {'current': 0, 'max': 5}
        }

    def update_power(self, level):
        power_levels = {1: 1, 3: 2, 5: 3, 7: 4, 10: 5}
        self.special_attributes['power'] = power_levels.get(level, 1)

    def set_resource(self, resource_name, current, max):
        if resource_name in self.resources:
            self.resources[resource_name]['current'] = current
            self.resources[resource_name]['max'] = max

    def update_resource(self, resource_name, amount, is_current=True):
        resource = self.resources.get(resource_name)
        if resource:
            key = 'current' if is_current else 'max'
            resource[key] = max(0, min(resource[key] + amount, resource['max'] if is_current else float('inf')))
            self.resources[resource_name] = resource

    def to_dict(self):
        return {
            'basic_attributes': self.basic_attributes,
            'special_attributes': self.special_attributes,
            'harm_tracks': self.harm_tracks,
            'wound_thresholds': self.wound_thresholds,
            'damage_dice': self.damage_dice,
            'resources': self.resources
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls(
            prowess=data['basic_attributes'].get('prowess', 0),
            might=data['basic_attributes'].get('might', 0),
            presence=data['basic_attributes'].get('presence', 0),
            power=data['special_attributes'].get('power', 0),
            armor_uses=data['special_attributes'].get('armor_uses', 1)
        )
        instance.harm_tracks = data.get('harm_tracks', {})
        instance.wound_thresholds = data.get('wound_thresholds', {})
        instance.damage_dice = data.get('damage_dice', {})
        instance.resources = data.get('resources', {})
        return instance

# new attributes. old class will remain for visual reference but will be phased out of code 

class BasicAttributes:
    def __init__(self, prowess=0, might=0, presence=0):
        self.prowess = prowess
        self.might = might
        self.presence = presence

    def to_dict(self):
        return {
            'prowess': self.prowess,
            'might': self.might,
            'presence': self.presence
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            prowess=data.get('prowess', 0),
            might=data.get('might', 0),
            presence=data.get('presence', 0)
        )
    
class SpecialAttributes:
    def __init__(self, power=1, armor_uses=1, armor=0):
        self.power = power
        self.armor_uses = armor_uses
        self.armor = armor

    def update_power(self, level):
        if level >= 9:
            self.power = 5
        else:
            self.power = (level + 1) // 2 # // is integer division and sets the value equal to the nearest lower integer 

    def to_dict(self):
        return {
            'power': self.power,
            'armor_uses': self.armor_uses,
            'armor': self.armor
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            power=data.get('power', 1),
            armor_uses=data.get('armor_uses', 1),
            armor=data.get('armor', 0)
        )

class HarmTracks:
    def __init__(self, physical=4, mental=4, spiritual=3):
        self.tracks = {
            'physical': [physical, physical],
            'mental': [mental, mental],
            'spiritual': [spiritual, spiritual]
        }

    def update_harm_track(self, track_name, value):
        if track_name in self.tracks:
            self.tracks[track_name][1] = max(0, value)
            self.tracks[track_name][0] = min(self.tracks[track_name][0], self.tracks[track_name][1])

    def to_dict(self):
        return {
            'physical': self.tracks['physical'],
            'mental': self.tracks['mental'],
            'spiritual': self.tracks['spiritual']
        }

    @classmethod
    def from_dict(cls, data):
        instance = cls()
        instance.tracks['physical'][1] = data.get('physical', [4, 4])[1]
        instance.tracks['mental'][1] = data.get('mental', [4, 4])[1]
        instance.tracks['spiritual'][1] = data.get('spiritual', [3, 3])[1]
        instance.reset_harm_tracks()  # Resets current to max
        return instance

    def reset_harm_tracks(self):
        for key in self.tracks:
            self.tracks[key][0] = self.tracks[key][1]

class WoundThresholds:
    def __init__(self, physical=5, mental=7, spiritual=9):
        self.physical = physical
        self.mental = mental
        self.spiritual = spiritual

    def to_dict(self):
        return {
            'physical': self.physical,
            'mental': self.mental,
            'spiritual': self.spiritual
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            physical=data.get('physical', 5),
            mental=data.get('mental', 7),
            spiritual=data.get('spiritual', 9)
        )
    
class DamageDice:
    def __init__(self, physical='1d4', mental='1d4', spiritual='1d4'):
        self.physical = physical
        self.mental = mental
        self.spiritual = spiritual

    def set_dice(self, type, dice):
        if hasattr(self, type):
            setattr(self, type, dice)

    def to_dict(self):
        return {
            'physical': self.physical,
            'mental': self.mental,
            'spiritual': self.spiritual
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            physical=data.get('physical', '1d4'),
            mental=data.get('mental', '1d4'),
            spiritual=data.get('spiritual', '1d4')
        )

class ManaResource:
    def __init__(self, flame=0, mist=0, stone=0, will=0, wind=0):
        self.flame = flame
        self.mist = mist
        self.stone = stone
        self.will = will
        self.wind = wind

    def update_resource(self, resource_type, amount, max_power):
        if hasattr(self, resource_type) and self.total_resources() + amount <= max_power + 1:
            setattr(self, resource_type, max(0, getattr(self, resource_type) + amount))

    def total_resources(self):
        return self.flame + self.mist + self.stone + self.will + self.wind

    def to_dict(self):
        return {
            'flame': self.flame,
            'mist': self.mist,
            'stone': self.stone,
            'will': self.will,
            'wind': self.wind
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            flame=data.get('flame', 0),
            mist=data.get('mist', 0),
            stone=data.get('stone', 0),
            will=data.get('will', 0),
            wind=data.get('wind', 0)
        )

class DevotionResource:
    def __init__(self, mercy=0, wrath=0):
        self.mercy = mercy
        self.wrath = wrath

    def update_resource(self, resource_type, amount, max_power):
        if hasattr(self, resource_type) and self.total_resources() + amount <= max_power + 1:
            setattr(self, resource_type, max(0, getattr(self, resource_type) + amount))

    def total_resources(self):
        return self.mercy + self.wrath

    def to_dict(self):
        return {
            'mercy': self.mercy,
            'wrath': self.wrath
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            mercy=data.get('mercy', 0),
            wrath=data.get('wrath', 0)
        )

class TrickeryDice:
    def __init__(self, count=1, dice='1d6'):
        self.count = count
        self.dice = dice

    def update_dice(self, new_dice):
        self.dice = new_dice

    def update_count(self, new_count, max_level):
        if new_count <= max_level + 1:
            self.count = new_count

    def to_dict(self):
        return {
            'count': self.count,
            'dice': self.dice
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            count=data.get('count', 1),
            dice=data.get('dice', '1d6')
        )
    
