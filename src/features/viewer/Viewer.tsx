import { useEffect, useMemo, useRef } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import {
  Box3,
  Group,
  Vector3,
  type AnimationClip,
  type Object3D,
} from 'three';
import { OrbitControls as OrbitControlsImpl } from 'three/addons/controls/OrbitControls.js';
import type { LoadedCharacter } from './types';
import { PlaybackController } from './playbackController';

type ViewerProps = {
  asset: LoadedCharacter;
  clip: AnimationClip | null;
  playing: boolean;
  loop: boolean;
  speed: number;
  restartRevision: number;
  onResetCameraReady: (reset: () => void) => void;
  onCameraActionsReady: (actions: CameraActions) => void;
};

export type CameraActions = {
  left: () => void;
  right: () => void;
  up: () => void;
  down: () => void;
  zoomIn: () => void;
  zoomOut: () => void;
};

export function Viewer({ asset, clip, playing, loop, speed, restartRevision, onResetCameraReady, onCameraActionsReady }: ViewerProps) {
  return (
    <Canvas
      className="viewer-canvas"
      camera={{ position: [3.4, 2.3, 4.2], fov: 34, near: 0.1, far: 80 }}
      dpr={[1, 1.75]}
      gl={{ antialias: true, alpha: false, powerPreference: 'low-power' }}
      shadows
      fallback={<div className="canvas-fallback">تعذر تشغيل العرض ثلاثي الأبعاد في هذا المتصفح.</div>}
    >
      <color attach="background" args={['#152a29']} />
      <ambientLight intensity={1.45} />
      <hemisphereLight args={['#eff7ef', '#51615a', 1.25]} />
      <directionalLight position={[4, 7, 3]} intensity={2.1} castShadow shadow-mapSize={[1024, 1024]} />
      <directionalLight position={[-4, 3, -2]} intensity={0.8} color="#b2dfcc" />
      <mesh rotation-x={-Math.PI / 2} position={[0, -0.025, 0]} receiveShadow>
        <circleGeometry args={[12, 80]} />
        <meshStandardMaterial color="#223a35" roughness={0.9} />
      </mesh>
      <gridHelper args={[14, 28, '#3a554d', '#2d453f']} position={[0, -0.018, 0]} />
      <FramedCharacter scene={asset.gltf.scene} />
      {clip && <AnimatedClip scene={asset.gltf.scene} clip={clip} playing={playing} loop={loop} speed={speed} restartRevision={restartRevision} />}
      <CameraOrbitControls onResetReady={onResetCameraReady} onActionsReady={onCameraActionsReady} />
    </Canvas>
  );
}

function CameraOrbitControls({
  onResetReady,
  onActionsReady,
}: {
  onResetReady: (reset: () => void) => void;
  onActionsReady: (actions: CameraActions) => void;
}) {
  const { camera, gl } = useThree();
  const controlsRef = useRef<OrbitControlsImpl | null>(null);

  useEffect(() => {
    const controls = new OrbitControlsImpl(camera, gl.domElement);
    controls.target.set(0, 0.95, 0);
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.enablePan = false;
    controls.minDistance = 1.4;
    controls.maxDistance = 7.5;
    controls.minPolarAngle = 0.08;
    controls.maxPolarAngle = Math.PI - 0.08;
    controls.screenSpacePanning = false;
    controls.update();
    controlsRef.current = controls;
    onResetReady(() => controlsRef.current?.reset());
    const step = Math.PI / 18;
    const rotate = (horizontal: number, vertical: number) => {
      controls.rotateLeft(horizontal);
      controls.rotateUp(vertical);
      controls.update();
    };
    const dolly = (inward: boolean) => {
      if (inward) controls.dollyIn(1.15);
      else controls.dollyOut(1.15);
      controls.update();
    };
    onActionsReady({
      left: () => rotate(step, 0),
      right: () => rotate(-step, 0),
      up: () => rotate(0, step),
      down: () => rotate(0, -step),
      zoomIn: () => dolly(true),
      zoomOut: () => dolly(false),
    });

    return () => {
      controls.dispose();
      controlsRef.current = null;
      onResetReady(() => undefined);
      onActionsReady({ left: () => undefined, right: () => undefined, up: () => undefined, down: () => undefined, zoomIn: () => undefined, zoomOut: () => undefined });
    };
  }, [camera, gl, onActionsReady, onResetReady]);

  useFrame((_, delta) => controlsRef.current?.update(delta));
  return null;
}

function FramedCharacter({ scene }: { scene: Object3D }) {
  const framedRoot = useMemo(() => {
    const group = new Group();
    group.add(scene);

    const bounds = new Box3().setFromObject(scene);
    if (!bounds.isEmpty()) {
      const size = bounds.getSize(new Vector3());
      const center = bounds.getCenter(new Vector3());
      const largestDimension = Math.max(size.x, size.y, size.z, 0.001);
      const scale = 1.85 / largestDimension;
      group.scale.setScalar(scale);
      group.position.set(-center.x * scale, -bounds.min.y * scale, -center.z * scale);
    }
    return group;
  }, [scene]);

  return <primitive object={framedRoot} />;
}

function AnimatedClip({
  scene,
  clip,
  playing,
  loop,
  speed,
  restartRevision,
}: {
  scene: Object3D;
  clip: AnimationClip;
  playing: boolean;
  loop: boolean;
  speed: number;
  restartRevision: number;
}) {
  const controllerRef = useRef<PlaybackController | null>(null);

  useEffect(() => {
    const controller = new PlaybackController(scene);
    controllerRef.current = controller;
    return () => {
      controller.dispose();
      if (controllerRef.current === controller) controllerRef.current = null;
    };
  }, [scene]);

  useEffect(() => {
    controllerRef.current?.select(clip, loop);
  }, [scene, clip]);

  useEffect(() => controllerRef.current?.setPlaying(playing), [playing, clip]);
  useEffect(() => controllerRef.current?.setLoop(loop), [loop, clip]);
  useEffect(() => controllerRef.current?.setSpeed(speed), [speed, clip]);
  useEffect(() => controllerRef.current?.restart(), [restartRevision, clip]);

  useFrame((_, delta) => controllerRef.current?.update(delta));
  return null;
}
