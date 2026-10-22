package app.xenocord.v8;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Locale;

public final class AdminActivity extends Activity {
    private static final int BG = Color.rgb(11, 11, 18);
    private static final int PANEL = Color.rgb(22, 22, 34);
    private static final int TEXT = Color.rgb(245, 244, 255);
    private static final int MUTED = Color.rgb(160, 159, 180);
    private static final int ACCENT = Color.rgb(155, 123, 255);
    private static final String PREFS = "hellenstar_owner_settings";
    private static final String PASS_KEY = "owner_password_sha256";
    private static final String DEFAULT_HASH = "4dbaf4dab1f7293a6b6c5eef766f36b78dd852c7b173915f2f8ed639e6a689b5";
    private static final int MAX_ATTEMPTS = 5;
    private SharedPreferences prefs;
    private int attempts = 0;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        prefs = getSharedPreferences(PREFS, Context.MODE_PRIVATE);
        getWindow().setStatusBarColor(BG);
        getWindow().setNavigationBarColor(BG);
        showLogin();
    }

    private void showLogin() {
        LinearLayout root = base();
        root.addView(text("HELLENSTAR / PRIVATE AREA", 12, ACCENT, true));
        root.addView(text("Owner authentication", 27, TEXT, true), lp(-1, -2, 0, 10, 0, 6));
        root.addView(text("This panel is local to this app installation. Enter the owner password to continue.", 13, MUTED, false), lp(-1, -2, 0, 0, 0, 18));
        EditText password = new EditText(this);
        password.setSingleLine(true);
        password.setHint("Owner password");
        password.setHintTextColor(MUTED);
        password.setTextColor(TEXT);
        password.setInputType(129);
        password.setPadding(dp(14), dp(12), dp(14), dp(12));
        password.setBackground(shape(PANEL, 12));
        root.addView(password, lp(-1, -2, 0, 0, 0, 12));
        Button login = button("UNLOCK ADMIN PANEL");
        root.addView(login, lp(-1, 52, 0, 0, 0, 10));
        login.setOnClickListener(v -> {
            if (attempts >= MAX_ATTEMPTS) {
                Toast.makeText(this, "Too many attempts. Close and reopen the panel to retry.", Toast.LENGTH_LONG).show();
                return;
            }
            String entered = password.getText().toString();
            String stored = prefs.getString(PASS_KEY, DEFAULT_HASH);
            if (constantTimeEquals(hash(entered), stored)) {
                attempts = 0;
                showDashboard();
            } else {
                attempts++;
                password.setText("");
                Toast.makeText(this, "Incorrect password (" + attempts + "/" + MAX_ATTEMPTS + ")", Toast.LENGTH_SHORT).show();
            }
        });
        Button back = button("BACK TO AUDIO LAB");
        root.addView(back, lp(-1, 48, 0, 0, 0, 0));
        back.setOnClickListener(v -> finish());
        root.addView(text("Security note: because this is a standalone offline APK, this is an app-level lock, not server-enforced identity security.", 11, MUTED, false), lp(-1, -2, 0, 18, 0, 0));
        setContentView(root);
    }

    private void showDashboard() {
        LinearLayout root = base();
        root.addView(text("HELLENSTAR / OWNER CONSOLE", 12, ACCENT, true));
        root.addView(text("Admin panel", 29, TEXT, true), lp(-1, -2, 0, 8, 0, 4));
        root.addView(text("Private controls and local diagnostics", 13, MUTED, false), lp(-1, -2, 0, 0, 0, 16));

        LinearLayout device = card();
        root.addView(device, lp(-1, -2, 0, 0, 0, 12));
        device.addView(text("DEVICE & BUILD", 12, ACCENT, true));
        device.addView(text("Brand: " + Build.BRAND + "\nModel: " + Build.MODEL + "\nAndroid: " + Build.VERSION.RELEASE + " (API " + Build.VERSION.SDK_INT + ")\nApp ID: " + getPackageName() + "\nAdmin storage: local SharedPreferences", 13, TEXT, false), lp(-1, -2, 0, 10, 0, 0));

        LinearLayout tools = card();
        root.addView(tools, lp(-1, -2, 0, 0, 0, 12));
        tools.addView(text("OWNER TOOLS", 12, ACCENT, true));
        addToggle(tools, "Diagnostics flag", "diagnostics_enabled", false);
        addToggle(tools, "Experimental UI flag", "experimental_ui_enabled", false);
        addToggle(tools, "Verbose local status", "verbose_status_enabled", false);
        addButton(tools, "CHANGE OWNER PASSWORD", v -> changePassword());
        addButton(tools, "RESET LOCAL PREFERENCES", v -> confirmReset());

        LinearLayout info = card();
        root.addView(info, lp(-1, -2, 0, 0, 0, 12));
        info.addView(text("CURRENT FLAGS", 12, ACCENT, true));
        info.addView(text("Diagnostics: " + enabled("diagnostics_enabled") + "\nExperimental UI: " + enabled("experimental_ui_enabled") + "\nVerbose status: " + enabled("verbose_status_enabled"), 13, TEXT, false), lp(-1, -2, 0, 8, 0, 0));

        Button close = button("LOCK ADMIN PANEL");
        root.addView(close, lp(-1, 50, 0, 0, 0, 0));
        close.setOnClickListener(v -> finish());
        setContentView(root);
    }

    private void addToggle(LinearLayout parent, String label, String key, boolean defaultValue) {
        android.widget.Switch toggle = new android.widget.Switch(this);
        toggle.setText(label);
        toggle.setTextColor(TEXT);
        toggle.setPadding(0, dp(8), 0, dp(8));
        toggle.setChecked(prefs.getBoolean(key, defaultValue));
        toggle.setOnCheckedChangeListener((button, checked) -> {
            prefs.edit().putBoolean(key, checked).apply();
            Toast.makeText(this, label + (checked ? " enabled" : " disabled"), Toast.LENGTH_SHORT).show();
        });
        parent.addView(toggle, lp(-1, -2, 0, 4, 0, 0));
    }

    private boolean enabled(String key) {
        return prefs.getBoolean(key, false) ? "ON" : "OFF";
    }

    private void changePassword() {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(20), dp(8), dp(20), 0);
        EditText first = new EditText(this);
        first.setHint("New password (12+ characters)");
        first.setInputType(129);
        EditText second = new EditText(this);
        second.setHint("Repeat new password");
        second.setInputType(129);
        box.addView(first);
        box.addView(second);
        new AlertDialog.Builder(this).setTitle("Change owner password").setView(box)
            .setNegativeButton("Cancel", (d, w) -> {})
            .setPositiveButton("Save", (d, w) -> {
                String a = first.getText().toString();
                String b = second.getText().toString();
                if (a.length() < 12 || !a.equals(b)) {
                    Toast.makeText(this, "Passwords must match and contain at least 12 characters.", Toast.LENGTH_LONG).show();
                    return;
                }
                prefs.edit().putString(PASS_KEY, hash(a)).apply();
                Toast.makeText(this, "Owner password updated on this device.", Toast.LENGTH_LONG).show();
            }).show();
    }

    private void confirmReset() {
        new AlertDialog.Builder(this).setTitle("Reset local settings?")
            .setMessage("This resets admin flags and the owner password to the initial password. It does not delete app files.")
            .setNegativeButton("Cancel", (d, w) -> {})
            .setPositiveButton("Reset", (d, w) -> {
                prefs.edit().clear().apply();
                Toast.makeText(this, "Local settings reset.", Toast.LENGTH_SHORT).show();
                showDashboard();
            }).show();
    }

    private String hash(String value) {
        try {
            byte[] bytes = MessageDigest.getInstance("SHA-256").digest(value.getBytes(StandardCharsets.UTF_8));
            StringBuilder out = new StringBuilder();
            for (byte b : bytes) out.append(String.format(Locale.US, "%02x", b & 0xff));
            return out.toString();
        } catch (Exception e) { return ""; }
    }

    private boolean constantTimeEquals(String a, String b) {
        if (a == null || b == null) return false;
        return MessageDigest.isEqual(a.getBytes(StandardCharsets.UTF_8), b.getBytes(StandardCharsets.UTF_8));
    }

    private LinearLayout base() {
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(BG);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(20), dp(22), dp(20), dp(28));
        scroll.addView(root);
        setContentView(scroll);
        return root;
    }

    private LinearLayout card() {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(16), dp(16), dp(16), dp(16));
        box.setBackground(shape(PANEL, 18));
        return box;
    }

    private TextView text(String value, int size, int color, boolean bold) {
        TextView t = new TextView(this);
        t.setText(value);
        t.setTextSize(size);
        t.setTextColor(color);
        if (bold) t.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        return t;
    }

    private Button button(String label) {
        Button b = new Button(this);
        b.setText(label);
        b.setTextColor(TEXT);
        b.setTextSize(12);
        b.setAllCaps(false);
        b.setBackground(shape(Color.rgb(43, 38, 65), 12));
        return b;
    }

    private void addButton(LinearLayout parent, String label, View.OnClickListener listener) {
        Button b = button(label);
        b.setOnClickListener(listener);
        parent.addView(b, lp(-1, 48, 0, 8, 0, 0));
    }

    private GradientDrawable shape(int color, int radius) {
        GradientDrawable d = new GradientDrawable();
        d.setColor(color);
        d.setCornerRadius(dp(radius));
        return d;
    }

    private LinearLayout.LayoutParams lp(int width, int height, int left, int top, int right, int bottom) {
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(width < 0 ? width : dp(width), height < 0 ? height : dp(height));
        p.setMargins(dp(left), dp(top), dp(right), dp(bottom));
        return p;
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
}
