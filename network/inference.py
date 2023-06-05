import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

MODEL = "models/test_model.h5"


def make_prediction(lk_df, permutation):
    """
        Make a prediction for a given time sequence and given permutation.
        The last row of the input data is adjusted to use the values of the permutation.

        @param lk_df:
            Type:  Pandas DataFrame
            Shape: ?x24 (Rows x Columns) | variable number of rows | fixed number of columns:
            ['confirmed', 'deaths', 'recovered', 'vaccines', 'people_vaccinated','people_fully_vaccinated',
            'school_closing', 'workplace_closing', 'cancel_events', 'gatherings_restrictions', 'transport_closing',
            'stay_home_restrictions', 'internal_movement_restrictions', 'international_movement_restrictions',
            'information_campaigns', 'testing_policy', 'contact_tracing', 'facial_coverings','vaccination_policy',
            'elderly_people_protection', 'population', 'cfr', 'cases_per_population', 'incidence']

        @param permutation:
            Type: Pandas DataFrame
            Shape: 1x14 (Rows x Columns)

            All columns that should be taken from the original data (from lk_data) have the value -1.

        @return
            type:  numpy ndarray
            shape: 6

    """
    assert lk_df.shape[1] == 24, "Provided Dataframe does not contain the necessary column count"
    assert permutation.shape == (1, 14), "The number of permutation does not match the number of covid measures"

    last_row = lk_df.iloc[-1]

    # insert permutation values
    for c in permutation.columns:
        col_val = permutation[c].values[0]
        if col_val != -1:
            last_row[c] = col_val

    lk_df.iloc[-1] = last_row

    input_scaler = MinMaxScaler(feature_range=(0, 1))
    output_scaler = MinMaxScaler(feature_range=(0, 1))  # TODO: richtige Min und Max werte
    output_scaler.fit(lk_df.to_numpy()[:, -1].reshape(lk_df.shape[0], 1))

    lk_data = lk_df.to_numpy()[:, :-1]
    lk_data_scaled = input_scaler.fit_transform(lk_data)
    lk_data_scaled = np.expand_dims(lk_data_scaled, axis=0)

    predict_model = tf.keras.models.load_model(MODEL, compile=True)
    # predict_model.compile(optimizer='adam', loss='mse')

    prediction_sequence = predict_model.predict(lk_data_scaled)
    prediction = np.squeeze(prediction_sequence, axis=0)
    prediction = output_scaler.inverse_transform(prediction)[:, 0]
    return prediction


def get_test_data():
    data_csv = pd.read_csv('../data/clean/df_weekly_incidence.csv')
    lk_data_full = data_csv[data_csv.administrative_area_level_3 == "LK Ahrweiler"]
    lk_data_frame = lk_data_full.loc[(lk_data_full.year == 2020) & (lk_data_full.week >= 20) & (lk_data_full.week < 51)]
    lk_data_frame = lk_data_frame[
        ['confirmed', 'deaths', 'recovered', 'vaccines', 'people_vaccinated', 'people_fully_vaccinated',
         'school_closing', 'workplace_closing',
         'cancel_events', 'gatherings_restrictions', 'transport_closing', 'stay_home_restrictions',
         'internal_movement_restrictions',
         'international_movement_restrictions', 'information_campaigns', 'testing_policy', 'contact_tracing',
         'facial_coverings', 'vaccination_policy',
         'elderly_people_protection', 'population', 'cfr', 'cases_per_population', 'incidence']]
    perm = pd.DataFrame(lk_data_frame.iloc[-1][lk_data_frame.columns[6:20]]).T
    select = perm.drop(
        columns=['stay_home_restrictions', 'transport_closing', 'cancel_events', 'gatherings_restrictions'])
    perm[select.columns] = -1

    return lk_data_frame, perm


if __name__ == "__main__":
    lk_df, permutation = get_test_data()
    make_prediction(lk_df, permutation)
