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
2. Wie wirken sich verschiedene Maßnahmenkombinationen auf die [Zielmetrik] (Hospilitierungsrate) aus?

### Motivation

- Hilfsmittel zur Bekämpfung weiterer Epedemien/Pademien und Erkrakungswellen, die in Zukunft verhäuft auftreten werden.

### Methodik

~~Die Fragestellungen sollen mittels des random forests Verfahren beantwortet werden.~~

Es soll eine Anwendung entwickelt werden, die basierend auf einer Zeitreihentabelle als variable Eingabe eine Vorhersage
zur Entwicklung der Zielmetrik bei verschiedenen Maßnahmenkombinationen für einen spezifischen Landkreis in Deutschland
trifft. Die Anwendung zielt darauf ab, die Ausgabe des neuronalen Netzwerks gegebenenfalls automatisch zu
interpretieren. Dies ermöglicht eine präzise Bewertung der Auswirkungen verschiedener Maßnahmen auf die Zielmetrik und
unterstützt Entscheidungsträger bei der Planung und Umsetzung effektiver Strategien zur Eingrenzung von
Covid-19-ähnlichen Erkrankungen.

#### Front-End

Die Anwendung wir in einem einfachen Jupyter Notebook realisiert. Dort soll die Eingabe und Ausgabe erfolgen.

#### Modell

Das Modell zur Vorhersage der Entwicklung der Zielmetrik wird mithilfe eines LSTM (Long Short-Term Memory) neuronalen
Netzwerks umgesetzt. Das LSTM-Netzwerk ist dafür bekannt, zeitliche Abhängigkeiten in den Daten zu erfassen und kann
daher geeignet sein, die Entwicklung der Zielmetrik im Zusammenhang mit verschiedenen sinnvollen Maßnahmenkombinationen
zu analysieren.

Das Modell wird darauf trainiert, die Auswirkungen der verschiedenen Maßnahmenpermutationen auf die Zielmetrik zu
simulieren und dabei den besten Verlauf zu identifizieren.

#### Zielmetrik

Als zu minimierende Zielmetrik dient die Hospitalisierungsrate auf Landkreisebene.
Diese Metrik gibt Auskunft über den Anteil der COVID-19-Fälle, die eine Krankenhauseinweisung erfordern.
_(Wird ggf. noch angepasst.)_

### Daten

- Deutschlanddatensatz: https://covid19datahub.io/articles/data.html
    - Verwendet in Paper: https://www.nature.com/articles/s41597-022-01797-2
- _Weitere Quelle für Bevölerkungsdichte & -größen_

Die Trainingsdaten sollen so aufbereitet werden, dass die Zielmetrikwerte auf Landkreisebene tägliche verfügbar sind.
Fehlenden Werte sollen durch interpolation ersetzt werden.

### Zielgruppen

- Gesundheitsämter
    - RKI
    - (Bernhard-Nocht-Institut für Tropenmedizin)

## Verwendung

Die Benutzeroberfläche kann mit folgendem Befehl gestartet werden:

```
python main.py
```

## Projektplan

<table class="tg" style="width: 793px;">
<thead>
<tr style="height: 23px;">
<th class="tg-66je" style="height: 23px; width: 30.828125px;">KW</th>
<th class="tg-66je" style="height: 23px; width: 182.171875px;">Meilenstein</th>
<th class="tg-66je" style="height: 23px; width: 428px;">Actions</th>
<th class="tg-66je" style="height: 23px; width: 134px;">Bearbeiter</th>
<th class="tg-66je" style="height: 23px; width: 14px;">Issue</th>
</tr>
</thead>
<tbody>
<tr style="height: 143px;">
<td class="tg-0pky" style="height: 143px; width: 30.828125px;">18</td>
<td class="tg-0pky" style="height: 143px; width: 182.171875px;">Projektkonzept</td>
<td class="tg-0pky" style="height: 143px; width: 428px;">Kl&auml;rung:<br />- Fragestellung<br />- Zielgruppe<br />- Motivation<br />- Daten<br />- Rollen<br />- Methodik</td>
<td class="tg-0pky" style="height: 143px; width: 134px;">Alle</td>
<td class="tg-0pky" style="height: 143px; width: 14px;">&nbsp;</td>
</tr>
<tr style="height: 23px;">
<td class="tg-0pky" style="height: 112px; width: 30.828125px;" rowspan="4">19</td>
<td class="tg-de2y" style="height: 46px; width: 182.171875px;" rowspan="2">Projektplan</td>
<td class="tg-de2y" style="height: 23px; width: 428px;">Projektplanerstellung im Git-Repo</td>
<td class="tg-de2y" style="height: 23px; width: 134px;">Kjell, Herberto</td>
<td class="tg-de2y" style="height: 23px; width: 14px;">&nbsp;</td>
</tr>
<tr style="height: 23px;">
<td class="tg-de2y" style="height: 23px; width: 428px;"><span style="font-weight: 400; font-style: normal; text-decoration: none;">ML-Canvas recherche</span></td>
<td class="tg-de2y" style="height: 23px; width: 134px;">Mario</td>
<td class="tg-de2y" style="height: 23px; width: 14px;">&nbsp;</td>
</tr>
<tr style="height: 43px;">
<td class="tg-de2y" style="height: 66px; width: 182.171875px;" rowspan="2">Explorative Datenanalyse</td>
<td class="tg-de2y" style="height: 43px; width: 428px;">Explorative Datenanalyse der Deutschland Covid Daten</td>
<td class="tg-de2y" style="height: 43px; width: 134px;">Jonathan, Bj&ouml;rn, Steffen</td>
<td class="tg-de2y" style="height: 43px; width: 14px;">&nbsp;</td>
</tr>
<tr style="height: 23px;">
<td class="tg-de2y" style="height: 23px; width: 428px;">Ges&auml;uberte extra Datens&auml;tze</td>
<td class="tg-de2y" style="height: 23px; width: 134px;">Thomas, Timon</td>
<td class="tg-de2y" style="height: 23px; width: 14px;">&nbsp;</td>
</tr>
<tr style="height: 23px;">
<td class="tg-0pky" style="height: 69px; width: 30.828125px;" rowspan="3">20</td>
<td class="tg-de2y" style="height: 23px; width: 182.171875px;">Zielmetrik</td>
<td class="tg-de2y" style="height: 23px; width: 428px;">
<p>- Eignet sich die Hospitalisierungsrate als Zielmetrik?</p>
<p>- Welche eignet sich besser?</p>
<p>- Daten aufbereiten (Auf Landkreisebene, t&auml;glich)&nbsp;</p>
</td>
<td class="tg-de2y" style="height: 23px; width: 134px;">&nbsp;Bj&ouml;rn, Timon</td>
<td class="tg-de2y" style="height: 23px; width: 14px;"><a href="https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27942255">https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27942255</a>&nbsp;</td>
</tr>
<tr style="height: 23px;">
<td class="tg-de2y" style="height: 23px; width: 182.171875px;">Zielvorstellung des Endproduktes</td>
<td class="tg-de2y" style="height: 23px; width: 428px;">
<p>- Wie k&ouml;nnte&nbsp;das Frontend aussehen? Eingabe/Ausgabe?</p>
<p>- Recherche zu Einbindung in JupyterNotebook (welche m&ouml;glichkeiten gibt es?)</p>
<p>- Wie k&ouml;nnte eine automatische Interpretation/Auswertung funktionieren?</p>
</td>
<td class="tg-de2y" style="height: 23px; width: 134px;">Herberto, Steffen&nbsp;</td>
<td class="tg-de2y" style="height: 23px; width: 14px;"><a href="https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27941797">https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27941797</a>&nbsp;</td>
</tr>
<tr style="height: 23px;">
<td class="tg-de2y" style="height: 23px; width: 182.171875px;">&nbsp;</td>
<td class="tg-de2y" style="height: 23px; width: 428px;">
<p>Projektupdate</p>
</td>
<td class="tg-de2y" style="height: 23px; width: 134px;">Herberto, Kjell</td>
<td class="tg-de2y" style="height: 23px; width: 14px;"><a href="https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27942794">https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27942794</a>&nbsp;</td>
</tr>
<tr style="height: 43px;">
<td class="tg-0lax" style="height: 172.5px; width: 30.828125px;" rowspan="4">21</td>
<td class="tg-de2y" style="height: 86.5px; width: 182.171875px;" rowspan="2">Funktionsf&auml;higer Prototyp</td>
<td class="tg-de2y" style="height: 43px; width: 428px;">Training und Verbesserung des&nbsp;LSTM Modells</td>
<td class="tg-de2y" style="height: 43px; width: 134px;">&nbsp;Mario, Thomas</td>
<td class="tg-de2y" style="height: 43px; width: 14px;"><a href="https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27941964">https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27941964</a>&nbsp;</td>
</tr>
<tr style="height: 43.5px;">
<td class="tg-de2y" style="height: 43.5px; width: 428px;">Front-End</td>
<td class="tg-de2y" style="height: 43.5px; width: 134px;">Herberto, Timon</td>
<td class="tg-de2y" style="height: 43.5px; width: 14px;">&nbsp;</td>
</tr>
<tr style="height: 43px;">
<td class="tg-de2y" style="height: 43px; width: 182.171875px;">EDA</td>
<td class="tg-de2y" style="height: 43px; width: 428px;">Auswertung der Vergangenheit</td>
<td class="tg-de2y" style="height: 43px; width: 134px;">Jonathan, Kjell</td>
<td class="tg-de2y" style="height: 43px; width: 14px;"><a href="https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27942676">https://github.com/users/mario-dg/projects/1/views/1?pane=issue&amp;itemId=27942676</a></td>
</tr>
<tr style="height: 43px;">
<td class="tg-de2y" style="height: 43px; width: 182.171875px;">&nbsp;</td>
<td class="tg-de2y" style="height: 43px; width: 428px;">Projektupdate</td>
<td class="tg-de2y" style="height: 43px; width: 134px;">Herberto, Kjell</td>
<td class="tg-de2y" style="height: 43px; width: 14px;">&nbsp;</td>
</tr>
<tr style="height: 23px;">
<td class="tg-0lax" style="height: 23px; width: 30.828125px;">22</td>
<td class="tg-de2y" style="height: 23px; width: 182.171875px;">Ergebnisanalyse</td>
<td class="tg-de2y" style="height: 23px; width: 428px;">Auswertungerstellung</td>
<td class="tg-de2y" style="height: 23px; width: 134px;">&nbsp;</td>
<td class="tg-de2y" style="height: 23px; width: 14px;">&nbsp;</td>
</tr>
<tr style="height: 23px;">
<td class="tg-0lax" style="height: 23px; width: 30.828125px;">23</td>
<td class="tg-de2y" style="height: 23px; width: 182.171875px;">Finale Pr&auml;sentation</td>
<td class="tg-de2y" style="height: 23px; width: 428px;">Foliensatzerstellung</td>
<td class="tg-de2y" style="height: 23px; width: 134px;">&nbsp;</td>
<td class="tg-de2y" style="height: 23px; width: 14px;">&nbsp;</td>
</tr>
</tbody>
</table>
