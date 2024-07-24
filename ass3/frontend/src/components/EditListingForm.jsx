import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import PropTypes from 'prop-types';
import { makeRequest, fileToDataUrl } from '../helpers';
import { useNavigate } from 'react-router-dom';

function EditListingForm (props) {
  const [file, setFile] = React.useState();
  const [fileDisplay, setFileDisplay] = React.useState();
  const navigate = useNavigate();

  // Input Data
  const [listingTitle, setListingTitle] = React.useState('');
  const [listingAddress, setListingAddress] = React.useState('');
  const [listingPrice, setListingPrice] = React.useState('');
  const [propertyType, setPropertyType] = React.useState('');
  const [numberOfBathrooms, setNumberOfBathrooms] = React.useState('');
  const [numberOfBedrooms, setNumberOfBedrooms] = React.useState('');
  const [numberOfBeds, setNumberOfBed] = React.useState('');
  const [propertyAmenities, setPropertyAmenities] = React.useState('');
  const [propertyImages, setPropertyImages] = React.useState([]);
  const [propertyImageDisplays, setPropertyImageDisplays] = React.useState([]);

  console.log(file)
  console.log(propertyImages)

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

  React.useEffect(() => {
    setListingTitle(props.listingInfo.listingTitle);
    setListingAddress(props.listingInfo.listingAddress);
    setListingPrice(props.listingInfo.listingPrice);
    setPropertyType(props.listingInfo.propertyType);
    setNumberOfBathrooms(props.listingInfo.numberOfBathrooms);
    setNumberOfBedrooms(props.listingInfo.numberOfBedrooms);
    setNumberOfBed(props.listingInfo.numberOfBeds);
    setPropertyAmenities(props.listingInfo.propertyAmenities);
    setFileDisplay(props.listingInfo.thumbnail);
    setPropertyImageDisplays(props.listingInfo.propertyImages)
  }, [])

  // Called when a thumbnail is uploaded
  const handleChange = async (e) => {
    setFile(e.target.files[0]);
    try {
      setFileDisplay(await fileToDataUrl(e.target.files[0]));
    } catch (error) {
      alert(error);
    }
  }

  // Called when property images are uploaded
  const handleChangeMultiple = async (e) => {
    setPropertyImages(e.target.files)

    const propImagesArr = [];
    let b64 = null;
    for (const fl of e.target.files) {
      try {
        b64 = await fileToDataUrl(fl);
      } catch (error) {
        alert(error.error);
      }
      propImagesArr.push(b64);
    }

    setPropertyImageDisplays(propImagesArr);
  }

  // Called when confirm button is clicked
  const handleConfirmBtn = async () => {
    for (const element of [listingTitle, listingAddress, listingPrice, propertyType, numberOfBathrooms, numberOfBedrooms, numberOfBeds, propertyAmenities]) {
      if (!element) {
        alert('Input cannot be blank');
        return;
      }
    }

    // Makes edit request to backend
    const response = makeRequest(`/listings/${props.listingInfo.id}`, 'PUT',
      {
        'Content-type': 'application/JSON',
        Authorization: `Bearer ${props.token}`
      },
      {
        title: listingTitle,
        address: listingAddress,
        price: listingPrice,
        thumbnail: fileDisplay,
        metadata: {
          propertyType,
          numberOfBathrooms,
          numberOfBedrooms,
          numberOfBeds,
          propertyAmenities,
          propertyImages: propertyImageDisplays,
        }
      }
    )

    try {
      await response;
      emptyInputs();
      props.handleCloseFn();
      navigate('/hosted')
      props.fetchListingsFn();
    } catch (error) {
      alert(error.error);
    }
  }

  return (
      <div>
        <Dialog open={props.open} onClose={props.handleCloseFn}>
          <DialogTitle>Edit Listing</DialogTitle>
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
              <Button sx={{ margin: '10px 0' }} variant='contained' component='label'>
                Upload Thumbnail
                <input type='file' onChange={handleChange} hidden />
              </Button> <br />
              <img src={fileDisplay} width='200px'alt='User uploaded thumbnail' /> <br />
              <Button sx={{ margin: '10px 0' }} variant='contained' component='label'>
                Upload Property Images
                <input multiple type='file' onChange={handleChangeMultiple} hidden />
              </Button>
              <br />
              {
                propertyImageDisplays.map((propertyImage) => {
                  return (
                      <img key={propertyImage} src={propertyImage} width = '200px' alt='User Uploaded Property Images' />
                  )
                })
              }
          </DialogContent>
          <DialogActions>
            <Button onClick={props.handleCloseFn}>Cancel</Button>
            <Button onClick={handleConfirmBtn}>Confirm</Button>
          </DialogActions>
        </Dialog>
      </div>
  );
}

EditListingForm.propTypes = {
  token: PropTypes.string,
  open: PropTypes.bool,
  handleCloseFn: PropTypes.func,
  fetchListingsFn: PropTypes.func,
  listingInfo: PropTypes.object
};

export default EditListingForm;
