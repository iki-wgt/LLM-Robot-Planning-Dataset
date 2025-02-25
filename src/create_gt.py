from utils.create_sentences import SentenceGeneration

import json
import os
import shutil

class GTCreation:

    def __init__(self, directory_name, gt_path='../gt', objects_json_path='../param_files/objects.json' ):
        self.__sentence_creator = SentenceGeneration()

        self.__gt_path = os.path.join(gt_path, directory_name)

        if os.path.exists(self.__gt_path):
            yes_or_no = input("The path already exist, should it be removed? (y, n)")
            if yes_or_no == 'y':
                shutil.rmtree(self.__gt_path)
            else:
                return 
            
        os.makedirs(self.__gt_path)

        self.__known_object_dict = self.__read_json(objects_json_path)

    def __read_json(self, path):
        with open(path, "r") as f:
            d = json.load(f)
        return d

    def __save_json_file(self, path, data):
        with open(path, 'w') as f:
            json.dump(data, f)
    
    def __get_location_for_specific_object(self, object):
        for rule in self.__known_object_dict.values():
            for category in rule.values():
                if object in category["objects"]:
                    return category["location"]

    def create_gt(self, gt_params_file):
        sentences = self.__sentence_creator.generate_sentences(gt_params_file)
        self.__save_json_file(os.path.join(self.__gt_path, "sentences.json"), sentences)
        
        for idx, value in sentences.items():
            gt_json = {"response": {"movements":[]}}

            used_objects = value["objects"]
            used_surface = value["surface"]

            for object in used_objects:
                location = self.__get_location_for_specific_object(object)

                navigate_surface = {"action": "navigate", "object": used_surface}
                serach = {"action": "search", "object": object}
                grasp = {"action": "grasp", "object": object}
                navigate_default_loc = {"action": "navigate", "object": location}
                place = {"action": "place", "object": object}

                gt_json["response"]["movements"].append(navigate_surface)
                gt_json["response"]["movements"].append(serach)
                gt_json["response"]["movements"].append(grasp)
                gt_json["response"]["movements"].append(navigate_default_loc)
                gt_json["response"]["movements"].append(place)
            
            path = os.path.join(self.__gt_path,  f"sentence_{idx}.json")
            self.__save_json_file(path, gt_json)

if __name__ == "__main__":
    gt_creation = GTCreation(directory_name="gt_dataset", 
                             gt_path='gt',
                             objects_json_path = 'param_files/objects.json')
    gt_creation.create_gt("param_files/gt_params.yml")
    
