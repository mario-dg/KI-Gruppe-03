import numpy as np
import tensorflow as tf

from utils import get_test_data
from sklearn.preprocessing import MinMaxScaler


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
    # TODO: richtige Min und Max werte (Sicher?, macht MinMaxScaler das nicht schon automatisch ~Mario)
    output_scaler = MinMaxScaler(feature_range=(0, 1))
    output_scaler.fit(lk_df.to_numpy()[:, -1].reshape(lk_df.shape[0], 1))

    lk_data = lk_df.to_numpy()[:, :-1]
    lk_data_scaled = input_scaler.fit_transform(lk_data)
    lk_data_scaled = np.expand_dims(lk_data_scaled, axis=0)

    predict_model = tf.keras.models.load_model(MODEL, compile=True)

    prediction_sequence = predict_model.predict(lk_data_scaled)
    prediction = np.squeeze(prediction_sequence, axis=0)
    prediction = output_scaler.inverse_transform(prediction)[:, 0]
    return prediction


if __name__ == "__main__":
    lk_df, permutation = get_test_data()
    make_prediction(lk_df, permutation)
