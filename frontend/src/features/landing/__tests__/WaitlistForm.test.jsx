// /frontend/src/features/landing/__tests__/WaitlistForm.test.jsx

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import WaitlistForm from '../WaitlistForm';
import '@testing-library/jest-dom';

describe('WaitlistForm', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  it('blocks form submission when required fields are empty', async () => {
    render(<WaitlistForm />);

    const submitButton = screen.getByRole('button', { name: /request early access/i });

    fireEvent.click(submitButton);

    // Since browser prevents submission, fetch shouldn't be called
    expect(global.fetch).not.toHaveBeenCalled();
  });



  it('blocks submission if honeypot fields are filled', async () => {
    render(<WaitlistForm />);

    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'user@example.com' } });
    fireEvent.change(screen.getByLabelText('Feedback'), { target: { value: 'Valid feedback input' } });
    fireEvent.change(screen.getByLabelText('Role'), { target: { value: 'trader' } });
    fireEvent.change(screen.getByLabelText('Phone Number'), { target: { value: '1234567890' } });

    fireEvent.click(screen.getByRole('button', { name: /request early access/i }));

    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('displays a server error when the submission fails', async () => {
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    global.fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ message: 'Submission failed.' }),
    });

    render(<WaitlistForm />);
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'fail@example.com' } });
    fireEvent.change(screen.getByLabelText('Feedback'), { target: { value: 'Some feedback text' } });
    fireEvent.change(screen.getByLabelText('Role'), { target: { value: 'trader' } });

    fireEvent.click(screen.getByRole('button', { name: /request early access/i }));

    const alert = await screen.findByText(/submission failed/i);
    expect(alert).toBeInTheDocument();

    errorSpy.mockRestore();
  });


  it('displays a network error if fetch throws', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network error'));

    render(<WaitlistForm />);

    // Fill required fields
    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'fail@example.com' },
    });
    fireEvent.change(screen.getByLabelText('Feedback'), {
      target: { value: 'Some feedback text' },
    });
    fireEvent.change(screen.getByLabelText('Role'), {
      target: { value: 'trader' },
    });

    // Click the submit button
    fireEvent.click(screen.getByRole('button', { name: /request early access/i }));

    // Match error by content
    const alert = await screen.findByText((text) =>
      text.toLowerCase().includes('network error')
    );

    expect(alert).toBeInTheDocument();
  });


  it('submits the form successfully with valid input', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ message: 'Success' }),
    });

    render(<WaitlistForm />);

    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'user@example.com' } });
    fireEvent.change(screen.getByLabelText('Feedback'), { target: { value: 'Some real feedback' } });
    fireEvent.change(screen.getByLabelText('Role'), { target: { value: 'manager' } });

    fireEvent.click(screen.getByRole('button', { name: /request early access/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(1);
    });
  });
});
