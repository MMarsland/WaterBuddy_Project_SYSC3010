package com.application.waterbuddy;

import java.util.ArrayList;

public class User {

    public String username;
    public String passwordHASH;
    public boolean isAdmin;
    public ArrayList<String> friends;
    public ArrayList<String> stations;
    public double height;
    public double weight;
    public double thirst;

    public int dailyWater;
    public int weeklyWater;

    public User () {
        // Default constructor required for dataSnapshot.getValue(User.class)
    }

    public User (String username, String password, ArrayList<String> stations, ArrayList<String> friends) {
        this.username = username;
        passwordHASH = password;
        this.stations = stations;
        this.friends = friends;
        dailyWater = 0;
        weeklyWater = 0;
        isAdmin = false;
    }
}
