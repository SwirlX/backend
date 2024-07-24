import React from 'react';
import PropTypes from 'prop-types';
import { makeRequest } from '../helpers';
import { TextField, Button } from '@mui/material';
import { makeStyles } from '@mui/styles';
import {
  useNavigate
} from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  loginContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  loginBtn: {
    margin: '20px',
  }
}))

function Login (props) {
  const classes = useStyles();
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const navigate = useNavigate();

  // Logs user in when login button clicked
  const loginBtn = async () => {
    console.log('Login Clicked!');

    const response = makeRequest('/user/auth/login', 'POST', { 'Content-type': 'application/JSON' }, {
      email,
      password,
    });

    try {
      const data = await response;
      props.setTokenFn(data.token);
      props.setCurrUserEmailFn(email);
      navigate('/')
    } catch (error) {
      alert(error.error);
    }
  }

  return (
    <>
    <div className={classes.loginContainer}>
      <TextField
        id="emailInput"
        className="text"
        label="Email"
        variant="outlined"
        placeholder="email@domain.com"
        size="small"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <br />
      <TextField
        id="passInput"
        className="text"
        label="Password"
        type='password'
        variant="outlined"
        placeholder="Enter password"
        size="small"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <Button name='loginConfirmButton' className={classes.loginBtn} variant='contained' onClick={loginBtn}>Login</Button>
    </div>
    </>
  )
}

Login.propTypes = {
  setTokenFn: PropTypes.func,
  setCurrUserEmailFn: PropTypes.func,
};

export default Login;
