def get_z_score(confidence_level):
    if confidence_level == 0.90:
        return 1.645
    elif confidence_level == 0.95:
        return 1.96
    elif confidence_level == 0.99:
        return 2.58
    else:
        raise ValueError("Invalid confidence level. Supported values: 0.90, 0.95, 0.99")