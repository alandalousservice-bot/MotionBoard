import type { AnimationClip } from 'three';
import type { GLTF } from 'three/addons/loaders/GLTFLoader.js';

export type LoadedCharacter = {
  fileName: string;
  gltf: GLTF;
};

export type MotionPhase = {
  id: string;
  title: string;
  description: string;
};

export type MotionMetadata = {
  id: string;
  clipName: string;
  labels: { ar: string; fr?: string; en?: string };
  descriptions?: { ar: string; fr?: string; en?: string };
  phases?: {
    ar: MotionPhase[];
    fr?: MotionPhase[];
    en?: MotionPhase[];
  };
};

export type ClipOption = Pick<AnimationClip, 'name' | 'duration'>;

export type LoadState = 'empty' | 'loading' | 'ready' | 'error';
