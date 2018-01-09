import pandas as pd
import json
import collections

data_location = \
    'https://raw.githubusercontent.com/Geoyi/Cleaning-Titanic-Data/' +\
    'master/titanic_clean.csv'


def transform_to_json(row: pd.Series) -> str:
    """
    Transforms a row of passenger data into a JSON-formatted string.
    :param row:
        pd.Series containing all data for a passenger
    :return:
        JSON-formatted string of the data row
    """
    passenger_dict = collections.OrderedDict()

    passenger_dict['name'] = row['name']

    demographic_dict = collections.OrderedDict()
    demographic_dict['sex'] = row['sex']
    demographic_dict['age'] = row['age']
    passenger_dict['demographics'] = demographic_dict

    family_dict = collections.OrderedDict()
    family_dict['sibsp'] = row['sibsp']
    family_dict['parch'] = row['parch']
    passenger_dict['family'] = family_dict

    geography_dict = collections.OrderedDict()
    geography_dict['embarked'] = row['embarked']
    geography_dict['home.dest'] = row['home.dest']
    passenger_dict['geography'] = geography_dict

    ticket_dict = collections.OrderedDict()
    ticket_dict['ticket'] = row['ticket']
    ticket_dict['pclass'] = row['pclass']
    ticket_dict['has_cabin_number'] = row['has_cabin_number']
    # nulls are encoded as the string "nan" in the CSV file
    ticket_dict['cabin'] = \
        None if row['cabin'] == 'nan' \
        else row['cabin']
    ticket_dict['fare'] = row['fare']
    passenger_dict['ticket'] = ticket_dict

    survival_dict = collections.OrderedDict()
    survival_dict['survived'] = row['survived']
    survival_dict['boat'] = \
        None if row['boat'] == 'nan' \
        else row['boat']
    survival_dict['body'] = \
        None if row['body'] == 'nan' \
        else row['body']
    passenger_dict['survival'] = survival_dict

    return json.dumps(passenger_dict)

# skip the last row of data in the file which doesn't relate to a passenger.
# also set data types for a few problematic fields
titanic_passengers = pd.read_csv(
    data_location,
    skipfooter=1,
    dtype={
        "cabin": str,
        "boat": str,
        "body": str
    }
)

titanic_passengers['json'] = titanic_passengers.apply(transform_to_json, axis=1)

json_file = open('titanic.json', 'w')
json_file.write(titanic_passengers['json'].str.cat(sep='\n'))
json_file.write('\n')
json_file.close()
