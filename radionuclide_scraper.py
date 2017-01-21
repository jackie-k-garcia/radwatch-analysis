import bs4
import urllib
import math
from Gamma_Isotopes import Isotope

def search(input):
    """
    if input is an energy (searching for multiple radionuclides), then a url
    will be created. if input is a string (searching for radionuclide
    information), then input will simply be reassigned as url.
    """
    if type(input) == int or type(input) == float:
        if input >= 2000:
            plus_three = input + 3
            minus_three = input - 3
            url = 'http://nucleardata.nuclear.lu.se/toi/Gamma.asp?sql=&Min=' \
            + str(minus_three) + '&Max=' + str(plus_three) \
            + '&HlifeMin=3600&tMinStr=1+h'
        elif input >= 1000:
            plus_two = input + 2
            minus_two = input - 2
            url = 'http://nucleardata.nuclear.lu.se/toi/Gamma.asp?sql=&Min=' \
            + str(minus_two) + '&Max=' + str(plus_two) \
            + '&HlifeMin=3600&tMinStr=1+h'
        else:
            plus_one = input + 1
            minus_one = input - 1
            url = 'http://nucleardata.nuclear.lu.se/toi/Gamma.asp?sql=&Min=' \
            + str(minus_one) + '&Max=' + str(plus_one) \
            + '&HlifeMin=3600&tMinStr=1+h'
    elif type(input) == str:
        url = input

    html = urllib.request.urlopen(url)
    bsobject = bs4.BeautifulSoup(html, 'lxml')

    return(bsobject)


def extract_table(bsobject):
    """
    table_extractor takes the bsobject and extracts all data in the table.
    """
    table = str(bsobject)

    data = []

    for i in range(len(table)):
        if table[i:i+8] == '<td>&lt;':
            for k in range(100):
                if table[i+8+k:i+8+k+1] == '*':
                    data.append('0')
                    break
                elif table[i+8+k:i+8+k+3] == '<i>':
                    data.append(table[i+8:i+8+k].strip())
                    for j in range(10):
                        if table[i+8+k+3+j:i+8+k+3+j+1] == '*':
                            data[-1] = '0'
                            break
                    break
                elif table[i+8+k:i+8+k+5] == '</td>':
                    data.append(table[i+8:i+8+k].strip())
                    break
        elif table[i:i+5] == '<td>~':
            for k in range(100):
                if table[i+5+k:i+5+k+1] == '*':
                    data.append('0')
                    break
                elif table[i+5+k:i+5+k+3] == '<i>':
                    data.append(table[i+5:i+5+k].strip())
                    for j in range(10):
                        if table[i+5+k+3+j:i+5+k+3+j+1] == '*':
                            data[-1] = '0'
                            break
                    break
                elif table[i+5+k:i+5+k+5] == '</td>':
                    data.append(table[i+5:i+5+k].strip())
                    break
        elif table[i:i+4] == '<td>':
            for k in range(100):
                if table[i+4+k:i+4+k+1] == '*':
                    data.append('0')
                    break
                elif table[i+4+k:i+4+k+3] == '<i>':
                    data.append(table[i+4:i+4+k].strip())
                    for j in range(10):
                        if table[i+4+k+3+j:i+4+k+3+j+1] == '*':
                            data[-1] = '0'
                            break
                    break
                elif table[i+4+k:i+4+k+5] == '</td>':
                    data.append(table[i+4:i+4+k].strip())
                    break

    return(data,table)


def extract_url(data):
    """
    Extracting all intensities and url addons from the table.
    """
    intensities = []
    for i in range(1, len(data), 5):
        intensities.append(data[i])

    url_add_ons = []
    for i in range(4, len(data), 5):
        for j in range(100):
            if data[i][j:j+4] == 'href':
                for k in range(100):
                    if data[i][j+4+k:j+4+k+2] == '><':
                        url_add_ons.append(data[i][j+4+2:j+4+k-1])
                        break
                break
    """
    Removing all intensities that are less than 1% and their corresponding
    radionuclide url addon.
    """
    for i in range(len(intensities)):
        if '(calc)' in intensities[i]:
            intensities[i] = intensities[i][:-6]
        if '&gt;' in intensities[i]:
            intensities[i] = '0'
        if '&lt;' in intensities[i]:
            intensities[i] = '0'
        if intensities[i] == '':
            intensities[i] = '0'
        intensities[i] = float(intensities[i])
        if intensities[i] < 1:
            intensities[i] = 0
    """
    taking the index of each intensity that is less than 1%.
    """
    indices = []
    for i,j in enumerate(intensities):
        if j == 0:
            indices.append(i)
    """
    removing intensities that are less than 1%.
    """
    while 0 in intensities: intensities.remove(0)

    for i in indices:
        url_add_ons[i] = 0
    """
    #removing coresponding urls that have intensities less than 1%.
    """
    while 0 in url_add_ons: url_add_ons.remove(0)
    """
    Creating full urls.
    """
    urls = []
    for i in range(len(url_add_ons)):
        urls.append('http://nucleardata.nuclear.lu.se/toi/' + url_add_ons[i])

    return(urls)


def extract_gamma(data):
    """
    Extracts gamma ray energies with intensities of at least 1%.
    """
    for i in range(len(data)):
        if '(calc)' in data[i]:
            data[i] = data[i][:-6]
        if '(' and ')' in data[i]:
            data[i] = data[i][1:-1]
        if '&gt;' in data[i]:
            data[i] = '0'
        if '&lt;' in data[i]:
            data[i] = '0'
        if data[i] == '':
            data[i] = '0'
        data[i] = float(data[i])
        if data[i] < float(1):
            if i%2 != 0:
                data[i] = 0
                data[i-1] = 0

    while 0 in data: data.remove(0)

    gamma_energies = []
    gamma_intensities_percent = []
    gamma_intensities = []

    for i in range(len(data)):
        if (i+1)%2 == 0:
            gamma_intensities_percent.append(data[i])
        else:
            gamma_energies.append(data[i])

    for value in gamma_intensities_percent:
        gamma_intensities.append(value*0.01)

    return(gamma_energies, gamma_intensities)


def extract_symbol(bsobject, table):
    """
    Acquires the symbol of the radionuclide.
    """
    """
    flag = False assumes that the radionuclide is not metastable.
    """
    flag = False

    bsradionuclide = bsobject.find('caption', {'align':'top'})

    text = bsradionuclide.get_text()

    symbol = ''

    for i in range(len(text)):
        try:
            float(text[i])
        except:
            symbol = symbol + text[i]
    """
    Had to add a whitespace for the special case of symbol = 'Ga' because
    extractor cannot distinguish between symbol = 'Ga' and 'Ga' from the string
    'Gammas from'.
    """
    symbol = symbol.strip() + ' '
    if symbol[0] == 'm':
        symbol = symbol[1:]
        flag = True
    """
    Acquires the half life and the decay constant of the radionuclide.
    """
    index = table.index(symbol)
    symbol = symbol.strip()
    """
    If flag equals True, then below conditional statement will append 'm' to
    the beginning of the symbol to show that it is a metastable state of a
    radionuclide.
    """
    if flag == True:
        symbol = 'm' + symbol

    return(symbol, index)


def extract_half_life(table, index):
    """
    Extracts the half life and decay constant of the radionuclide in seconds.
    """
    for i in range(len(table)):
        if table[i:i+3] == '<i>':
            time_symbol = table[i-2]
            label = i-2
            break
        elif table[i] == ')':
            time_symbol = table[i-1]
            label = i-1
            break

    half_life_text = table[index+2:label].strip()

    if half_life_text[0] == '(':
        half_life_text = half_life_text[1:]
        half_life_text = half_life_text.strip()
    if half_life_text[0] == '~':
        half_life_text = half_life_text[1:]
        half_life_text = half_life_text.strip()
    if half_life_text[0] == '>':
        half_life_text = half_life_text[1:]
        half_life_text = half_life_text.strip()
    if half_life_text[0] == '<':
        half_life_text = half_life_text[1:]
        half_life_text = half_life_text.strip()

    half_life = float(half_life_text)

    if time_symbol == 'm':
        half_life_seconds = 60*half_life
    elif time_symbol == 'h':
        half_life_seconds = 3600*half_life
    elif time_symbol == 'd':
        half_life_seconds = 3600*24*half_life
    elif time_symbol == 'y':
        half_life_seconds = (3.154*10**7)*half_life

    decay_constant_seconds = (math.log(2))/(half_life_seconds)

    return(half_life_seconds, decay_constant_seconds)


def extract_atomic_mass_numbers(url):
    """
    Acquiring atomic number and mass number.
    """
    numbers = ''

    for i in range(len(url)):
        if url[i] == '=':
            numbers = numbers + url[i+1:]
            numbers = numbers
            mass_number = int(numbers[-3:])
            atomic_number = numbers[:-3]
            break
    """
    For mass number.
    """
    if mass_number > int(300):
        mass_number = mass_number - 300
    """
    For atomic number.
    """
    if len(atomic_number) == 2:
        atomic_number = int(atomic_number[0])
    elif len(atomic_number) == 3:
        atomic_number = int(atomic_number[0:2])
    elif len(atomic_number) == 4:
        atomic_number = int(atomic_number[0:3])

    return(atomic_number, mass_number)


def compile_objects(info):
    """
    Returns a list of objects.
    """
    database = []
    for i in range(len(info)):
        vars()[info[i][0] + '_' + str(info[i][2])] = Isotope(info[i][0],
                                                             info[i][1],
                                                             info[i][2],
                                                             info[i][3],
                                                             info[i][4],
                                                             info[i][5],
                                                             info[i][6])

        database.append(vars()[info[i][0] + '_' + str(info[i][2])])

    return(database)


def main(energy):
    """
    Takes in gamma ray energy and calls the above functions to output the
    radionuclides' information (symbol, atomic number, mass number, half life,
    decay constant, gamma ray energies and their corresponding intensities)
    that emit a gamma ray at the specified energy.
    """
    radionuclides_bsobject = search(energy)
    data = extract_table(radionuclides_bsobject)
    urls = extract_url(data[0])

    info = []
    for i in range(len(urls)):
        bsobject = search(urls[i])
        """
        bsgammatable takes the gamma ray energy/intensity table from the
        bsobject.
        """
        bsgammatable = bsobject.table.findAll('table', {'border':'0',
                                              'cellpadding':'0',
                                              'cellspacing':'0'}, limit=1)

        table_data = extract_table(bsgammatable)
        gamma_info = extract_gamma(table_data[0])
        symbol = extract_symbol(bsobject, table_data[1])
        half_life = extract_half_life(table_data[1], symbol[1])
        atomic_mass_numbers = extract_atomic_mass_numbers(urls[i])

        radionuclide_info = [symbol[0], atomic_mass_numbers[0],
                             atomic_mass_numbers[1], half_life[0],half_life[1],
                             gamma_info[0], gamma_info[1]]


        info.append(radionuclide_info)

    database = compile_objects(info)

    return(database)


def isotope_peaks(energies):
    """
    Input a list of peak energies.
    """
    results = []
    for val in energies:
        results.append(main(val))
    return(results)
