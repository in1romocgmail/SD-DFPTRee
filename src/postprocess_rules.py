import pandas as pd

def postprocess_rules(rules_file, output_file, confidence_threshold=0.8, min_courses=1):
    """
    Postprocess rules to filter by confidence and redundancy.

    Parameters:
        rules_file (str): Path to the rules CSV file.
        output_file (str): Path to save the final postprocessed rules.
        confidence_threshold (float): Minimum confidence to keep a rule.
        min_courses (int): Minimum number of courses in which a rule should appear.

    Returns:
        pd.DataFrame: Dataframe containing the final postprocessed rules.
    """
    # Load the rules
    rules = pd.read_csv(rules_file)

    # Step 3.1: Filter rules by confidence and minimum courses
    filtered_rules = rules[(rules['confidence'] >= confidence_threshold) & (rules['support'] * len(rules) >= min_courses)]

    # Step 3.2: Remove redundant rules
    def is_redundant(rule, rules):
        for _, other_rule in rules.iterrows():
            if (set(other_rule['antecedents']).issubset(set(rule['antecedents'])) and
                set(other_rule['consequents']) == set(rule['consequents']) and
                other_rule['confidence'] >= rule['confidence'] and
                len(other_rule['antecedents']) < len(rule['antecedents'])):
                return True
        return False

    non_redundant_rules = []
    for _, rule in filtered_rules.iterrows():
        if not is_redundant(rule, filtered_rules):
            non_redundant_rules.append(rule)

    # Create a DataFrame for non-redundant rules
    final_rules = pd.DataFrame(non_redundant_rules)

    # Save the final rules
    final_rules.to_csv(output_file, index=False)

    return final_rules