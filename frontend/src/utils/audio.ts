// Web Audio SFX Synthesizer with Volume Control & Mute State
let audioCtx: AudioContext | null = null;

// Volume range: 0 to 100
let currentVolumePercent = 70;
let isAudioMuted = false;

// Initialize from localStorage if available in browser
if (typeof window !== 'undefined') {
  try {
    const savedVol = localStorage.getItem('spider_radar_sfx_volume');
    if (savedVol !== null) {
      const parsed = parseInt(savedVol, 10);
      if (!isNaN(parsed) && parsed >= 0 && parsed <= 100) {
        currentVolumePercent = parsed;
      }
    }
    const savedMuted = localStorage.getItem('spider_radar_sfx_muted');
    if (savedMuted !== null) {
      isAudioMuted = savedMuted === 'true';
    }
  } catch {}
}

export const getVolumePercent = (): number => currentVolumePercent;

export const setVolumePercent = (percent: number): void => {
  const clamped = Math.max(0, Math.min(100, Math.round(percent)));
  currentVolumePercent = clamped;
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem('spider_radar_sfx_volume', clamped.toString());
    } catch {}
  }
};

export const getIsAudioMuted = (): boolean => isAudioMuted;

export const setIsAudioMuted = (muted: boolean): void => {
  isAudioMuted = muted;
  if (typeof window !== 'undefined') {
    try {
      localStorage.setItem('spider_radar_sfx_muted', muted ? 'true' : 'false');
    } catch {}
  }
};

const getAudioContext = (): AudioContext | null => {
  if (typeof window === 'undefined') return null;
  if (!audioCtx) {
    const AudioCtxClass = window.AudioContext || (window as any).webkitAudioContext;
    if (AudioCtxClass) {
      audioCtx = new AudioCtxClass();
    }
  }
  if (audioCtx && audioCtx.state === 'suspended') {
    audioCtx.resume();
  }
  return audioCtx;
};

export const playSfx = (type: 'water_drop' | 'paper_rustle' | 'wind_chime' | 'click') => {
  try {
    if (isAudioMuted || currentVolumePercent <= 0) return;

    const ctx = getAudioContext();
    if (!ctx) return;

    // Master volume scalar: 0.0 to 1.0
    const masterGainScalar = (currentVolumePercent / 100);

    if (type === 'water_drop') {
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      
      const now = ctx.currentTime;
      osc.frequency.setValueAtTime(800, now);
      osc.frequency.exponentialRampToValueAtTime(1400, now + 0.08);
      osc.frequency.exponentialRampToValueAtTime(400, now + 0.18);

      gain.gain.setValueAtTime(0.3 * masterGainScalar, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.22);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.22);
    } else if (type === 'paper_rustle') {
      // Filtered noise for paper rustle
      const bufferSize = ctx.sampleRate * 0.12;
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }

      const noise = ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.value = 1600;
      filter.Q.value = 2.5;

      const gain = ctx.createGain();
      const now = ctx.currentTime;
      gain.gain.setValueAtTime(0.2 * masterGainScalar, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      noise.start(now);
    } else if (type === 'wind_chime') {
      const now = ctx.currentTime;
      const freqs = [1046.5, 1318.5, 1567.98]; // C6, E6, G6
      freqs.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.value = freq;
        const start = now + idx * 0.05;
        gain.gain.setValueAtTime(0.15 * masterGainScalar, start);
        gain.gain.exponentialRampToValueAtTime(0.001, start + 0.4);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(start);
        osc.stop(start + 0.4);
      });
    } else {
      // Subdued soft click
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      const now = ctx.currentTime;
      osc.frequency.setValueAtTime(500, now);
      osc.frequency.exponentialRampToValueAtTime(200, now + 0.04);
      gain.gain.setValueAtTime(0.15 * masterGainScalar, now);
      gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(now);
      osc.stop(now + 0.05);
    }
  } catch {
    // Audio context not allowed or failed gracefully
  }
};
