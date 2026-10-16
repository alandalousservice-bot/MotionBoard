import { lazy, Suspense, useCallback, useEffect, useMemo, useState, type ChangeEvent } from 'react';
import type { AnimationClip } from 'three';
import { CameraPad } from '../features/viewer/CameraPad';
import type { CameraActions } from '../features/viewer/Viewer';
import { PlaybackToolbar } from '../features/viewer/PlaybackToolbar';
import type { LoadedCharacter, LoadState, MotionMetadata } from '../features/viewer/types';

const Viewer = lazy(() => import('../features/viewer/Viewer').then((module) => ({ default: module.Viewer })));

export function App() {
  const [glbFile, setGlbFile] = useState<File | null>(null);
  const [metadataFile, setMetadataFile] = useState<File | null>(null);
  const [asset, setAsset] = useState<LoadedCharacter | null>(null);
  const [loadState, setLoadState] = useState<LoadState>('empty');
  const [loadError, setLoadError] = useState('');
  const [metadata, setMetadata] = useState<MotionMetadata | null>(null);
  const [metadataError, setMetadataError] = useState('');
  const [selectedClipIndex, setSelectedClipIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [loop, setLoop] = useState(true);
  const [speed, setSpeed] = useState(1);
  const [restartRevision, setRestartRevision] = useState(0);
  const [resetCamera, setResetCamera] = useState<() => void>(() => () => undefined);
  const [cameraActions, setCameraActions] = useState<CameraActions>({
    left: () => undefined, right: () => undefined, up: () => undefined,
    down: () => undefined, zoomIn: () => undefined, zoomOut: () => undefined,
  });

  useEffect(() => {
    if (!glbFile) {
      setAsset(null);
      setLoadError('');
      setLoadState('empty');
      return;
    }

    let cancelled = false;
    let loadedGltf: LoadedCharacter['gltf'] | null = null;
    setAsset(null);
    setLoadError('');
    setLoadState('loading');
    setSelectedClipIndex(0);
    setPlaying(false);

    void glbFile.arrayBuffer()
      .then(async (buffer) => {
        const { GLTFLoader } = await import('three/addons/loaders/GLTFLoader.js');
        return new GLTFLoader().parseAsync(buffer, '');
      })
      .then((gltf) => {
        if (cancelled) {
          void import('../features/viewer/gltf').then(({ disposeGltf }) => disposeGltf(gltf));
          return;
        }
        loadedGltf = gltf;
        setAsset({ fileName: glbFile.name, gltf });
        setPlaying(gltf.animations.length > 0);
        setLoop(gltf.animations[0]?.name === 'jump_two_foot' ? false : true);
        setLoadState('ready');
      })
      .catch((error: unknown) => {
        if (cancelled) return;
        setLoadError(error instanceof Error ? error.message : 'تعذر قراءة ملف GLB.');
        setLoadState('error');
      });

    return () => {
      cancelled = true;
      if (loadedGltf) {
        const assetToDispose = loadedGltf;
        loadedGltf = null;
        void import('../features/viewer/gltf').then(({ disposeGltf }) => disposeGltf(assetToDispose));
      }
    };
  }, [glbFile]);

  useEffect(() => {
    if (!metadataFile) {
      setMetadata(null);
      setMetadataError('');
      return;
    }
    let cancelled = false;
    void metadataFile.text().then(async (source) => {
      if (cancelled) return;
      try {
        const { parseMotionMetadata } = await import('../features/viewer/metadata');
        if (cancelled) return;
        setMetadata(parseMotionMetadata(source));
        setMetadataError('');
      } catch (error) {
        setMetadata(null);
        setMetadataError(error instanceof Error ? error.message : 'تعذر قراءة بيانات المهارة.');
      }
    });
    return () => { cancelled = true; };
  }, [metadataFile]);

  const clips = asset?.gltf.animations ?? [];
  const selectedClip: AnimationClip | null = clips[selectedClipIndex] ?? null;
  const clipMetadata = useMemo(
    () => metadata && selectedClip?.name === metadata.clipName ? metadata : null,
    [metadata, selectedClip],
  );
  const resetCameraHandler = useCallback((reset: () => void) => setResetCamera(() => reset), []);
  const cameraActionsHandler = useCallback((actions: CameraActions) => setCameraActions(actions), []);

  const onGlbChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.currentTarget.files?.[0] ?? null;
    if (file) {
      setMetadataFile(null);
      setMetadata(null);
      setMetadataError('');
      setGlbFile(file);
    }
    event.currentTarget.value = '';
  };

  const onMetadataChange = (event: ChangeEvent<HTMLInputElement>) => {
    setMetadataFile(event.currentTarget.files?.[0] ?? null);
    event.currentTarget.value = '';
  };

  const onClipChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const nextIndex = Number(event.currentTarget.value);
    const nextClip = clips[nextIndex];
    setSelectedClipIndex(nextIndex);
    setPlaying(true);
    setLoop(nextClip?.name === 'jump_two_foot' ? false : true);
  };

  return (
    <main className="app-shell" dir="rtl">
      <header className="topbar">
        <a className="brand-lockup" href="#main" aria-label="MotionBoard 3D، الصفحة الرئيسية">
          <span className="brand-mark" aria-hidden="true"><span /></span>
          <span className="brand-copy">
            <strong>MotionBoard <b>3D</b></strong>
            <small>مكتبة المهارات الحركية</small>
          </span>
        </a>
        <div className="topbar-center">
          <span className="eyebrow">التربية البدنية · المرحلة الابتدائية</span>
          <h1>استكشف الحركة من كل زاوية</h1>
        </div>
        <span className="status-pill"><i /> نسخة تجريبية</span>
      </header>

      <div className="workspace" id="main">
        <section className="viewer-column" aria-label="عارض الحركة ثلاثي الأبعاد">
          <div className="viewer-heading">
            <div>
              <p className="section-kicker">مساحة العرض</p>
              <h2>{asset ? 'عارض الشخصية' : 'مساحة الحركة'}</h2>
            </div>
            <div className="view-hint"><span aria-hidden="true">⤢</span> اسحب للدوران · مرّر للتقريب</div>
          </div>

          <div className={`viewer-stage ${loadState === 'empty' ? 'is-empty' : ''}`}>
            {loadState === 'ready' && asset && (
              <Suspense fallback={<div className="stage-message" role="status"><span className="loading-spinner" /><strong>جارٍ تشغيل العارض ثلاثي الأبعاد…</strong></div>}>
                <Viewer
                  asset={asset}
                  clip={selectedClip}
                  playing={playing}
                  loop={loop}
                  speed={speed}
                  restartRevision={restartRevision}
                  onResetCameraReady={resetCameraHandler}
                  onCameraActionsReady={cameraActionsHandler}
                />
              </Suspense>
            )}
            {loadState !== 'ready' && <StageMessage state={loadState} error={loadError} onChoose={() => document.getElementById('glb-picker')?.click()} />}
            {loadState === 'ready' && (
              <div className="stage-corner-note"><span aria-hidden="true">✦</span> معاينة محلية · غير معتمدة تربوياً</div>
            )}
            {loadState === 'ready' && <CameraPad actions={cameraActions} />}
            {loadState === 'ready' && !selectedClip && (
              <div className="no-animation-overlay" role="status">
                <strong>تم تحميل النموذج</strong>
                <span>هذا الملف لا يحتوي على مقاطع حركة قابلة للاختيار.</span>
              </div>
            )}
          </div>

          <PlaybackToolbar
            hasClip={loadState === 'ready' && Boolean(selectedClip)}
            cameraReady={loadState === 'ready' && Boolean(asset)}
            playing={playing}
            loop={loop}
            speed={speed}
            onTogglePlaying={() => setPlaying((value) => !value)}
            onRestart={() => setRestartRevision((value) => value + 1)}
            onToggleLoop={() => setLoop((value) => !value)}
            onSpeedChange={setSpeed}
            onResetCamera={resetCamera}
          />

          <div className="interaction-note">
            <span className="note-icon" aria-hidden="true">i</span>
            <p><strong>طريقة العرض</strong> حرّك المؤشر أو إصبعك حول الشخصية للدوران، واستخدم عجلة الفأرة أو إيماءة التقريب لتغيير المسافة.</p>
          </div>
        </section>

        <aside className="details-column" aria-label="معلومات المهارة والحركات">
          <section className="panel import-panel">
            <div className="panel-heading">
              <span className="panel-icon upload-icon" aria-hidden="true">↑</span>
              <div><p className="section-kicker">مكتبة العرض</p><h2>المهارات الحركية</h2></div>
            </div>
            <p className="panel-description">تظهر هنا المهارات التي أضيفت إلى المكتبة بعد مراجعتها واعتمادها.</p>
            <div className="catalog-empty"><span aria-hidden="true">◇</span><span>لا توجد مهارات معتمدة في هذه النسخة.</span></div>
            <label className="primary-action" htmlFor="glb-picker">
              <span aria-hidden="true">＋</span> استيراد ملف GLB محلياً
            </label>
            <input id="glb-picker" className="visually-hidden" type="file" accept=".glb,model/gltf-binary" onChange={onGlbChange} aria-label="اختيار ملف GLB من الجهاز" />
            <p className="local-only-note"><span aria-hidden="true">⌑</span> يبقى الملف على جهازك ولا يتم رفعه إلى خادم.</p>
            {asset && (
              <div className="loaded-file" title={asset.fileName}>
                <span className="file-check" aria-hidden="true">✓</span>
                <span className="loaded-file-text"><strong>ملف محلي</strong><small>{asset.fileName}</small></span>
                <button type="button" className="clear-file" aria-label="إزالة الملف المحلي" onClick={() => { setGlbFile(null); setMetadataFile(null); }}>×</button>
              </div>
            )}
          </section>

          <section className="panel skill-panel">
            <div className="panel-heading compact-heading">
              <span className="panel-icon skill-icon" aria-hidden="true">✳</span>
              <div><p className="section-kicker">تفاصيل الحركة</p><h2>المهارة المختارة</h2></div>
            </div>
            {asset && clips.length > 0 ? (
              <>
                <label className="field-label" htmlFor="clip-select">مقطع الحركة داخل الملف</label>
                <select id="clip-select" className="clip-select" value={selectedClipIndex} onChange={onClipChange}>
                  {clips.map((clip, index) => <option key={`${clip.name}-${index}`} value={index}>{clip.name || `مقطع ${index + 1}`}</option>)}
                </select>
                <div className="skill-title-row">
                  <h3>{clipMetadata?.labels.ar ?? selectedClip?.name ?? 'حركة محلية'}</h3>
                  <span className="review-badge">غير معتمدة</span>
                </div>
                <p className="skill-description">
                  {clipMetadata?.descriptions?.ar ?? 'لم تُرفق بيانات وصفية تعليمية بهذا المقطع. اسم المقطع وحده لا يثبت صحة الحركة.'}
                </p>
                <div className="phases-header"><h4>مراحل الحركة</h4><span>{clipMetadata?.phases?.ar.length ?? 0}</span></div>
                {clipMetadata?.phases?.ar.length ? (
                  <ol className="phase-list">
                    {clipMetadata.phases.ar.map((phase, index) => (
                      <li key={phase.id}>
                        <span className="phase-number">{String(index + 1).padStart(2, '0')}</span>
                        <span><strong>{phase.title}</strong><small>{phase.description}</small></span>
                      </li>
                    ))}
                  </ol>
                ) : (
                  <p className="phase-empty">لا توجد مراحل حركة مرفقة أو مراجعة لهذا المقطع.</p>
                )}
                <label className="secondary-action" htmlFor="metadata-picker">
                  <span aria-hidden="true">▧</span> تحميل بيانات وصفية اختيارية
                </label>
                <input id="metadata-picker" className="visually-hidden" type="file" accept=".json,application/json" onChange={onMetadataChange} aria-label="اختيار ملف بيانات وصفية للحركة" />
                <p className="metadata-help">تُقبل ملفات JSON المطابقة لمخطط الحركة فقط. تظل المعاينة غير معتمدة في هذا العارض.</p>
                {metadataError && <p className="inline-error" role="alert">{metadataError}</p>}
                {metadata && metadata.clipName !== selectedClip?.name && <p className="inline-error" role="status">البيانات الوصفية تخص مقطعاً آخر: {metadata.clipName}</p>}
              </>
            ) : (
              <div className="skill-empty">
                <span className="empty-orbit" aria-hidden="true"><i /><b /></span>
                <strong>{asset ? 'لا توجد مقاطع حركة' : 'اختر ملفاً للبدء'}</strong>
                <p>{asset ? 'يمكن عرض النموذج، لكن لا يحتوي هذا الملف على حركات.' : 'بعد تحميل ملف GLB، ستظهر أسماء المقاطع هنا لتختار الحركة التي تريد استكشافها.'}</p>
              </div>
            )}
          </section>

          <div className="review-reminder"><span aria-hidden="true">✦</span><p>الملفات المستوردة محلياً للمعاينة التقنية فقط، ولا تمثل محتوى تعليمياً معتمداً.</p></div>
        </aside>
      </div>

      <footer className="app-footer">
        <span>MotionBoard 3D <i>·</i> مكتبة عرض مستقلة</span>
        <span>واجهة عربية <b>RTL</b></span>
      </footer>
    </main>
  );
}

function StageMessage({ state, error, onChoose }: { state: LoadState; error: string; onChoose: () => void }) {
  if (state === 'loading') {
    return <div className="stage-message" role="status"><span className="loading-spinner" /><strong>جارٍ تجهيز مساحة العرض…</strong><p>تتم معالجة الملف على جهازك.</p></div>;
  }
  if (state === 'error') {
    return <div className="stage-message error-state" role="alert"><span className="state-symbol">!</span><strong>تعذر تحميل الملف</strong><p>{error || 'تحقق من أن الملف GLB صالح ومكتفٍ ذاتياً.'}</p><button type="button" onClick={onChoose}>اختيار ملف آخر</button></div>;
  }
  return (
    <div className="stage-message empty-state">
      <div className="empty-art" aria-hidden="true"><span className="orbit-line orbit-one" /><span className="orbit-line orbit-two" /><span className="empty-star">✦</span><span className="empty-dot dot-one" /><span className="empty-dot dot-two" /></div>
      <span className="stage-kicker">مساحة العرض جاهزة</span>
      <h3>أضف شخصية ثلاثية الأبعاد لبدء الاستكشاف</h3>
      <p>لا يوجد حالياً أي ملف شخصية أو حركة في المشروع. يمكنك فتح ملف GLB مرخّص من جهازك لمعاينته محلياً.</p>
      <button type="button" className="stage-import-button" onClick={onChoose}><span aria-hidden="true">＋</span> اختيار ملف GLB</button>
      <small>لا يتم إنشاء أو اعتماد أي حركة تلقائياً.</small>
    </div>
  );
}
