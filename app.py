# this is for the app portion of the homework
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

Station = Base.classes.station





app = Flask(__name__)

@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    Measurement_date = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        Measurement_date.append(measurement_dict)

    return jsonify(Measurement_date)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)
      
    results = session.query(Station.station).all()

    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():
    
    session = Session(engine)

    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date > "2016-08-23").\
        order_by(Measurement.date).all()

    session.close()

    Busy_temp = list(np.ravel(results))

    return jsonify(Busy_temp)

@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)
    
    date = dt.date(*(int(s) for s in start.split("-")))
    
    query_start = session.query(Measurement.station, func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).all()

    session.close()

    start_date_list = []
    for station, min, avg, max in query_start:
        date_dict = {}
        date_dict["Station"] = station
        date_dict["Min Temperature"] = min
        date_dict["Avg Temperature"] = avg
        date_dict["Max Temperature"] = max
        start_date_list.append(date_dict)

    if date >= dt.date(2010, 1, 1) and date <= dt.date(2017, 8, 23):
        return jsonify(start_date_list)
    else: 
        return jsonify({"404 error"})

if __name__ == '__main__':
    app.run(debug=True)