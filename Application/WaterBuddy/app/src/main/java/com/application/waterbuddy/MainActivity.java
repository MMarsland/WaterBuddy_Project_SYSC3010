

package com.application.waterbuddy;

import static android.content.ContentValues.TAG;
import androidx.appcompat.app.AppCompatActivity;
import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Spinner;
import android.widget.TextView;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import java.util.ArrayList;
import java.util.List;

/** Tutorials used:
 * https://firebase.google.com/docs/database/android/read-and-write
 */
public class MainActivity extends AppCompatActivity {

    private DatabaseReference myRef;
    private ArrayList<Station> sReference;
    private Spinner selection;
    private int selected_index;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        FirebaseDatabase database = FirebaseDatabase.getInstance();

        myRef = database.getReference("users");

        Activity reference = this;
        sReference = new ArrayList<>();
        selected_index = 0;

        selection = findViewById(R.id.selector);
        ValueEventListener stationListener = new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot dataSnapshot) {
                // Get Station objects and use the values to update the UI
                sReference.clear();
                List<String> user_vals = new ArrayList<>();
                for (DataSnapshot snapshot : dataSnapshot.getChildren()) {
                    user_vals.add(snapshot.getKey());
                    sReference.add(snapshot.getValue(Station.class));
                }

                ArrayAdapter<String> adapter = new ArrayAdapter<>(reference,
                        android.R.layout.simple_spinner_item, user_vals);
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
        myRef.addValueEventListener(stationListener);

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

    }

    /**
     * Set value for a child in the database
     * @param view: Current activity view
     */
    public void change_db(View view) {

        Station station1 = new Station("thing1", "thing2");
        myRef.child("station2").setValue(station1);
    }

    /**
     * Update display values for the main view
     * @param index: index for which station is selected
     */
    public void update_values(int index) {
        Station selected_station = sReference.get(index);

        TextView val1 = findViewById(R.id.val1);
        val1.setText(selected_station.data1);

        TextView val2 = findViewById(R.id.val2);
        val2.setText(selected_station.data2);

    }
}