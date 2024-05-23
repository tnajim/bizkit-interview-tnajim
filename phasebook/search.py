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
        result_list.append(matchingId[0])

    # name search
    if 'name' in args:
        search_name = args['name'].lower()
        # iterates USERS then checks if 'name' is in obj['name'] if true adds obj to result_list
        matchingNames = [obj for obj in USERS if search_name in obj['name'].lower()]
        result_list.extend(matchingNames)

    # age search
    if 'age' in args:
        search_age = int(args['age'])
        matchingAges = [obj for obj in USERS if search_age - 1 <= obj['age'] and obj['age'] <= search_age + 1]
        result_list.extend(matchingAges)

    # occupation = partially matched and is case insensitive
    if 'occupation' in args:
        search_occupations = args['occupation'].lower()
        matchingOccupations = [obj for obj in USERS if search_occupations in obj['occupation'].lower()]
        result_list.extend(matchingOccupations)

    return result_list
