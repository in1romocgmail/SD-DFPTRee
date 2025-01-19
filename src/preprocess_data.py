import pandas as pd
import numpy as np

def preprocess_data(input_file, output_file):
    # Load the dataset
    data = pd.read_csv(input_file)

    # Drop unnecessary columns
    columns_to_drop = ['userid_DI', 'start_time_DI', 'last_event_DI', 'roles', 'registered']
    data = data.drop(columns=columns_to_drop, errors='ignore')

    # Create new attributes
    data['onlyregistered'] = (data['viewed'] == 0) & (data['explored'] == 0) & (data['certified'] == 0)
    data['Onlyviewed'] = (data['viewed'] == 1) & (data['explored'] == 0) & (data['certified'] == 0)
    data['Onlyexplored'] = (data['explored'] == 1) & (data['certified'] == 0)
    data[['onlyregistered', 'Onlyviewed', 'Onlyexplored']] = data[['onlyregistered', 'Onlyviewed', 'Onlyexplored']].astype(int)

    # Manual discretization
    bins_yob = [0, 1963, 1973, 1983, 1993, 1999, np.inf]
    labels_yob = ['>54', '45-54', '35-44', '25-34', '18-24', '<18']
    data['YoB_discretized'] = pd.cut(data['YoB'], bins=bins_yob, labels=labels_yob, right=False)

    bins_grade = [0, 0.5, 1.0]
    labels_grade = ['low', 'high']
    data['grade_discretized'] = pd.cut(pd.to_numeric(data['grade'], errors='coerce'), bins=bins_grade, labels=labels_grade, right=False)

    # Automatic discretization (Equal-Width Binning)
    def discretize_column(course_data, column, bins=3, labels=['low', 'medium', 'high']):
        unique_values = course_data[column].nunique()
        if unique_values < 2 or course_data[column].dropna().empty:
            # Skip discretization for insufficient unique values
            course_data[column + '_discretized'] = pd.NA
        else:
            try:
                bins = min(bins, unique_values)  # Adjust bins to unique values
                labels_dynamic = labels[:bins - 1]  # Adjust labels dynamically
                course_data[column + '_discretized'] = pd.qcut(
                    course_data[column],
                    q=bins,
                    labels=labels_dynamic,
                    duplicates='drop'
                )
            except ValueError:
                # Assign NA if discretization fails
                course_data[column + '_discretized'] = pd.NA
        return course_data

    columns_to_discretize = ['nevents', 'ndays_act', 'nchapters', 'nplay_video', 'nforum_posts']

    for column in columns_to_discretize:
        data = data.groupby('course_id', group_keys=False).apply(lambda group: discretize_column(group, column))

    # Rename columns for better understanding
    data = data.rename(columns={
        'final_cc_cname_DI': 'countryName',  # Rename to 'countryName'
        'YoB': 'age'                        # Rename to 'age'
    })

    # Save the final preprocessed dataset
    data.to_csv(output_file, index=False)
