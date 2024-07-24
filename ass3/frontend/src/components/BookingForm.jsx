import React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import { makeStyles } from '@mui/styles';
import PropTypes from 'prop-types';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { makeRequest, getPriceFromNightsStayed } from '../helpers';

const useStyles = makeStyles((theme) => ({
  dialogTitle: {
    marginBottom: '10px',
  },
  dialogContent: {
    paddingTop: '5px'
  }
}))

BookingForm.propTypes = {
  token: PropTypes.string,
  open: PropTypes.bool,
  handleCloseFn: PropTypes.func,
  listingId: PropTypes.string,
  listingInfo: PropTypes.object,
  availability: PropTypes.array,
};

function BookingForm (props) {
  const classes = useStyles();
  const [from, setFrom] = React.useState();
  const [to, setTo] = React.useState();

  const handleClose = () => {
    setFrom();
    setTo();
    props.handleCloseFn();
  }

  const handleBookBtn = async () => {
    if (typeof from === 'undefined' || typeof to === 'undefined') {
      alert('Must pick booking date');
      return;
    }

    const price = getPriceFromNightsStayed(from, to, props.listingInfo.price)

    const response = makeRequest(`/bookings/new/${props.listingId}`, 'POST',
      {
        'Content-type': 'application/JSON',
        Authorization: `Bearer ${props.token}`
      },
      {
        dateRange: {
          start: from,
          end: to
        },
        totalPrice: price,
      }
    );

    try {
      await response;
      alert(`Made a booking at ${props.listingInfo.title} for a total price of $${price}`)
    } catch (error) {
      alert(error.error);
      return;
    }

    props.handleCloseFn();
  }

  return (
      <div>
        <Dialog open={props.open} onClose={props.handleCloseFn}>
          <DialogTitle className={classes.dialogTitle}>Making a Booking</DialogTitle>
          <DialogContent className={classes.dialogContent}>
            <Typography variant='h6'>
              Available Dates:
            </Typography>
            {
              props.availability?.map((avail) => {
                const startDateObj = new Date(avail.start)
                const endDateObj = new Date(avail.end)

                const startMonth = startDateObj.getMonth();
                const startDay = startDateObj.getDate();
                const startYear = startDateObj.getFullYear();

                const endMonth = endDateObj.getMonth();
                const endDay = endDateObj.getDate();
                const endYear = endDateObj.getFullYear();
                return (
                  <Typography key={avail.start}>
                    {`${startMonth}/${startDay}/${startYear}`} - {`${endMonth}/${endDay}/${endYear}`}
                  </Typography>
                )
              })
            }
            <br />
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker
                label="From"
                value={from}
                onChange={(newValue) => {
                  setFrom(newValue);
                }}
                renderInput={(params) => <TextField {...params} />}
              />
              <DatePicker
                label="To"
                value={to}
                onChange={(newValue) => {
                  setTo(newValue);
                }}
                renderInput={(params) => <TextField {...params} />}
              />
            </LocalizationProvider>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button onClick={handleBookBtn}>Book</Button>
          </DialogActions>
        </Dialog>
      </div>
  );
}

export default BookingForm;
