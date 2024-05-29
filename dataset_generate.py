#  Create a dummy dataset 1 t test

# import numpy as np
# import pandas as pd

# # Set random seed for reproducibility
# np.random.seed(42)

# # Parameters for the dummy dataset
# mean1 = 10  # Mean of first sample
# std_dev1 = 2  # Standard deviation of first sample
# sample_size1 = 100  # Sample size of first sample

# mean2 = 12  # Mean of second sample
# std_dev2 = 2  # Standard deviation of second sample
# sample_size2 = 100  # Sample size of second sample

# # Generate random samples from normal distribution
# sample1 = np.random.normal(mean1, std_dev1, sample_size1)
# sample2 = np.random.normal(mean2, std_dev2, sample_size2)

# # Combine samples into a DataFrame
# df = pd.DataFrame({'Sample 1': sample1, 'Sample 2': sample2})

# # Save DataFrame to a CSV file
# df.to_csv('dummy_dataset.csv', index=False)

# print("Data saved to 'dummy_dataset.csv'")


# Create a dummy dataset 2 linear regression

# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn.linear_model import LinearRegression

# # Set random seed for reproducibility
# np.random.seed(42)

# # Generate random data for independent variable (X)
# X = np.random.rand(100, 1) * 10

# # Generate dependent variable (Y) with noise added
# # Let's assume the true relationship is Y = 2*X + 5
# true_slope = 2
# true_intercept = 5
# noise = np.random.randn(100, 1) * 2
# Y = true_slope * X + true_intercept + noise

# # Combine X and Y into a DataFrame
# df = pd.DataFrame({'X': X.flatten(), 'Y': Y.flatten()})

# # Save DataFrame to a CSV file
# df.to_csv('dummy_regression_dataset.csv', index=False)

# print("Data saved to 'dummy_regression_dataset.csv'")

# Generate survival analysis data
# import numpy as np
# import pandas as pd
# np.random.seed(42)  # For reproducibility

# # Parameters
# n_A = 100  # Number of subjects in group A
# n_B = 100  # Number of subjects in group B
# median_survival_A = 30  # Median survival time for group A
# median_survival_B = 20  # Median survival time for group B

# # Simulating time-to-event data using exponential distribution
# time_A = np.random.exponential(scale=median_survival_A, size=n_A)
# time_B = np.random.exponential(scale=median_survival_B, size=n_B)

# # Simulating censoring
# censor_A = np.random.binomial(1, p=0.3, size=n_A)  # 30% censoring in group A
# censor_B = np.random.binomial(1, p=0.3, size=n_B)  # 30% censoring in group B

# # Creating DataFrame
# df_A = pd.DataFrame({'Time': time_A, 'Event': 1 - censor_A, 'Group': 'A'})
# df_B = pd.DataFrame({'Time': time_B, 'Event': 1 - censor_B, 'Group': 'B'})
# df = pd.concat([df_A, df_B], ignore_index=True)
# df.to_csv('survival_analysis_data.csv', index=False)


# Generate 2 ind var and 1 dep cont and 1 dep bin variable dataset
import pandas as pd
import numpy as np

# Create a dataset with continuous dependent variable
continuous_data = pd.DataFrame({
    'Independent_Var1': np.random.normal(0, 1, 25),  # Independent variable 1 (continuous)
    'Independent_Var2': np.random.normal(0, 1, 25),  # Independent variable 2 (continuous)
    'Dependent_Var': np.random.normal(0, 1, 25)      # Dependent variable (continuous)
})

# Create a dataset with binary dependent variable
binary_data = pd.DataFrame({
    'Independent_Var1': np.random.normal(0, 1, 25),  # Independent variable 1 (continuous)
    'Independent_Var2': np.random.normal(0, 1, 25),  # Independent variable 2 (continuous)
    'Dependent_Var': np.random.choice([0, 1], size=25)  # Dependent variable (binary)
})

# Save datasets to CSV files
continuous_data.to_csv('continuous_data.csv', index=False)
binary_data.to_csv('binary_data.csv', index=False)
