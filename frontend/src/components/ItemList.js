import React, { useState, useEffect } from 'react';
import { 
  List, 
  ListItem, 
  ListItemText, 
  Typography, 
  Box, 
  CircularProgress,
  Alert
} from '@mui/material';
import ShoppingListService from '../services/shoppingListService';

const ItemList = ({ listName }) => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchItems = async () => {
      if (!listName) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);
        
        const itemsData = await ShoppingListService.fetchItems(listName);
        
        // Sort items alphabetically (case insensitive)
        const sortedItems = itemsData.sort((a, b) => 
          a.toLowerCase().localeCompare(b.toLowerCase())
        );
        
        setItems(sortedItems);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchItems();
  }, [listName]);

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

  if (items.length === 0) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={200}>
        <Typography variant="body1" color="textSecondary">
          No items in this list
        </Typography>
      </Box>
    );
  }

  return (
    <List>
      {items.map((itemName, index) => (
        <ListItem key={index}>
          <ListItemText primary={itemName} />
        </ListItem>
      ))}
    </List>
  );
};

export default ItemList;