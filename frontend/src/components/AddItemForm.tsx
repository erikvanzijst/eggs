import React, { useState } from 'react';
import {
  Box,
  TextField,
  Button,
  Alert
} from '@mui/material';
import ShoppingListService from '../services/shoppingListService';
import {ConflictError} from "../exceptions";

interface AddItemFormProps {
  listName?: string;
  onItemAdded?: () => void;
}

const AddItemForm = ({ listName, onItemAdded }: AddItemFormProps) => {
  const [itemName, setItemName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Reset previous messages
    setError(null);
    setSuccess(false);
    
    // Validation
    if (!itemName.trim()) {
      setError('Item name is required');
      return;
    }
    
    if (!listName) {
      setError('List name is required');
      return;
    }
    
    setLoading(true);
    
    try {
      // Create the item
      await ShoppingListService.createItem(listName, {name: itemName.trim()});

      // Reset form
      setItemName('');
      setSuccess(true);

      // Call parent callback if provided
      if (onItemAdded) {
        onItemAdded();
      }
    } catch (err: any) {
      if (err instanceof ConflictError) {
        setError(`We already have ${itemName}!`);
      } else {
        setError(`Error adding item: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      {success && (
        <Alert severity="success" sx={{ mb: 2 }} data-testid="success-message">
          Item added successfully!
        </Alert>
      )}
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }} data-testid="error-message">
          {error}
        </Alert>
      )}
      
      <Box sx={{ display: 'flex', gap: 2, alignItems: 'end' }}>
        <TextField
          fullWidth
          label="Item name"
          variant="outlined"
          value={itemName}
          onChange={(e) => setItemName(e.target.value)}
          error={!!error && error.includes('required')}
          helperText={error && error.includes('required') ? 'Item name is required' : ''}
          data-testid="item-name-input"
        />
        <Button
          type="submit"
          variant="contained"
          disabled={loading || !itemName.trim()}
          sx={{ height: '56px' }}
          data-testid="add-item-button"
        >
          {loading ? 'Adding...' : 'Add Item'}
        </Button>
      </Box>
    </Box>
  );
};

export default AddItemForm;