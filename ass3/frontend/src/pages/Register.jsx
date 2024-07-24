import React from 'react';
import PropTypes from 'prop-types';
import { makeRequest } from '../helpers';
import { makeStyles } from '@mui/styles';
import { TextField, Button } from '@mui/material';

import {
  useNavigate
} from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  registerContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '20px'
  },
  registerBtn: {
    margin: '20px',
  }
}))

function Register (props) {
  const classes = useStyles();
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [passwordConfirm, setPasswordConfirm] = React.useState('');
  const [name, setName] = React.useState('');
  const navigate = useNavigate();

  // Registers user when register button clicked
  const registerBtn = async () => {
    console.log('Register Clicked!');

    if (password !== passwordConfirm) {
      alert('Confirm password does not match given password');
      return;
    }

    const response = makeRequest('/user/auth/register', 'POST', { 'Content-type': 'application/JSON' }, {
      email,
      password,
      name,
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
    <div className={classes.registerContainer}>
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
        <TextField
          id="passConfirmInput"
          className="text"
          label="Confirm Password"
          type='password'
          variant="outlined"
          placeholder="Confirm password"
          size="small"
          value={passwordConfirm}
          onChange={(e) => setPasswordConfirm(e.target.value)}
        />
      <TextField
          id="nameInput"
          className="text"
          label="Name"
          variant="outlined"
          placeholder="Enter name"
          size="small"
          value={name}
          onChange={(e) => setName(e.target.value)}
      />
      <Button name='submitRegisterButton' variant='contained' onClick={registerBtn}>Register</Button>
    </div>
    </>
  )
}

Register.propTypes = {
  setTokenFn: PropTypes.func,
  setCurrUserEmailFn: PropTypes.func,
};

export default Register;
