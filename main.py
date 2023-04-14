import requests, argparse, random, mrz, img_gen, datetime
from unidecode import unidecode
from faker import Faker

# parser = argparse.ArgumentParser()

# # command-line arguments
# parser.add_argument('-n', '--name', help='')

data = requests.get('http://api.namefake.com/romanian-romania/').json()

with open('last_person_generated.txt', 'w', encoding='utf-8') as last_generated:
    last_generated.write(str(data))

judetList = open('judete.csv', 'r', encoding='utf-8').read().split(',')

name = data['name'].split()
if name[0][-1] == '.':
    name = name[1:]

first_name = name[-2]
last_name = name[-1]

gender = data['url'][42] # 'm' or 'f'

birthday = data['birth_data'].split('-')

area = data['address'].split(', ')[-2].replace(' ', '-')
if area == 'Satu-Mare':
    area == 'Satu Mare'
area_code = judetList.index(area) + 1
area_code = str(area_code + 10) if area_code > 40 else str(area_code)
area_code = '0' * (2 - len(area_code)) + area_code

locality = data['address'].split(', ')[-3].split(' ')
print(locality)
if locality[0][-1] == '.':
    locality = locality[0] + ' '.join(locality[1:])
else:
    locality = 'Loc.' + ' '.join(locality)
address = ' '.join(data['address'].split(', ')[0:-3]).replace('. ', '.')
print(address)

print(locality)

nnn = str(random.randint(1, 999))
nnn = '0' * (3 - len(nnn)) + nnn

# calculating CNP
cnp = [None] * 13

birthyear = int(birthday[0])

# S
if birthyear >= 2000:
    cnp[0] = 5 if gender == 'm' else 6
elif birthyear >= 1900:
    cnp[0] = 1 if gender == 'm' else 2
else:
    cnp[0] = 3 if gender == 'm' else 4

cnp[0] = str(cnp[0])

cnp[1:3] = list(birthday[0][-2:]) # AA

cnp[3:5] = list(birthday[1]) # LL

cnp[5:7] = list(birthday[2]) # ZZ

cnp[7:9] = list(area_code) # JJ

cnp[9:12] = list(nnn) # NNN

constant = list('279146358279')
constant_sum = 0

for i in range(12):
    constant_sum += int(cnp[i]) * int(constant[i])

c = constant_sum % 11
c = 1 if c == 10 else c

cnp[12] = str(c)

# start & expiry date
fake = Faker()
expiry_date = fake.date_between('+1y', '+7y')
start_date = expiry_date

expiry_date = datetime.date(expiry_date.year, int(birthday[1]), int(birthday[2]))
start_date = datetime.date(start_date.year - 10, start_date.month, start_date.day)

print(f'{start_date}-{expiry_date}')

# calculating bottom rows
bottomrow = [['<'] * 36] * 2

# calculating bottom row 1
bottomrow[0][:5] = list('IDROU')

name_adapted = [name[-2].replace('-', '<').replace(' ', '<'), name[-1].replace('-', '<').replace(' ', '<')]
first_name_a = unidecode(name_adapted[0])
last_name_a = unidecode(name_adapted[1])

bottomrow[0][5:(5 + len(last_name_a))] = last_name_a.upper()

br1 = 7 + len(last_name_a)

bottomrow[0][br1:(br1 + len(first_name_a))] = first_name_a.upper()

print(name)

print(bottomrow[0])

# calculating bottom row 2
series = {
            '01': ['AX'], # ALba
            '02': ['AR', 'ZR'], # Arad
            '03': ['AS', 'AZ'], # Arges
            '04': ['XC', 'ZC'], # Bacau
            '05': ['XH', 'ZH'], # Bihor
            '06': ['XB'], # Bistrita-Nasaud
            '07': ['XT'], # Botosani
            '08': ['BV', 'ZV'], # Brasov
            '09': ['XR'], # Braila
            '10': ['XZ'], # Buzau
            '11': ['KS'], # Caras-Severin
            '12': ['KX', 'CJ'], # Cluj
            '13': ['KT', 'KZ'], # Constanta
            '14': ['KV'], # Covasna
            '15': ['DD', 'ZD'], # Dambovita
            '16': ['DX', 'DZ'], # Dolj
            '17': ['GL', 'ZL'], # Galati
            '18': ['GZ'], # Gorj
            '19': ['HR'], # Harghita
            '20': ['HD', 'XD'], # Hunedoara
            '21': ['SZ'], # Ialomita
            '22': ['MX', 'MZ', 'IZ'], # Iasi
            '23': ['IF'], # Ilfov
            '24': ['MM', 'XM'], # Maramures
            '25': ['MH'], # Mehedinti
            '26': ['ZS', 'MS'], # Mures
            '27': ['NT', 'NZ'], # Neamt
            '28': ['OT'], # Olt
            '29': ['PH', 'PX'], # Prahova
            '30': ['SM'], # Satu Mare
            '31': ['SX'], # Salaj
            '32': ['SB'], # Sibiu
            '33': ['SV', 'XV'], # Suceava
            '34': ['TR'], # Teleorman
            '35': ['TM', 'TZ'], # Timis
            '36': ['TC'], # Tulcea
            '37': ['VS', 'XS'], # Vaslui
            '38': ['VX'], # Valcea
            '39': ['VN'], # Vrancea
            '40': ['DP', 'DR', 'DT', 'DX', 'RD', 'RR', 'RT', 'RX', 'RK', 'RZ'], # Bucuresti
            '51': ['KL'], # Calarasi
            '52': ['GG'], # Giurgiu
          }
area_ids = {
            '01': 'AB', # ALba
            '02': 'AR', # Arad
            '03': 'AG', # Arges
            '04': 'BC', # Bacau
            '05': 'BH', # Bihor
            '06': 'BN', # Bistrita-Nasaud
            '07': 'BT', # Botosani
            '08': 'BV', # Brasov
            '09': 'BR', # Braila
            '10': 'BZ', # Buzau
            '11': 'CS', # Caras-Severin
            '12': 'CJ', # Cluj
            '13': 'CT', # Constanta
            '14': 'CV', # Covasna
            '15': 'DB', # Dambovita
            '16': 'DJ', # Dolj
            '17': 'GL', # Galati
            '18': 'GJ', # Gorj
            '19': 'HR', # Harghita
            '20': 'HD', # Hunedoara
            '21': 'IL', # Ialomita
            '22': 'IS', # Iasi
            '23': 'IF', # Ilfov
            '24': 'MM', # Maramures
            '25': 'MH', # Mehedinti
            '26': 'MS', # Mures
            '27': 'NT', # Neamt
            '28': 'OT', # Olt
            '29': 'PH', # Prahova
            '30': 'SM', # Satu Mare
            '31': 'SJ', # Salaj
            '32': 'SB', # Sibiu
            '33': 'SV', # Suceava
            '34': 'TR', # Teleorman
            '35': 'TM', # Timis
            '36': 'TL', # Tulcea
            '37': 'VS', # Vaslui
            '38': 'VL', # Valcea
            '39': 'VN', # Vrancea
            '40': 'B', # Bucuresti
            '51': 'CL', # Calarasi
            '52': 'GR', # Giurgiu
}

bottomrow[1] = ['<'] * 36

id_code = series[area_code][random.randint(0, len(series[area_code]) - 1)]

id_num = [None] * 6

for i in range(len(id_num)):
    id_num[i] = str(random.randint(0, 9))

id_series = list(id_code) + id_num

bottomrow[1][:8] = id_series

bottomrow[1][9] = str(mrz.checksum(id_series))

bottomrow[1][10:13] = list('ROU')

bottomrow[1][13:19] = cnp[1:7]

bottomrow[1][19] = str(mrz.checksum(cnp[1:7]))

bottomrow[1][20] = gender.upper()

bottomrow[1][21:23] = str(expiry_date.year)[2:]

bottomrow[1][23:25] = '0' * (2 - len(str(expiry_date.month))) + str(expiry_date.month)

bottomrow[1][25:27] = '0' * (2 - len(str(expiry_date.day))) + str(expiry_date.day)

bottomrow[1][27] = str(mrz.checksum(bottomrow[1][21:27]))

bottomrow[1][28] = cnp[0] # just an educated guess, may not be correct

bottomrow[1][29:35] = cnp[-6:]

bottomrow[1][35] = str(mrz.checksum(bottomrow[1][0:10] + bottomrow[1][13:20] + bottomrow[1][21:35]))

print(bottomrow[1])

# create image
img_gen.generate_id({
    'surname': last_name,
    'name': first_name,
    'sex': gender.upper(),
    'cnp': cnp,
    'area_id': area_ids[area_code],
    'locality': locality,
    'address': address,
    'emmitting_institution': area,
    'emission_date': start_date,
    'expiry_date': expiry_date,
    'series': id_code,
    'series_number': id_num,
    'mrz': bottomrow,
})