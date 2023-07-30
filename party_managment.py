import asyncio
from random import choice, randint
from random_username.generate import generate_username
class Party_managment:

    checking = True

    finished_party = []
    all_player_list = {}
    all_sorted_role = {'tank': {}, 'heal': {}, 'support': {}, 'MDD': {}, 'RDD': {}, 'battle_mount' :{}}
    splited_party_list = {'tank': [], 'heal': [], 'support': [], 'MDD': [], 'RDD': [], 'battle_mount' :[]}

    def __init__(self, tank_count=0, heal_count=0, support_count=0,
                 mdd_count=0, rdd_count=0, battle_mount_count=0):
        self.all_role_counts = {'tank': tank_count, 'heal': heal_count, 'support': support_count,
                                'MDD': mdd_count, 'rdd': rdd_count, 'battle_mount': battle_mount_count}

    async def add_to_party(self, role, build_name, user_name, ip):
        self.all_player_list[user_name] = {'role': role, 'build_name': build_name, 'ip': ip}
        await asyncio.sleep(1)

    async def remove_party_member(self, user_name):
        del self.all_player_list[user_name]

    async def filter_players_by_role(self, role): #асинхронна функція
        players_list = {}
        for key in self.all_player_list:
            if self.all_player_list[key]['role'] == role:
                players_list[key] = self.all_player_list[key]
        return players_list

    async def role_sort(self):
        for role in self.all_sorted_role:
            player_list = await self.filter_players_by_role(role)
            self.all_sorted_role[role].update(dict(sorted(player_list.items(), key=lambda x: x[1]['ip'], reverse=True)))


    async def create_party(self):
        self.splited_party_list = {'tank': [], 'heal': [], 'support': [], 'MDD': [], 'RDD': [], 'battle_mount' :[]}
        form_party = []
        for keys in self.all_sorted_role:
            roles = self.all_sorted_role[keys]
            for role in roles:
                form_party.append({role: self.all_player_list[role]})
                if len(form_party) == self.all_role_counts[keys]:
                    self.splited_party_list[keys].append(form_party)
                    form_party = []
            else:
                if len(form_party) > 0:
                    self.splited_party_list[keys].append(form_party)
                    form_party = []


    async def finish_party(self):
        self.finished_party = []
        if len(self.all_player_list) > 0:
            await self.role_sort()
            await self.create_party()
            party_size = max([len(self.splited_party_list[i]) for i in self.splited_party_list])
            party_manage = []
            for i in range(party_size):
                for role in self.splited_party_list:
                    if len(self.splited_party_list[role]) - 1 >= i:
                        party_manage += self.splited_party_list[role][i]
                self.finished_party.append(party_manage)
                party_manage = []
        print(f"finished party is {self.finished_party}")



if __name__ == '__main__':

    async def stop_check(obj: Party_managment):
        await asyncio.sleep(30)
        obj.checking = False
    async def main():
        test = Party_managment(2, 3, 2, 5, 5)
        async with asyncio.TaskGroup() as tg:
            for i in range(40):
                tg.create_task(test.add_to_party(choice(['tank', 'heal', 'support', 'mdd', 'rdd']), generate_username(1)[0], generate_username(1)[0], randint(1100, 2000)))
            tg.create_task(stop_check(test))
            tg.create_task(test.finish_party())

    #test = Party_managment(2, 3, 2, 5, 5)

    #test.add_to_party('tank', 'булава', 'DearDie', 1300)
    #test.add_to_party('tank', 'булава', 'Toper228', 1350)
    #test.add_to_party('heal', 'друід', 'ark4sky', 1300)
    #test.add_to_party('mdd', 'демон фанг', 'doctor_pepper', 1300)
    asyncio.run(main())
    #print(test)