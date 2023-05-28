import csv
import json

PATHS_TO_CSV = {
    'ad': 'ad.csv',
    'category': 'category.csv',
    'location': 'location.csv',
    'user': 'user.csv'
}

PATHS_TO_JSON = {
    'ad': 'ad.json',
    'category': 'category.json',
    'location': 'location.json',
    'user': 'user.json',
}

MODELS = {
    'ad': 'ads.ad',
    'category': 'ads.category',
    'location': 'users.location',
    'user': 'users.user'

}


def convert_data(path_to_csv, model):
    with open(path_to_csv, 'r', encoding='utf-8') as file:
        result = []
        for row in csv.DictReader(file):
            if 'is_published' in row:
                if row['is_published'] == 'TRUE':
                    row['is_published'] = True
                else:
                    row['is_published'] = False
            if 'location_id' in row:
                row['location'] = [row['location_id']]
                del row['location_id']
            result.append({"model": model, "fields": row})
    return result


def write_to_json(data, path_to_json):
    with open(path_to_json, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    for path in PATHS_TO_CSV:
        data_csv = convert_data(PATHS_TO_CSV[path], MODELS[path])
        write_to_json(data_csv, PATHS_TO_JSON[path])
