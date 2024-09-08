from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

def convert_date(timestamp_string):
    """
    Implement a function to take in a string timestamp and convert that to an encoded string.
    Input strings are in the following format 'YYYY-MM-DD HH:MM:SS'

    The output string is in 4 components:
        1. Shift  (A, B or C)
            Shift A is between the hours of 07:00 to 15:00(exclusive)
            Shift B ""                   "" 15:00 to 23:00(exclusive)
            Shift C ""                   "" 23:00 to 07:00(exclusive)

        2. Day of month in two digits e.g. (01, 02, ..., 31)

        3. Month encoded as a letter:
            Jan -> 'A'
            Feb -> 'B'
            Mar -> 'C'
            *NB the letters used to replace the months of January to December skip 'I'
            [ABCDEFGHJKLM]

        4 Last two digits of the year:
            2019 -> 19

    For example:
    convert_date(timestamp_string='2019-07-15 02:03:16')
    ->C15G19

    convert_date(timestamp_string='2015-01-05 07:00:01')
    ->A05A15


    Parameters:
    ----------
    timestamp_string - a string timestamp in the format 'YYYY-MM-DD HH:MM:SS'

    """
    
    # Parse the input timestamp to a datetime object
    dt = datetime.strptime(timestamp_string, '%Y-%m-%d %H:%M:%S')
    
    # Determine the shift based on hour
    hour = dt.hour
    if 7 <= hour < 15:
        shift = 'A'
    elif 15 <= hour < 23:
        shift = 'B'
    else:
        shift = 'C'

    # Encode the day of the month as two digits
    day = f"{dt.day:02d}"

    # Map the month number to the corresponding letter
    month_map = {
        1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F',
        7: 'G', 8: 'H', 9: 'J', 10: 'K', 11: 'L', 12: 'M'
    }
    month = month_map[dt.month]

    # Extract the last two digits of the year
    year = f"{dt.year % 100:02d}"

    # Combine all parts to make the encoded string
    encoded_string = shift + day + month + year

    # Prepare data to return
    info = {
        'hour': hour,
        'shift': shift,
        'day': day,
        'month': month,
        'year': year,
        'encoded_string': encoded_string
    }

    return info

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        timestamp_string = request.form['timestamp']
        try:
            result = convert_date(timestamp_string)
        except Exception as e:
            result = {'error': str(e)}

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

