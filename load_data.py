import csv
import os
import json


def load_records(filepath, encoding='utf-8'):
    if not os.path.exists(filepath):
        raise ValueError(f"Error: File '{filepath}' not found.")
    if os.path.isdir(filepath):
        data = []
        for filename in os.listdir(filepath):
            if filename.endswith(".txt"):
                with open(os.path.join(filepath, filename), "r") as f:
                    data.append(f.read())
        return data
    if filepath.endswith(".csv"):
        with open(filepath, 'r', newline='', encoding=encoding) as file:
            csv_reader = csv.DictReader(file)
            return list(csv_reader)
    elif filepath.endswith(".json"):
        with open(filepath, "r", encoding=encoding) as f:
            return json.load(f)
    elif filepath.endswith(".jsonl"):
        data = []
        with open(filepath, "r", encoding=encoding) as f:
            for line in f.readlines():
                if not line or not line.strip():
                    continue
                data.append(json.loads(line))
        return data
    elif filepath.endswith(".txt"):
        data = []
        with open(filepath, "r", encoding=encoding) as f:
            for line in f.readlines():
                if not line or not line.strip():
                    continue
                data.append(line.strip())
        return data
    else:
        raise NotImplementedError(f"Don't know how to load this file! {filepath}")


if __name__ == "__main__":
    for ix, rec in enumerate(load_records(sys.argv[1])):
        print("Record:", ix, "Text:", rec)
