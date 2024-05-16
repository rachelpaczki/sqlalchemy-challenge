# Import the dependencies.
import numpy as np
import pandas as pd
import datetime as datetime

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, desc, func
from Flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to Honolulu, Hawaii - Climate Data API<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-08-18"
    )


@app.route("/api/v1.0/precipitation")
def precipitation(): 
    # Open session
    session = Session(engine)

    # Start query
    precip_query = session.query(measurement.date , measurement.prcp).filter(
        measurement.date >= '2017').all()
    session.close()

    # convert list to normal list
    precip = list(np.ravel(precip_query))
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations(): 
    # Open session
    session = Session(engine)

    # Start query
    station_query = session.query(station.station , station.name).all()
    session.close()

    # convert list to normal list
    stations = list(np.ravel(station_query))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs(): 
    # Open session
    session = Session(engine)

    # Start query
    tobs_query = session.query(measurement.station , measurement.date, measurement.tobs).filter(
        measurement.date >= '2017').filter(measurement.station == 'USC00519281').all()
    session.close()

    # convert list to normal list
    active_station = list(np.ravel(tobs_query))
    return jsonify(active_station)

@app.route("/api/v1.0/<start>")
def temp_start(start): 
    # Open session
    session = Session(engine)

    # Start query
    start_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(
        measurement.date >= 'start').all()
    session.close()

    # convert list to normal list
    temps = list(np.ravel(start_query))
    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end): 
    # Open session
    session = Session(engine)

    # Start query
    start_end_query =func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs).filter(
        measurement.date >= 'start').filter(measurement.date <= 'end').all()
    session.close()

    # convert list to normal list
    temps = list(np.ravel(start_end_query))
    return jsonify(temps)

if __name__=="__main__":
    app.run(debug=True)