import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Item from './Item';
import ShoppingListService from '../services/shoppingListService';

// Mock the ShoppingListService
jest.mock('../services/shoppingListService');

const mockDeleteItem = ShoppingListService.deleteItem as jest.Mock;

describe('Item Component', () => {
  const listName = 'Test List';
  const itemName = 'Test Item';
  
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders the item name correctly', () => {
    render(<Item listName={listName} itemName={itemName} />);
    
    expect(screen.getByText(itemName)).toBeInTheDocument();
  });

  it('calls deleteItem when delete button is clicked', async () => {
    mockDeleteItem.mockResolvedValue({ message: 'Item deleted successfully' });
    
    const user = userEvent.setup();
    render(<Item listName={listName} itemName={itemName} onItemDeleted={jest.fn()} />);
    
    const deleteButton = screen.getByLabelText('delete');
    await user.click(deleteButton);
    
    await waitFor(() => {
      expect(mockDeleteItem).toHaveBeenCalledWith(listName, itemName);
    });
  });

  it('calls onItemDeleted callback after successful deletion', async () => {
    mockDeleteItem.mockResolvedValue({ message: 'Item deleted successfully' });
    
    const mockCallback = jest.fn();
    const user = userEvent.setup();
    render(<Item listName={listName} itemName={itemName} onItemDeleted={mockCallback} />);
    
    const deleteButton = screen.getByLabelText('delete');
    await user.click(deleteButton);
    
    await waitFor(() => {
      expect(mockCallback).toHaveBeenCalled();
    });
  });

  it('handles deletion error gracefully', async () => {
    mockDeleteItem.mockRejectedValue(new Error('Delete failed'));
    
    const mockCallback = jest.fn();
    const user = userEvent.setup();
    render(<Item listName={listName} itemName={itemName} onItemDeleted={mockCallback} />);
    
    const deleteButton = screen.getByLabelText('delete');
    await user.click(deleteButton);
    
    // Should not throw an error, just log to console
    await waitFor(() => {
      expect(mockDeleteItem).toHaveBeenCalledWith(listName, itemName);
    });
  });
});