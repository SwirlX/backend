import React from 'react';
import { Typography, Button } from '@mui/material';
import { PropTypes } from 'prop-types';
import { useParams, useNavigate } from 'react-router-dom';
import { makeRequest } from '../helpers';
import BookingForm from '../components/BookingForm';

const styles = {
  infoContainer: {
    margin: '0 70px'
  }
}

ViewListing.propTypes = {
  token: PropTypes.string,
};

function ViewListing (props) {
  const params = useParams();
  const navigate = useNavigate();
  const listingId = params.listingId;
  const [listingInfo, setListingInfo] = React.useState();
  const [openBooking, setOpenBooking] = React.useState(false);

  const handleBookingClose = () => {
    setOpenBooking(false);
  }

  const getListingInfo = async () => {
    const request = makeRequest(`/listings/${listingId}`, 'GET', {
      'Content-type': 'application/JSON',
      Authorization: `Bearer ${props.token}`
    });
    try {
      const data = await request;
      setListingInfo(data.listing);
    } catch (error) {
      alert(error.error);
    }
  }

  React.useEffect(() => {
    getListingInfo();
  }, [])

  return (
    <>
    <div style={styles.infoContainer}>
      <Typography variant='h4'>
        {listingInfo?.title}
      </Typography>

      <img src={listingInfo?.thumbnail} width='350px' alt="Thumbnail photo" />

      <Typography variant='h5' >
        Property Images:
      </Typography>

      {
        listingInfo?.metadata.propertyImages.map((image) => {
          return (
            <img key={image} src={image} width='200px' alt='Provided property images' />
          )
        })
      }

      <Typography >
        Address: {listingInfo?.address}
      </Typography>

      <Typography >
        Amenities: {listingInfo?.metadata.propertyAmenities}
      </Typography>

      <Typography >
        Price: ${listingInfo?.price}
      </Typography>

      <Typography >
        Listing Type: {listingInfo?.metadata.propertyType}
      </Typography>

      <Typography >
        Review Ratings
      </Typography>

      <Typography >
        Reviews
      </Typography>

      <Typography >
        Number of Bedrooms: {listingInfo?.metadata.numberOfBedrooms}
      </Typography>

      <Typography >
        Number of Beds: {listingInfo?.metadata.numberOfBeds}
      </Typography>

      <Typography >
        Number of Bathrooms: {listingInfo?.metadata.numberOfBathrooms}
      </Typography>
      <br />
      {
        props.token // Check whether user is logged in or not
          ? <Button variant='contained' onClick={() => setOpenBooking(true) }>
            Make a booking
            </Button>
          : <Button variant='contained' onClick={() => navigate('/login') }>
            Login to make a booking
            </Button>

      }
      <Button disabled sx={{ margin: '0 10px' }} variant='contained'>Leave a review</Button>
    </div>

    <BookingForm
      open={openBooking}
      handleCloseFn={handleBookingClose}
      token={props.token}
      availability={listingInfo?.availability}
      listingInfo={listingInfo}
      listingId={listingId} />
    </>

  )
}

export default ViewListing;
