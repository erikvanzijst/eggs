import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ItemList from './ItemList';

// Mock fetch globally for testing
(global.fetch as jest.Mock) = jest.fn();

describe('ItemList', () => {
  beforeEach(() => {
    jest.resetAllMocks();
  });

  it('should display loading state when fetching items', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValue([])
    });

    render(<ItemList listName="Groceries" />);
    
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('should display items sorted alphabetically', async () => {
    const mockItems = ['zebra', 'apple', 'Banana'];
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValue(mockItems)
    });

    render(<ItemList listName="Groceries" />);
    
    // Wait for items to load
    await waitFor(() => {
      expect(screen.getByText('apple')).toBeInTheDocument();
      expect(screen.getByText('Banana')).toBeInTheDocument();
      expect(screen.getByText('zebra')).toBeInTheDocument();
    });
    
    // Check that items are in sorted order
    const items = screen.getAllByText(/apple|Banana|zebra/);
    expect(items[0]).toHaveTextContent('apple');
    expect(items[1]).toHaveTextContent('Banana');
    expect(items[2]).toHaveTextContent('zebra');
  });

  it('should display empty state when no items', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: jest.fn().mockResolvedValue([])
    });

    render(<ItemList listName="Groceries" />);
    
    await waitFor(() => {
      expect(screen.getByText('No items in this list')).toBeInTheDocument();
    });
  });

  it('should display error when fetch fails', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      status: 500
    });

    render(<ItemList listName="Groceries" />);
    
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });
  });

  it('should handle null/undefined listName gracefully', async () => {
    render(<ItemList listName={null} />);
    
    // Should not try to fetch items and should not crash
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
  });
});