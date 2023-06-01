import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

MODEL = "models/test_model.h5"


'''
Make a prediction for a given time sequence and given permutation.
The last row of the input data is adjusted to use the values of the permutation.

@param lk_data:
    Type:  Pandas DataFrame
    Shape: ?x14 (Rows x Columns) | variable number of rows

@param permutation:
    Type: Pandas DataFrame
    Shape: 1x14 (Rows x Columns)
    
    All columns that should be taken from the original data (from lk_data) have the value -1.
    
@return
    type:  numpy ndarray
    shape: 6
    
'''
def make_prediction(lk_df, permutation):
    last_row = lk_df.iloc[-1]
    
    # insert permutation values
    for c in permutation.columns:
        col_val = permutation[c].values[0]
        if col_val != -1:
            last_row[c] = col_val
    
    lk_df.iloc[-1] = last_row
    
    
    input_scaler = MinMaxScaler(feature_range=(0, 1))
    output_scaler = MinMaxScaler(feature_range=(0, 1)) # TODO: richtige Min und Max werte 
    output_scaler.fit(lk_df.to_numpy()[:,-1].reshape(lk_df.shape[0],1))
    
    lk_data = lk_df.to_numpy()[:,:-1]
    lk_data_scaled = input_scaler.fit_transform(lk_data)
    lk_data_scaled = np.expand_dims(lk_data_scaled,axis=0)

    
    
    predict_model = tf.keras.models.load_model(MODEL, compile=True)
    # predict_model.compile(optimizer='adam', loss='mse')
    
    prediction_sequence = predict_model.predict(lk_data_scaled)
    prediction = np.squeeze(prediction_sequence,axis=0)
    prediction = output_scaler.inverse_transform(prediction)[:,0]
    return prediction
    