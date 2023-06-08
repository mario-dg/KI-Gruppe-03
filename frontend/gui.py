


import os
import gradio as gr
import pandas as pd
from datetime import datetime
from .inference import get_permutations, run_permutations, compare_integrals, interpret_permutation_results, make_prediction as make_prediction_model
import csv

import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import matplotlib.pyplot as plt
# Plots



# Dummy Model
class LSTMModel:
    def __init__(self):
        pass

  


class GUI():

    def __init__(self):
        
        self.df = pd.read_csv("data/clean/df_weekly_incidence.csv")
        self.landkreise = self.df['administrative_area_level_3'].unique().tolist()
        self.run_permutations_var = False
        self.run_single_var = False

        self.group_choices = ["Schließung der Schulen",
                            "Schließung der Arbeitsplätze",
                            "Events verbieten","Versammlungsrestriktionen",
                            "Schließung des Verkehrs",
                            "Beschränkungen des Zuhausebleibens",
                            "Bewegungseinschränkungen (intern)",
                            "Bewegungseinschränkungen (international)",
                            "Informationskampagnen","Test Richtlinien",
                            "Kontaktverfolgung","Gesichtsbedeckung",
                            "Impfrichtlinien", "Schutz älterer Menschen"]

        self.mapped_values = [
                    'school_closing',
                    'workplace_closing',
                    'cancel_events',
                    'gatherings_restrictions',
                    'transport_closing',
                    'stay_home_restrictions',
                    'internal_movement_restrictions',
                    'international_movement_restrictions',
                    'information_campaigns',
                    'testing_policy',
                    'contact_tracing',
                    'facial_coverings',
                    'vaccination_policy',
                    'elderly_people_protection'
                ]


    def compute_graph(self,df_to_graph: pd.DataFrame):
        if df_to_graph.empty:
            return None
        fig, ax = plt.subplots()
        x1 = df_to_graph['year'].astype(str) + '-W' + df_to_graph['week'].astype(str)
        y1 = df_to_graph['incidence'].reset_index(drop=True)

        ax.plot(x1, y1, label='Inzidenz Entwicklung in {}'.format(df_to_graph['administrative_area_level_3'].iloc[0]))
        ax.set_xlabel('Zeit')
        ax.set_ylabel('Inzidenz')
        ax.set_title('Inzidenzverlauf')
        ax.set_xticks(np.arange(len(x1)))
        ax.set_xticklabels(x1, rotation=45)
        ax.legend()
        ax.grid("on")
        return fig

    def compute_diff_graphs(self,actual_course: pd.DataFrame, alternate_course: pd.DataFrame):
        fig, ax = plt.subplots()

        x1 = actual_course['year'].astype(str) + '-W' + actual_course['week'].astype(str)
        x2 = alternate_course['year'].astype(str) + '-W' + alternate_course['week'].astype(str)
        y1 = actual_course['incidence'].reset_index(drop=True)
        y2 = alternate_course['incidence'].reset_index(drop=True)

        ax.plot(x1, y1, label='Reale Entwicklung')
        ax.plot(x2, y2, label='Alternative Entwicklung')
        ax.set_xlabel('Zeit')
        ax.set_ylabel('Inzidenz')
        ax.set_title('Inzidenzverlauf')
        ax.set_xticks(range(len(x1)))
        ax.grid("on")
        ax.set_xticklabels(x1, rotation=45)

        ax.fill_between(x1, y1, y2, color='green', alpha=0.5)
        ax.legend()
        return fig

    def compute_integral(self,original_graph: pd.DataFrame, alternative_graph: pd.DataFrame):
        """
        Compute integral
        :param original_graph: df of the original course
        :param alternative_graph:df of the alternative course
        :return: diff integral between both scenario
        High positive values means: alternative course is better
        High negative values means: original course is better
        """
        incidence_one = original_graph['incidence']
        incidence_two = alternative_graph['incidence']
        return np.trapz(incidence_one - incidence_two)


     # def predict_permutation(self, results, permutations, plt):
    def predict_permutation(self, final_perms, plt):
        csv_file_path = "../test_result.csv"
        file_description = self.get_positive_value_descriptions(csv_file_path)

        prediction = [file_description, plt]
        return prediction

    def predict(self, df_district, df_prediction):
        prediction = [self.compute_graph(df_district), self.compute_graph(df_prediction), self.compute_diff_graphs(df_district, df_prediction)]
        return prediction

    def current_measures(self):
        aktuelle_Maßnahmen = ["face_mask", "school_closing", "clubs_closing"]
        return aktuelle_Maßnahmen



    def create_suggestion_text(results, permutations):
            return results + permutations

    def make_prediction(self,data): # TODO Validierung, dass ein LK gewählt wurde
        try:
            date = datetime.strptime(data[self.in_inzidenz_bisher_tb_start], "%Y-%m-%d")
            if date < datetime(2019, 1, 1) or date > datetime(2022, 12, 31):
                raise ValueError("Date out of range")
        except ValueError:
            return "Invalid date format or range"
        
        landkreis = self.df.loc[self.df['administrative_area_level_3'] == str(data[self.in_landkreis_tb])]

        date_object_start = datetime.strptime(data[self.in_inzidenz_bisher_tb_start], "%Y-%m-%d")
        year_start, week_start, _ = date_object_start.isocalendar()
        if year_start != date_object_start.year:
            week_start -= 1

        date_object_end = datetime.strptime(data[self.in_inzidenz_bisher_tb_ende], "%Y-%m-%d")
        year_end, week_end, _ = date_object_end.isocalendar()
        if year_end != date_object_end.year:
            week_end -= 1

        filtered_df = landkreis[(landkreis['year'] == year_start) & (landkreis['week'] >= week_start) |
                    (self.df['year'] > year_start) & (self.df['year'] < year_end) |
                    (self.df['year'] == year_end) & (self.df['week'] <= week_end)]
        
        week_end = (week_end + 6) % 52 if week_end + 6 > 52 else week_end + 6
        year_end = year_end + 1 if week_end < 6 else year_end

        filtered_df_validation = landkreis[(landkreis['year'] == year_start) & (landkreis['week'] >= week_start) |
                    (self.df['year'] > year_start) & (self.df['year'] < year_end) |
                    (self.df['year'] == year_end) & (self.df['week'] <= week_end)]

        filtered_df_model = filtered_df[['confirmed', 'deaths', 'recovered', 'vaccines', 'people_vaccinated','people_fully_vaccinated', 'school_closing', 'workplace_closing',
            'cancel_events', 'gatherings_restrictions', 'transport_closing', 'stay_home_restrictions', 'internal_movement_restrictions',
            'international_movement_restrictions', 'information_campaigns', 'testing_policy', 'contact_tracing', 'facial_coverings','vaccination_policy',
            'elderly_people_protection', 'population', 'cfr', 'cases_per_population', 'incidence']]

        if self.run_single_var:
            permutation = pd.DataFrame([data[self.school_close_intensity],data[self.workplace_close_intensity], data[self.cancel_events_intensity], data[self.gatherings_restrictions_intensity], data[self.transport_closing_intensity], \
                            data[self.stay_home_restrictions_intensity], data[self.internal_movements_restrictions_intensity], data[self.international_movements_restrictions_intensity], data[self.information_campgaings_intensity], \
                            data[self.testing_policy_intensity], data[self.contact_tracing_intensity], data[self.facial_coverings_intensity], data[self.vaccination_policy_intensity], data[self.elderly_people_protection_intensity]])
            permutation = permutation.T
            permutation.columns = self.mapped_values

            prediction_model = make_prediction_model(filtered_df_model, permutation)
            filtered_df_prediction = pd.DataFrame({'incidence': prediction_model})

            new_rows = pd.DataFrame({
                'incidence': filtered_df_prediction['incidence'].values
            })

            last_week = filtered_df['week'].iloc[-1]
            last_year = filtered_df['year'].iloc[-1]

            new_rows['new_week'] = [(last_week + i) % 52 + 1 for i in range(len(new_rows))]
            new_rows['new_year'] = [last_year + ((last_week + i) // 52) for i in range(len(new_rows))]

            last_row = filtered_df.iloc[-1]
            for column in filtered_df.columns:
                if column not in ['incidence', 'week', 'year']:
                    new_rows[column] = last_row[column]
            new_rows = new_rows.rename(columns={'new_week': 'week', 'new_year': 'year'})
            concatenated_df = pd.concat([filtered_df, new_rows], ignore_index=True)
            prediction = self.predict(filtered_df_validation, concatenated_df)
        if self.run_permutations_var:
            # print(data[self.checkbox_self.group_choices])

            mapping = dict(zip(self.group_choices, self.mapped_values))
            values_to_map = data[self.checkbox_group_choices]
            mapped_results = [mapping[value] for value in values_to_map]

            # print(mapped_results)

            results, permutations = run_permutations(filtered_df_model, mapped_results)
            results = np.asarray(results)

            transposed_data = np.transpose(results[0:5, :])

            plt.plot(transposed_data[0, :], label='Top 1 ')
            plt.plot(transposed_data[1, :], label='Top 2')
            plt.plot(transposed_data[2, :], label='Top 3')
            plt.plot(transposed_data[3, :], label='Top 4')
            plt.plot(transposed_data[4, :], label='Top 5')

            plt.xlabel('Zeit')
            plt.ylabel('Inzidenz')
            plt.title('Inzidenzverlauf')
            plt.grid('on')
            plt.legend()

            final_perms = compare_integrals(results, permutations)
            for perm in final_perms:
                print(perm)
            interpret_permutation_results(final_perms)
            prediction = self.predict_permutation(final_perms, plt)

        # TODO Else fehlermeldung

        return prediction

    

    def get_positive_value_descriptions(self,file_path):
        file_description = ""
        
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            data = list(reader)

            headers = data[0][1:]

            for row in data[1:]:
                values = row[1:]
                solution_number = row[0]

                file_description += f"Variante {solution_number}:\n"

                for header, value in zip(headers, values):
                    value = int(value)
                    if value > -1:
                        file_description += f"{header.replace('_', ' ').title()}: {value}\n"

                file_description += "\n"

        return file_description


    # def get_current_measures(self):
    #     model = LSTMModel()
    #     curr_measures = model.current_measures()
    #     return curr_measures

    def validate_checkbox_choices_len(self,data):
        if len(data) < 4:
            return {self.error_box: gr.update(value="Wählen Sie genau 4 Maßnahmen!", visible=True),
                    self.submit_btn_permutation: gr.update(visible=False)}
        elif len(data) == 4:
            return {self.error_box: gr.update(visible=False),
                    self.submit_btn_permutation: gr.update(visible=True)}
        else:
            return {self.error_box: gr.update(visible=False),
                    self.submit_btn_permutation: gr.update(visible=False)}

    def mode_switch(self, mode):
        if "Szenarienvorhersage" in mode and "Maßnahmenempfehlung" in mode:
            self.run_permutations_var = False
            self.run_single_var = False
            return {self.maßnahmen_abfrage1_col: gr.update(visible=False),
                    self.maßnahmen_abfrage2_col: gr.update(visible=False),
                    self.submit_btn_single: gr.update(visible=False),
                    self.submit_btn_permutation: gr.update(visible=False),
                    self.plots_single: gr.update(visible=False),
                    self.plots_permutation: gr.update(visible=False),
                    self.out_prognose_tb: gr.update(visible=False)
                    }
        elif "Szenarienvorhersage" in mode:
            self.run_single_var = True
            return {self.maßnahmen_abfrage1_col: gr.update(visible=True),
                    self.maßnahmen_abfrage2_col: gr.update(visible=False),
                    self.submit_btn_single: gr.update(visible=True),
                    self.submit_btn_permutation: gr.update(visible=False),
                    self.plots_single: gr.update(visible=True),
                    self.plots_permutation: gr.update(visible=False),
                    self.out_prognose_tb: gr.update(visible=False)
                    }
        elif "Maßnahmenempfehlung" in mode:
            self.run_permutations_var = True
            return {self.maßnahmen_abfrage1_col: gr.update(visible=False),
                    self.maßnahmen_abfrage2_col: gr.update(visible=True),
                    self.submit_btn_single: gr.update(visible=False),
                    self.submit_btn_permutation: gr.update(visible=True),
                    self.plots_single: gr.update(visible=False),
                    self.plots_permutation: gr.update(visible=True),
                    self.out_prognose_tb: gr.update(visible=True)
                    }
        else:
            self.run_permutations_var = False
            self.run_single_var = False
            return {self.maßnahmen_abfrage1_col: gr.update(visible=False),
                    self.maßnahmen_abfrage2_col: gr.update(visible=False),
                    self.submit_btn_single: gr.update(visible=False),
                    self.submit_btn_permutation: gr.update(visible=False),
                    self.plots_single: gr.update(visible=False),
                    self.plots_permutation: gr.update(visible=False),
                    self.out_prognose_tb: gr.update(visible=False)
                    }


    #self.school_close_intensity, self.workplace_close_intensity, self.cancel_events_intensity, self.gatherings_restrictions_intensity, self.transport_closing_intensity, \
    #self.stay_home_restrictions_intensity, self.internal_movements_restrictions_intensity, self.international_movements_restrictions_intensity, self.information_campgaings_intensity, \
    #self.testing_policy_intensity, self.contact_tracing_intensity, self.facial_coverings_intensity, self.vaccination_policy_intensity, self.elderly_people_protection_intensity

    #
    def use_preset(self,presets_dropdown):
        selected_preset = presets_dropdown
        changes = []
        if selected_preset == "Szenario 1":        
            changes.extend([gr.Slider.update(value=0) for _ in range(14)])
            changes.extend([
                    gr.Textbox.update(value="2020-03-09"),
                    gr.Textbox.update(value="2021-01-06"),
                    gr.Dropdown.update(value="SK Hamburg"),
                    gr.CheckboxGroup.update(value="Szenarienvorhersage")
                        ])

        if selected_preset == "Szenario 2":        
            changes.extend([
                gr.Slider.update(value=2),
                gr.Slider.update(value=1),
                gr.Slider.update(value=2),
                gr.Slider.update(value=4),
                gr.Slider.update(value=0),
                gr.Slider.update(value=3),
                gr.Slider.update(value=0),
                gr.Slider.update(value=0),
                gr.Slider.update(value=0),
                gr.Slider.update(value=0),
                gr.Slider.update(value=0),
                gr.Slider.update(value=4),
                gr.Slider.update(value=0),
                gr.Slider.update(value=0),
                ])
            changes.extend([
                    gr.Textbox.update(value="2021-08-09"),
                    gr.Textbox.update(value="2022-01-06"),
                    gr.Dropdown.update(value="SK Hamburg"),
                    gr.CheckboxGroup.update(value="Szenarienvorhersage")
                ])

        return changes

    def start(self):

        with gr.Blocks() as demo:
            with gr.Column() as presets:
                with gr.Row():
                    self.presets_dropdown = gr.Dropdown([f"Szenario {i}" for i in range(1,3)], label="Beispiel Szenarien")
            gr.Markdown(
                """
                # Vorhersage für Ihren Landkreis
                Geben Sie den Namen des self.landkreises ein, um die Vorhersage zu erhalten.
                """
            )
            with gr.Column():
                
                with gr.Row():
                    self.in_landkreis_tb = gr.Dropdown(self.landkreise, label="Landkreis")

                gr.Markdown(
                """
                # Auswahl zwischen zwei Modi:
                ##  1. Szenarienvorhersage
                ### Vergleich der Szenarien zwischen Vorhersage und tatsächliche Inzidenz. Die Auswahl enthält folgende Informationen:
                1. Maßnahme
                2. Intensität der Maßnahme
                3. Beschreibung der Intensität

                ## 2. Maßnahmenempfehlung
                ###  Angabe von Maßnahmenempfehlungen für einen bestimmten Zeitraum unter Berücksichtigung von genau 4 Maßnahmen
                """
                )
            
            with gr.Column() as mode_decide:
                self.checkbox_mode_choices = gr.CheckboxGroup(["Szenarienvorhersage", "Maßnahmenempfehlung"],
                                                        label="Modi",
                                                        info="Wählen Sie einen von beiden Modi aus...")
            # Mode 1
            with gr.Column(visible=False) as self.maßnahmen_abfrage1_col:
                # school_closing
                with gr.Tab("Schließung der Schulen"):
                    with gr.Row():
                        self.school_close_intensity = gr.Slider(0,3, label="Intensität der Maßnahme",step=1) 
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Schließung der Schulen

                        0 - keine Maßnahmen

                        1 - Maßnahmenempfehlung der Schließung oder Öffnung aller Schulen mit Änderungen, die zu signifikanten Unterschieden im Vergleich zum Nicht-Covid-19-Betrieb führen
                    
                        2 - Schließung vorschreiben (nur einige Stufen oder Kategorien, z. B. nur Gymnasien oder nur öffentliche Schulen)
                    
                        3 - Schließung aller Stufen erforderlich
                        """
                        )
                # workplace_closing
                with gr.Tab("Schließung der Arbeitsplätze"):
                    with gr.Row():
                        self.workplace_close_intensity = gr.Slider(0,3, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Schließung der Arbeitsplätze

                        0 - keine Maßnahmen

                        1 - Maßnahmenempfehlung der Schließung (oder Maßnahmenempfehlung der Heimarbeit) oder Öffnung aller Betriebe mit Änderungen, die zu erheblichen Unterschieden im Vergleich zum Nicht-Covid-19-Betrieb führen
                    
                        2 - Schließung (oder Heimarbeit) für einige Sektoren oder Kategorien von Arbeitnehmern vorschreiben
                    
                        3 - Schließung (oder Arbeit von zu Hause aus) für alle Arbeitsplätze, die nicht unbedingt notwendig sind (z. B. Lebensmittelgeschäfte, Ärzte)
                        """
                        )

                # cancel_events
                with gr.Tab("Events verbieten"):
                    with gr.Row():
                        self.cancel_events_intensity = gr.Slider(0,2, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Events verbieten

                        0 - keine Maßnahmen

                        1 - Annullierung empfehlen

                        2 - Annullierung erforderlich
                        """
                    )
                
                # gatherings_restrictions
                with gr.Tab("Versammlungsrestriktionen"):
                    with gr.Row():
                        self.gatherings_restrictions_intensity = gr.Slider(0,4, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Versammlungsrestriktionen

                        0 - keine Einschränkungen

                        1 - Beschränkungen für sehr große Versammlungen (die Grenze liegt bei über 1000 Personen)
                        
                        2 - Beschränkungen für Versammlungen zwischen 101-1000 Personen
                        
                        3 - Beschränkungen für Versammlungen zwischen 11-100 Personen
                        
                        4 - Beschränkungen für Versammlungen von 10 Personen oder weniger
                        """
                    )

                # transport_closing
                with gr.Tab("Schließung des Verkehrs"):
                    with gr.Row():
                        self.transport_closing_intensity = gr.Slider(0,2, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Schließung des Verkehrs

                        0 - keine Maßnahmen

                        1 - Maßnahmenempfehlung der Schließung (oder erhebliche Reduzierung des Volumens/der Strecke/der verfügbaren Verkehrsmittel)

                        2 - Schließung vorschreiben (oder den meisten Bürgern verbieten, sie zu benutzen)
                        """
                    )

                # stay_home_restrictions
                with gr.Tab("Beschränkungen des Zuhausebleibens"):
                    with gr.Row():
                        self.stay_home_restrictions_intensity = gr.Slider(0,3, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Beschränkungen des Zuhausebleibens

                        0 - keine Maßnahmen

                        1 - Maßnahmenempfehlung, das Haus nicht zu verlassen

                        2 - Verbot, das Haus zu verlassen, mit Ausnahmen für tägliche Bewegung, Lebensmitteleinkäufe und "notwendige" Fahrten
                        
                        3 - Verbot des Verlassens des Hauses mit minimalen Ausnahmen (z. B. einmal pro Woche, oder nur eine Person darf gleichzeitig das Haus verlassen, usw.)
                        """
                    )

                # internal_movements_restrictions
                with gr.Tab("Bewegungseinschränkungen (intern)"):
                    with gr.Row():
                        self.internal_movements_restrictions_intensity = gr.Slider(0,2, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Bewegungseinschränkungen (intern)

                        0 - keine Maßnahmen

                        1 - Maßnahmenempfehlung, nicht zwischen Regionen/Städten zu reisen

                        2 - interne Bewegungseinschränkungen sind vorhanden
                        """
                )
                
                # international_movements_restrictions
                with gr.Tab("Bewegungseinschränkungen (international)"):
                    with gr.Row():
                        self.international_movements_restrictions_intensity = gr.Slider(0,4, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Bewegungseinschränkungen (international)

                        0 - keine Einschränkungen

                        1 - Überprüfung von Ankünften

                        2 - Quarantäne für Ankünfte aus einigen oder allen Regionen

                        3 - Verbot von Ankünften aus einigen Regionen

                        4 - Verbot für alle Regionen oder vollständige Schließung der Grenzen
                        """
                )
                
                # information_campgaings
                with gr.Tab("Informationskampagnen"):
                    with gr.Row():
                        self.information_campgaings_intensity = gr.Slider(0,2, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Informationskampagnen

                        0 - keine öffentliche Informationskampagne zu Covid-19

                        1 - öffentliche Beamte mahnen zur Vorsicht in Bezug auf Covid-19

                        2 - koordinierte öffentliche Informationskampagne (z. B. über traditionelle und soziale Medien)
                        """
                )
                        
                # testing_policy
                with gr.Tab("Test Richtlinien"):
                    with gr.Row():
                        self.testing_policy_intensity = gr.Slider(0,3, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Test Richtlinien

                        0 - keine Testpolitik
                        
                        1 - nur Personen, die a) Symptome aufweisen UND b) bestimmte Kriterien erfüllen (z. B. Mitarbeiter in Schlüsselpositionen, die ins Krankenhaus eingeliefert wurden, die mit einem bekannten Fall in Kontakt gekommen sind, die aus dem Ausland zurückgekehrt sind)
                        
                        2 - Tests für alle, die Covid-19-Symptome aufweisen
                        
                        3 - offene öffentliche Tests (z. B. "Drive-Through"-Tests für asymptomatische Personen)
                        """
                )
                        
                # contact_tracing
                with gr.Tab("Kontaktverfolgung"):
                    with gr.Row():
                        self.contact_tracing_intensity = gr.Slider(0,2, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                        # Beschreibung der Maßnahme: Kontaktverfolgung

                    0 - keine Ermittlung von Kontaktpersonen

                    1 - begrenzte Ermittlung von Kontaktpersonen; nicht bei allen Fällen durchgeführt

                    2 - umfassende Ermittlung von Kontaktpersonen; durchgeführt für alle identifizierten Fälle
                        """
                )
                        
                # facial_coverings
                with gr.Tab("Gesichtsbedeckung"):
                    with gr.Row():
                        self.facial_coverings_intensity = gr.Slider(0,4, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                    # Beschreibung der Maßnahme: Gesichtsbedeckung

                    0 - keine Richtlinie

                    1 - Empfohlen

                    2 - Erforderlich in einigen bestimmten gemeinsamen/öffentlichen Räumen außerhalb der Wohnung, in denen andere Personen anwesend sind, oder in einigen Situationen, in denen eine soziale Distanzierung nicht möglich ist
                    
                    3 - Erforderlich in allen gemeinsamen/öffentlichen Räumen außerhalb des Hauses, in denen andere Personen anwesend sind, oder in allen Situationen, in denen eine soziale Distanzierung nicht möglich ist
                    
                    4 - Außerhalb der Wohnung jederzeit erforderlich, unabhängig vom Ort oder der Anwesenheit anderer Personen
                        """
                )
                
                # vaccination_policy
                with gr.Tab("Impfrichtlinien"):
                    with gr.Row():
                        self.vaccination_policy_intensity = gr.Slider(0,5, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                    # Beschreibung der Maßnahme: Impfrichtlinien

                        0 - Keine Verfügbarkeit
                        
                        1 - Verfügbarkeit für EINE der folgenden Gruppen: Schlüsselkräfte/ klinisch gefährdete Gruppen (nicht ältere Menschen) / ältere Menschen
                        
                        2 - Verfügbarkeit für ZWEI der folgenden Gruppen: Schlüsselpersonal/ klinisch gefährdete Gruppen (nicht ältere Menschen) / ältere Menschen
                        
                        3 - Verfügbarkeit für ALLE der folgenden Bereiche: Schlüsselkräfte/ klinisch gefährdete Gruppen (nicht ältere Menschen) / ältere Menschen
                        
                        4 - Verfügbarkeit für alle drei plus teilweise zusätzliche Verfügbarkeit (Auswahl breiter Gruppen/Alter)
                        
                        5 - Universelle Verfügbarkeit
                        """
                )
                        
                # elderly_people_protection
                with gr.Tab("Schutz älterer Menschen"):
                    with gr.Row():
                        self.elderly_people_protection_intensity = gr.Slider(0,3, label="Intensität der Maßnahme",step=1)
                        gr.Markdown(
                        """
                    # Beschreibung der Maßnahme: Schutz älterer Menschen

                        0 - keine Maßnahmen
                        
                        1 - Empfohlene Isolierungs-, Hygiene- und Besuchsbeschränkungsmaßnahmen in LTCFs und/oder ältere Menschen sollen zu Hause bleiben
                        
                        2 - Geringe Einschränkungen für Isolierung, Hygiene in LTCFs, einige Einschränkungen für externe Besucher und/oder Einschränkungen zum Schutz älterer Menschen zu Hause
                        
                        3 - Weitreichende Beschränkungen für Isolierung und Hygiene in LTCFs, Verbot aller nicht unbedingt erforderlichen externen Besucher und/oder alle älteren Menschen müssen zu Hause bleiben und dürfen das Haus mit minimalen Ausnahmen nicht verlassen und keine externen Besucher empfangen
                        """
                )
            
            #Errorbox for Mode 2
            self.error_box = gr.Textbox(label="Error", visible=False)

            # Mode 2
            with gr.Column(visible=False) as self.maßnahmen_abfrage2_col:
                self.checkbox_group_choices = gr.CheckboxGroup(["Schließung der Schulen",
                                "Schließung der Arbeitsplätze",
                                "Events verbieten","Versammlungsrestriktionen",
                                "Schließung des Verkehrs",
                                "Beschränkungen des Zuhausebleibens",
                                "Bewegungseinschränkungen (intern)",
                                "Bewegungseinschränkungen (international)",
                                "Informationskampagnen","Test Richtlinien",
                                "Kontaktverfolgung","Gesichtsbedeckung",
                                "Impfrichtlinien", "Schutz älterer Menschen"], label="Maßnahmen", info="Wählen Sie exakt 4 Maßnahmen aus...")
            
            # Inteferenz
            self.in_inzidenz_bisher_tb_start = gr.Textbox(label="Pandemie-Daten von ...", placeholder="Format: 2021-01-01")
            self.in_inzidenz_bisher_tb_ende = gr.Textbox(label="bis ...", placeholder="Format: 2021-01-01") 

            # Outputs
            with gr.Column():
                self.out_prognose_tb = gr.Textbox(label="Vorschläge")
                with gr.Column(visible=False) as self.plots_single: # gr.Row alternativ
                    self.out_inzidenz_ahrweiler_plot = gr.Plot(label="Vorhersage")
                    self.out_inzidenz_hamburg_plot = gr.Plot(label="Realität")
                    self.out_inzidenz_integral_plot = gr.Plot(label="Differenz")
                with gr.Row(visible=False) as self.plots_permutation:
                    self.out_inzidenz_permutation_plot = gr.Plot(label="Inzidenzentwicklung")

            self.submit_btn_single = gr.Button("Start", visible=False)
            self.submit_btn_permutation = gr.Button("Start", visible=False)

            # Events
            ## Visibility Mode Changes
            self.checkbox_mode_choices.change(self.mode_switch,inputs=self.checkbox_mode_choices,outputs=[self.maßnahmen_abfrage1_col, self.maßnahmen_abfrage2_col,self.submit_btn_permutation,self.submit_btn_single, self.plots_single, self.plots_permutation,self.out_prognose_tb])
            ## Validation Checkboxes Choices Length
            self.checkbox_group_choices.change(self.validate_checkbox_choices_len, inputs=self.checkbox_group_choices,outputs=[self.error_box, self.submit_btn_permutation])

            self.presets_dropdown.change(self.use_preset,inputs=self.presets_dropdown,outputs=[self.school_close_intensity, self.workplace_close_intensity, self.cancel_events_intensity, self.gatherings_restrictions_intensity, self.transport_closing_intensity, \
                                                        self.stay_home_restrictions_intensity, self.internal_movements_restrictions_intensity, self.international_movements_restrictions_intensity, self.information_campgaings_intensity, \
                                                        self.testing_policy_intensity, self.contact_tracing_intensity, self.facial_coverings_intensity, self.vaccination_policy_intensity, self.elderly_people_protection_intensity,
                                                        self.in_inzidenz_bisher_tb_start, self.in_inzidenz_bisher_tb_ende, self.in_landkreis_tb,self.checkbox_mode_choices
                                                        ])

            self.submit_btn_permutation.click(fn=self.make_prediction, inputs={self.in_landkreis_tb, self.school_close_intensity, self.workplace_close_intensity, self.cancel_events_intensity, self.gatherings_restrictions_intensity, self.transport_closing_intensity, \
                                                        self.stay_home_restrictions_intensity, self.internal_movements_restrictions_intensity, self.international_movements_restrictions_intensity, self.information_campgaings_intensity, \
                                                        self.testing_policy_intensity, self.contact_tracing_intensity, self.facial_coverings_intensity, self.vaccination_policy_intensity, self.elderly_people_protection_intensity, \
                                                        self.in_inzidenz_bisher_tb_start, self.in_inzidenz_bisher_tb_ende, self.checkbox_group_choices}, outputs=[self.out_prognose_tb, self.out_inzidenz_permutation_plot])
            
            self.submit_btn_single.click(fn=self.make_prediction, inputs={self.in_landkreis_tb, self.school_close_intensity, self.workplace_close_intensity, self.cancel_events_intensity, self.gatherings_restrictions_intensity, self.transport_closing_intensity, \
                                                        self.stay_home_restrictions_intensity, self.internal_movements_restrictions_intensity, self.international_movements_restrictions_intensity, self.information_campgaings_intensity, \
                                                        self.testing_policy_intensity, self.contact_tracing_intensity, self.facial_coverings_intensity, self.vaccination_policy_intensity, self.elderly_people_protection_intensity, \
                                                        self.in_inzidenz_bisher_tb_start, self.in_inzidenz_bisher_tb_ende, self.checkbox_group_choices}, outputs=[self.out_inzidenz_hamburg_plot, self.out_inzidenz_ahrweiler_plot, self.out_inzidenz_integral_plot])


        demo.launch()

def gui_main():
    g = GUI()
    g.start()