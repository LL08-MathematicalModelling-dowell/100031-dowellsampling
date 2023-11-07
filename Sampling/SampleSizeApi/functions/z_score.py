from scipy.stats import norm

def get_z_score(confidence_level):
    alpha = 1 - confidence_level

    # For a two-tailed test, divide alpha by 2
    alpha /= 2

    # Find the critical z-value
    critical_z = norm.ppf(1 - alpha)

    return critical_z