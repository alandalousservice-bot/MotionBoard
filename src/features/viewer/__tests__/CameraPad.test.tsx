import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { CameraPad } from '../CameraPad';

describe('CameraPad', () => {
  it('routes keyboard-accessible orbit and zoom buttons to camera actions', () => {
    const actions = {
      left: vi.fn(), right: vi.fn(), up: vi.fn(), down: vi.fn(), zoomIn: vi.fn(), zoomOut: vi.fn(),
    };
    render(<CameraPad actions={actions} />);

    fireEvent.click(screen.getByRole('button', { name: 'تحريك الكاميرا للأعلى' }));
    fireEvent.click(screen.getByRole('button', { name: 'تحريك الكاميرا لليمين' }));
    fireEvent.click(screen.getByRole('button', { name: 'تقريب الكاميرا' }));
    fireEvent.click(screen.getByRole('button', { name: 'إبعاد الكاميرا' }));

    expect(actions.up).toHaveBeenCalledOnce();
    expect(actions.right).toHaveBeenCalledOnce();
    expect(actions.zoomIn).toHaveBeenCalledOnce();
    expect(actions.zoomOut).toHaveBeenCalledOnce();
  });
});
