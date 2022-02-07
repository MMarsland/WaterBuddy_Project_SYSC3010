package com.application.waterbuddy;

/**
 * Station info for reading/writing from database
 */
public class Station {

    public String data1;
    public String data2;

    public Station () {
        // Default constructor required for dataSnapshot.getValue(Station.class)
    }

    public Station (String data1, String data2) {
        this.data1 = data1;
        this.data2 = data2;
    }
}
