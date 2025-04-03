// /frontend/src/features/auth/__tests__/Register.test.jsx
import React from 'react';
import { describe, it, vi, beforeEach, expect } from 'vitest';
import { screen, fireEvent, waitFor } from '@testing-library/react';
import Register from '../Register';
import * as api from '../auth_api';
import renderWithProviders from '@/test-utils/renderWithProviders';

vi.mock('../auth_api');

describe('Register Form', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('shows error when passwords do not match', async () => {
    renderWithProviders(<Register />);

    fireEvent.change(screen.getByLabelText(/Username/i), { target: { value: 'newuser' } });
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/^Password$/i), { target: { value: 'pass1234' } });
    fireEvent.change(screen.getByLabelText(/Confirm Password/i), { target: { value: 'wrongpass' } });

    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    await screen.findByText(/passwords do not match/i);
  });

  it('shows error when no role is selected', async () => {
    renderWithProviders(<Register />);

    fireEvent.change(screen.getByLabelText(/Username/i), { target: { value: 'newuser' } });
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/^Password$/i), { target: { value: 'pass1234' } });
    fireEvent.change(screen.getByLabelText(/Confirm Password/i), { target: { value: 'pass1234' } });

    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    await screen.findByText(/please select a role/i);
  });

  it('successfully registers and shows toast', async () => {
    api.register.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ message: 'success' }),
    });

    renderWithProviders(<Register />);

    fireEvent.change(screen.getByLabelText(/Username/i), { target: { value: 'newuser' } });
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/^Password$/i), { target: { value: 'pass1234' } });
    fireEvent.change(screen.getByLabelText(/Confirm Password/i), { target: { value: 'pass1234' } });
    fireEvent.click(screen.getByLabelText(/Trader/i)); // Select role

    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    await waitFor(() => {
      expect(screen.getByText(/check your email/i)).toBeInTheDocument();
    });
  });

  it('shows server error when registration fails', async () => {
    api.register.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: 'Email already exists' }),
    });

    renderWithProviders(<Register />);

    fireEvent.change(screen.getByLabelText(/Username/i), { target: { value: 'newuser' } });
    fireEvent.change(screen.getByLabelText(/Email/i), { target: { value: 'duplicate@example.com' } });
    fireEvent.change(screen.getByLabelText(/^Password$/i), { target: { value: 'pass1234' } });
    fireEvent.change(screen.getByLabelText(/Confirm Password/i), { target: { value: 'pass1234' } });
    fireEvent.click(screen.getByLabelText(/Trader/i)); // Select role

    fireEvent.click(screen.getByRole('button', { name: /register/i }));

    await screen.findByText(/email already exists/i);
  });
});
