package com.application.waterbuddy;

import java.util.ArrayList;

/**
 *  User class template for User sections in Firebase Console
 */
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

    /**
     * Default constructor required for dataSnapshot.getValue(User.class)
     */
    public User () { }

    /**
     *  Constructor for creating user accounts, used for new accounts and debugging
     * @param username Account identifier
     * @param password Account password
     * @param stations Any stations registered to the account
     * @param friends Array of string identifiers, friends registered to the account
     */
    public User (String username, String password, ArrayList<String> stations, ArrayList<String> friends) {
        this.userID = username;
        passwordHASH = password;
        this.stations = stations;
        this.friends = friends;
        dailyWater = 0;
        weeklyWater = 0;
        isAdmin = false;
        thirst = 1;
        weight = 62;
        height = 177;
    }
}
