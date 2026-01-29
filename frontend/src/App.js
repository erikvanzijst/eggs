import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = createTheme();

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <h1>React Frontend for Eggs API</h1>
          <p>Welcome to the React frontend for the Eggs API</p>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;