test = {'endernaga': {'role': 'tank', 'build_name': 'булава', 'ip': 1200}, 'DearDie': {'role': 'tank', 'build_name': 'булава', 'ip': 1300}, 'Toper228': {'role': 'tank', 'build_name': 'булава', 'ip': 1350}}
print(sorted(test.items(), key=lambda x: x[1]['ip']))