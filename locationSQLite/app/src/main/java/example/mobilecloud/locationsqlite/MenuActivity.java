package example.mobilecloud.locationsqlite;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;

public class MenuActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
    }
    // for onclick - goes to activity
    protected void goToActivity(View v) {
        Intent intent = new Intent(MenuActivity.this, locationSQLite.class);
        startActivity(intent);
    }

}
