import pandas as pd

def dowellQuotaSampling(quotaSamplingInput):
    # Get input data and quota categories
    df = quotaSamplingInput['sam']
    quota_categories = quotaSamplingInput['quota_categories']
    
    # Initialize empty DataFrame for sampled data
    sampled_data = pd.DataFrame(columns=df.columns)
    
    print('Here it is ==>', sampled_data)
    print("======")
    
    # Performing quota sampling
    for category, quotas in quota_categories.items():
        print('Category:', category)
        for category_value, quota in quotas.items():
            print('Category value:', category_value)
            print('Quota:', quota)
            # Select observations matching the category value
            category_data = df[df[category] == category_value]
            print('Category data:', category_data)
            if len(category_data) >= quota:
                # Sample observations from the category data
                sampled_category_data = category_data.sample(n=quota, replace=True)
                print('Sampled category data:', sampled_category_data)
                # Add sampled data to the sampled_data DataFrame
                sampled_data = pd.concat([sampled_data, sampled_category_data])
                print('Sampled data so far:', sampled_data)
            else:
                print(f"Warning: Not enough data for {category_value}. Skipping sampling.")
                continue

    print('This is quota:', sampled_data)
    
    # Reset index of sampled data
    sampled_data.reset_index(drop=True, inplace=True)
    print('Final sampled data:', sampled_data)
        
    return sampled_data
