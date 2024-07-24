import React from 'react';
import Register from './pages/Register'
import Login from './pages/Login'
import Home from './pages/Home';
import HostedListings from './pages/HostedListings';
import './App.css';
import NavBar from './components/NavBar';
import { CssBaseline } from '@mui/material';
import ViewListing from './pages/ViewListing';

import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';

function App () {
  const [token, setToken] = React.useState(null);
  const [currUserEmail, setCurrUserEmail] = React.useState(null);
  console.log(token);

  return (
    <BrowserRouter>
      <CssBaseline />
      <NavBar token={token} setTokenFn={setToken} />
      <br />
      <main>
        <Routes>
          <Route path='/login' element={<Login setTokenFn={setToken} setCurrUserEmailFn={setCurrUserEmail} />} />
          <Route path='/register' element={<Register setTokenFn={setToken} setCurrUserEmailFn={setCurrUserEmail} />} />
          <Route path='/hosted/*' element={<HostedListings token={token} currUserEmail={currUserEmail} />} />
          <Route path='/listing/:listingId' element={<ViewListing token={token} />} />
          <Route path='/' element={<Home token={token} currUserEmail={currUserEmail}/>} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
