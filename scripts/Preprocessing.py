import tensorflow_transform as tft

# Preprocessing function for the dataset
def preprocessing_fn(inputs):
    outputs = {}
    # Normalize numeric features
    outputs['CRIM'] = tft.scale_to_z_score(inputs['CRIM'])
    outputs['ZN'] = tft.scale_to_z_score(inputs['ZN'])
    outputs['INDUS'] = tft.scale_to_z_score(inputs['INDUS'])
    outputs['RM'] = tft.scale_to_z_score(inputs['RM'])
    outputs['AGE'] = tft.scale_to_z_score(inputs['AGE'])
    outputs['DIS'] = tft.scale_to_z_score(inputs['DIS'])
    outputs['TAX'] = tft.scale_to_z_score(inputs['TAX'])
    outputs['PTRATIO'] = tft.scale_to_z_score(inputs['PTRATIO'])
    outputs['LSTAT'] = tft.scale_to_z_score(inputs['LSTAT'])
    
    # Keep the target column as is
    outputs['MEDV'] = inputs['MEDV']
    
    return outputs