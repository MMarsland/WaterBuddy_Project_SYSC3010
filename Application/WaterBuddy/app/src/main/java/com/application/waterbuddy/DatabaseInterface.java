package com.application.waterbuddy;

import static android.content.ContentValues.TAG;
import android.util.Log;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import java.util.ArrayList;

/**
 * Java Class for interfacing database commands with main application
 * Provides different functions to read and update Firebase Database data
 * @author Caleb Turcotte
 */
public class DatabaseInterface {
    /**
     * Lint Tool Used: Android Lint
     * Output: No problems in DatabaseInterface
     */

    public DatabaseReference userRef, stationRef, messageRef;
    public ArrayList<String> users;
    public ArrayList<User> userList;
    public User username;

    /**
     * Constructor for DatabaseInterface
     * Creates initial database references and empty user lists
     */
    public DatabaseInterface () {
        FirebaseDatabase database = FirebaseDatabase.getInstance();
        userRef = database.getReference("users");
        stationRef = database.getReference("stations");
        messageRef = database.getReference("messages");

        users = new ArrayList<>();
        userList = new ArrayList<>();
    }

    /**
     * Handles adding a friend to the user
     * @param friend_id String id of friend the user wishes to add
     * @return String message based on if friend was added or not
     */
    public String add_friend(String friend_id) {
        if (username == null) {
            return "Error";
        }
        if (username.friends == null) {
            username.friends = new ArrayList<>();
        }
        if (username.friends.contains(friend_id)) {
            return "Friend already on list";
        }
        if(users.contains(friend_id)) {
            username.friends.add(friend_id);
            userRef.child(username.userID).setValue(username);
            return "Friend successfully added";
        }
        return "Id does not exist";
    }

    /**
     * Create a new user account
     * @param user Account username
     * @param password Account password
     * @return False if the account already exists
     */
    public boolean create_account(String user, String password) {
        if(user.equals("") || password.equals("")) {
            return false;
        }
        if (!users.contains(user)) {
            ArrayList<String> stations = new ArrayList<>();
            ArrayList<String> friends = new ArrayList<>();

            User tempUser = new User(user,password, stations, friends);
            userRef.child(tempUser.userID).setValue(tempUser);
            return true;
        }
        return false;
    }

    /**
     * Delete User account
     * @param user String id for User account
     */
    public void delete_account(String user){
        userRef.child(user).removeValue();
    }

    public void load(String userid) {
        ValueEventListener userListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    if(snapshot.getKey() != null &&
                            snapshot.getKey().equals(userid)) {
                            username = snapshot.getValue(User.class);
                    }
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                // Getting Post failed, log a message
                Log.w(TAG, "loadStation:onCancelled", databaseError.toException());
            }
        };
        userRef.addValueEventListener(userListener);
    }

    /**
     * Attempt to log in to user account
     * @param user Username string
     * @param password Password string
     * @return False if login fails
     */
    public boolean login(String user, String password) {
        if(user.equals("") || password.equals("")) {
            return false;
        }
        if (users.contains(user)) {
            // check password
            for (User tempUser : userList) {
                if (tempUser.passwordHASH.equals(password) && tempUser.userID.equals(user)) {
                    return true;
                }
            }
        }
        return false;
    }

    /**
     * Register station with user account
     * @return true if the station was added
     */
    public boolean register_station(String station_name) {
        if (username.stations == null) {
            username.stations = new ArrayList<>();
        }
        if (!username.stations.contains(station_name)) {
            username.stations.add(station_name);
            userRef.child(username.userID).setValue(username);
            return true;
        }
        else {
            return false;
        }
    }

    /**
     * Initialize user listeners
     */
    public void sign_in(){
        ValueEventListener userListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                users.clear();
                userList.clear();
                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    users.add(snapshot.getKey());
                    userList.add(snapshot.getValue(User.class));
                }
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                // Getting Post failed, log a message
                Log.w(TAG, "loadStation:onCancelled", databaseError.toException());
            }
        };
        userRef.addValueEventListener(userListener);
    }
}
