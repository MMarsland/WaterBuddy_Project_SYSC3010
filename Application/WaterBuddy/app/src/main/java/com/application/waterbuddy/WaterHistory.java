package com.application.waterbuddy;

/**
 *  WaterHistory class template for drinking history sections in Firebase Console
 */
public class WaterHistory {
    public String datetime;
    public double amount;

    /**
     * Default constructor required for dataSnapshot.getValue(WaterHistory.class)
     */
    public WaterHistory() {

    };
}
