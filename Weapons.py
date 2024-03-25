
class Weapon():
    def __init__(self, name, damage, accuracy, range, weight, magSize, fireRate, reloadTime, CQC, attachment):
        self.name = name
        self.damage = damage
        self.accuracy = accuracy
        self.range = range
        self.weight = weight
        self.magSize = magSize
        self.fireRate = fireRate
        self.reloadTime = reloadTime
        self.CQC = CQC
        self.attachment = attachment

    def use_attachment(self):
        # if attachment.ability != 'none'
        pass
class Attachment():
    def __init__(self, name, damage, accuracy, range, weight, magSize, fireRate, reloadTime, CQC, ability):
        self.name = name
        self.damage = damage
        self.accuracy = accuracy
        self.range = range
        self.weight = weight
        self.magSize = magSize
        self.fireRate = fireRate
        self.reloadTime = reloadTime
        self.CQC = CQC
        self.ability = ability
