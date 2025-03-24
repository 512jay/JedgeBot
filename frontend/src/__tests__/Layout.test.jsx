import { render, screen } from '@testing-library/react';
import App from '@/App';

test('renders Navbar and Sidebar in full layout', () => {
  render(<App />);
  expect(screen.getByText(/jedgebot/i)).toBeInTheDocument();
  expect(screen.getByText(/welcome to jedgebot/i)).toBeInTheDocument();
  expect(screen.getByRole('button', { name: /login/i })).toBeInTheDocument();
});
