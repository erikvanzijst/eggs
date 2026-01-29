# Frontend for Eggs API

This directory contains the React frontend for the Eggs API project.

## Structure

- `src/` - Source code for the React application
- `public/` - Static files like HTML, images, etc.

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

### `npm test -- --watchAll=false`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

## Dependencies

- React
- React DOM
- React Router DOM
- MUI (Material UI)
- Emotion for styling

## Testing

This project includes unit tests for the shopping list service using React Testing Library and fetch mocks. To run the tests:

```bash
npm test
```

Tests are located in `src/services/shoppingListService.test.ts`.