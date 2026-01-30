import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useParams } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ListHeader from './components/ListHeader';
import ItemList from './components/ItemList';
import ShoppingListService from './services/shoppingListService';
import { NotFoundError } from "./exceptions";

const theme = createTheme();

// Component to display a specific list by name
const ListDisplay = ({ listName }: { listName: string }) => {
  return (
    <div className="App">
      <ListHeader listName={listName} />
      <ItemList listName={listName} />
    </div>
  );
};

// Component to handle the list route with dynamic list name
const ListRoute = () => {
  const { listName } = useParams<{ listName: string }>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchOrCreateList = async () => {

      if (listName) {
        try {
          try {
            await ShoppingListService.getList(listName);
          } catch (error) {
            if (error instanceof NotFoundError) {
              console.log('List not found -- auto-creating...');
              await ShoppingListService.createList(listName);
            } else {
              throw error;
            }
          }
        } catch (error) {
          console.error('Error fetching list:', error);
          setError('Failed to load lists');
        } finally {
          setLoading(false);
        }
      } else {
        console.log("listName not set!");
      }
    };

    fetchOrCreateList();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
        Loading list...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
        <h2>{error}</h2>
      </div>
    );
  }

  if (!listName) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
        <h2>Invalid list name: {listName || 'No list specified'}</h2>
      </div>
    );
  }

  return <ListDisplay listName={listName} />;
};

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <Routes>
            <Route path="/:listName" element={<ListRoute />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;