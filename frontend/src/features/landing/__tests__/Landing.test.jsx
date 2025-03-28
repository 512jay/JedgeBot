// /frontend/src/features/landing/__tests__/Landing.test.jsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import Landing from '../Landing';

// ✅ Mock WaitlistForm to avoid document-related errors
vi.mock('../WaitlistForm', () => ({
  default: () => (
    <form>
      <label htmlFor="email">Email</label>
      <input id="email" aria-label="Email" />
      <button type="submit">Join the Waitlist</button>
    </form>
  ),
}));

describe('Landing Page', () => {
  it('renders the title and subheading', () => {
    render(<Landing />);
    expect(screen.getByText('Fordis Ludus')).toBeInTheDocument();
    expect(screen.getByText(/Multi-Broker Trading/i)).toBeInTheDocument();
  });

  it('renders the waitlist form', () => {
    render(<Landing />);
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Join the Waitlist/i })).toBeInTheDocument();
  });
});
