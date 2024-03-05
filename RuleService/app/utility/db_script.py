from service.query import save_rule
from utility.rules import rules_data
from service.query import clean_the_rule_table


def add_rules_in_to_the_db():
    clean_the_rule_table()
    for rules in rules_data:
        save_rule(*rules)

