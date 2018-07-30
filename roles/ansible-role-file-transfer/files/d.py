def handicap_index(differential_list):
    """
    This function takes a list of a golfers handicap differentials and returns the index associated with that golfers last 20 rounds.
    :param differential_list: a given list of the golfers handicap differentials (of any length) from oldest to newest
    :return: the golfers handicap index value
    """
    if len(differential_list) < 20:
        return 36.4
    else:
        recent_twenty = differential_list[-20:]
        print(recent_twenty)
        sort_recent = sorted(recent_twenty)
        print(sort_recent)
        top_ten = sort_recent[0:10]
        print(top_ten)
        tally = sum(top_ten)
        print(tally)
        avg = float(tally)/10.0
        print(avg)
        index = avg*0.96
        return index



a = [6.6,8.1,9.2,8.3,8.5,3.0,7.7,9.0,6.1,8.9,9.9,6.5,8.1,7.2,5.2,3.4,9.0,9.1,3.7,9.1]
b = handicap_index(a)
print(b)
