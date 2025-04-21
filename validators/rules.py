REQUIRED_COLUMNS = ["date", "amount", "description"]

def validate_file_extension(filename):
    return filename.endswith('.csv')

def check_required_columns(df):
    return [col for col in REQUIRED_COLUMNS if col not in df.columns]

def validate_amount_column(df):
    if "amount" not in df.columns:
        return False
    return df["amount"].apply(lambda x: isinstance(x, (int, float))).all()

def validate_dataframe(df):
    errors = []
    missing = check_required_columns(df)
    if missing:
        errors.append("Missing columns: " + ", ".join(missing))
    if not validate_amount_column(df):
        errors.append("Invalid or missing 'amount' values.")
    return errors
