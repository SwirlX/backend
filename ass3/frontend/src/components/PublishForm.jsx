import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import Typography from '@mui/material/Typography';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import PropTypes from 'prop-types';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { makeStyles } from '@mui/styles';

import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

import { makeRequest } from '../helpers';

const useStyles = makeStyles((theme) => ({
  dialogTitle: {
    marginBottom: '10px',
  },
  dialogContent: {
    paddingTop: '5px'
  }
}))

PublishForm.propTypes = {
  token: PropTypes.string,
  open: PropTypes.bool,
  handleCloseFn: PropTypes.func,
  listingInfo: PropTypes.object,
  channelToPublish: PropTypes.number,
  fetchListingsFn: PropTypes.func,
};

function PublishForm (props) {
  const classes = useStyles();
  const [from, setFrom] = React.useState();
  const [to, setTo] = React.useState();
  const [disablePublishBtn, setDisablePublishBtn] = React.useState(true);

  const [availList, setAvailList] = React.useState([]);

  // Called when the add button is clicked.
  // Adds the inputted availability into a list
  const handleAddAvail = () => {
    if (!from || !to) {
      alert('Must pick a date range!')
      return;
    }

    setAvailList([...availList, {
      start: from,
      end: to,
    }])
    setFrom()
    setTo()
    setDisablePublishBtn(false);
  }

  // Called when cancel button is clicked
  const handleCancel = () => {
    setAvailList([]);
    props.handleCloseFn();
  }

  // Called when the publish button is clicked
  const handlePublishBtn = async () => {
    if (availList.length === 0) {
      alert('Must add availability dates!')
      return;
    }

    const response = makeRequest(`/listings/publish/${props.channelToPublish}`, 'PUT',
      {
        'Content-type': 'application/JSON',
        Authorization: `Bearer ${props.token}`
      },
      {
        availability: availList
      }
    )

    try {
      await response;
      props.handleCloseFn();
      props.fetchListingsFn();
    } catch (error) {
      alert(error.error)
    }
  }

  return (
      <div>
        <Dialog open={props.open} onClose={props.handleCloseFn}>
          <DialogTitle className={classes.dialogTitle}>Availabilities</DialogTitle>
          <br />
          <DialogContent className={classes.dialogContent}>
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker
                label="From"
                value={from}
                onChange={(newValue) => {
                  setFrom(newValue);
                }}
                renderInput={(params) => <TextField name='fromDatepicker' {...params} />}
              />
              <DatePicker
                label="To"
                value={to}
                onChange={(newValue) => {
                  setTo(newValue);
                }}
                renderInput={(params) => <TextField name='toDatepicker' {...params} />}
              />
            </LocalizationProvider>
            <br />
          <Button name='addAvailButton' sx={{ margin: '10px 0' }} variant='contained' component='label' onClick={handleAddAvail}>
              Add
          </Button>
          <Typography variant='h6'>
            Added Availabilities:
          </Typography>
          {
            availList.map((availRange) => {
              const start = availRange.start;
              const end = availRange.end;
              return (
                <>
                  <Typography>
                    {`${start.$M}/${start.$D}/${start.$y}`} - {`${end.$M}/${end.$D}/${end.$y}`}
                  </Typography>
                </>
              )
            })
          }
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCancel}>Cancel</Button>
            <Button name='publishConfirmButton' disabled={disablePublishBtn} onClick={handlePublishBtn}>Publish</Button>
          </DialogActions>
        </Dialog>
      </div>
  );
}

export default PublishForm;
