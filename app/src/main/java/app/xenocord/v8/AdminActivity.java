package app.xenocord.v8;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ClipboardManager;
import android.content.ClipData;
import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Locale;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public final class AdminActivity extends Activity {
    private static final int BG = Color.rgb(11,11,18), PANEL = Color.rgb(22,22,34);
    private static final int TEXT = Color.rgb(245,244,255), MUTED = Color.rgb(160,159,180), ACCENT = Color.rgb(155,123,255);
    private static final String PREFS = "hellenstar_owner_settings";
    private static final String PASS_KEY = "owner_password_pbkdf2", SALT_KEY = "owner_password_salt";
    // PBKDF2-SHA256, 180k rounds. Change this password after first unlock.
    private static final String DEFAULT_SALT = "7af59a76ec4ed580a304c13d011ab9f6";
    private static final String DEFAULT_HASH = "a84cf91258698f8110ac477dda3d125f0811e93837f5e6bedab707cd539eef2a";
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
        root.addView(text("HELLENSTAR / PRIVATE AREA",12,ACCENT,true));
        root.addView(text("Owner authentication",27,TEXT,true),lp(-1,-2,0,10,0,6));
        root.addView(text("Unlock the local owner console. This password is separate from your phone lock.",13,MUTED,false),lp(-1,-2,0,0,0,18));
        EditText password = new EditText(this);
        password.setSingleLine(true); password.setHint("Owner password"); password.setHintTextColor(MUTED);
        password.setTextColor(TEXT); password.setInputType(129); password.setPadding(dp(14),dp(12),dp(14),dp(12));
        password.setBackground(shape(PANEL,12)); root.addView(password,lp(-1,-2,0,0,0,12));
        Button login = button("UNLOCK ADMIN PANEL"); root.addView(login,lp(-1,52,0,0,0,10));
        login.setOnClickListener(v -> {
            if (attempts >= MAX_ATTEMPTS) { Toast.makeText(this,"Too many attempts. Reopen the panel to retry.",Toast.LENGTH_LONG).show(); return; }
            String salt = prefs.getString(SALT_KEY,DEFAULT_SALT);
            String expected = prefs.getString(PASS_KEY,DEFAULT_HASH);
            if (constantTimeEquals(pbkdf2(password.getText().toString(),salt),expected)) {
                attempts=0; log("Admin login successful"); showDashboard();
            } else {
                attempts++; password.setText("");
                Toast.makeText(this,"Incorrect password ("+attempts+"/"+MAX_ATTEMPTS+")",Toast.LENGTH_SHORT).show();
                log("Failed admin login attempt");
            }
        });
        Button back=button("BACK TO AUDIO LAB"); root.addView(back,lp(-1,48,0,0,0,0)); back.setOnClickListener(v->finish());
        root.addView(text("Offline security note: this is an app-level lock, not server-enforced identity. Someone with the APK can modify it. Do not reuse another account's password.",11,MUTED,false),lp(-1,-2,0,18,0,0));
    }

    private void showDashboard() {
        LinearLayout root=base();
        root.addView(text("HELLENSTAR / OWNER CONSOLE",12,ACCENT,true));
        root.addView(text("Admin panel",29,TEXT,true),lp(-1,-2,0,8,0,4));
        root.addView(text("Local controls • diagnostics • audit trail",13,MUTED,false),lp(-1,-2,0,0,0,16));

        LinearLayout device=card(); root.addView(device,lp(-1,-2,0,0,0,12));
        device.addView(text("DEVICE & BUILD",12,ACCENT,true));
        device.addView(text("Brand: "+Build.BRAND+"\nModel: "+Build.MODEL+"\nAndroid: "+Build.VERSION.RELEASE+" (API "+Build.VERSION.SDK_INT+")\nPackage: "+getPackageName()+"\nCPU ABI: "+Build.SUPPORTED_ABIS[0],13,TEXT,false),lp(-1,-2,0,10,0,0));
        addButton(device,"COPY DIAGNOSTICS",v->{
            String report="Hellenstar local diagnostics\nDevice: "+Build.BRAND+" "+Build.MODEL+"\nAndroid: "+Build.VERSION.RELEASE+" / API "+Build.VERSION.SDK_INT+"\nPackage: "+getPackageName()+"\nEffects enabled: "+prefs.getBoolean("device_effects_enabled",true)+"\nTest tone enabled: "+prefs.getBoolean("test_tone_enabled",true)+"\nAdvanced controls: "+prefs.getBoolean("advanced_controls_enabled",true);
            ClipboardManager cm=(ClipboardManager)getSystemService(CLIPBOARD_SERVICE);
            cm.setPrimaryClip(ClipData.newPlainText("Hellenstar diagnostics",report));
            Toast.makeText(this,"Diagnostics copied to clipboard.",Toast.LENGTH_SHORT).show(); log("Diagnostics copied");
        });

        LinearLayout controls=card(); root.addView(controls,lp(-1,-2,0,0,0,12));
        controls.addView(text("APP CONTROLS",12,ACCENT,true));
        addToggle(controls,"Allow local test tone","test_tone_enabled",true);
        addToggle(controls,"Enable Android audio effects","device_effects_enabled",true);
        addToggle(controls,"Show advanced presets","advanced_controls_enabled",true);
        addButton(controls,"CHANGE OWNER PASSWORD",v->changePassword());
        addButton(controls,"RESET APP CONTROLS",v->confirmReset());

        LinearLayout audit=card(); root.addView(audit,lp(-1,-2,0,0,0,12));
        audit.addView(text("RECENT ADMIN ACTIVITY",12,ACCENT,true));
        String entries=prefs.getString("audit_log","No admin actions recorded yet.");
        audit.addView(text(entries,12,MUTED,false),lp(-1,-2,0,8,0,0));
        addButton(audit,"CLEAR AUDIT LOG",v->{prefs.edit().putString("audit_log","Audit log cleared.").apply(); log("Audit log cleared"); showDashboard();});

        Button close=button("LOCK ADMIN PANEL"); root.addView(close,lp(-1,50,0,0,0,0)); close.setOnClickListener(v->{log("Admin panel locked");finish();});
    }

    private void addToggle(LinearLayout parent,String label,String key,boolean fallback) {
        android.widget.Switch sw=new android.widget.Switch(this); sw.setText(label); sw.setTextColor(TEXT);
        sw.setPadding(0,dp(8),0,dp(8)); sw.setChecked(prefs.getBoolean(key,fallback));
        sw.setOnCheckedChangeListener((b,on)->{prefs.edit().putBoolean(key,on).apply();log(label+(on?" enabled":" disabled"));Toast.makeText(this,label+(on?" enabled":" disabled"),Toast.LENGTH_SHORT).show();});
        parent.addView(sw,lp(-1,-2,0,4,0,0));
    }

    private void changePassword() {
        LinearLayout box=new LinearLayout(this); box.setOrientation(LinearLayout.VERTICAL); box.setPadding(dp(20),dp(8),dp(20),0);
        EditText a=new EditText(this); a.setHint("New password (12+ characters)"); a.setInputType(129);
        EditText b=new EditText(this); b.setHint("Repeat new password"); b.setInputType(129); box.addView(a);box.addView(b);
        new AlertDialog.Builder(this).setTitle("Change owner password").setView(box).setNegativeButton("Cancel",(d,w)->{})
        .setPositiveButton("Save",(d,w)->{
            String one=a.getText().toString(),two=b.getText().toString();
            if(one.length()<12||!one.equals(two)){Toast.makeText(this,"Passwords must match and contain at least 12 characters.",Toast.LENGTH_LONG).show();return;}
            byte[] salt=new byte[16];new SecureRandom().nextBytes(salt);String saltHex=toHex(salt);
            prefs.edit().putString(SALT_KEY,saltHex).putString(PASS_KEY,pbkdf2(one,saltHex)).apply();
            log("Owner password changed");Toast.makeText(this,"Owner password changed on this device.",Toast.LENGTH_LONG).show();
        }).show();
    }

    private void confirmReset() {
        new AlertDialog.Builder(this).setTitle("Reset app controls?")
        .setMessage("Resets the three app toggles to their defaults. It does not reset your owner password.")
        .setNegativeButton("Cancel",(d,w)->{}).setPositiveButton("Reset",(d,w)->{
            prefs.edit().remove("test_tone_enabled").remove("device_effects_enabled").remove("advanced_controls_enabled").apply();
            log("App controls reset");showDashboard();
        }).show();
    }

    private String pbkdf2(String value,String saltHex) {
        try {
            PBEKeySpec spec=new PBEKeySpec(value.toCharArray(),fromHex(saltHex),180000,256);
            byte[] out=SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256").generateSecret(spec).getEncoded();
            spec.clearPassword();return toHex(out);
        } catch(Exception e){return "";}
    }
    private byte[] fromHex(String s) {
        byte[] out=new byte[s.length()/2];for(int i=0;i<out.length;i++)out[i]=(byte)Integer.parseInt(s.substring(i*2,i*2+2),16);return out;
    }
    private String toHex(byte[] data) {
        StringBuilder out=new StringBuilder();for(byte b:data)out.append(String.format(Locale.US,"%02x",b&255));return out.toString();
    }
    private boolean constantTimeEquals(String a,String b) {
        if(a==null||b==null)return false;return MessageDigest.isEqual(a.getBytes(StandardCharsets.UTF_8),b.getBytes(StandardCharsets.UTF_8));
    }
    private void log(String item) {
        String old=prefs.getString("audit_log","");String line=java.text.DateFormat.getDateTimeInstance().format(new java.util.Date())+" — "+item;
        String next=line+(old.isEmpty()?"":"\n"+old);String[] lines=next.split("\n");StringBuilder trimmed=new StringBuilder();
        for(int i=0;i<Math.min(8,lines.length);i++){if(i>0)trimmed.append('\n');trimmed.append(lines[i]);}
        prefs.edit().putString("audit_log",trimmed.toString()).apply();
    }
    private LinearLayout base() {
        ScrollView scroll=new ScrollView(this);scroll.setFillViewport(true);scroll.setBackgroundColor(BG);
        LinearLayout root=new LinearLayout(this);root.setOrientation(LinearLayout.VERTICAL);root.setPadding(dp(20),dp(22),dp(20),dp(28));
        scroll.addView(root);setContentView(scroll);return root;
    }
    private LinearLayout card(){LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);box.setPadding(dp(16),dp(16),dp(16),dp(16));box.setBackground(shape(PANEL,18));return box;}
    private TextView text(String value,int size,int color,boolean bold){TextView t=new TextView(this);t.setText(value);t.setTextSize(size);t.setTextColor(color);if(bold)t.setTypeface(Typeface.DEFAULT,Typeface.BOLD);return t;}
    private Button button(String label){Button b=new Button(this);b.setText(label);b.setTextColor(TEXT);b.setTextSize(12);b.setAllCaps(false);b.setBackground(shape(Color.rgb(43,38,65),12));return b;}
    private void addButton(LinearLayout parent,String label,View.OnClickListener listener){Button b=button(label);b.setOnClickListener(listener);parent.addView(b,lp(-1,48,0,8,0,0));}
    private GradientDrawable shape(int color,int radius){GradientDrawable d=new GradientDrawable();d.setColor(color);d.setCornerRadius(dp(radius));return d;}
    private LinearLayout.LayoutParams lp(int w,int h,int l,int t,int r,int b){LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(w<0?w:dp(w),h<0?h:dp(h));p.setMargins(dp(l),dp(t),dp(r),dp(b));return p;}
    private int dp(int n){return Math.round(n*getResources().getDisplayMetrics().density);}
}
