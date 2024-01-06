# Automatizēšanas Projekts priekšmeta "Lietojumprogrammatūras automatizēšanas rīki"

Darba autors: Ralfs Aizsils (231RDB026)

## Uzdevuma aprakasts

### Projekta nosacijums:
Noslēguma projekts ir jūsu iespēja izmantot jauniegūtās prasmes, lai izstrādātu pilnvērtīgo programmatūru noteikto uzdevuma risināšanai. Projektā jāizmanto zināšanas, kas ir iegūtas kursa laikā, bet projekta uzdevumu jāģenerē jums pašiem. Mēs gribam, lai Jūs izveidotu sistēmu, kas automatizēs kādu no jūsu ikdienas uzdevumiem.

### Pāš-ģenerētais uzdevums:
Nolasīt PDF dokumentus pa gabaliem un tos atskaņot ar [Google Translate](https://translate.google.com/) brīvi pieejamo atskaņošanas funkciju, ievietojot tekstu (zem 5000 simbolus reizē) mājaslapā un nospiežot atskaņošanas pogu.

Programmai jāstrādā ar saskarni, kurā var nomainīt iestatītjumus un izvēlēties PDF.

## Bibliotēkas

```python
import tkinter # saskarnes izveidošanai
import PyPDF2 # pdf failu nolasīšanai
import selenium # internata pārlūka izmantošanai
import time # ērtām laika pauzēm, "app.after" vietā
```

## Lietošana

> ✏️ Lietošanas aprakstā ir pieņemts, ka Jums ir pamata zināšanas kā darboties ar konsoli, direktorijām un Python

> ⚠️ Programma izmanto Selenium, kam vajag [Google Chrome](https://www.google.com/chrome/) pārlūkprogrammu lai strādātu.

Palaižiet programmu caur konsoli no _main.py_ skripta direktorijas.

```
python main.py
```
Izvēlaties atbilstošo valodu savam tekstam. Sistēma atbalsta latviešu, angļu, krievu valodas un "auto-detect". Auto ir pēc noklusējuma.

Izvēlaties PDF failu, ko vēlaties noklausīties, nospiežot "PDF" pogu un atrodot savu PDF failu.

Klausaties kā Google Translate izlasa visu PDF failu pa lapai. Pārlūks pēctam automātiski aizvērsies un varēs likt nākamo PDF vai atskaņot vēlreiz.

> ⚠️ Ja lapā ir vairāk nekā 5000 simboli, Google Translate nevarēs nolasīt visu lapu. Pilnā MS Word lapā ietilpst 3872 "a" burti, bet 8140 "i" burti (fonts "Calibri",izmērs 11).

> Apstādinot GT atskaņošanu, programma turpinās lasīt nākamo lapu. Šo var lietot kā nejaušu “izlaist” pogu.

## Sistēmas Apraksts

Programma/sistēma izmanto Tkinter bibliotēku saskarnes izveidošanai, lai varētu viegli izvēlēties PDF un pievienot papildus izvēles/iestatījumus (piem., valodas izvēle). 

Lai dabūtu failu, PDF poga izsauc funkciju, kas ar "filedialog.askopenfilename" atver failu meklētāju un ļauj lietotājam izvēlēties PDF.

Kad PDF fails ir izvēlēts, tās "path" tiek izmantots lai to izlasītu ar PyPDF2. Tad mēs inicializējam Selenium un atveram Google Translate mājas lapu (turpmāk GT). GT valoda tik izvēlēta ierakstot valodas izvēlētās valodas kodu mājas lapa URL parametros.

> GT reti izmanto ID un izlasāmie atribūti mainījās pēc pārlūka iestatītās valodas, tādēļ elementu atrašanai tika lietoti CSS izvēlētāji un elementu klases, kad varēja.

Katru reizi, kad GT tiek atvērts ar Selenium, GT prasa lai apstiprina sīkdatņu lietošanu. Programma nospiež pogu, ja atrod, bet ja gadījumā tā nav, programma turpina strādāt.

Programma pēc tam atkārtoti izsauc lasīšanas funkciju katru sekundi, kas ievieto PDF faila lapas saturu GT tulkošanas laukā un (pēc īsas pauzes) nospiež atskaņošanas pogu. Katru reizi, kad funkcija tiek izsaukta, tā pārbauda vai atskaņošanas poga vēl rāda ka tā atskaņo tekstu. Kad vairs neatskaņo, tad funkcija izdzēš tekstu, ieraksta nākamās lapas saturu un atkārto procesu līdz visas lapas tiek izlasītas.

