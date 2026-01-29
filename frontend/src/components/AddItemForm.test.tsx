import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import AddItemForm from './AddItemForm';
import ShoppingListService from '../services/shoppingListService';

// Mock the ShoppingListService
jest.mock('../services/shoppingListService');

describe('AddItemForm', () => {
  const mockListName = 'Test List';
  const mockOnItemAdded = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders correctly', () => {
    render(
      <AddItemForm 
        listName={mockListName} 
        onItemAdded={mockOnItemAdded} 
      />
    );

    expect(screen.getByLabelText('Item name')).toBeInTheDocument();
    expect(screen.getByTestId('add-item-button')).toBeInTheDocument();
  });

  test('shows error when item name is empty', async () => {
    render(
      <AddItemForm 
        listName={mockListName} 
        onItemAdded={mockOnItemAdded} 
      />
    );

    const addButton = screen.getByTestId('add-item-button');
    
    // Click without entering text
    fireEvent.click(addButton);
    
    expect(screen.getByTestId('error-message')).toBeInTheDocument();
  });

  test('shows error when list name is empty', async () => {
    render(
      <AddItemForm 
        listName={undefined} 
        onItemAdded={mockOnItemAdded} 
      />
    );

    const itemNameInput = screen.getByTestId('item-name-input');
    const addButton = screen.getByTestId('add-item-button');
    
    // Enter text and click
    fireEvent.change(itemNameInput, { target: { value: 'Test Item' } });
    fireEvent.click(addButton);
    
    expect(screen.getByTestId('error-message')).toBeInTheDocument();
  });

  test('submits form successfully', async () => {
    (ShoppingListService.createItem as jest.Mock).mockResolvedValue({});

    render(
      <AddItemForm 
        listName={mockListName} 
        onItemAdded={mockOnItemAdded} 
      />
    );

    const itemNameInput = screen.getByTestId('item-name-input');
    const addButton = screen.getByTestId('add-item-button');

    fireEvent.change(itemNameInput, { target: { value: 'Test Item' } });
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(ShoppingListService.createItem).toHaveBeenCalledWith(mockListName, { name: 'Test Item' });
    });
    
    expect(screen.getByTestId('success-message')).toBeInTheDocument();
    expect(mockOnItemAdded).toHaveBeenCalledTimes(1);
  });

  test('shows error when submission fails', async () => {
    (ShoppingListService.createItem as jest.Mock).mockRejectedValue(new Error('Network error'));

    render(
      <AddItemForm 
        listName={mockListName} 
        onItemAdded={mockOnItemAdded} 
      />
    );

    const itemNameInput = screen.getByTestId('item-name-input');
    const addButton = screen.getByTestId('add-item-button');

    fireEvent.change(itemNameInput, { target: { value: 'Test Item' } });
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(ShoppingListService.createItem).toHaveBeenCalledWith(mockListName, { name: 'Test Item' });
    });
    
    expect(screen.getByTestId('error-message')).toBeInTheDocument();
  });
});