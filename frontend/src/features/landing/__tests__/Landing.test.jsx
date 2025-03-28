// /frontend/src/features/landing/__tests__/Landing.test.jsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Landing from '../Landing';
import { HelmetProvider } from 'react-helmet-async';

describe('Landing Page', () => {
  it('renders the title and subheading', () => {
    render(
      <HelmetProvider>
        <Landing />
      </HelmetProvider>
    );

    expect(screen.getByText('Fordis Ludus')).toBeInTheDocument();
    expect(screen.getByText(/Multi-Broker Trading/i)).toBeInTheDocument();
  });

  it('renders the waitlist form', () => {
    render(
      <HelmetProvider>
        <Landing />
      </HelmetProvider>
    );

    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Join the Waitlist/i })).toBeInTheDocument();
  });
});
