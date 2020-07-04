# this is for the app portion of the homework
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

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
        f"/api/v1.0/tobs"
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










if __name__ == '__main__':
    app.run(debug=True)