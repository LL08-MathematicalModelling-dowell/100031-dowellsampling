def dowellSampleSize(N, e):
    n = int(N / (1 + N * e * e))
    print(n)
    if n > 30 and n < 500:
        return n
    else:
        return(f"Sample size is not adequate")