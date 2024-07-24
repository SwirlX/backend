import React from 'react';
import { Typography, AppBar, Button, Toolbar } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import { makeRequest } from '../helpers';

function NavBar (props) {
  const navBtnStyle = { m: 1 };
  const navigate = useNavigate();

  const logoutBtn = async () => {
    console.log('Logout Clicked')
    console.log(props.token)
    const response = makeRequest('/user/auth/logout', 'POST', {
      'Content-type': 'application/JSON',
      Authorization: `Bearer ${props.token}`
    });

    try {
      await response;
      props.setTokenFn(null);
      navigate('/')
    } catch (error) {
      alert(error.error);
    }
  }

  return (
    <AppBar position='relative'>
      <Toolbar>
        <Typography variant='h6' component={Link} to='/' color='inherit'>
          AirBrB
        </Typography>
        {!props.token && (
          <>
            <Button sx={navBtnStyle} name='loginButton' variant='outlined' color='inherit' component={Link} to='/login'>
              Login
            </Button>
            <Button sx={navBtnStyle} name='registerButton' variant='outlined' color='inherit' component={Link} to='/register'>
                Register
            </Button>
          </>
        )}
        {props.token && (
          <>
            <Button sx={navBtnStyle} name='logoutButton' variant='outlined' color='inherit' onClick={logoutBtn}>
              Logout
            </Button>
            <Button sx={navBtnStyle} name='hostedListingsButton' variant='outlined' color='inherit' component={Link} to='/hosted'>
              Hosted Listings
            </Button>
          </>
        )}
      </Toolbar>
    </AppBar>
  )
}

NavBar.propTypes = {
  token: PropTypes.string,
  setTokenFn: PropTypes.func,
};

export default NavBar;
