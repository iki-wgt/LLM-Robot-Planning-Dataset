import random
import copy
import math

from utils.gt_rules import GtRules

class Connectors:
    def __init__(self):
        pass

    def get_objects_connectors(self):
        objects_connectors = [
            "and",
            "as well as",
            "along with",
            "plus",
            "in addition to",
            "together with",
            "besides",
            "alongside",
            "including",
            "also"
        ]
        return objects_connectors
    
    
    def get_object_starter_type_one(self):
        starter = [
            "There's a", 
            "There is a", 
            "There are a",
            "You can find a",
            "There lies a",
            "Here lies a",
            "There exists a",
            "Here stands a"
        ]
        return starter
    
    def get_object_starter_type_two(self):
        starter = [
            "A",
            "An assortment of items including",
            "Various objects like"
        ]
        return starter
    
    def get_sentence_connectors(self):
        sentence_connectors = [
            "on the",
            "lying on the",
            "resting on the",
            "sitting atop the",
            "placed on the",
            "found on the",
            "scattered across the",
            "littered on the",
            "cluttering the",
            "messing up the"
        ]
        return sentence_connectors
        

    def get_clean_polite_words(self):
        words = [
            "please",
            "kindly",
            "could you"
        ]
        return words

    def get_clean_words(self):
        clean_words = [
            "clean",
            "tidy it up", 
            "organize", 
            "clear", 
        ]

        return clean_words

    def get_on_surface_words(self):
        surface_words = [
            "on it"
            "on top",
            "on the surface",
            "placed there",
            "resting there",
            "positioned there",
            "located there",
            "placed on the surface",
            "left there",
            "lying there"
        ]
        return surface_words

class SentenceGeneration:
    def __init__(self):
        self.connectors = Connectors()
    
    def __get_objects(self, gt_rules: GtRules) -> list:
        applied_rules = gt_rules.get_applied_rules()
        objects = []
        for rule in applied_rules:
            rule_objects = gt_rules.get_objects_for_specific_rule(rule.get_rule_name())
            objects.extend(random.sample(rule_objects, rule.get_rule_per_sentence()))
        return objects
    
    def __get_equally_distributed_objects(self, gt_rules: GtRules, sub_rules) -> list:
        objects = []
        for rule in sub_rules:
            rule_objects = gt_rules.get_objects_for_specific_rule(rule)
            sub_rule_objects = [item for item in rule_objects if item not in objects]
            objects.extend(random.sample(sub_rule_objects, 1))
        return objects
    
    def generate_sentences(self, param_file):
        
        gt_rules = GtRules(param_file)

        surfaces = gt_rules.get_surfaces()
        objects_per_sentence = gt_rules.get_objects_per_sentence()
        num_sentences = gt_rules.get_num_sentences()
        rules_equally_distributed = gt_rules.get_rules_equally_distributed()
        
        # Equally Distribution of applied rules
        if rules_equally_distributed:
            applied_rules = gt_rules.get_applied_rules()
            rule_names = [rule.get_rule_name() for rule in applied_rules]
            num_per_rule = math.floor((num_sentences * objects_per_sentence) / len(rule_names))
            num_per_rule_left = (num_sentences * objects_per_sentence) % len(rule_names)
            rule_names_list = rule_names * num_per_rule
            rule_names_list += rule_names[:num_per_rule_left]
            random.shuffle(rule_names_list)
   
        # Equally Distribution of sentence strucutures
        num_different_sentence_structures = 6
        structure_ids = [0,1,2,3,4,5]

        num_per_sentence_struct = math.floor(num_sentences/num_different_sentence_structures)
        left = num_sentences % num_different_sentence_structures

        sentence_structures = structure_ids * num_per_sentence_struct
        sentence_structures += structure_ids[:left]  

        random.shuffle(sentence_structures)

        sentences = {}
        sentence_counter = 0

        while sentence_counter < num_sentences:
            
            if rules_equally_distributed:
                sub_rules = rule_names_list[sentence_counter * objects_per_sentence: (sentence_counter +1) * objects_per_sentence]
                objects = self.__get_equally_distributed_objects(gt_rules, sub_rules)
            else:
                objects = self.__get_objects(gt_rules)
            
            # get right object connector type 
            object_connetor_type = random.randint(1,2)
            if object_connetor_type == 1:
                object_connector = random.choice(self.connectors.get_object_starter_type_one())
                past_object_connector = random.choice(self.connectors.get_on_surface_words())
            else:
                object_connector = random.choice(self.connectors.get_object_starter_type_two())
                past_object_connector = f"are {random.choice(self.connectors.get_on_surface_words())}"

            surface_connector = random.choice(self.connectors.get_sentence_connectors())
            surface = random.choice(surfaces)

            object_list, objects = self.__format_object_list(objects)
            
            clean_command, surface_in_clean_command = self.__format_clean_command(surface, use_surface=False)
            sentence_structure = sentence_structures[sentence_counter]

            if sentence_structure == 0:
                # {object list} {surface} {clean_command}
                sentence = f"{object_connector} {object_list} {surface_connector} {surface} {clean_command}"
                sentence_structure_str = "{object list} {surface} {clean_command}"


            elif sentence_structure == 1:
                # {surface} {object list} {clean_command}
                sentence = f"{surface_connector.capitalize()} {surface} {object_connector.lower()} {object_list} {clean_command}"
                sentence_structure_str = "{surface} {object list} {clean_command}"

            elif sentence_structure == 2:
                 # {surface} {clean_command} {object_list}
                sentence = f"{surface_connector.capitalize()} {surface} {clean_command} {object_connector.lower()} {object_list}"
                sentence_structure_str = "{surface} {clean_command} {object_list}"
                
            elif sentence_structure == 3:
                 # {object_list} {clean_command} {surface}
                if surface_in_clean_command:
                    sentence = f"{object_connector} {object_list} {clean_command}"
                else:
                    sentence = f"{object_connector} {object_list} {clean_command} {surface_connector} {surface}"

                sentence_structure_str = "{object_list} {clean_command} {surface}"


            elif sentence_structure == 4:
                 # {clean_command} {object list} {surface}
                if surface_in_clean_command:
                    sentence = f"{clean_command.capitalize()} {object_connector.lower()} {object_list} {past_object_connector}"
                else:
                    sentence = f"{clean_command.capitalize()} {object_connector.lower()} {object_list} {surface_connector} {surface}"

                sentence_structure_str = "{clean_command} {object list} {surface}"


            elif sentence_structure == 5: 
                # {clean_command} {surface} {object_list}
                clean_command, surface_in_clean_command = self.__format_clean_command(surface, use_surface=True)
                with_surface = random.randint(0,1)
                
                if with_surface:
                    sentence = f"{clean_command.capitalize()} {surface_connector} {surface} {object_connector.lower()} {object_list}"
                else:
                    sentence = f"{clean_command.capitalize()} {object_connector.lower()} {object_list} {past_object_connector}"

                sentence_structure_str = "{clean_command} {surface} {object_list}"

            elif sentence_structure == 6:
                pass
         

            if not self.__check_for_duplicates(sentence, sentences):
                sentences[str(sentence_counter)] = {"sentence": sentence, 
                                                "sentence_structure_id": sentence_structure, 
                                                "sentence_structure": sentence_structure_str, 
                                                "objects": objects,
                                                "surface": surface}
                sentence_counter +=1

        return sentences

    def __check_for_duplicates(self, sentence, sentences:dict):
        for idx, value in sentences.items():
            if value["sentence"] == sentence:
                return True
        
        return False


    def __format_clean_command(self, surface, use_surface=False):

        polite = random.randint(0,1) # optionale polite

        if not use_surface:
            opt_surface = random.randint(0,1) # optional surface
        else:
            opt_surface = 1

        clean_command = random.choice(self.connectors.get_clean_words())

        not_surface_default_word = "it"
        surface_default_word = "the "

        if clean_command == "tidy it up":
            not_surface_default_word = ""
            surface_default_word = "from the "

        if polite:
            polite_word = random.choice(self.connectors.get_clean_polite_words())
            sentence = f"{polite_word} {clean_command} {not_surface_default_word if not opt_surface else surface_default_word + surface}"        
        else:
            sentence = f"{clean_command} {not_surface_default_word if not opt_surface else surface_default_word + surface}"        

        return sentence, opt_surface


    def __format_object_list(self, objects):
        
        copied_objects = copy.deepcopy(objects)

        random.shuffle(copied_objects)        
        
        num_connectors = random.randint(0, len(copied_objects)-1)

        add_additional_connector = random.randint(0,1)
        
        if num_connectors == 0:
            return ', '.join(copied_objects), copied_objects

        # Connect all except the ones who has a connector        
        objects_text = ', '.join(copied_objects[:len(copied_objects) - num_connectors])

        # Fill the other obects with connectors
        for i in reversed(range(num_connectors)):
            current_pos = len(copied_objects)-1-i
            if add_additional_connector:
                objects_text += f" {random.choice(self.connectors.get_objects_connectors())} a {copied_objects[current_pos]}"
            else:
                objects_text += f" {random.choice(self.connectors.get_objects_connectors())} a {copied_objects[current_pos]}"

        return objects_text, copied_objects