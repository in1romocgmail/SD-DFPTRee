import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from pyspark.sql import SparkSession
from pyspark.ml.fpm import FPGrowth

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

def sd_dfptree(dataset_path, output_file, min_support=0.05, min_confidence=0.6):
    """
    Discover IF-THEN rules using FP-Growth with Spark for subgroup discovery.

    Parameters:
        dataset_path (str): Path to the preprocessed dataset CSV file.
        output_file (str): Path to save the discovered rules as a CSV file.
        min_support (float): Minimum support for FP-Growth.
        min_confidence (float): Minimum confidence for association rules.

    Returns:
        None: Saves the discovered rules directly to the output file.
    """
    # Initialize Spark Session
    spark = SparkSession.builder.appName("SD-DFPTree").getOrCreate()

    # Load the dataset into a Spark DataFrame
    data = spark.read.csv(dataset_path, header=True, inferSchema=True)

    # Combine all attributes into a single transactions column
    target_classes = ['onlyregistered', 'Onlyviewed', 'Onlyexplored']
    transaction_columns = [col for col in data.columns if col not in target_classes]

    # Create a transactions column
    from pyspark.sql.functions import array, col
    data = data.withColumn("transactions", array(*[col(c).cast("string") for c in transaction_columns]))

    # Apply FP-Growth using Spark's FPGrowth
    fp_growth = FPGrowth(itemsCol="transactions", minSupport=min_support, minConfidence=min_confidence)
    model = fp_growth.fit(data)

    # Extract frequent itemsets and association rules
    frequent_itemsets = model.freqItemsets
    rules = model.associationRules

    # Filter rules to keep only those where consequents contain target classes
    filtered_rules = rules.filter(
        rules.consequent.contains("onlyregistered") |
        rules.consequent.contains("Onlyviewed") |
        rules.consequent.contains("Onlyexplored")
    )

    # Save the filtered rules to the output file
    filtered_rules.toPandas().to_csv(output_file, index=False)

    # Stop the Spark Session
    spark.stop()
