import pandas as pd


RELEVANT_COLUMNS = ['confirmed', 'deaths', 'recovered', 'vaccines', 'people_vaccinated', 'people_fully_vaccinated',
                    'school_closing', 'workplace_closing',
                    'cancel_events', 'gatherings_restrictions', 'transport_closing', 'stay_home_restrictions',
                    'internal_movement_restrictions',
                    'international_movement_restrictions', 'information_campaigns', 'testing_policy', 'contact_tracing',
                    'facial_coverings', 'vaccination_policy',
                    'elderly_people_protection', 'population', 'cfr', 'cases_per_population', 'incidence']


def get_test_data():
    data_csv = pd.read_csv('../data/clean/df_weekly_incidence.csv')
    lk_data_full = data_csv[data_csv.administrative_area_level_3 == "LK Ahrweiler"]
    lk_data_frame = lk_data_full.loc[(lk_data_full.year == 2020) & (lk_data_full.week >= 20) & (lk_data_full.week < 51)]
    lk_data_frame = lk_data_frame[RELEVANT_COLUMNS]
    perm = pd.DataFrame(lk_data_frame.iloc[-1][lk_data_frame.columns[6:20]]).T
    select = perm.drop(
        columns=['stay_home_restrictions', 'transport_closing', 'cancel_events', 'gatherings_restrictions'])
    perm[select.columns] = -1

    return lk_data_frame, perm
