# KI-Gruppe-03

## Projektteam

| Name            | Rolle          |
|-----------------|----------------|
| Björn Dittmann  |                |
| Thomas Schaibel |                |
| Timon Rupelt,   |                |
| Herberto Werner |                |
| Mario da Graca  | Projektmanager |
| Steffen Hespe   |                |
| Jonathan Jander |                |
| Kjell Binici    |                |


## Thema
Maßnahmenanalyse zur Eingrenzung der Ausbreitung von Covid-19 ähnlichen Erkrankungen.

### Konkrete Fragestellungen
1. Welche Maßnahmen sind für bestimmte Bevölkerungsgrößen und -dichten am besten geeignet?
2. Wie wirken sich verschiedene Maßnahmenkombinationen auf die Hospilitierungsrate aus?

### Motivation
- Hilfsmittel zur Bekämpfung weiterer Epedemien/Pademien und Erkrakungswellen, die in Zukunft verhäuft auftreten werden

### Methodik
Die Fragestellungen sollen mittels des random forests Verfahren beantwortet werden.

### Daten
- Deutschlanddatensatz: https://covid19datahub.io/articles/data.html
  - Verwendet in Paper: https://www.nature.com/articles/s41597-022-01797-2
- _Weitere Quelle für Bevölerkungsdichte & -größen_

### Zielgruppen
- Gesundheitsämter
  - RKI
  - (Bernhard-Nocht-Institut für Tropenmedizin)



## Projektplan

<table class="tg">
<thead>
  <tr>
    <th class="tg-66je">KW</th>
    <th class="tg-66je">Meilenstein</th>
    <th class="tg-66je">Actions</th>
    <th class="tg-66je">Bearbeiter</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="tg-0pky">18</td>
    <td class="tg-0pky">Projektkonzept</td>
    <td class="tg-0pky">Klärung:<br>- Fragestellung<br>- Zielgruppe<br>- Motivation<br>- Daten<br>- Rollen<br>- Methodik</td>
    <td class="tg-0pky">Alle</td>
  </tr>
  <tr>
    <td class="tg-0pky" rowspan="4">19</td>
    <td class="tg-de2y" rowspan="2">Projektplan</td>
    <td class="tg-de2y">Projektplanerstellung im Git-Repo</td>
    <td class="tg-de2y">Kjell, Herberto</td>
  </tr>
  <tr>
    <td class="tg-de2y"><span style="font-weight:400;font-style:normal;text-decoration:none">ML-Canvas recherche</span></td>
    <td class="tg-de2y">Mario</td>
  </tr>
  <tr>
    <td class="tg-de2y" rowspan="2">Explorative Datenanalyse</td>
    <td class="tg-de2y">Explorative Datenanalyse der Deutschland Covid Daten</td>
    <td class="tg-de2y">Jonathan, Björn, Steffen</td>
  </tr>
  <tr>
    <td class="tg-de2y">Gesäuberte extra Datensätze</td>
    <td class="tg-de2y">Thomas, Timon</td>
  </tr>
  <tr>
    <td class="tg-0pky" rowspan="3">20</td>
    <td class="tg-de2y">Architekturdesign</td>
    <td class="tg-de2y">Architekturdesign</td>
    <td class="tg-de2y"></td>
  </tr>
  <tr>
    <td class="tg-de2y" rowspan="2">Prototyp des random forest</td>
    <td class="tg-de2y">Vereinigung der Datensätze</td>
    <td class="tg-de2y"></td>
  </tr>
  <tr>
    <td class="tg-de2y"><span style="font-weight:400;font-style:normal;text-decoration:none">Aufbau eines ersten Forests</span></td>
    <td class="tg-de2y"></td>
  </tr>
  <tr>
    <td class="tg-0lax">21</td>
    <td class="tg-de2y">Implementierter und trainierter random forest</td>
    <td class="tg-de2y">Training und Verbesserung des random Forests<br>Forent-End/Interface</td>
    <td class="tg-de2y"></td>
  </tr>
  <tr>
    <td class="tg-0lax">22</td>
    <td class="tg-de2y">Ergebnisanalyse</td>
    <td class="tg-de2y">Auswertungerstellung</td>
    <td class="tg-de2y"></td>
  </tr>
  <tr>
    <td class="tg-0lax">23</td>
    <td class="tg-de2y">Finale Präsentation</td>
    <td class="tg-de2y">Foliensatzerstellung</td>
    <td class="tg-de2y"></td>
  </tr>
</tbody>
</table>
