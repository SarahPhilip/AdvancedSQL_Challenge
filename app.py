import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# 2. Create an app
app = Flask(__name__)


# 3. Define static routes
@app.route("/")
def home():
    return (
        f"Hawaii Climate Analysis API!<br/><br/>"
        f"Avalable Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
	max_date = session.query(func.max(Measurement.date)).first()
	max_date = [r for r in max_date]
	last_date = dt.datetime.strptime(max_date[0], '%Y-%m-%d')
	prev_year = last_date - dt.timedelta(days=365)

	query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
	query_dict = {date: prcp for date, prcp in query}
	return jsonify(query_dict)

@app.route("/api/v1.0/stations")
def stations():
	stations_query = session.query(Station.station,).all()
	stations = list(np.ravel(stations_query))
	return jsonify(stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
	max_date = session.query(func.max(Measurement.date)).first()
	max_date = [r for r in max_date]
	last_date = dt.datetime.strptime(max_date[0], '%Y-%m-%d')
	prev_year = last_date - dt.timedelta(days=365)
	tobs_q = session.query(Measurement.tobs).filter(Measurement.date >= prev_year).all()
	tobs = list(np.ravel(tobs_q))
	return jsonify(tobs)                 

@app.route("/api/v1.0/<start>")
def start_temp(start):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    return jsonify(temp_data)

    

@app.route("/api/v1.0/<start>/<end>")
def range_temp(start, end):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    return jsonify(temp_data)
# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)
