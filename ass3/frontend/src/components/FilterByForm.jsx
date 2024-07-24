import React from 'react';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import PropTypes from 'prop-types';
import Slider from '@mui/material/Slider';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';

export default function FilterByForm (props) {
  return (
    <div>
      <Dialog open={props.open} onClose={props.handleCloseFn}>
        <DialogTitle>Filter By</DialogTitle>
        <br />
        <DialogContent>

          <Typography variant='h7'>
            Number of Bedrooms:
          </Typography>
          <Slider
            getAriaLabel={() => 'Number of Bedrooms range'}
            value={props.bedroomRange}
            onChange={(e, newValue) => props.setBedroomRangeFn(newValue)}
            valueLabelDisplay="auto"
            getAriaValueText={() => `${props.bedroomRange}`}
            max={20}
          />
          <Typography variant='h7'>
            Availability Range:
          </Typography>
          <br />
          <br />
          <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker
                label="From"
                value={props.from}
                onChange={(newValue) => {
                  props.setFromFn(newValue);
                }}
                renderInput={(params) => <TextField {...params} />}
              />
              <DatePicker
                label="To"
                value={props.to}
                onChange={(newValue) => {
                  props.setToFn(newValue);
                }}
                renderInput={(params) => <TextField {...params} />}
              />
              <Typography variant='h7'>
                  Price Range:
              </Typography>
              <Slider
                getAriaLabel={() => 'Price Range'}
                value={props.priceRange}
                onChange={(e, newValue) => props.setPriceRangeFn(newValue)}
                valueLabelDisplay="auto"
                getAriaValueText={() => `${props.priceRange}`}
                max={2000}
              />
            </LocalizationProvider>
        </DialogContent>
        <DialogActions>
          <Button onClick={props.handleCloseFn}>Cancel</Button>
          <Button onClick={props.handleDiscardFiltersFn} >Discard Filters</Button>
          <Button onClick={props.handleFilterApplyFn}>Apply</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

FilterByForm.propTypes = {
  token: PropTypes.string,
  currUserEmail: PropTypes.string,
  open: PropTypes.bool,
  handleCloseFn: PropTypes.func,
  bedroomRange: PropTypes.array,
  setBedroomRangeFn: PropTypes.func,
  priceRange: PropTypes.array,
  setPriceRangeFn: PropTypes.func,
  from: PropTypes.object,
  setFromFn: PropTypes.func,
  to: PropTypes.object,
  setToFn: PropTypes.func,
  handleFilterApplyFn: PropTypes.func,
  handleDiscardFiltersFn: PropTypes.func
};
