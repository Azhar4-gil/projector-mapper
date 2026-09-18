from projector_mapper import ProjectorMapperEngine
from rule_optimizer import RuleOptimizer
from validation_engine import ValidationEngine


class FinalProjectorMapper(

    ProjectorMapperEngine,
    RuleOptimizer,
    ValidationEngine

):

    """
    Final Production Build
    """

    def __init__(self):

        super().__init__()

        self.initialize_optimizer()

    def run(

        self,

        source_file,

        database_file,

        output_folder

    ):

        self.source_df = self.pd.read_excel(
            source_file
        )

        self.detect_columns()

        self.validate_source_columns()

        self.load_database(
            database_file
        )

        self.process_source()

        self.validate_output()

        self.validate_new_values()

        result = self.export_results(
            output_folder
        )

        self.print_summary()

        return result


def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "source"
    )

    parser.add_argument(
        "database"
    )

    parser.add_argument(
        "--out",
        default="."
    )

    args = parser.parse_args()

    mapper = FinalProjectorMapper()

    mapper.run(

        args.source,

        args.database,

        args.out

    )


if __name__ == "__main__":
    main()