

package com.application.waterbuddy;

import static android.content.ContentValues.TAG;
import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;
import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewTreeObserver;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.PopupWindow;
import android.widget.Spinner;
import android.widget.TextView;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import java.util.ArrayList;
import java.util.List;

/**
 * Main Activity for Water Buddy Smart Application
 * Tutorials used:
 * https://firebase.google.com/docs/database/android/read-and-write
 */
public class MainActivity extends AppCompatActivity {

    private DatabaseReference userRef, stationRef, messageRef;
    private ArrayList<Station> sReference;
    private Spinner selection;
    private int selected_index;

    private ArrayList<String> users;
    private ArrayList<User> userList;

    private User username;

    public static final String PREFS_NAME = "MyPrefsFile";
    static SharedPreferences settings;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        settings = getSharedPreferences(PREFS_NAME, 0);

        FirebaseDatabase database = FirebaseDatabase.getInstance();

        userRef = database.getReference("users");
        stationRef = database.getReference("stations");
        messageRef = database.getReference("messages");


        sReference = new ArrayList<>();
        users = new ArrayList<>();
        userList = new ArrayList<>();
        selected_index = 0;

        selection = findViewById(R.id.selector);

        selection.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parentView, View selectedItemView, int position, long id) {
                update_values(position);
                selected_index = position;
            }

            @Override
            public void onNothingSelected(AdapterView<?> parentView) {
            }
        });

        // wait for activity to load before loading popups
        findViewById(R.id.main).getViewTreeObserver().addOnGlobalLayoutListener(new ViewTreeObserver.OnGlobalLayoutListener() {
            @Override
            public void onGlobalLayout() {
                sign_in();
                findViewById(R.id.main).getViewTreeObserver().removeOnGlobalLayoutListener(this);
            }
        });
    }

    /**
     * Load the main layout
     * @param userid Username for the account
     */
    public void load_layout(String userid) {
        ValueEventListener userListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    if(snapshot.getKey().equals(userid)) {
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

        TextView identifier = findViewById(R.id.identifier);
        identifier.setText(userid);
        Activity reference = this;

        ValueEventListener stationListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // Get Station objects and use the values to update the UI
                sReference.clear();
                List<String> station_vals = new ArrayList<>();
                if (username.stations == null ) {
                    username.stations = new ArrayList<>();
                }
                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    if (username.stations.contains(snapshot.getKey()) || username.isAdmin) {
                        station_vals.add(snapshot.getKey());
                        sReference.add(snapshot.getValue(Station.class));
                    }
                }

                ArrayAdapter<String> adapter = new ArrayAdapter<>(reference,
                        android.R.layout.simple_spinner_item, station_vals);
                adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                selection.setAdapter(adapter);
                selection.setSelection(selected_index);
            }

            @Override
            public void onCancelled(DatabaseError databaseError) {
                // Getting Post failed, log a message
                Log.w(TAG, "loadStation:onCancelled", databaseError.toException());
            }
        };
        stationRef.addValueEventListener(stationListener);
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
            for (User tempuser : userList) {
                if (tempuser.passwordHASH.equals(password)) {
                    return true;
                }
            }
        }
        return false;
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
            userRef.child(tempUser.username).setValue(tempUser);
            return true;
        }
        return false;
    }

    /**
     * Update display values for the main view
     * @param index: index for which station is selected
     */
    public void update_values(int index) {
        Station selected_station = sReference.get(index);

        TextView humidity = findViewById(R.id.humidity);
        humidity.setText(String.valueOf(selected_station.humidity));

        EditText cupSize = findViewById(R.id.cupSize);
        cupSize.setText(String.valueOf(selected_station.cupSize));


    }

    /**
     * Send a custom message to desired station
     */
    public void custom_message(View view) {
        LayoutInflater inflater = (LayoutInflater)
                getSystemService(LAYOUT_INFLATER_SERVICE);
        assert inflater != null;
        View messageView = inflater.inflate(R.layout.message, findViewById(R.id.main), false);
        int width = ConstraintLayout.LayoutParams.MATCH_PARENT;
        int height = ConstraintLayout.LayoutParams.MATCH_PARENT;
        final PopupWindow messageWindow = new PopupWindow(messageView, width, height, true);
        messageWindow.setOutsideTouchable(true);
        messageWindow.setElevation(20);

        Spinner user_select = messageView.findViewById(R.id.friend_select);
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, users);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        user_select.setAdapter(adapter);
        user_select.setSelection(users.indexOf(username.username));

        Spinner station_select = messageView.findViewById(R.id.station_select);

        user_select.setOnItemSelectedListener( new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parentView, View selectedItemView, int position, long id) {
                set_message_stations(userList.get(user_select.getSelectedItemPosition()), station_select);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parentView) {
            }
        });

        EditText message = messageView.findViewById(R.id.user_text);
        Button message_button = messageView.findViewById(R.id.send_message);

        message_button.setOnClickListener(v -> {
            messageRef.push().setValue(new Message(username.username, station_select.getSelectedItem().toString(), message.getText().toString()));
            messageWindow.dismiss();
        });

        messageWindow.showAtLocation(findViewById(R.id.main), Gravity.CENTER, 0, 0);
    }

    /**
     * Set stations to select from for the message spinner
     * @param selected_user User currently selected
     * @param station_select Spinner to set values for
     */
    public void set_message_stations(User selected_user, Spinner station_select){
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, selected_user.stations);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        station_select.setAdapter(adapter);
    }

    /**
     * Create popup that you can register a new station with
     * @param view Main view for the button click
     */
    public void register_station_view(View view) {
        LayoutInflater inflater = (LayoutInflater)
                getSystemService(LAYOUT_INFLATER_SERVICE);
        assert inflater != null;
        View registerView = inflater.inflate(R.layout.register, findViewById(R.id.main), false);
        int width = ConstraintLayout.LayoutParams.MATCH_PARENT;
        int height = ConstraintLayout.LayoutParams.MATCH_PARENT;
        final PopupWindow optionsWindow = new PopupWindow(registerView, width, height, true);
        optionsWindow.setOutsideTouchable(true);
        optionsWindow.setElevation(20);
        EditText station_name = registerView.findViewById(R.id.station_text);
        Button message_button = registerView.findViewById(R.id.register_station);

        TextView errortext = registerView.findViewById(R.id.error_text);

        message_button.setOnClickListener(v -> {
            if(register_station(station_name.getText().toString())) {
                errortext.setText("Successfully added station!");
            }
            else {
                errortext.setText("Error adding station");
            }
        });

        optionsWindow.showAtLocation(findViewById(R.id.main), Gravity.CENTER, 0, 0);
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
            userRef.child(username.username).setValue(username);
            return true;
        }
        else {
            return false;
        }
    }

    /**
     * Update cupSize for selected child
     */
    public void update_cupSize(View v) {
        EditText cupSize = findViewById(R.id.cupSize);
        stationRef.child(sReference.get(selected_index).id).child("cupSize").setValue(cupSize.getText().toString());
    }

    /**
     * Load user options and information
     * @param view The main view for the button click
     */
    public void load_options(View view) {
        // display options
        LayoutInflater inflater = (LayoutInflater)
                getSystemService(LAYOUT_INFLATER_SERVICE);
        assert inflater != null;
        View optionsView = inflater.inflate(R.layout.user_options, findViewById(R.id.main), false);
        int width = ConstraintLayout.LayoutParams.MATCH_PARENT;
        int height = ConstraintLayout.LayoutParams.MATCH_PARENT;
        final PopupWindow optionsWindow = new PopupWindow(optionsView, width, height, true);
        optionsWindow.setOutsideTouchable(true);
        optionsWindow.setElevation(20);
        Button message_button = optionsView.findViewById(R.id.logout);

        message_button.setOnClickListener(v -> {
            log_out();
            optionsWindow.dismiss();
            sign_in();
        });

        optionsWindow.showAtLocation(findViewById(R.id.main), Gravity.CENTER, 0, 0);
        // update userRef parts
    }

    /**
     * log in info for system
     */
    public void sign_in() {
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

        String userid = settings.getString("userid", null);
        if (userid == null) {
            LayoutInflater confirminflater = (LayoutInflater)
                    getSystemService(LAYOUT_INFLATER_SERVICE);
            assert confirminflater != null;
            View loginView = confirminflater.inflate(R.layout.login, findViewById(R.id.main), false);
            int width = ConstraintLayout.LayoutParams.MATCH_PARENT;
            int height = ConstraintLayout.LayoutParams.MATCH_PARENT;
            final PopupWindow loginWindow = new PopupWindow(loginView, width, height, true);
            loginWindow.setOutsideTouchable(false);
            loginWindow.setElevation(20);
            EditText username = loginView.findViewById(R.id.user_text);
            EditText password = loginView.findViewById(R.id.pass_text);
            TextView error = loginView.findViewById(R.id.error);

            loginView.findViewById(R.id.create_account).setOnClickListener(v -> {
                if (create_account(username.getText().toString(), password.getText().toString())) {
                    SharedPreferences.Editor editor = settings.edit();
                    editor.putString("userid", username.getText().toString());
                    editor.apply();
                    loginWindow.dismiss();
                }
                else {
                    error.setText(R.string.account_error);
                }
            });

            loginView.findViewById(R.id.login).setOnClickListener(v -> {
                if (login(username.getText().toString(), password.getText().toString())) {
                    SharedPreferences.Editor editor = settings.edit();
                    editor.putString("userid", username.getText().toString());
                    editor.apply();
                    loginWindow.dismiss();
                }
                else {
                    error.setText(R.string.login_error);
                }
            });
            loginWindow.setOnDismissListener(() -> load_layout(username.getText().toString()));
            loginWindow.showAtLocation(loginView, Gravity.CENTER, 0, 0);
        }
        else {
            load_layout(userid);
        }
    }

    /**
     * log out of account
     */
    public void log_out() {
        SharedPreferences.Editor editor = settings.edit();
        editor.putString("userid", null);
        editor.apply();
    }
}