import json
import os


def guess_filenames(filenames):
    case_filenames = {'nav-data': 'nav-data.json',
                      'maneuvers': 'maneuver.json',
                      'targets': 'target-data.json',
                      'target-settings': 'target-settings.json',
                      'targets_maneuvers': 'target-maneuvers.json',
                      'targets_real': 'real-target-maneuvers.json',
                      'analyse': 'nav-report.json',
                      'constraints': 'constraints.json',
                      'route': 'route-data.json',
                      'settings': 'settings.json',
                      'hydrometeo': 'hmi-data.json'}

    case_filenames_kt = {'nav-data': 'navigation.json',
                         'maneuvers': 'result_maneuver.json',
                         'targets': 'targets.json',
                         'target-settings': 'targets_settings.json',
                         'targets_maneuvers': 'predicted_tracks.json',
                         'targets_real': 'real-target-maneuvers.json',
                         'analyse': 'evaluation.json',
                         'constraints': 'constraints.json',
                         'route': 'route.json',
                         'settings': 'settings.json',
                         'hydrometeo': 'hydrometeo.json'}

    case_filenames_vse = {'nav-data': 'nav-data.json',
                          'maneuvers': 'maneuver.json',
                          'targets': 'targets.json',
                          'target-settings': 'target-settings.json',
                          'targets_maneuvers': 'predict.json',
                          'targets_real': 'real-target-maneuvers.json',
                          'analyse': 'analyse.json',
                          'constraints': 'constraints.json',
                          'route': 'route.json',
                          'settings': 'settings.json',
                          'hydrometeo': 'hydrometeo.json'}

    if "nav-data.json" in filenames and "targets.json" in filenames:
        return case_filenames_vse
    elif "navigation.json" in filenames:
        return case_filenames_kt
    else:
        return case_filenames


def gather_jsons(directory):
    filenames = guess_filenames(os.listdir(directory))
    big_dict = {}

    for k in filenames:
        try:
            with open(directory + '/' + filenames[k]) as f:
                big_dict[k] = json.load(f)
        except FileNotFoundError:
            continue

    return big_dict


if __name__ == "__main__":
    for filename in os.listdir("."):
        fullpath = os.path.abspath(filename)
        if os.path.isdir(fullpath):
            with open(f"{filename}.json", "w") as f:
                json.dump(gather_jsons(fullpath), f)
