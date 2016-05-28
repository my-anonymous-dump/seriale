# seriale

[PL]  glupotka do sprawdzania i zarzadzania serialami. Brzydko w Pythonie.
[EN]  dummy script to manage online series - watching, looking up when new is aired, writen ugly way in Py.

## [PL] Wymagania i format pliku / [EN] requirements and file format

[PL]
Wymaga posiadania pliku > ~/WAZNE/seriale/last_seen z przykladowa zawartoscia jak ponizej:
[EN]
Requires file at  > ~/WAZNE/seriale/last_seen with example contents as below:

some_series_name       ; s0XeYZ  ; comments here
some_series_name2      ; s0XeYZ  ; comments here
obrady_sejmu           ; s66e11  ;  hehe
sense8                 ; s01e01  ; [EN] oh, btw - colons should be separated with tabs.
spejson vlog           ; s01e01  ; [PL] i tak, średniki powinny być oddzielone tabulatorem.

## [PL] Jak korzystać / [EN] usage

[PL]
ustaw sobie alias w pliku .bash_aliases np.
ser = "python /home/username/sciezka_do_pliku/seriale.py"

sposób użycia ==> ser KOMENDA ARGUMENTY
KOMENDA to jedno z {list|check|when|update}, najczęściej może być skrócona do jednej literki.
Argument czasem jest opcjonalny :) przeczytaj poniżej.

[EN]
setup handy alias in .bash_aliases like
ser = "python /home/username/script_location/seriale.py"

usage ==> ser CMD ARGUMENTS
CMD is one of {list|check|when|update}, can be shortened to single letter.
ARGUMENTS are sometimes optional, sometimes not :)


[PL] list - wypisuje liste zapisanych seriali. Przyjmuje opcjonalny argument, jesli podany to wypisze tylko linie z pasujacym tekstem.
[EN] list - print what is saved. Accepts optional argument, when provided matches only line containing argument.
```
#show some_seri only
$ ser list some_seri
some_series_name       ; s0XeYZ  ; comments here
some_series_name2      ; s0XeYZ  ; comments here
Saved: 5 

#show all
$ ser list 
some_series_name       ; s0XeYZ  ; comments here
some_series_name2      ; s0XeYZ  ; comments here
obrady_sejmu           ; s66e11  ;  hehe
sense8                 ; s01e01  ; [EN] oh, btw - colons should be separated with tabs.
spejson vlog           ; s01e01  ; [PL] i tak, średniki powinny być oddzielone tabulatorem.
```
[PL] check - sprawdza czy kolejny odcinek jest dostepny na cda. Wymaga argumentu (nazwy, moze byc czesciowa)
[EN] check - checks if next episode is available at cda. Requires argument (name, or partial name)
```
$ ser check obrady
Not found...
$ ser check sens
Last seen: sense8 s01e01 next...s01e02
Looking up... http://cda.pl/info/sense8+s01e02
1st hit:
http://cda.pl/video/xxxxxxxxxxxxxxx
```
[PL] when - sprawdza kiedy bedzie kolejny oddcinek, czy odcinki. Pokazuje tylko wieksze niz ostatnio widziany. 
[EN] when - checks when is next episode. Or episodes actually. Shows only not seen in current month if available.
```
$ ser when sens
Matched: sense8 s01e02
Not this month.
# or 
at 18_5_2016 s07e05
at 24_5_2016 s07e06
at 25_5_2016 s07e07
last day of month 31_5_2016 s07e08
```
[PL] update - wymaga argumentu, aktualizuje ostatnio widziany odcinek. Opcjonalnie drugi argument - liczbe, takze ujemna, pozwala zwiekszyc lub zmniejszyc licznik o te liczbe
[EN] update - requires argument. Matches name, and updates last seen episode, optionally accepts second argument, number (also can be negative) that allows increase/decrease seen counter of this episodes
