
# Import dependencies
import pandas as pd
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from flask import Flask, jsonify

# Setting up Flask Database
app = Flask(__name__)
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

#Create references to Station table
Station = Base.classes.station

#Create references to Measurement tables
Measurement = Base.classes.measurement

#Query the server 
session = Session(bind=engine)

#Setting up Flask Routes
# Calulate the date 1 year ago from today   
    # Query database for stations
    # Convert object to a list
    # Return jsonified list


@app.route("/")
def home():
    """List of all returnable API routes."""
    return(
        f"Available Routes:<br/>"

        f"/api/v1.0/precipitation<br/>"
        f"- Query last year's dates and temperature. <br/>"

        f"/api/v1.0/stations<br/>"
        f"- Returns a json list of stations. <br/>"

        f"/api/v1.0/tobs<br/>"
        f"- Returns list of Temperature Observations(tobs) for previous year. <br/>"

        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"- Returns an avg, Max, and Min temperature for given date.<br/>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"- Returns an avg Max, and Min temperature for given period.<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
        year_ago_dt = dt.date.today() - dt.timedelta(days=365)
    
    prcp = session.query(Measurement.date, Measurement.prcp)\
            .filter(Measurement.date >= year_ago_dt)\
            .order_by(Measurement.date).all()
    
    prcp_list={}
    for item in prcp:
        prcp_list[item[0]]=item[1]
    
    return (jsonify(prcp_list))
    

@app.route("/api/v1.0/stations")
def stations():
    
    stations = session.query(Station.station).all()
    
    station_list=[]
    for sublist in stations:
        for item in sublist:
            station_list.append(item)
    
    return (jsonify(station_list))


@app.route("/api/v1.0/tobs")
def tobs():
    
    year_ago_dt = dt.date.today() - dt.timedelta(days=365)
    
    tobs = session.query(Measurement.date, Measurement.tobs)\
            .filter(Measurement.date >= year_ago_dt)\
            .order_by(Measurement.date).all()
    
    tobs_list=[]
    for sublist in tobs:
        for item in sublist:
            tobs_list.append(item)
    
    return (jsonify(tobs_list))


@app.route("/api/v1.0/<start_date>")
@app.route("/api/v1.0/<start_date>/<end_date>")
def temp_stats(start_date, end_date=0):
    # Return a json list of the minimum, average and maximum temperature for a given date range
    
    # Make end date today's date if no date
    if end_date == 0:
        end_date = dt.date.today()
    
    # Query for tobs between start and end date
    tobs = session.query(Measurement.tobs)\
            .filter(Measurement.date >= start_date)\
            .filter(Measurement.date <= end_date).all()
   
    # Convert results to df
    tobs_df = pd.DataFrame(tobs, columns=['tobs'])
    
    # Append integer versions of each item into a list
    tobs_list = []
    tobs_list.append(np.asscalar(np.int16(tobs_df['tobs'].min())))
    tobs_list.append(np.asscalar(np.int16(tobs_df['tobs'].mean())))
    tobs_list.append(np.asscalar(np.int16(tobs_df['tobs'].max())))
    
    return (jsonify(tobs_list))

if __name__ == "__main__":
    app.run(debug=True)
