from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200

# this would probably be more efficient if i just 
# did the searches in the sql/mongoose query
# instead of getting all the data then organizing it using up memory and time
def search_users(args):
    result_list = []
    added_ids = set()

    # id search
    if 'id' in args:
        matchingId = [obj for obj in USERS if obj['id'] == args['id']]
        # check if matchingId exists then check if its id is already in added_ids
        if matchingId and matchingId[0]['id'] not in added_ids:
            result_list.append(matchingId[0])
            added_ids.add(matchingId[0]['id'])

    # name search
    if 'name' in args:
        search_name = args['name'].lower()
        # iterates USERS then checks if 'name' is in obj['name'] if true adds obj to result_list
        matchingNames = [obj for obj in USERS if search_name in obj['name'].lower()]
        for obj in matchingNames:
            if obj['id'] not in added_ids:
                result_list.append(obj)
                added_ids.add(obj['id'])

    # age search
    if 'age' in args:
        search_age = int(args['age'])
        matchingAges = [obj for obj in USERS if search_age - 1 <= obj['age'] and obj['age'] <= search_age + 1]
        for obj in matchingAges:
            if obj['id'] not in added_ids:
                result_list.append(obj)
                added_ids.add(obj['id'])

    # occupation search
    if 'occupation' in args:
        search_occupations = args['occupation'].lower()
        matchingOccupations = [obj for obj in USERS if search_occupations in obj['occupation'].lower()]
        for obj in matchingOccupations:
            if obj['id'] not in added_ids:
                result_list.append(obj)
                added_ids.add(obj['id'])

    return result_list
