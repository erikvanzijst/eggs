import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ListHeader from './components/ListHeader';
import ItemList from './components/ItemList';
import ShoppingListService from './services/shoppingListService';

const theme = createTheme();

function App() {
  const [lists, setLists] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLists = async () => {
      try {
        setLoading(true);
        const fetchedLists = await ShoppingListService.fetchLists();
        setLists(fetchedLists);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchLists();
  }, []);

  // Render component for list display
  const ListDisplay = ({ listName }: { listName: string }) => {
    return (
      <div className="App">
        <ListHeader listName={listName} />
        <ItemList listName={listName} />
      </div>
    );
  };

  // Route handler for /lists/:listName
  const ListRoute = () => {
    // This will be handled by routing
    return null;
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Navigate to="/lists/Grocery List" replace />} />
            <Route 
              path="/lists/:listName" 
              element={
                loading ? (
                  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
                    Loading lists...
                  </div>
                ) : error ? (
                  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
                    <h2>Error: {error}</h2>
                  </div>
                ) : lists.length > 0 ? (
                  <ListDisplay listName={lists[0]} />
                ) : (
                  <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
                    <h2>No lists available</h2>
                  </div>
                )
              } 
            />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;