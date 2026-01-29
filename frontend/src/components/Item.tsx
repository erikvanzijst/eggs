import React from 'react';
import {
  ListItem,
  ListItemText,
  IconButton,
  Typography
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import ShoppingListService from '../services/shoppingListService';

interface ItemProps {
  listName: string;
  itemName: string;
  onItemDeleted?: () => void;
}

const Item = ({ listName, itemName, onItemDeleted }: ItemProps) => {
  const handleDelete = async () => {
    if (!listName || !itemName) return;
    
    try {
      await ShoppingListService.deleteItem(listName, itemName);
      if (onItemDeleted) {
        onItemDeleted();
      }
    } catch (error) {
      console.error(`Error deleting item ${itemName}:`, error);
      // In a real app, you might want to show an error to the user
    }
  };

  return (
    <ListItem 
      sx={{ 
        py: 1,
        px: 2,
        borderRadius: 1,
        mb: 1,
        bgcolor: 'background.paper',
        boxShadow: 1
      }}
    >
      <ListItemText 
        primary={
          <Typography variant="body1" component="span">
            {itemName}
          </Typography>
        } 
      />
      <IconButton 
        aria-label="delete"
        onClick={handleDelete}
        size="small"
        sx={{ ml: 2 }}
      >
        <DeleteIcon fontSize="small" />
      </IconButton>
    </ListItem>
  );
};

export default Item;