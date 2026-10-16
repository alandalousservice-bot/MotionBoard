import Ajv2020 from 'ajv/dist/2020';
import addFormats from 'ajv-formats';
import { describe, expect, it } from 'vitest';
import characterSchema from '../../../../schemas/character-asset.schema.json';
import animationSchema from '../../../../schemas/animation-asset.schema.json';
import { parseMotionMetadata } from '../metadata';

const ajv = new Ajv2020({ allErrors: true });
addFormats(ajv);

const character = {
  schemaVersion: '1.0.0',
  id: 'schoolboy-primary',
  version: '1.0.0',
  assetPath: 'assets/characters/schoolboy-v1.glb',
  format: 'glTF 2.0 binary',
  units: 'meters',
  axes: { up: '+Z', forward: '+Y' },
  rig: { id: 'schoolboy-rig', version: '1.0.0', restPose: 'A-pose' },
  license: { status: 'pending', sources: [] },
  review: { technical: { status: 'pending' } },
};

const walkMotion = {
  schemaVersion: '1.0.0',
  id: 'locomotion-walk',
  version: '1.0.0',
  clipName: 'walk_cycle',
  characterId: 'schoolboy-primary',
  characterVersion: '1.0.0',
  skillFamily: 'locomotion',
  movement: 'walking',
  assetPath: 'assets/animations/locomotion-walk-v1.glb',
  format: 'glTF 2.0 binary',
  durationSeconds: 1,
  frameRate: 30,
  loop: true,
  rootMotion: 'in-place',
  labels: { ar: 'المشي' },
  descriptions: { ar: 'وصف تجريبي لا يمثل محتوى معتمداً.' },
  phases: { ar: [{ id: 'sample-phase', title: 'مرحلة تجريبية', description: 'بيانات اختبار للمخطط فقط.' }] },
  license: { status: 'pending', sources: [] },
  review: { technical: { status: 'pending' }, pedagogical: { status: 'pending' } },
};

describe('Draft 2020-12 asset schemas', () => {
  it('compiles the character schema and accepts a pending technical asset record', () => {
    const validate = ajv.compile(characterSchema);
    expect(validate(character), JSON.stringify(validate.errors)).toBe(true);
  });

  it('compiles the animation schema and accepts a pending movement record', () => {
    const validate = ajv.compile(animationSchema);
    expect(validate(walkMotion), JSON.stringify(validate.errors)).toBe(true);
  });

  it('rejects a clip whose movement family conflicts with its stable clip name', () => {
    const validate = ajv.compile(animationSchema);
    expect(validate({ ...walkMotion, movement: 'running' })).toBe(false);
  });

  it('parses schema-valid metadata without elevating its pending review status', () => {
    const parsed = parseMotionMetadata(JSON.stringify(walkMotion));
    expect(parsed.labels.ar).toBe('المشي');
    expect(parsed.phases?.ar).toHaveLength(1);
    expect(walkMotion.review.pedagogical.status).toBe('pending');
  });

  it('rejects malformed JSON and schema-invalid metadata', () => {
    expect(() => parseMotionMetadata('{')).toThrow('ليس JSON صالحاً');
    expect(() => parseMotionMetadata(JSON.stringify({ clipName: 'walk_cycle' }))).toThrow('لا تطابق مخطط الحركة');
  });
});
