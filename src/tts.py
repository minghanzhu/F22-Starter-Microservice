import json
from columbia_student_resource import ArtistResource


def t1():

    res = ArtistResource.get_by_key('d65239a5-d26c-48fc-83e0-9add1cc8e689')
    print(json.dumps(res, indent=2, default=str))


if __name__ == "__main__":
    print("\n\n Use test_rest.py instead of this file. \n\n")
    t1()
