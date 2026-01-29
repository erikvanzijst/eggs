import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useParams } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ListHeader from './components/ListHeader';
import ItemList from './components/ItemList';
import ShoppingListService from './services/shoppingListService';

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
  const [validLists, setValidLists] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchLists = async () => {
      try {
        const lists = await ShoppingListService.fetchLists();
        setValidLists(lists);
      } catch (error) {
        console.error('Error fetching lists:', error);
        setError('Failed to load lists');
      } finally {
        setLoading(false);
      }
    };

    fetchLists();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '200px' }}>
        Loading lists...
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

  // Check if the list exists
  if (!listName || !validLists.includes(listName)) {
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
            <Route path="/" element={<Navigate to="/lists/Grocery List" replace />} />
            <Route path="/lists/:listName" element={<ListRoute />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;