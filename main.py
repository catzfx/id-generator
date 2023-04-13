import requests, argparse, random

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

print(cnp)
for i in range(13):
    print(cnp[i], end='')