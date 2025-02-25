import os
import json

class GTReader:
    def __init__(self, gt_dir:str):
        self.__gt_dir = gt_dir

        self.__sentences , self.__gt_sentence_dict = self.__read_files()

    def __read_json(self, path:str) -> dict:
        with open(path, "r") as f:
            json_file = json.load(f)

        return json_file

    def __read_files(self) -> tuple[dict, dict]:
        gt_sentences_dict = {}
        sentences = os.path.join(self.__gt_dir, "sentences.json")
        sentences_json = self.__read_json(sentences)
        for sentence_id in sentences_json.keys():
            sentence_json_path = os.path.join(self.__gt_dir, f"sentence_{sentence_id}.json")
            sentence_json = self.__read_json(sentence_json_path)
            gt_sentences_dict[sentence_id] = sentence_json

        return sentences_json, gt_sentences_dict

    def get_sentence_ids(self) -> list:
        return self.__sentences.keys()

    def get_sentences(self) -> dict:
        return self.__sentences
    
    def get_gt_sentence_dict(self) -> dict:
        return self.__gt_sentence_dict

    def get_sentence_by_id(self, id):
        return self.__sentences[f"{id}"]

    def get_gt_by_id(self, id):
        return self.__gt_sentence_dict[f"{id}"]

def main():
    gt_reader = GTReader("../../data/gt/test_run1")
    for id in gt_reader.get_sentence_ids():
        print(f"---------- Sentence from id {id}------------ ")
        print(gt_reader.get_sentence_by_id(id))
        print("--------------------")
        print(gt_reader.get_gt_by_id(id))


if __name__ == "__main__":
    main()
