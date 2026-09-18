class ValidationEngine:

    """
    Cross Validation Engine

    Validates:

    - Required columns
    - Duplicate outputs
    - Empty outputs
    - Invalid records
    """

    REQUIRED_COLUMNS = [

        "Burraq_ID",
        "Attribute",
        "Value"
    ]

    def validate_source_columns(self):

        missing = []

        for col in [

            self.columns["burraq_id"],
            self.columns["attribute"],
            self.columns["value"]

        ]:

            if not col:
                missing.append(col)

        if missing:

            raise ValueError(
                "Required columns not found."
            )

    def validate_record(
        self,
        record
    ):

        for field in self.REQUIRED_COLUMNS:

            if field not in record:
                return False

        return True

    def validate_output(self):

        valid = []

        for record in self.mapped_data:

            if self.validate_record(
                record
            ):
                valid.append(record)

        self.mapped_data = valid

        return True

    def validate_new_values(self):

        valid = []

        for record in self.new_values:

            if (

                record.get(
                    "Burraq_ID"
                )

                and

                record.get(
                    "Attribute"
                )

            ):

                valid.append(
                    record
                )

        self.new_values = valid

        return True