

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
import com.google.firebase.database.ValueEventListener;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Main Activity for Water Buddy Smart Application
 * Tutorials used:
 * https://firebase.google.com/docs/database/android/read-and-write
 */
public class MainActivity extends AppCompatActivity {

    private ArrayList<Station> sReference;
    private Spinner selection;
    private int selected_index;
    private DatabaseInterface dbInterface;

    public static final String PREFS_NAME = "MyPrefsFile";
    static SharedPreferences settings;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        settings = getSharedPreferences(PREFS_NAME, 0);

        dbInterface = new DatabaseInterface();


        sReference = new ArrayList<>();
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
        dbInterface.load(userid);

        TextView identifier = findViewById(R.id.identifier);
        identifier.setText(userid);
        Activity reference = this;

        ValueEventListener stationListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // Get Station objects and use the values to update the UI
                sReference.clear();
                List<String> station_vals = new ArrayList<>();
                if (dbInterface.username.stations == null ) {
                    dbInterface.username.stations = new ArrayList<>();
                }
                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    if (dbInterface.username.stations.contains(snapshot.getKey())
                            || dbInterface.username.isAdmin) {
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
        dbInterface.stationRef.addValueEventListener(stationListener);
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
                android.R.layout.simple_spinner_item, dbInterface.users);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        user_select.setAdapter(adapter);
        user_select.setSelection(dbInterface.users.indexOf(dbInterface.username.userID));

        Spinner station_select = messageView.findViewById(R.id.station_select);

        user_select.setOnItemSelectedListener( new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parentView, View selectedItemView, int position, long id) {
                set_message_stations(dbInterface.userList.get(user_select.getSelectedItemPosition()), station_select);
            }

            @Override
            public void onNothingSelected(AdapterView<?> parentView) {
            }
        });

        EditText message = messageView.findViewById(R.id.user_text);
        Button message_button = messageView.findViewById(R.id.send_message);

        message_button.setOnClickListener(v -> {
            dbInterface.messageRef.push().setValue(new Message(dbInterface.username.userID,
                    station_select.getSelectedItem().toString(), message.getText().toString()));
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
        if (selected_user.stations == null) {
            selected_user.stations = new ArrayList<>();
        }
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
            if(dbInterface.register_station(station_name.getText().toString())) {
                errortext.setText(R.string.register_success);
            }
            else {
                errortext.setText(R.string.register_fail);
            }
        });

        optionsWindow.showAtLocation(findViewById(R.id.main), Gravity.CENTER, 0, 0);
    }

    /**
     * Update cupSize for selected child
     */
    public void update_cupSize(View v) {
        EditText cupSize = findViewById(R.id.cupSize);
        dbInterface.stationRef.child(sReference.get(selected_index).stationID).child("cupSize").setValue(Double.parseDouble(cupSize.getText().toString()));
    }

    /**
     * Load user options and information
     * @param view The main view for the button click
     */
    public void load_options(View view) {
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
        Button settings_button = optionsView.findViewById(R.id.settings_button);
        Button friend_add = optionsView.findViewById(R.id.friend_add);

        EditText user_height = optionsView.findViewById(R.id.height);
        EditText user_weight = optionsView.findViewById(R.id.weight);
        EditText friend_id = optionsView.findViewById(R.id.friend_id);

        Spinner thirst = optionsView.findViewById(R.id.thirst);
        ArrayList<String> thirst_list = new ArrayList<>();

        Collections.addAll(thirst_list, "Hydrophobic", "Average", "Thirsty", "Parched");
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this,
                android.R.layout.simple_spinner_item, thirst_list);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        thirst.setAdapter(adapter);
        thirst.setSelection(dbInterface.username.thirst);

        TextView friend_message = optionsView.findViewById(R.id.friend_message);

        message_button.setOnClickListener(v -> {
            log_out();
            optionsWindow.dismiss();
            sign_in();
        });

        settings_button.setOnClickListener(v -> {
            dbInterface.username.height = Double.parseDouble(user_height.getText().toString());
            dbInterface.username.weight = Double.parseDouble(user_weight.getText().toString());
            dbInterface.username.thirst = thirst.getSelectedItemPosition();
            dbInterface.userRef.child(dbInterface.username.userID).setValue(dbInterface.username);
        });

        friend_add.setOnClickListener(v -> {
            String message = "Please enter an id";
            if (!friend_id.getText().toString().equals("")) {
                message = dbInterface.add_friend(friend_id.getText().toString());
            }
            friend_message.setText(message);
        });

        optionsWindow.showAtLocation(findViewById(R.id.main), Gravity.CENTER, 0, 0);
    }

    /**
     * log in info for system
     */
    public void sign_in() {
        dbInterface.sign_in();

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
                if (dbInterface.create_account(username.getText().toString(), password.getText().toString())) {
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
                if (dbInterface.login(username.getText().toString(), password.getText().toString())) {
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