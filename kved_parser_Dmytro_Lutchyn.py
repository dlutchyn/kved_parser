import json
import doctest


def path_finder(classCode: str, kved: dict) -> list:
    '''
    (str), (dict) -> (list)
    Returns a path to a needed element with given classCode.
    >>> path_finder("09.90", {"sections": [{"classCode": "09.90"}, \
{"classCode": "09.91"}]})
    ['09.90', 'classCode', 0, 'sections']
    '''
    temp = []
    if len(temp) == 0:
        if kved != classCode:
            if isinstance(kved, dict):
                for key in kved:
                    temp = path_finder(classCode, kved[key])
                    if len(temp) != 0:
                        temp += [key]
                        return temp
            if isinstance(kved, list):
                for i in range(len(kved)):
                    temp = path_finder(classCode, kved[i])
                    if len(temp) != 0:
                        temp += [i]
                        return temp
            return []
        else:
            return [kved]
    return temp


def build_json(path: list, kved: dict) -> dict:
    '''
    (list), (dict) -> (dict)
    Returns builded dict based on given classCode.
    '''

    sections = kved['sections'][path[-2]]
    section_name = sections[path[-3]]['sectionName']
    sect_children_num = len(sections)

    divisions = sections[path[-3]]['divisions']
    division_name = divisions[path[-5]]['divisionName']
    div_children_num = len(divisions)

    groups = divisions[path[-5]]['groups']
    group_name = groups[path[-7]]['groupName']
    group_children_num = len(groups)

    classes = groups[path[-7]]['classes']
    class_name = classes[path[-9]]['className']

    new_json = {
        "name": class_name,
        "type": "class",
        "parent": {
            "name": group_name,
            "type": "group",
            "num_children": group_children_num,
            "parent": {
                "name": division_name,
                "type": "division",
                "num_children": div_children_num,
                "parent": {
                    "name": section_name,
                    "type": "section",
                    "num_children": sect_children_num
                }
            }
        }
    }
    return new_json


if __name__ == "__main__":
    doctest.testmod()

    path = "kved.json"
    with open(path, 'r', encoding='utf-8') as f:
        decoded_kved = json.load(f)

    class_path = path_finder("10.73", decoded_kved)
    new_json = build_json(class_path, decoded_kved)

    with open('student_list.json', 'w', encoding='utf-8') as f:
        json.dump(new_json, f, ensure_ascii=False, indent=2)
