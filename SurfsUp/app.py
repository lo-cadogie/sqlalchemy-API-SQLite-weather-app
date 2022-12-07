import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# 1. import Flask
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
        return (
        f"Climate API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"

        #Add a link
        f"<a href='/api/v1.0/precipitation'>api/v1.0/precipitation</a><br/>"

        f"/api/v1.0/stations<br/>"
        f"<a href='/api/v1.0/stations'>api/v1.0/stations</a><br/>"

        f"/api/v1.0/tobs<br/>"
        f"<a href='/api/v1.0/tobs'>api/v1.0/tobs</a><br/>"


        f"The format for start and end date is mm-dd-yyyy<br/>"
        f"/api/v1.0/start<br/>"
        f"<a href='/api/v1.0/start'>api/v1.0/start</a><br/>"

        f"/api/v1.0/start/end<br/>"
        f"<a href='/api/v1.0/start/end'>api/v1.0/start/end</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # limit dates to one year back from the last date
    most_recent_date = dt.date(2017, 8, 23)
    year_back_date = most_recent_date - dt.timedelta(days=365)

    #query
    precip_query = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= year_back_date).all()

    precip = {date: prcp for date, prcp in precip_query}

    #close session
    session.close()

    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #query
    station_query = session.query(station.station, station.name, station.latitude, station.longitude, station.elevation).all()

    all_stations = []
    for STation, name, latitude, longitude, elevation in station_query:
        station_dict = {}
        station_dict["station"] = STation
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        all_stations.append(station_dict)

    #close session
    session.close()
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # limit dates to one year back from the last date
    most_recent_date = dt.date(2017, 8, 23)
    year_back_date = most_recent_date - dt.timedelta(days=365)

    #query
    tobs_query = session.query(measurement.station, measurement.date, measurement.prcp, measurement.tobs).\
        filter(measurement.station == 'USC00519281', measurement.date >= year_back_date).all()

    st_tobs = []
    for STation, date, prcp, tobs, in tobs_query:
        tobs_dict = {}
        tobs_dict["station"] = STation
        tobs_dict["date"] = date
        tobs_dict["prcp"] = prcp
        tobs_dict["tobs"] = tobs
        st_tobs.append(tobs_dict)

    #close session
    session.close()

    return jsonify(st_tobs)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):   

    # Create our session (link) from Python to the DB


    session = Session(engine)


    # Select Variable
    sel = [func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)]
    
    # Query if start only (no end)
    if not end:
        start = dt.datetime.strptime(start, "%m%d%Y")   
        results = session.query(*sel).\
            filter(measurement.date >= start).all()

        temps = list(np.ravel(results))
        session.close()
        #return(start)
        return jsonify(temps)

    # Query if start and end
    start = dt.datetime.strptime(start, "%m%d%Y")   
    end = dt.datetime.strptime(end, "%m%d%Y")
    
    results = session.query(*sel).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()


    temps = list(np.ravel(results))
    session.close()
    return jsonify(temps=temps)
    
    #return(start, end)


if __name__ == "__main__":
    app.run(debug=True)






