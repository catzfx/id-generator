import requests, argparse, random
from unidecode import unidecode

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
area_code = str(judetList.index(area) + 1)
area_code = '0' * (2 - len(area_code)) + area_code

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