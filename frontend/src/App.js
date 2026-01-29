import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import ListHeader from './components/ListHeader';
import ItemList from './components/ItemList';

const theme = createTheme();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <ListHeader listName="Grocery List" />
          <ItemList listName="Grocery List" />
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;