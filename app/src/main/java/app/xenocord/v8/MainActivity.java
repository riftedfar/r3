package app.xenocord.v8;

import android.app.Activity;
import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.media.audiofx.BassBoost;
import android.media.audiofx.Equalizer;
import android.media.audiofx.LoudnessEnhancer;
import android.media.audiofx.Virtualizer;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;
import java.util.Locale;
import java.util.concurrent.atomic.AtomicBoolean;

public final class MainActivity extends Activity {
    private static final int BG = Color.rgb(11, 11, 18);
    private static final int PANEL = Color.rgb(22, 22, 34);
    private static final int TEXT = Color.rgb(245, 244, 255);
    private static final int MUTED = Color.rgb(160, 159, 180);
    private static final int ACCENT = Color.rgb(155, 123, 255);
    private static final int SAMPLE_RATE = 44100;

    private AudioTrack track;
    private Thread toneThread;
    private final AtomicBoolean playing = new AtomicBoolean(false);
    private BassBoost bassBoost;
    private Virtualizer virtualizer;
    private Equalizer equalizer;
    private LoudnessEnhancer loudnessEnhancer;
    private SeekBar pitchBar;
    private SeekBar gainBar;
    private SeekBar bassBar;
    private SeekBar widthBar;
    private TextView playButton;
    private TextView statusText;
    private volatile int frequency = 440;
    private volatile int level = 65;

    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(BG);
        getWindow().setNavigationBarColor(BG);
        getWindow().getDecorView().setSystemUiVisibility(0);
        buildUi();
    }

    private void buildUi() {
        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(BG);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(20), dp(18), dp(20), dp(28));
        scroll.addView(root);
        setContentView(scroll);

        TextView brand = text("HELLENSTAR / AUDIO LAB", 12, ACCENT, true);
        brand.setLetterSpacing(0.16f);
        root.addView(brand, params(-1, -2, 0, 0, 0, 8));

        TextView title = text("Hellenstar", 32, TEXT, true);
        root.addView(title);
        TextView version = text("V8  •  LOCAL AUDIO CONTROLS", 12, MUTED, true);
        root.addView(version, params(-1, -2, 0, 2, 0, 20));

        LinearLayout hero = card();
        root.addView(hero, params(-1, -2, 0, 0, 0, 14));
        TextView heroTitle = text("Audio workspace", 19, TEXT, true);
        hero.addView(heroTitle);
        TextView heroCopy = text("Tune a local test tone and preview supported device audio effects. No Discord login or network connection.", 13, MUTED, false);
        heroCopy.setLineSpacing(dp(3), 1f);
        hero.addView(heroCopy, params(-1, -2, 0, 8, 0, 14));

        playButton = text("▶   PLAY TEST TONE", 14, Color.WHITE, true);
        playButton.setGravity(Gravity.CENTER);
        playButton.setPadding(dp(16), dp(14), dp(16), dp(14));
        playButton.setBackground(shape(ACCENT, 16));
        playButton.setOnClickListener(v -> {
            if (playing.get()) stopTone(); else startTone();
        });
        hero.addView(playButton, params(-1, -2, 0, 0, 0, 8));

        statusText = text("READY  •  AUDIO STAYS INSIDE THIS APP", 11, MUTED, true);
        statusText.setGravity(Gravity.CENTER);
        hero.addView(statusText, params(-1, -2, 0, 3, 0, 0));

        LinearLayout tone = card();
        root.addView(tone, params(-1, -2, 0, 0, 0, 14));
        tone.addView(text("Tone & output", 18, TEXT, true));
        pitchBar = addSlider(tone, "Pitch", "440 Hz", 110, 880, 440, value -> {
            frequency = value;
        });
        gainBar = addSlider(tone, "Output level", "65%", 0, 100, 65, value -> {
            level = value;
            if (track != null) {
                float volume = value / 100f;
                try { track.setVolume(volume); } catch (IllegalStateException ignored) {}
            }
        });

        LinearLayout fx = card();
        root.addView(fx, params(-1, -2, 0, 0, 0, 14));
        fx.addView(text("Device effects", 18, TEXT, true));
        TextView note = text("Effects availability depends on your Android device. These affect only the test tone played by this app.", 12, MUTED, false);
        note.setLineSpacing(dp(2), 1f);
        fx.addView(note, params(-1, -2, 0, 6, 0, 10));
        bassBar = addSlider(fx, "Bass boost", "30%", 0, 100, 30, value -> setBass(value * 10));
        widthBar = addSlider(fx, "Stereo widening", "35%", 0, 100, 35, value -> setWidth(value * 10));
        addActionButton(fx, "RESET CONTROLS", v -> {
            pitchBar.setProgress(440 - 110);
            gainBar.setProgress(65);
            bassBar.setProgress(30);
            widthBar.setProgress(35);
            frequency = 440;
            level = 65;
            setBass(300);
            setWidth(350);
            if (track != null) try { track.setVolume(0.65f); } catch (IllegalStateException ignored) {}
        });

        LinearLayout safety = card();
        root.addView(safety, params(-1, -2, 0, 0, 0, 0));
        safety.addView(text("Privacy by design", 17, TEXT, true));
        TextView safetyCopy = text("No token/password fields • No microphone permission • No internet permission • No background process", 12, MUTED, false);
        safetyCopy.setLineSpacing(dp(3), 1f);
        safety.addView(safetyCopy, params(-1, -2, 0, 8, 0, 0));
        TextView limitation = text("Note: Android does not let an ordinary app automatically apply these effects to Discord's voice stream.", 12, ACCENT, false);
        limitation.setLineSpacing(dp(3), 1f);
        root.addView(limitation, params(-1, -2, 0, 16, 0, 0));
    }

    private interface ValueChange { void changed(int value); }

    private SeekBar addSlider(LinearLayout parent, String label, String valueText, int min, int max, int initial, ValueChange callback) {
        LinearLayout block = new LinearLayout(this);
        block.setOrientation(LinearLayout.VERTICAL);
        block.setPadding(0, dp(8), 0, dp(8));
        parent.addView(block, params(-1, -2, 0, 0, 0, 2));
        LinearLayout labels = new LinearLayout(this);
        labels.setGravity(Gravity.CENTER_VERTICAL);
        labels.setOrientation(LinearLayout.HORIZONTAL);
        block.addView(labels);
        TextView left = text(label, 13, TEXT, true);
        labels.addView(left, new LinearLayout.LayoutParams(0, -2, 1f));
        TextView right = text(valueText, 12, ACCENT, true);
        labels.addView(right);
        SeekBar bar = new SeekBar(this);
        bar.setMax(max - min);
        bar.setProgress(initial - min);
        bar.setProgressTintList(android.content.res.ColorStateList.valueOf(ACCENT));
        bar.setThumbTintList(android.content.res.ColorStateList.valueOf(Color.WHITE));
        block.addView(bar, params(-1, 34, 0, 2, 0, 0));
        bar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                int actual = progress + min;
                if (label.equals("Pitch")) right.setText(actual + " Hz");
                else right.setText(actual + "%");
                callback.changed(actual);
            }
            @Override public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override public void onStopTrackingTouch(SeekBar seekBar) {}
        });
        return bar;
    }

    private void startTone() {
        try {
            int minBuffer = AudioTrack.getMinBufferSize(SAMPLE_RATE, AudioFormat.CHANNEL_OUT_STEREO, AudioFormat.ENCODING_PCM_16BIT);
            if (minBuffer <= 0) throw new IllegalStateException("Audio output is unavailable on this device.");
            int bufferSize = Math.max(minBuffer, SAMPLE_RATE / 2);
            AudioFormat format = new AudioFormat.Builder()
                    .setEncoding(AudioFormat.ENCODING_PCM_16BIT)
                    .setSampleRate(SAMPLE_RATE)
                    .setChannelMask(AudioFormat.CHANNEL_OUT_STEREO)
                    .build();
            AudioAttributes attrs = new AudioAttributes.Builder()
                    .setUsage(AudioAttributes.USAGE_MEDIA)
                    .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                    .build();
            track = new AudioTrack.Builder()
                    .setAudioAttributes(attrs)
                    .setAudioFormat(format)
                    .setTransferMode(AudioTrack.MODE_STREAM)
                    .setBufferSizeInBytes(bufferSize)
                    .build();
            if (track.getState() != AudioTrack.STATE_INITIALIZED) throw new IllegalStateException("Could not initialize audio output.");
            attachEffects(track.getAudioSessionId());
            track.setVolume(level / 100f);
            track.play();
            playing.set(true);
            playButton.setText("■   STOP TEST TONE");
            statusText.setText("PLAYING  •  LOCAL TEST TONE");
            toneThread = new Thread(() -> {
                short[] samples = new short[2048];
                double phase = 0.0;
                try {
                    while (playing.get()) {
                        int hz = frequency;
                        double step = 2.0 * Math.PI * hz / SAMPLE_RATE;
                        for (int i = 0; i < samples.length; i += 2) {
                            short sample = (short) (Math.sin(phase) * 11000);
                            samples[i] = sample;
                            samples[i + 1] = sample;
                            phase += step;
                            if (phase >= 2.0 * Math.PI) phase -= 2.0 * Math.PI;
                        }
                        AudioTrack current = track;
                        if (current == null || !playing.get()) break;
                        int written = current.write(samples, 0, samples.length);
                        if (written < 0) break;
                    }
                } catch (Exception ignored) {
                }
            }, "HellenstarTone");
            toneThread.start();
        } catch (Exception e) {
            stopTone();
            Toast.makeText(this, e.getMessage() == null ? "Audio output could not start." : e.getMessage(), Toast.LENGTH_LONG).show();
        }
    }

    private void attachEffects(int sessionId) {
        releaseEffects();
        try {
            bassBoost = new BassBoost(0, sessionId);
            bassBoost.setEnabled(true);
            setBass(bassBar == null ? 300 : bassBar.getProgress() * 10);
        } catch (Exception ignored) { bassBoost = null; }
        try {
            virtualizer = new Virtualizer(0, sessionId);
            virtualizer.setEnabled(true);
            setWidth(widthBar == null ? 350 : widthBar.getProgress() * 10);
        } catch (Exception ignored) { virtualizer = null; }
        try {
            equalizer = new Equalizer(0, sessionId);
            equalizer.setEnabled(true);
        } catch (Exception ignored) { equalizer = null; }
        try {
            loudnessEnhancer = new LoudnessEnhancer(sessionId);
            loudnessEnhancer.setTargetGain(0);
            loudnessEnhancer.setEnabled(true);
        } catch (Exception ignored) { loudnessEnhancer = null; }
    }

    private void setBass(int strength) {
        if (bassBoost == null) return;
        try {
            short safe = (short) Math.max(0, Math.min(1000, strength));
            bassBoost.setStrength(safe);
        } catch (Exception ignored) {}
    }

    private void setWidth(int strength) {
        if (virtualizer == null) return;
        try {
            short safe = (short) Math.max(0, Math.min(1000, strength));
            virtualizer.setStrength(safe);
        } catch (Exception ignored) {}
    }

    private void stopTone() {
        playing.set(false);
        Thread thread = toneThread;
        toneThread = null;
        if (thread != null && thread != Thread.currentThread()) {
            try { thread.join(250); } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }
        AudioTrack old = track;
        track = null;
        if (old != null) {
            try { old.pause(); } catch (Exception ignored) {}
            try { old.flush(); } catch (Exception ignored) {}
            try { old.stop(); } catch (Exception ignored) {}
            try { old.release(); } catch (Exception ignored) {}
        }
        releaseEffects();
        if (playButton != null) playButton.setText("▶   PLAY TEST TONE");
        if (statusText != null) statusText.setText("READY  •  AUDIO STAYS INSIDE THIS APP");
    }

    private void releaseEffects() {
        if (bassBoost != null) { try { bassBoost.release(); } catch (Exception ignored) {} bassBoost = null; }
        if (virtualizer != null) { try { virtualizer.release(); } catch (Exception ignored) {} virtualizer = null; }
        if (equalizer != null) { try { equalizer.release(); } catch (Exception ignored) {} equalizer = null; }
        if (loudnessEnhancer != null) { try { loudnessEnhancer.release(); } catch (Exception ignored) {} loudnessEnhancer = null; }
    }

    private LinearLayout card() {
        LinearLayout box = new LinearLayout(this);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(dp(16), dp(16), dp(16), dp(16));
        box.setBackground(shape(PANEL, 20));
        return box;
    }

    private TextView text(String value, int sp, int color, boolean bold) {
        TextView t = new TextView(this);
        t.setText(value);
        t.setTextSize(sp);
        t.setTextColor(color);
        if (bold) t.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        return t;
    }

    private void addActionButton(LinearLayout parent, String label, View.OnClickListener listener) {
        Button button = new Button(this);
        button.setText(label);
        button.setTextSize(12);
        button.setTextColor(TEXT);
        button.setAllCaps(false);
        button.setBackground(shape(Color.rgb(43, 38, 65), 12));
        button.setOnClickListener(listener);
        parent.addView(button, params(-1, 48, 0, 8, 0, 0));
    }

    private GradientDrawable shape(int color, int radius) {
        GradientDrawable d = new GradientDrawable();
        d.setColor(color);
        d.setCornerRadius(dp(radius));
        return d;
    }

    private LinearLayout.LayoutParams params(int width, int height, int left, int top, int right, int bottom) {
        LinearLayout.LayoutParams p = new LinearLayout.LayoutParams(width < 0 ? width : dp(width), height < 0 ? height : dp(height));
        p.setMargins(dp(left), dp(top), dp(right), dp(bottom));
        return p;
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }

    @Override protected void onStop() {
        stopTone();
        super.onStop();
    }

    @Override protected void onDestroy() {
        stopTone();
        super.onDestroy();
    }
}
