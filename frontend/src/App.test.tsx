import { render } from '@testing-library/react';
import App from './App';

test('renders app without crashing', () => {
  // This test just verifies the component renders
  expect(() => {
    render(<App />);
  }).not.toThrow();
});