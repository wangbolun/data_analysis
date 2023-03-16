import csv


class ReadCase:
    def __init__(self):
        self.cases_list_dict = {
            'id': [],
            'modular': [],
            'name': [],
            'id_name': [],
            'lcm_name': [],
            'key': [],
            'condition': [],
            'step': [],
            'result': [],
        }

    def read(self, case_data_name):
        with open(case_data_name, encoding="utf8") as f:
            csv_reader = csv.reader(f)
            next(csv_reader) 
            for line in csv_reader:
                self.cases_list_dict['id'].append(line[0])
                self.cases_list_dict['modular'].append(line[2])
                self.cases_list_dict['name'].append(line[4])
                self.cases_list_dict['id_name'].append(line[0] + line[4])
                self.cases_list_dict['lcm_name'].append(
                    str('_') + line[2][1:4] + str('_') + line[2][-4:-1] + str('_') + line[0] + str('_'))
                self.cases_list_dict['key'].append(line[9])
                self.cases_list_dict['condition'].append(line[5])
                self.cases_list_dict['step'].append(line[6])
                self.cases_list_dict['result'].append(line[7])
