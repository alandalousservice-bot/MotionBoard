import { fireEvent, render, screen } from '@testing-library/react';
import type { ComponentProps } from 'react';
import { describe, expect, it, vi } from 'vitest';
import { PlaybackToolbar } from '../PlaybackToolbar';

function renderToolbar(overrides: Partial<ComponentProps<typeof PlaybackToolbar>> = {}) {
  const props = {
    hasClip: true,
    cameraReady: true,
    playing: true,
    loop: true,
    speed: 1,
    onTogglePlaying: vi.fn(),
    onRestart: vi.fn(),
    onToggleLoop: vi.fn(),
    onSpeedChange: vi.fn(),
    onResetCamera: vi.fn(),
    ...overrides,
  };
  render(<PlaybackToolbar {...props} />);
  return props;
}

describe('PlaybackToolbar', () => {
  it('exposes play/pause, restart, loop, speed and camera actions', () => {
    const props = renderToolbar();
    fireEvent.click(screen.getByRole('button', { name: 'إيقاف مؤقت' }));
    fireEvent.click(screen.getByRole('button', { name: 'إعادة الحركة من البداية' }));
    fireEvent.click(screen.getByRole('button', { name: 'إيقاف التكرار' }));
    fireEvent.click(screen.getByRole('button', { name: '0.5×' }));
    fireEvent.click(screen.getByRole('button', { name: 'إعادة ضبط زاوية الكاميرا' }));

    expect(props.onTogglePlaying).toHaveBeenCalledOnce();
    expect(props.onRestart).toHaveBeenCalledOnce();
    expect(props.onToggleLoop).toHaveBeenCalledOnce();
    expect(props.onSpeedChange).toHaveBeenCalledWith(0.5);
    expect(props.onResetCamera).toHaveBeenCalledOnce();
  });

  it('disables playback actions until an animation clip is available', () => {
    renderToolbar({ hasClip: false, cameraReady: false });
    expect(screen.getByRole('button', { name: 'تشغيل الحركة' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'إعادة الحركة من البداية' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'إيقاف التكرار' })).toBeDisabled();
    expect(screen.getByRole('button', { name: 'إعادة ضبط زاوية الكاميرا' })).toBeDisabled();
  });
});
