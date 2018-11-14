from flask import Flask, render_template
import datetime
from lib import googleSheets
#import argparse
app = Flask(__name__)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1JrT-RQUs4ohRYtdKBCrCcvGY48xFez3QZopYuuAL3oc'
TABLE_RANGE_REFERENCE = 'Utility!B2:C2'

@app.template_filter()
def datetimefilter(value, format='%Y/%m/%d %H:%M'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter

@app.route("/")
def getRenderedTemplate(headless = False):
    service = googleSheets.setup('lib/credentials.json')
    myRange = googleSheets.getRange(service, SPREADSHEET_ID, TABLE_RANGE_REFERENCE)
    # myTable = googleSheets.getRange(service, SPREADSHEET_ID, TABLE_RANGE_REFERENCE)
    naughtyTableRange = 'Tracking!' + myRange['values'][0][0] + ':' + myRange['values'][0][1]
    
    naughtyReport = googleSheets.getRange(service, SPREADSHEET_ID, naughtyTableRange)

    render_results = render_template('template.html',
        myTable = naughtyReport['values']
    )
    
    return render_results

if __name__ == '__main__':

#    parser = argparse.ArgumentParser(description='CFDS Shadow Command Line Interface.')
#    parser.add_argument('--headless', action='store_true', help='use this option to avoid starting a server')
#    args = parser.parse_args()

#    if (args.headless):
#        myResult = getRenderedTemplate(args.headless)
#        print( myResult )
#    else:
    app.run(debug=True)
