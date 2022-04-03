package com.application.waterbuddy;

import static android.content.ContentValues.TAG;
import android.util.Log;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.HashMap;
import java.util.Locale;

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
    public HashMap<String,WaterHistory> waterHistory;

    public Station () {
        // Default constructor required for dataSnapshot.getValue(Station.class)
    }

    public Station (String id, double cupSize) {
        this.cupSize = cupSize;
        this.stationID = id;
        humidity = 25;

    }

    /**
     * Calculate water consumption for today in ml
     * @param year The selected year
     * @param month The selected month
     * @param day The selected day
     * @return Double value of Daily water Consumed
     */
    public int getDailyWater(int year, int month, int day) {
        if (waterHistory == null){
            return 0;
        }
        int amount = 0;

        Date today = new GregorianCalendar(year, month, day).getTime();
        for (WaterHistory history : waterHistory.values()){
            Date date = null;
            try{
                date = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss", Locale.CANADA).parse(history.datetime);
            } catch (Exception e) {
                Log.e(TAG, "Error Reading Daily Water");
            }

            SimpleDateFormat fmt = new SimpleDateFormat("yyyyMMdd", Locale.CANADA);
            if ( date != null &&
                    fmt.format(date).equals(fmt.format(today))){
                amount += history.amount;
            }
        }
        return amount;
    }

    /**
     * Calculate monthly water consumption for this month in ml
     * @return Monthly Water Consumed
     */
    public int getMonthlyWater(){
        int amount = 0;
        Date today = new Date();
        for (WaterHistory history : waterHistory.values()){
            Date date = null;
            try{
                date = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss", Locale.CANADA).parse(history.datetime);
            } catch (Exception e) {
                Log.e(TAG, "Error Reading Daily Water");
            }

            SimpleDateFormat fmt = new SimpleDateFormat("yyyyMM", Locale.CANADA);
            if ( date != null &&
                    fmt.format(date).equals(fmt.format(today))){
                amount += history.amount;
            }
        }

        return amount;
    }
}
