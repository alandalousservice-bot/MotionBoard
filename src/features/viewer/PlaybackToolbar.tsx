type PlaybackToolbarProps = {
  hasClip: boolean;
  cameraReady: boolean;
  playing: boolean;
  loop: boolean;
  speed: number;
  onTogglePlaying: () => void;
  onRestart: () => void;
  onToggleLoop: () => void;
  onSpeedChange: (speed: number) => void;
  onResetCamera: () => void;
};

const speeds = [0.25, 0.5, 1] as const;

export function PlaybackToolbar({
  hasClip,
  cameraReady,
  playing,
  loop,
  speed,
  onTogglePlaying,
  onRestart,
  onToggleLoop,
  onSpeedChange,
  onResetCamera,
}: PlaybackToolbarProps) {
  return (
    <div className="playback-toolbar" aria-label="أدوات العرض والتحكم">
      <div className="transport-controls">
        <button className="icon-button" type="button" onClick={onRestart} disabled={!hasClip} aria-label="إعادة الحركة من البداية" title="إعادة من البداية">
          <span aria-hidden="true">↺</span>
        </button>
        <button className="play-button" type="button" onClick={onTogglePlaying} disabled={!hasClip} aria-label={hasClip && playing ? 'إيقاف مؤقت' : 'تشغيل الحركة'}>
          <span aria-hidden="true">{hasClip && playing ? 'Ⅱ' : '▶'}</span>
          <span>{hasClip && playing ? 'إيقاف' : 'تشغيل'}</span>
        </button>
        <button className={`icon-button ${loop ? 'is-active' : ''}`} type="button" onClick={onToggleLoop} disabled={!hasClip} aria-pressed={loop} aria-label={loop ? 'إيقاف التكرار' : 'تفعيل التكرار'} title="تكرار الحركة">
          <span aria-hidden="true">⟳</span>
        </button>
      </div>

      <div className="toolbar-divider" aria-hidden="true" />

      <fieldset className="speed-control" disabled={!hasClip}>
        <legend>سرعة العرض</legend>
        <div className="speed-options" role="group" aria-label="سرعة الحركة">
          {speeds.map((option) => (
            <button
              key={option}
              className={speed === option ? 'speed-option is-selected' : 'speed-option'}
              type="button"
              aria-pressed={speed === option}
              onClick={() => onSpeedChange(option)}
            >
              {option}×
            </button>
          ))}
        </div>
      </fieldset>

      <button className="camera-reset" type="button" onClick={onResetCamera} disabled={!cameraReady} aria-label="إعادة ضبط زاوية الكاميرا">
        <span aria-hidden="true">◎</span>
        <span>إعادة الكاميرا</span>
      </button>
    </div>
  );
}
