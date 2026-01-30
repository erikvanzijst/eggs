import React, { useState, useEffect, useCallback } from 'react';
import { 
  List, 
  Typography, 
  Box, 
  CircularProgress,
  Alert
} from '@mui/material';
import ShoppingListService from '../services/shoppingListService';
import AddItemForm from './AddItemForm';
import Item from './Item';

interface ItemListProps {
  listName?: string;
}

const ItemList = ({ listName }: ItemListProps) => {
  const [items, setItems] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchItems = useCallback(async () => {
    if (!listName) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const itemsData = await ShoppingListService.getItems(listName);

      // Sort items alphabetically (case insensitive)
      const sortedItems = itemsData.sort((a, b) =>
        a.toLowerCase().localeCompare(b.toLowerCase())
      );

      setItems(sortedItems);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [listName]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]);

  const handleItemAdded = () => {
    // Refresh the items list after adding a new item
    fetchItems();
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Error loading items: {error}
      </Alert>
    );
  }

  return (
    <>
      <AddItemForm listName={listName!} onItemAdded={handleItemAdded} />
      {items.length === 0 ? (
        <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
          <Typography variant="body1" color="textSecondary">
            No items in this list
          </Typography>
        </Box>
      ) : (
        <List>
          {items.map((itemName) => (
            <Item
              key={itemName}
              listName={listName!}
              itemName={itemName}
              onItemDeleted={fetchItems}
            />
          ))}
        </List>
      )}
    </>
  );
};

export default ItemList;