# PolEval2019_INL_PJATK
Cyberbullying detection (NLP) in Python.


Naszym zadaniem było rozwiązanie jednego z zadań z konkursu PolEval 2019 (zadanie 6). W podzadaniu 6-1 mieliśmy wytrenować sieć neuronową, która miałaby rozpoznawać wpisy internetowe (z portalu Twitter), które zawierają szkodliwe informacje (klasa 1) oraz takie, które nimi nie są (klasa 0). Do szkodliwych informacji należą: cyberprzemoc, mowa nienawiści oraz związane z tym koncepcje. Podzadanie 6-2 miało na celu wytrenowanie sieci neuronowej, która powinna mieć możliwość rozróżniać trzy typy wpisów internetowych: nieszkodliwe (klasa 0), cyberprzemoc (klasa 1) oraz mowę nienawiści (klasa 2). Różnica pomiędzy cyberprzemocą, a mową nienawiści jest taka, że mowa nienawiści dotyczy osoby publicznej lub grupy ludzi, natomiast cyberprzemoc dotyczy osoby prywatnej.
Dane, z których korzystaliśmy pobraliśmy poprzez MS Teams, po wcześniejszym umieszczeniu ich na tej platformie przez prowadzącego zajęcia. Do podzadań otrzymaliśmy odpowiednio po dwa pliki tekstowe, które zawierały klasy wpisów oraz ich treści. Przykładowe wpisy wraz z ich klasami:
-	Dla mnie faworytem do tytułu będzie Cracovia. Zobaczymy, czy typ się sprawdzi. (6-1: klasa 0, 6-2: klasa 0)
- @anonymized_account @anonymized_account Brawo ty Daria kibic ma być na dobre i złe (6-1: klasa 0, 6-2: klasa 0)
- @anonymized_account @anonymized_account Super, polski premier składa kwiaty na grobach kolaborantów. Ale doczekaliśmy czasów. (6-1: klasa 0, 6-2: klasa 0)
