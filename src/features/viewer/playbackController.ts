import {
  AnimationMixer,
  LoopOnce,
  LoopRepeat,
  type AnimationAction,
  type AnimationClip,
  type Object3D,
} from 'three';

export class PlaybackController {
  readonly mixer: AnimationMixer;
  private action: AnimationAction | null = null;
  private clip: AnimationClip | null = null;
  private loop = true;
  private playing = true;
  private speed = 1;
  private disposed = false;

  constructor(private readonly root: Object3D) {
    this.mixer = new AnimationMixer(root);
  }

  select(clip: AnimationClip, loop = true): void {
    this.assertActive();
    this.mixer.stopAllAction();
    if (this.clip) this.mixer.uncacheAction(this.clip, this.root);

    this.clip = clip;
    this.loop = loop;
    this.action = this.mixer.clipAction(clip, this.root);
    this.applyLoop();
    this.action.timeScale = this.speed;
    this.action.reset().play();
    this.action.paused = !this.playing;
  }

  setPlaying(playing: boolean): void {
    this.assertActive();
    this.playing = playing;
    if (this.action) this.action.paused = !playing;
  }

  setSpeed(speed: number): void {
    this.assertActive();
    if (![0.25, 0.5, 1].includes(speed)) {
      throw new RangeError('Playback speed must be 0.25x, 0.5x, or 1x.');
    }
    this.speed = speed;
    if (this.action) this.action.timeScale = speed;
  }

  setLoop(loop: boolean): void {
    this.assertActive();
    this.loop = loop;
    this.applyLoop();
  }

  restart(): void {
    this.assertActive();
    if (!this.action) return;
    this.action.reset();
    this.action.paused = !this.playing;
    this.action.play();
  }

  update(deltaSeconds: number): void {
    if (!this.disposed) this.mixer.update(deltaSeconds);
  }

  dispose(): void {
    if (this.disposed) return;
    this.mixer.stopAllAction();
    if (this.clip) this.mixer.uncacheAction(this.clip, this.root);
    this.mixer.uncacheRoot(this.root);
    this.action = null;
    this.clip = null;
    this.disposed = true;
  }

  private applyLoop(): void {
    if (!this.action) return;
    this.action.setLoop(this.loop ? LoopRepeat : LoopOnce, this.loop ? Infinity : 1);
    this.action.clampWhenFinished = !this.loop;
  }

  private assertActive(): void {
    if (this.disposed) throw new Error('Playback controller has been disposed.');
  }
}
