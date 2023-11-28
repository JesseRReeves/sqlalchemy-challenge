# Import the dependencies.
import sqlalchemy
from flask import Flask, jsonify
import datetime as dt
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"start and end dates should be in format: mm-dd-yyyy"
    )

@app.route("/api/v1.0/precipitation")
def precip():
    last_year = dt.date(2017,8,23)- dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).\
                            order_by(Measurement.date).all()
    result_dict = dict(results)
    session.close()
    return jsonify(result_dict)
                                     
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Measurement.station, func.count(Measurement.id)).\
            group_by(Measurement.station).order_by(func.count(Measurement.id).desc()).all()
                     
    stations_dict = dict(stations)
    session.close()
    return jsonify(stations_dict)
                     
@app.route("/api/v1.0/tobs")
def tobs():
    temperature_data = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.date >= '2016-08-23').all()
                     
    tobs_dict = dict(temperature_data)
    session.close()
    return jsonify(tobs_dict)
                     
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start(start=None, end=None):
    start = dt.datetime.strptime(start, "%m-%d-%Y")    
    if not end:
        # start = dt.datetime.strptime(start, "%m-%d-%Y") 
        result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                                    func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
        
        session.close()                                                               
        tobsall = list(np.ravel(result))                                                            
        return jsonify(tobsall)   
    end = dt.datetime.strptime(end, "%m-%d-%Y")                                                           
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs),\
                func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()               
                                
    session.close()                            
                                
    tobsall = list(np.ravel(result))                      
        
    return jsonify(tobsall)                                                                   
                                                                                                                   
if __name__== '__main__':                                                                   
   app.run()                                                                
                                                                   
                                                                   
                                                                   
                                                                   