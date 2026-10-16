import { fireEvent, render, screen } from '@testing-library/react';
import { AnimationClip, Group } from 'three';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { App } from '../App';

const { parseAsyncMock } = vi.hoisted(() => ({ parseAsyncMock: vi.fn() }));

vi.mock('three/addons/loaders/GLTFLoader.js', () => ({
  GLTFLoader: class {
    parseAsync(...args: unknown[]) { return parseAsyncMock(...args); }
  },
}));

vi.mock('../../features/viewer/Viewer', () => ({
  Viewer: () => <div data-testid="mock-3d-canvas" />,
}));

describe('MotionBoard app shell', () => {
  beforeEach(() => {
    parseAsyncMock.mockResolvedValue({
      scene: new Group(),
      animations: [new AnimationClip('technical_cycle', 1, [])],
    });
  });

  it('starts in an honest empty state without claiming an asset exists', () => {
    render(<App />);
    expect(screen.getByRole('heading', { name: 'أضف شخصية ثلاثية الأبعاد لبدء الاستكشاف' })).toBeInTheDocument();
    expect(screen.getByText('لا توجد مهارات معتمدة في هذه النسخة.')).toBeInTheDocument();
    expect(screen.getByText('لا يتم إنشاء أو اعتماد أي حركة تلقائياً.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /إيقاف مؤقت|تشغيل الحركة/ })).toBeDisabled();
  });

  it('loads a selected local GLB, exposes its clip and routes playback controls', async () => {
    render(<App />);
    const file = new File([new Uint8Array([0, 1, 2, 3])], 'technical-test.glb', { type: 'model/gltf-binary' });
    Object.defineProperty(file, 'arrayBuffer', { value: async () => new ArrayBuffer(4) });
    fireEvent.change(screen.getByLabelText('اختيار ملف GLB من الجهاز'), { target: { files: [file] } });

    expect(await screen.findByTestId('mock-3d-canvas')).toBeInTheDocument();
    expect(await screen.findByRole('option', { name: 'technical_cycle' })).toBeInTheDocument();
    expect(screen.getByText('technical-test.glb')).toBeInTheDocument();
    expect(screen.getByText('لم تُرفق بيانات وصفية تعليمية بهذا المقطع. اسم المقطع وحده لا يثبت صحة الحركة.')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'إيقاف مؤقت' })).toBeEnabled();

    fireEvent.click(screen.getByRole('button', { name: 'إيقاف مؤقت' }));
    expect(screen.getByRole('button', { name: 'تشغيل الحركة' })).toBeEnabled();
    fireEvent.click(screen.getByRole('button', { name: '0.25×' }));
    expect(screen.getByRole('button', { name: '0.25×' })).toHaveAttribute('aria-pressed', 'true');
  });
});
