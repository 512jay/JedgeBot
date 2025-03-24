// frontend/src/__tests__/Navbar.test.jsx
import { renderWithProviders } from "~test-utils/renderWithProviders";
import Navbar from '@/components/Navbar';

test('renders logout when user is authenticated', () => {
  renderWithProviders(<Navbar />, {
    auth: { user: { email: 'test@test.com', role: 'client' } }
  });
  expect(screen.getByText(/logout/i)).toBeInTheDocument();
});
