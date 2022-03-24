package com.application.waterbuddy;

import java.util.ArrayList;

public class User {

    public String userID;
    public String passwordHASH;
    public boolean isAdmin;
    public ArrayList<String> friends;
    public ArrayList<String> stations;
    public double height;
    public double weight;
    public int thirst;

    public int dailyWater;
    public int weeklyWater;

    public User () {
        // Default constructor required for dataSnapshot.getValue(User.class)
    }

    public User (String username, String password, ArrayList<String> stations, ArrayList<String> friends) {
        this.userID = username;
        passwordHASH = password;
        this.stations = stations;
        this.friends = friends;
        dailyWater = 0;
        weeklyWater = 0;
        isAdmin = false;
        friends = new ArrayList<>();
        stations = new ArrayList<>();
        thirst = 1;
    }
}
