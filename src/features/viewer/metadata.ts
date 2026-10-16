import Ajv2020 from 'ajv/dist/2020';
import addFormats from 'ajv-formats';
import animationSchema from '../../../schemas/animation-asset.schema.json';
import type { MotionMetadata } from './types';

const ajv = new Ajv2020({ allErrors: true, strict: true });
addFormats(ajv);
const validateAnimation = ajv.compile(animationSchema);

export function parseMotionMetadata(source: string): MotionMetadata {
  let candidate: unknown;
  try {
    candidate = JSON.parse(source);
  } catch {
    throw new Error('ملف البيانات الوصفية ليس JSON صالحاً.');
  }

  if (!validateAnimation(candidate)) {
    const reason = ajv.errorsText(validateAnimation.errors, { separator: '، ' });
    throw new Error(`البيانات لا تطابق مخطط الحركة: ${reason}`);
  }

  return candidate as MotionMetadata;
}
