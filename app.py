from flask import Flask, render_template
import pandas as pd
import pyodbc
import io
from io import StringIO
import base64
from matplotlib import pyplot as plt
import seaborn as sns
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

server = 'azuresqlorange.database.windows.net'
database = 'orange_azure'
username = 'orange'
password = 'Supermotdepasse!42'
driver= [item for item in pyodbc.drivers()][-1]
cnx = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

# get the data you need
request = """ 
SELECT * FROM last_join ORDER BY movie_rank DESC
"""

df = pd.read_sql(request,cnx)

# plot da thing-a-magic
@app.route('/plot.png')
def test():
	img = io.BytesIO()
	sns.set_style("darkgrid")
	f, ax = plt.subplots(figsize=(16, 8))
	sns.countplot(x = 'movie_rank', hue = 'gender', data = df, palette="Set3")
	bars = ax.patches
	half = int(len(bars)/2)
	left_bars = bars[:half]
	right_bars = bars[half:]
	for left, right in zip(left_bars, right_bars):
		height_l = left.get_height()
		height_r = right.get_height()
		total = height_l + height_r
		ax.text(left.get_x() + left.get_width()/2., height_l + 3, '{0:.0%}'.format(height_l/total), ha="center")
		ax.text(right.get_x() + right.get_width()/2., height_r + 3, '{0:.0%}'.format(height_r/total), ha="center")
	plt.savefig(img, format='png')
	plt.close()
	img.seek(0)
	return Response(img.getvalue(), mimetype='image/png')

@app.route("/")
def home():
    return render_template("test.html")

if __name__ == '__main__':
    app.run(debug=True)