import random

def dodajFiszke(slowo, znaczenie, slownik):
    slownik.update({slowo.lower(): {'znaczenie': znaczenie.lower(), 'levenshtein': 0.0}})
    return slownik

def obliczOdlegloscLevenshteina(slowo1, slowo2):
    m, n = len(slowo1), len(slowo2)
    macierz = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                macierz[i][j] = j
            elif j == 0:
                macierz[i][j] = i
            elif slowo1[i - 1] == slowo2[j - 1]:
                macierz[i][j] = macierz[i - 1][j - 1]
            else:
                macierz[i][j] = 1 + min(macierz[i - 1][j],  # usuwanie
                                        macierz[i][j - 1],  # wstawianie
                                        macierz[i - 1][j - 1])  # zamiana

    return macierz[m][n] / len(slowo1)

def levenshtein_key(item):
    return fiszki[item]['levenshtein']


def wybierzPytanieDoQuizu(fiszki):
    pomieszane_klucze = list(fiszki.keys())
    random.shuffle(pomieszane_klucze)
    return max(pomieszane_klucze, key=levenshtein_key)

print("Wpisanie słowa null zakończy wczytywanie fiszek do słownika.")
fiszki = dict({'hamster': {'znaczenie': 'chomik', 'levenshtein': 0.0},
               'bird': {'znaczenie': 'ptak', 'levenshtein': 0.0},
               'turtle': {'znaczenie': 'żółw', 'levenshtein': 0.0}})

slowo = ""

while slowo != 'null':
    slowo = input("Podaj słowo: ")
    if slowo == "null":
        break
    else:
        znaczenie = input(f"Podaj znaczenie słowa {slowo}: ")
        if znaczenie.lower() in [f['znaczenie'] for f in fiszki.values()]:
            print("To znaczenie już istnieje w słowniku. Podaj następne słowo.")
    dodajFiszke(slowo, znaczenie, fiszki)

print(fiszki)
print("Teraz czas na quiz! Wybiorę losowe słowo, a Twoim zadaniem jest podanie mi poprawnego tłumaczenia. Zaczynamy :D")

licznik_slow = 0
poprawne_odpowiedzi = 0
bledne_odpowiedzi = 0

while True:
    slowo_do_przetlumaczenia = wybierzPytanieDoQuizu(fiszki)
    print(f"Przetłumacz: {slowo_do_przetlumaczenia}")
    odpowiedz = input("Podaj tłumaczenie: ")
    if odpowiedz.lower() == fiszki[slowo_do_przetlumaczenia]['znaczenie']:
        licznik_slow += 1
        poprawne_odpowiedzi += 1
        fiszki[slowo_do_przetlumaczenia]['levenshtein'] = 0.0
        print("Poprawna odpowiedź!")
    else:
        licznik_slow += 1
        bledne_odpowiedzi += 1
        blad = obliczOdlegloscLevenshteina(slowo_do_przetlumaczenia, odpowiedz)
        fiszki[slowo_do_przetlumaczenia]['levenshtein'] = blad
        print(f"Błędna odpowiedź. Wielkość błędu: {blad:.2f}")
    print(f"Odpowiedzi poprawne: {poprawne_odpowiedzi} || Odpowiedzi błędne: {bledne_odpowiedzi}")
    if licznik_slow == 3:
        licznik_slow = 0
        kontynuacja = input("Czy chcesz kontynuować quiz? t/n\n")
        if kontynuacja.lower() == 't':
            pass
        else:
            break