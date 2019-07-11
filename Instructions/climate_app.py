from flask import Flask,jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False})
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

climate=Flask(__name__)

@climate.route("/")
def home():
    print("Server received request for home Page")
    return(f"API for Climate<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date i.e.: /api/v1.0/2017-08-23<br/>"
        f"/api/v1.0/start date/end date  i.e.: /api/v1.0/2017-08-23/2017-09-10 <br/>")

@climate.route("/api/v1.0/precipitation")
def precipitation(): 
    response=session.query(Measurement.date,Measurement.prcp).all()
    all_prcp=[]
    for date, prcp in response:
        prcp_dic={}
        prcp_dic[date]=prcp
        all_prcp.append(prcp_dic)
    return jsonify(all_prcp)
    
@climate.route("/api/v1.0/stations")
def stations(): 
    response=session.query(Station.station).all()
    station_list=[]
    for station in response:
        station_list.append(station)
    return jsonify({"station":station_list})


@climate.route("/api/v1.0/tobs")
def tobs(): 
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    response=session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=query_date).order_by(Measurement.date.desc()).all()
    all_tobs=[]
    for date,tobs in response:
        tobs_dic={}
        tobs_dic[date]=tobs
        all_tobs.append(tobs_dic)
    return jsonify(all_tobs)

@climate.route("/api/v1.0/<start>")
def start(start):
    response=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    for min,avg,max in response:
        dic={"Min":min,"Avg":avg,"Max":max}
    return jsonify(dic)

@climate.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    response=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    for min,avg,max in response:
        dic={"Min":min,"Avg":avg,"Max":max}
    return jsonify(dic)

if __name__ == "__main__":
    climate.run(debug=True)
