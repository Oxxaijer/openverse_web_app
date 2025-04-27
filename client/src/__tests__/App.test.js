import { render, screen } from '@testing-library/react';
import App from '../App';

test('renders Openverse text', () => {
  render(<App />);
  const linkElement = screen.getByText(/Openverse/i);
  expect(linkElement).toBeInTheDocument();
});
