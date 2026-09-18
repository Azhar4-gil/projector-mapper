from main import ProjectorMapper


class ProjectorMapperEngine(ProjectorMapper):

    """
    Final Mapper Layer

    Adds:

    - progress tracking
    - engine lifecycle
    - statistics
    - execution wrapper
    """

    def __init__(self):

        super().__init__()

        self.progress = 0

        self.stats = {

            "processed": 0,
            "mapped": 0,
            "new_values": 0

        }

    def update_progress(
        self,
        current,
        total
    ):

        if total <= 0:
            return

        self.progress = round(
            (current / total) * 100,
            2
        )

    def process_source(self):

        total = len(
            self.source_df
        )

        for index, (_, row) in enumerate(
            self.source_df.iterrows(),
            start=1
        ):

            generated = self.process_row(
                row
            )

            if generated == 0:

                self.generic_fallback(
                    row
                )

            self.stats[
                "processed"
            ] += 1

            self.update_progress(
                index,
                total
            )

        self.stats[
            "mapped"
        ] = len(
            self.mapped_data
        )

        self.stats[
            "new_values"
        ] = len(
            self.new_values
        )

    def execute(

        self,

        source_file,

        database_file,

        output_folder

    ):

        self.source_df = self.pd.read_excel(
            source_file
        )

        self.detect_columns()

        self.load_database(
            database_file
        )

        self.process_source()

        return self.export_results(
            output_folder
        )