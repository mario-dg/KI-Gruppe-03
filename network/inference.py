import random
import itertools
import numpy as np
import pandas as pd
import tensorflow as tf

from utils import RELEVANT_COLUMNS, MEASURES_COLUMNS, get_test_data
from sklearn.preprocessing import MinMaxScaler


MODEL = "models/test_model.h5"


def make_permutation_predictions(chosen_features_str):
    """
    Computes all permutations available for the specified set of Covid measurements
    :param chosen_features_str: List of covid measurements to permute (their identical name in the original dataset)
    :return: List of all permutations, in the format needed for the inference function
    """
    assert len(chosen_features_str) == 4, "The number of chosen features has to be 4"
    data = {'measurement': MEASURES_COLUMNS, 'num_values': [4, 4, 3, 5, 2, 3, 3, 5, 3, 4, 3, 3, 6, 4]}
    max_values_df = pd.DataFrame.from_dict(data)
    # Let's say you want to consider features 1, 3, 5, 7 (0-based index)
    chosen_features = [MEASURES_COLUMNS.index(meas) for meas in chosen_features_str]

    # Each feature has a different range of values, represented as a list of lists
    feature_values = [range(i) for i in max_values_df['num_values'].values]
    chosen_features_values = [feature_values[i] for i in chosen_features]

    # Generate all possible permutations for the selected 4 features.
    permutations = list(itertools.product(*chosen_features_values))
    print(f"Inference on {len(permutations)} Permutations of following Covid measurements: {chosen_features_str}")

    # Final result will be stored here.
    result = []

    # For each permutation of values for the selected features.
    for permutation in permutations:
        # Create a list with -1 for unselected features.
        features = [-1] * len(max_values_df.iloc[:, 0].unique())
        # Assign the values of the selected features.
        for idx, value in zip(chosen_features, permutation):
            features[idx] = value
        # Add to the result.
        result.append(features)

    return permutations


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
    # make_prediction(*get_test_data())
    chosen_features = random.sample(MEASURES_COLUMNS, 4)
    permutations = make_permutation_predictions(chosen_features)
