def scale_value(value, in_min, in_max, out_min, out_max):
    # # Check if the input range is valid
    # if in_min >= in_max:
    #     raise ValueError("Invalid input range: in_min must be less than in_max")
    
    # # Check if the output range is valid
    # if out_min >= out_max:
    #     raise ValueError("Invalid output range: out_min must be less than out_max")
    
    # Calculate the scaled value
    scaled_value = (value - in_min) / (in_max - in_min) * (out_max - out_min) + out_min
    
    # Clamp the scaled value within the output range
    if scaled_value < out_min:
        return out_min
    elif scaled_value > out_max:
        return out_max
    else:
        return scaled_value
