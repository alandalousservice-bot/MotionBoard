import type { CameraActions } from './Viewer';

export function CameraPad({ actions }: { actions: CameraActions }) {
  return (
    <div className="camera-pad" role="group" aria-label="تحريك الكاميرا بلوحة المفاتيح">
      <span className="camera-pad-label">زاوية العرض</span>
      <div className="camera-direction-grid">
        <span />
        <button type="button" aria-label="تحريك الكاميرا للأعلى" onClick={actions.up}>↑</button>
        <span />
        <button type="button" aria-label="تحريك الكاميرا لليسار" onClick={actions.left}>←</button>
        <button type="button" aria-label="تحريك الكاميرا للأسفل" onClick={actions.down}>↓</button>
        <button type="button" aria-label="تحريك الكاميرا لليمين" onClick={actions.right}>→</button>
      </div>
      <div className="camera-zoom-controls">
        <button type="button" aria-label="تقريب الكاميرا" onClick={actions.zoomIn}>＋</button>
        <button type="button" aria-label="إبعاد الكاميرا" onClick={actions.zoomOut}>−</button>
      </div>
    </div>
  );
}
