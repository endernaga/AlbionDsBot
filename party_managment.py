class Party_managment:

    finished_party = []
    all_party_list = {}
    all_sorted_role = {'tank': {}, 'heal': {}, 'support': {}, 'mdd': {}, 'rdd': {}, 'battle_mount' :{}}
    splited_party_list = {'tank': [], 'heal': [], 'support': [], 'mdd': [], 'rdd': [], 'battle_mount' :[]}

    def __init__(self, tank_count=0, heal_count=0, support_count=0,
                 mdd_count=0, rdd_count=0, battle_mount_count=0):
        self.all_role_counts = {'tank': tank_count, 'heal': heal_count, 'support': support_count,
                                'mdd': mdd_count, 'rdd': rdd_count, 'battle_mount': battle_mount_count}

    def add_to_party(self, role, build_name, user_name, ip):
        self.all_party_list[user_name] = {'role': role, 'build_name': build_name, 'ip': ip}

    def remove_party_member(self, user_name):
        del self.all_party_list[user_name]

    def filter_players_by_role(self, role): #асинхронна функція
        players_list = {}
        for key in self.all_party_list:
            if self.all_party_list[key]['role'] == role:
                players_list[key] = self.all_party_list[key]
        return players_list

    def role_sort(self):
        for role in self.all_sorted_role:
            self.all_sorted_role[role].update(dict(sorted(self.filter_players_by_role(role).items(), key=lambda x: x[1]['ip'], reverse=True)))


    def create_party(self):
        form_party = []
        for keys in self.all_sorted_role:
            roles = self.all_sorted_role[keys]
            for role in roles:
                form_party.append({role: self.all_party_list[role]})
                if len(form_party) == self.all_role_counts[keys]:
                    self.splited_party_list[keys].append(form_party)
                    form_party = []
            else:
                if len(form_party) > 0:
                    self.splited_party_list[keys].append(form_party)
                    form_party = []


    def finish_party(self):
        party_size = max([len(self.splited_party_list[i]) for i in self.splited_party_list])
        party_manage = []
        for i in range(party_size):
            for role in self.splited_party_list:
                if len(self.splited_party_list[role]) - 1 >= i:
                    party_manage += self.splited_party_list[role][i]
            self.finished_party.append(party_manage)
            party_manage = []



if __name__ == '__main__':
    test = Party_managment(2, 3, 2, 5, 5)
    test.add_to_party('tank', 'булава', 'endernaga', 1200)
    test.add_to_party('tank', 'булава', 'DearDie', 1300)
    test.add_to_party('tank', 'булава', 'Toper228', 1350)
    test.add_to_party('heal', 'друід', 'ark4sky', 1300)
    test.add_to_party('mdd', 'демон фанг', 'doctor_pepper', 1300)
    test.role_sort()
    #print(test.all_sorted_role)
    test.create_party()
    #print(test.splited_party_list)
    test.finish_party()
    print(test.finished_party[0])