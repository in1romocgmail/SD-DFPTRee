import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

def discover_rules(dataset_path, output_file, min_support=0.05, min_confidence=0.6):
    """
    Discover IF-THEN rules using FP-Growth for subgroup discovery.

    Parameters:
        dataset_path (str): Path to the preprocessed dataset CSV file.
        output_file (str): Path to save the discovered rules as a CSV file.
        min_support (float): Minimum support for FP-Growth.
        min_confidence (float): Minimum confidence for association rules.

    Returns:
        pd.DataFrame: Dataframe containing the discovered rules.
    """
    # Load the preprocessed dataset
    data = pd.read_csv(dataset_path)

    # Prepare data for FP-Growth: Convert to transactional format
    target_classes = ['onlyregistered', 'Onlyviewed', 'Onlyexplored']
    binarized_data = data.copy()
    
    # Ensure all target classes are binary (1 or 0)
    binarized_data[target_classes] = binarized_data[target_classes].astype(int)

    # One-hot encoding for categorical/discretized attributes
    for column in binarized_data.columns:
        if column not in target_classes:
            binarized_data = pd.get_dummies(binarized_data, columns=[column], prefix=column)

    # Apply FP-Growth to find frequent itemsets
    frequent_itemsets = fpgrowth(binarized_data, min_support=min_support, use_colnames=True)

    # Generate association rules
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

    # Filter rules where consequent is one of the target classes
    filtered_rules = rules[rules['consequents'].apply(lambda x: any(cls in x for cls in target_classes))]

    # Save rules to CSV
    filtered_rules.to_csv(output_file, index=False)

    return filtered_rules
