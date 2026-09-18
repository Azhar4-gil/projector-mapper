import re
from collections import defaultdict


class RuleOptimizer:

    """
    Rule Optimizer

    Responsibilities

    1. Remove duplicate rule registrations
    2. Cache expensive lookups
    3. Cache normalized attributes
    4. Cache regex evaluations
    5. Prevent duplicate outputs
    6. Speed up database matching
    7. Reduce RuleRegistry execution cost
    """

    # ==========================================
    # INITIALIZATION
    # ==========================================

    def initialize_optimizer(self):

        self.attribute_cache = {}

        self.regex_cache = {}

        self.database_cache = {}

        self.rule_cache = {}

    # ==========================================
    # ATTRIBUTE CACHE
    # ==========================================

    def get_cached_attribute(
        self,
        attribute
    ):

        if attribute is None:
            return ""

        attribute = str(attribute)

        if attribute in self.attribute_cache:

            return self.attribute_cache[
                attribute
            ]

        normalized = (
            attribute
            .strip()
            .lower()
        )

        self.attribute_cache[
            attribute
        ] = normalized

        return normalized

    # ==========================================
    # REGEX CACHE
    # ==========================================

    def regex_search(

        self,

        pattern,

        value,

        flags=re.I

    ):

        key = (
            pattern,
            str(value)
        )

        if key in self.regex_cache:

            return self.regex_cache[
                key
            ]

        result = re.search(
            pattern,
            str(value),
            flags
        )

        self.regex_cache[
            key
        ] = result

        return result

    # ==========================================
    # DATABASE CACHE
    # ==========================================

    def optimized_database_lookup(
        self,
        value
    ):

        if value is None:
            return None

        value = str(
            value
        ).strip().lower()

        if value in self.database_cache:

            return self.database_cache[
                value
            ]

        result = self.find_in_database(
            value
        )

        self.database_cache[
            value
        ] = result

        return result

    # ==========================================
    # REMOVE DUPLICATE RULES
    # ==========================================

    def optimize_rule_list(
        self,
        rules
    ):

        seen = set()

        optimized = []

        for rule in rules:

            name = rule.__name__

            if name in seen:
                continue

            seen.add(name)

            optimized.append(rule)

        return optimized

    # ==========================================
    # OPTIMIZED REGISTRY
    # ==========================================

    def get_optimized_rule_engine(self):

        return self.optimize_rule_list(

            self.get_rule_engine()

        )

    # ==========================================
    # EXECUTE RULE
    # ==========================================

    def run_optimized_rule(

        self,

        rule,

        row

    ):

        row_id = id(row)

        cache_key = (

            row_id,

            rule.__name__

        )

        if cache_key in self.rule_cache:

            return self.rule_cache[
                cache_key
            ]

        try:

            result = rule(row)

        except Exception:

            result = []

        self.rule_cache[
            cache_key
        ] = result

        return result

    # ==========================================
    # PROCESS ROW
    # ==========================================

    def process_row_optimized(
        self,
        row
    ):

        generated = 0

        rules = (
            self.get_optimized_rule_engine()
        )

        for rule in rules:

            records = (
                self.run_optimized_rule(
                    rule,
                    row
                )
            )

            for record in records:

                if self.add_final_record(
                    record
                ):

                    generated += 1

        return generated

    # ==========================================
    # PROFILE RULE USAGE
    # ==========================================

    def profile_rules(self):

        usage = defaultdict(int)

        for record in self.mapped_data:

            attr = record.get(
                "Attribute"
            )

            usage[attr] += 1

        return dict(usage)

    # ==========================================
    # SHOW TOP ATTRIBUTES
    # ==========================================

    def print_rule_profile(self):

        usage = self.profile_rules()

        print()
        print("=" * 60)
        print("RULE PROFILE")
        print("=" * 60)

        for key, value in sorted(

            usage.items(),

            key=lambda x: x[1],

            reverse=True

        )[:20]:

            print(
                f"{key}: {value}"
            )

    # ==========================================
    # MEMORY CLEANUP
    # ==========================================

    def clear_caches(self):

        self.attribute_cache.clear()

        self.regex_cache.clear()

        self.database_cache.clear()

        self.rule_cache.clear()

    # ==========================================
    # SMART ATTRIBUTE PRIORITY
    # ==========================================

    PRIORITY_ATTRIBUTES = {

        "HDMI",
        "DisplayPort",

        "Network (RJ-45)",
        "Wireless LAN",

        "Native Resolution",
        "Maximum Resolution",

        "Standard Mode Brightness",

        "Contrast Ratio",

        "Product Name",

        "Product Model"
    }

    def sort_records(self):

        def score(record):

            attribute = record.get(
                "Attribute"
            )

            if (
                attribute
                in self.PRIORITY_ATTRIBUTES
            ):
                return 0

            return 1

        self.mapped_data.sort(
            key=score
        )

    # ==========================================
    # FINALIZE OUTPUT
    # ==========================================

    def optimize_output(self):

        self.sort_records()

        self.clear_caches()

        return True