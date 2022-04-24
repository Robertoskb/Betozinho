from random import randint
from commands.utils.users import User


class UserLevel(User):

    def __init__(self, id):
        super().__init__(id)

    def give_xp(self, xp):
        level, new_xp, descr = self.get_updates(xp)

        if level and xp != None and descr:
            updates = f'level={level}, xp={new_xp}, description="{descr}"'
            self.update_user(updates)

    def get_updates(self, xp):
        if not self.infos:
            return None, None, None

        level, new_xp = self.get_level_xp(xp)
        descr = self.get_description(level)

        return level, new_xp, descr

    def get_level_xp(self, xp):
        level = self.infos['level']
        new_xp = self.infos['xp'] + randint(int(xp*0.7), xp)

        xp_needed = level * 20000
        while new_xp >= xp_needed and level < 7:
            level += 1
            new_xp = new_xp - xp_needed
            xp_needed = level * 20000

        return level, new_xp

    def get_description(self, level):
        descriptions = {
            1: 'Adotado! Ef 1:5',
            2: 'Adotado! Ef 1:5',
            3: 'Filho de Deus! Rm 8:16',
            4: 'Filho de Deus! Rm 8:16',
            5: 'Perdoado! Lc 7:50 ',
            6: 'Perdoado! Lc 7:50 ',
            7: 'Cidadão do Céu! Fp 3:20'
        }

        return descriptions[level]


if __name__ == '__main__':
    user = UserLevel(1)
    user.create_user()
    for i in range(1, 100000):
        user.give_xp(7000)
    
        print(user.infos, end = '\n\n')
        
        if user.infos['level'] == 7:
            print(f'Versículos lidos: {i}')
            break
    
    user.delete_user()