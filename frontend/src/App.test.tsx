import { render, screen } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from 'react-query';
import { MemoryRouter } from 'react-router-dom';
import { HomePage } from './pages/HomePage';
import { ThemeProvider } from './contexts/ThemeContext';

const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

const renderWithProviders = (ui: React.ReactElement) => {
  const testQueryClient = createTestQueryClient();
  return render(
    <ThemeProvider>
      <QueryClientProvider client={testQueryClient}>
        <MemoryRouter>
          {ui}
        </MemoryRouter>
      </QueryClientProvider>
    </ThemeProvider>
  );
};

test('renders data contracts studio header', () => {
  renderWithProviders(<HomePage />);
  const headerElement = screen.getByText(/Data Contract Studio/i);
  expect(headerElement).toBeInTheDocument();
});
