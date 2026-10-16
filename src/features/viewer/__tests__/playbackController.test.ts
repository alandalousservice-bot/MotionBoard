import { AnimationClip, NumberKeyframeTrack, Object3D, LoopOnce, LoopRepeat } from 'three';
import { describe, expect, it, vi } from 'vitest';
import { PlaybackController } from '../playbackController';

function makeRigAndClip() {
  const root = new Object3D();
  root.name = 'root';
  const track = new NumberKeyframeTrack('root.position[x]', [0, 1], [0, 1]);
  return { root, clip: new AnimationClip('walk_cycle', 1, [track]) };
}

describe('PlaybackController', () => {
  it('plays at selected speed and pauses without advancing the animation', () => {
    const { root, clip } = makeRigAndClip();
    const player = new PlaybackController(root);
    player.select(clip);
    player.setSpeed(0.5);
    player.update(0.4);
    const action = player.mixer.existingAction(clip, root)!;
    expect(action.time).toBeCloseTo(0.2, 4);

    player.setPlaying(false);
    const pausedAt = action.time;
    player.update(0.5);
    expect(action.time).toBe(pausedAt);
    player.dispose();
  });

  it('restarts the clip and switches between repeat and one-shot looping', () => {
    const { root, clip } = makeRigAndClip();
    const player = new PlaybackController(root);
    player.select(clip);
    player.update(0.6);
    const action = player.mixer.existingAction(clip, root)!;
    expect(action.loop).toBe(LoopRepeat);
    player.setLoop(false);
    expect(action.loop).toBe(LoopOnce);
    player.restart();
    expect(action.time).toBe(0);
    player.dispose();
  });

  it('accepts only the viewer playback speed options', () => {
    const { root } = makeRigAndClip();
    const player = new PlaybackController(root);
    expect(() => player.setSpeed(0.75)).toThrow(RangeError);
    player.dispose();
  });

  it('keeps a newly selected clip paused when playback was already paused', () => {
    const { root, clip } = makeRigAndClip();
    const player = new PlaybackController(root);
    player.select(clip);
    player.setPlaying(false);
    const secondClip = new AnimationClip('run_cycle', 1, [new NumberKeyframeTrack('root.position[z]', [0, 1], [0, 1])]);
    player.select(secondClip);
    const action = player.mixer.existingAction(secondClip, root)!;
    expect(action.paused).toBe(true);
    const pausedAt = action.time;
    player.update(0.3);
    expect(action.time).toBe(pausedAt);
    player.dispose();
  });

  it('uncaches mixer resources on disposal and rejects further controls', () => {
    const { root, clip } = makeRigAndClip();
    const player = new PlaybackController(root);
    player.select(clip);
    const stopAll = vi.spyOn(player.mixer, 'stopAllAction');
    const uncache = vi.spyOn(player.mixer, 'uncacheRoot');
    player.dispose();
    player.dispose();
    expect(stopAll).toHaveBeenCalledOnce();
    expect(uncache).toHaveBeenCalledWith(root);
    expect(() => player.setPlaying(false)).toThrow('disposed');
  });
});
