import yaml
import json
import sys
from typing import List

class Rule:
    def __init__(self, rule_name, apply_rule, rule_per_sentence):
        self.__rule_name = rule_name
        self.__apply_rule = apply_rule
        self.__rule_per_sentence = rule_per_sentence
    
    def get_rule_name(self)->str:
        return self.__rule_name

    def get_apply_rule(self)->bool:
        return self.__apply_rule

    def get_rule_per_sentence(self) -> int:
        return self.__rule_per_sentence

class GtRules:
    def __init__(self, rules_file):
        self.__rules_file = rules_file
        self.__params = self.__read_params()["gt_params"]
        self.__objects = self.__read_json(self.get_objects_json_file())
        self.__objects_per_rule = self.__get_objects_per_rule()
        self.__check_if_param_file_is_valid()

    def __read_params(self):
        with open(self.__rules_file, 'r') as file:
            params = yaml.safe_load(file)
        return params
    
    def __read_json(self, file_path) -> dict:
        with open(file_path, 'r') as f: 
            objects = json.load(f)
        return objects

    def __get_objects_per_rule(self) -> dict:
        objects_per_rule = {}
        for rule_key, rule_value in self.__objects.items():
            objects_per_rule[rule_key] = []
            for category, cat_value in rule_value.items():
                objects_per_rule[rule_key].extend(cat_value["objects"])
        
        return objects_per_rule

    def __check_if_param_file_is_valid(self):
        rules = self.get_applied_rules()
        sum_objects = 0
        for rule in rules:
            sum_objects += rule.get_rule_per_sentence()

        if sum_objects != self.get_objects_per_sentence() and not self.get_rules_equally_distributed():
            print("\033[93mThe sum of rules per sentence are not equal then objects per sentence\033[0m")
            sys.exit(0)

    def get_objects_json_file(self):
        return self.__params["objects_json_file"]
    
    def get_surfaces(self):
        return self.__params["surfaces"]
    
    def get_num_sentences(self):
        return self.__params["num_sentences"]
    
    def get_objects_per_sentence(self):
        return self.__params["objects_per_sentence"]
    
    def get_rules_equally_distributed(self):
        return self.__params["rules_equally_distributed"]
    
    def get_num_of_applied_rules(self):
        return len(self.get_applied_rules())
    
    def get_applied_rules(self)->List[Rule]:
        rules = self.__params["rules"]
        applied_rules: List[Rule] = []
        for rule, rule_info in rules.items():
            if rule_info["apply_rule"]:
                rule = Rule(rule_name=rule, apply_rule=rule_info["apply_rule"], 
                            rule_per_sentence=rule_info["rule_per_sentence"])
                applied_rules.append(rule)

        return applied_rules
    
    def get_objects_for_specific_rule(self, rule):
        return self.__objects_per_rule[rule]