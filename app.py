from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

from sql_fns import query_dwell_times
from sql_fns import query_dwell

from sql_fns import stats_directional
from sql_fns import current_visitors_query
from sql_fns import current_visitors_query_nondirectional

from datetime import date
from datetime import timedelta


app = Flask(__name__)


#-------------------------------------------------------------------------------
# Directional


@app.route('/')
def index():
    #return render_template('index.html')
    return render_template('index.html')


@app.route('/chart_data_directional', methods = ['GET', 'POST'])
def chart_data_directional():
    if request.method == 'POST':
        date_selected = request.form['date_selected']
    else:
        return "nothing sent"

    data_visitors = current_visitors_query(date_selected)
    data_stats = stats_directional(date_selected)
    total_visitors = data_stats['total_visitors']
    average_dwell = data_stats['average_dwell']

    return jsonify(data_visitors_probable=data_visitors,
                   total_visitors=total_visitors,
                   average_dwell_probable=average_dwell)


#-------------------------------------------------------------------------------
# Non-Directional


@app.route('/chart_data_non_directional', methods = ['GET', 'POST'])
def chart_data_non_directional():
    if request.method == 'POST':
        date_selected = request.form['date_selected']
    else:
        return "nothing sent"

    data_visitors_min, total_visitors, average_dwell_min = current_visitors_query_nondirectional(date_selected, 'min_m')
    data_visitors_max, total_visitors, average_dwell_max = current_visitors_query_nondirectional(date_selected, 'max_m')
    data_visitors_expected, total_visitors, average_dwell_expected = current_visitors_query_nondirectional(date_selected, 'expected_m')
    data_visitors_probable, total_visitors, average_dwell_probable = current_visitors_query_nondirectional(date_selected, 'probable_m')
    # total_visitors = data_stats['total_visitors']
    # average_dwell = data_stats['average_dwell']

    return jsonify(data_visitors_min=data_visitors_min,
                   data_visitors_max=data_visitors_max,
                   data_visitors_expected=data_visitors_expected,
                   data_visitors_probable=data_visitors_probable,
                   total_visitors=total_visitors,
                   average_dwell_min=average_dwell_min,
                   average_dwell_max=average_dwell_max,
                   average_dwell_expected=average_dwell_expected,
                   average_dwell_probable=average_dwell_probable)



#-------------------------------------------------------------------------------
@app.route('/date_loader_directional', methods = ['GET'])
def date_loader():
    date_data = str(date.today() - timedelta(1))
    print(date_data)
    return jsonify(date_data=date_data)


if __name__ == '__main__':
    app.run(debug=True)
