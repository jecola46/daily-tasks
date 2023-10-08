# Define allowed tasks and their default values as well as the data types for each.
DAILY_TASKS = {
    'hasWorkedout': {
        'default_value': False,
        'data_type': bool,
    },
    'ateBreakfast': {
        'default_value': False,
        'data_type': bool,
    },
    'ateLunch': {
        'default_value': False,
        'data_type': bool,
    },
    'ateDinner': {
        'default_value': False,
        'data_type': bool,
    },
    'hasHomework': {
        'default_value': False,
        'data_type': bool,
    },
    'homeworkComplete': {
        'default_value': False,
        'data_type': bool,
        'requires_parent_field': 'homework',
    },
    'makeupStudyComplete': {
        'default_value': False,
        'data_type': bool,
    },
    'isRoomClean': {
        'default_value': False,
        'data_type': bool,
    },
    'hasDrawn': {
        'default_value': False,
        'data_type': bool,
    },
    'miscSkills': {
        'default_value': '',
        'data_type': str,
    }
}

def create_default_daily_tasks_object():
    default_field_values = {}
    
    for field_name, field_info in DAILY_TASKS.items():
        default_field_values[field_name] = field_info['default_value']
    
    return default_field_values