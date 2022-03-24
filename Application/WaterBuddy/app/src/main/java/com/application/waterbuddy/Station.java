package com.application.waterbuddy;

/**
 * Station info for reading/writing from database
 */
public class Station {

    public double dailyWater;
    public double weeklyWater;
    public double humidity;
    public double cupSize;
    public int waterFrequency;
    public String stationID;
    public String notification;
    public boolean mute;
    public WaterHistory waterHistory;

    public Station () {
        // Default constructor required for dataSnapshot.getValue(Station.class)
    }

    public Station (String id, double cupSize) {
        this.cupSize = cupSize;
        this.stationID = id;
        humidity = 25;

    }
}
