import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import PropTypes from 'prop-types';
import { makeRequest, fileToDataUrl } from '../helpers';

function CreateListingForm (props) {
  const [file, setFile] = React.useState();
  const [fileDisplay, setFileDisplay] = React.useState();

  // Input Data
  const [listingTitle, setListingTitle] = React.useState('');
  const [listingAddress, setListingAddress] = React.useState('');
  const [listingPrice, setListingPrice] = React.useState('');
  const [propertyType, setPropertyType] = React.useState('');
  const [numberOfBathrooms, setNumberOfBathrooms] = React.useState('');
  const [numberOfBedrooms, setNumberOfBedrooms] = React.useState('');
  const [numberOfBeds, setNumberOfBed] = React.useState('');
  const [propertyAmenities, setPropertyAmenities] = React.useState('');

  const emptyInputs = () => {
    setListingTitle('');
    setListingAddress('');
    setListingPrice('');
    setPropertyType('');
    setNumberOfBathrooms('');
    setNumberOfBedrooms('');
    setNumberOfBed('');
    setPropertyAmenities('');
    setFile();
    setFileDisplay();
  }

  // Called when a thumbnail is uploaded
  const handleChange = (e) => {
    setFile(e.target.files[0]);
    setFileDisplay(URL.createObjectURL(e.target.files[0]));
  }

  // Called when create button is clicked
  const handleCreateBtn = async () => {
    if (!file) {
      alert('Thumbnail required');
      return;
    }

    for (const element of [listingTitle, listingAddress, listingPrice, propertyType, numberOfBathrooms, numberOfBedrooms, numberOfBeds, propertyAmenities]) {
      if (!element) {
        alert('Input cannot be blank');
        return;
      }
    }

    let fileDataURL = null;
    try {
      fileDataURL = await fileToDataUrl(file);
    } catch (error) {
      alert(error);
      return;
    }

    const response = makeRequest('/listings/new', 'POST',
      {
        'Content-type': 'application/JSON',
        Authorization: `Bearer ${props.token}`
      },
      {
        title: listingTitle,
        address: listingAddress,
        price: listingPrice,
        thumbnail: fileDataURL,
        metadata: {
          propertyType,
          numberOfBathrooms,
          numberOfBedrooms,
          numberOfBeds,
          propertyAmenities,
          propertyImages: [],
        }
      }
    )

    try {
      const listingId = await response;
      console.log(listingId);
      props.handleCloseFn();
      emptyInputs();
      props.fetchListingsFn();
    } catch (error) {
      alert(error.error);
    }
  }

  return (
    <div>
      <Dialog open={props.open} onClose={props.handleCloseFn}>
        <DialogTitle>Add New Listing</DialogTitle>
        <DialogContent>
          <TextField
            required
            autoFocus
            margin="dense"
            id="listingTitle"
            label="Listing Title"
            type="text"
            fullWidth
            variant="standard"
            onChange={(event) => setListingTitle(event.target.value)}
            value={listingTitle}
          />
          <TextField
            required
            margin="dense"
            id="listingAddress"
            label="Listing Address"
            type="text"
            fullWidth
            variant="standard"
            value={listingAddress}
            onChange={(event) => setListingAddress(event.target.value)}
          />
          <TextField
            required
            margin="dense"
            id="listingPrice"
            label="Listing Price"
            type="text"
            fullWidth
            variant="standard"
            value={listingPrice}
            onChange={(event) => setListingPrice(event.target.value)}
            />
          <TextField
            required
            margin="dense"
            id="propertyType"
            label="Property Type"
            type="text"
            fullWidth
            variant="standard"
            value={propertyType}
            onChange={(event) => setPropertyType(event.target.value)}
            />
          <TextField
            required
            margin="dense"
            id="numberOfBathrooms"
            label="Number of Bathrooms"
            type="number"
            fullWidth
            variant="standard"
            value={numberOfBathrooms}
            onChange={(event) => setNumberOfBathrooms(event.target.value)}
            />
          <TextField
            required
            margin="dense"
            id="numberOfBedrooms"
            label="Number of Bedrooms"
            type="number"
            fullWidth
            variant="standard"
            value={numberOfBedrooms}
            onChange={(event) => setNumberOfBedrooms(event.target.value)}
            />
          <TextField
            required
            margin="dense"
            id="numberOfBeds"
            label="Number of Beds"
            type="number"
            fullWidth
            variant="standard"
            value={numberOfBeds}
            onChange={(event) => setNumberOfBed(event.target.value)}
            />
          <TextField
            margin="dense"
            id="propertyAmenities"
            label="Property Amenities"
            type="text"
            fullWidth
            variant="standard"
            value={propertyAmenities}
            onChange={(event) => setPropertyAmenities(event.target.value)}
            />
            <Button name='listingThumbnailUpload' variant='contained' component='label'>
              Upload Thumbnail
              <input type='file' onChange={handleChange} hidden />
            </Button>
            <img src={fileDisplay} width='200px' alt='User uploaded thumbnail'/>
        </DialogContent>
        <DialogActions>
          <Button onClick={props.handleCloseFn}>Cancel</Button>
          <Button name='listingCreateButton' onClick={handleCreateBtn}>Create</Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

CreateListingForm.propTypes = {
  token: PropTypes.string,
  open: PropTypes.bool,
  handleCloseFn: PropTypes.func,
  fetchListingsFn: PropTypes.func,
};

export default CreateListingForm;
