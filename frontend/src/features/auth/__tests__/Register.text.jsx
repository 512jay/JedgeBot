
it('shows error when passwords do not match', async () => {
  renderWithProviders(<Register />);
  fireEvent.change(screen.getByLabelText(/email/i), { target: { value: 'test@example.com' } });
  fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'abc123' } });
  fireEvent.change(screen.getByLabelText(/confirm password/i), { target: { value: 'xyz789' } });
  fireEvent.click(screen.getByRole('button', { name: /register/i }));
  expect(await screen.findByText(/passwords do not match/i)).toBeInTheDocument();
});
