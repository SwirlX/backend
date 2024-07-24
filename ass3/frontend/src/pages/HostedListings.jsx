import React from 'react';
import { Button, Container, Grid, Card, CardMedia, CardContent, CardActions, Typography } from '@mui/material';
import { makeStyles } from '@mui/styles';
import CreateListingForm from '../components/CreateListingForm';
import PropTypes from 'prop-types';
import { makeRequest, fetchAllListings, fetchListingInfo } from '../helpers';
import EditListingForm from '../components/EditListingForm';
import PublishForm from '../components/PublishForm';
import { Route, Routes, useNavigate, useParams } from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  cardGrid: {
    padding: '20px 0'
  },
  card: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column'
  },
  cardMedia: {
    paddingTop: '56.25%'
  },
  cardContent: {
    flexGrow: 1,
  },
}))

function HostedListings (props) {
  const classes = useStyles();
  const navigate = useNavigate();
  const params = useParams();
  console.log(params);

  const [open, setOpen] = React.useState(false);
  const [openEdit, setOpenEdit] = React.useState(false);
  const [openAvail, setOpenAvail] = React.useState(false);

  const [userListingInfo, setUserListingInfo] = React.useState([]);
  const [editableItems, setEditableItems] = React.useState({});

  const [channelToPublish, setChannelToPublish] = React.useState()

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  // Called when edit option is clicked on a particular listing.
  // Sends necessary info to the edit form pop-up
  const handleEditBtn = (listingInfo) => {
    setOpenEdit(true);

    // Object to send to the edit listing form, to populate input boxes
    const editableItemsObj = {
      id: listingInfo.id,
      listingTitle: listingInfo.title,
      listingAddress: listingInfo.address,
      listingPrice: listingInfo.price,
      propertyType: listingInfo.metadata.propertyType,
      numberOfBathrooms: listingInfo.metadata.numberOfBathrooms,
      numberOfBedrooms: listingInfo.metadata.numberOfBedrooms,
      numberOfBeds: listingInfo.metadata.numberOfBeds,
      propertyAmenities: listingInfo.metadata.propertyAmenities,
      thumbnail: listingInfo.thumbnail,
      propertyImages: listingInfo.metadata.propertyImages
    }

    setEditableItems(editableItemsObj);
    navigate(`/hosted/edit/${listingInfo.id}`)
  }

  // Closes edit form
  const handleCloseEdit = () => {
    setOpenEdit(false);
    navigate('/hosted')
  }

  // Opens the publish form to pick availabilities
  const handleAvailBtn = (listingInfo) => {
    setOpenAvail(true);
    setChannelToPublish(listingInfo.id);
  }

  // Closes the publish/availability form
  const handleAvailClose = () => {
    setOpenAvail(false);
    setChannelToPublish(null);
  }

  // Unpublishes a published a listing
  const handleUnpublish = async (listingInfo) => {
    const response = makeRequest(`/listings/unpublish/${listingInfo.id}`, 'PUT', {
      'Content-type': 'application/JSON',
      Authorization: `Bearer ${props.token}`
    });

    try {
      await response;
      fetchListings();
    } catch (error) {
      alert(error.error);
    }
  }

  // Deletes a listing
  const handleDeleteBtn = async (listingInfo) => {
    const response = makeRequest(`/listings/${listingInfo.id}`, 'DELETE', {
      'Content-type': 'application/JSON',
      Authorization: `Bearer ${props.token}`
    });

    try {
      await response;
      fetchListings();
    } catch (error) {
      alert(error.error)
    }
  }

  // Gets all listings that are hosted by the logged in user
  const fetchListings = async () => {
    const data = await fetchAllListings(props.token);

    const userListingData = []
    for (const userListing of data.listings) {
      const listingData = await fetchListingInfo(userListing.id, props.token);
      listingData.listing.id = userListing.id;
      userListingData.push(listingData);
    }
    const ownerListings = userListingData.filter((element) => element.listing.owner === props.currUserEmail)
    setUserListingInfo(ownerListings);
  }

  React.useEffect(() => {
    fetchListings();
  }, [])

  return (
    <>
    <Button sx={{ margin: '0 10px' }} name='addListingButton' variant='contained' onClick={handleClickOpen}>Add new listing</Button>

    <Container maxWidth='lg' className={classes.cardGrid} >
      <Grid container spacing={4}>
        {
          userListingInfo.map((element) => (
            <Grid key={element.listing.id} item>
              <Card className={classes.card}>
                <CardMedia
                  className={classes.cardMedia}
                  image={element.listing.thumbnail}
                  title='Image title' />
                <CardContent className={classes.cardContent}>
                  <Typography gutterBottom variant='h5'>
                    {element.listing.title}
                  </Typography>
                  <Typography>
                    Address: {element.listing.address} <br />
                    Price: ${element.listing.price} per night <br />
                    Property Type: {element.listing.metadata.propertyType} <br />
                    Number of Beds: {element.listing.metadata.numberOfBeds} <br />
                    Number of Bathrooms: {element.listing.metadata.numberOfBathrooms} <br />
                    {element.listing.reviews.length} Reviews
                  </Typography>
                  <CardActions>
                    <Button size='small' color='primary' onClick={() => handleEditBtn(element.listing)}>Edit</Button>
                    <Button size='small' color='primary' onClick={() => handleDeleteBtn(element.listing)}>Delete</Button>
                    {element.listing.published
                      ? <Button name='unpublishButton' size='small' color='primary' onClick={() => handleUnpublish(element.listing)}>Unpublish</Button>
                      : <Button name='publishButton' size='small' color='primary' onClick={() => handleAvailBtn(element.listing)}>Publish</Button>}
                  </CardActions>
                </CardContent>
              </Card>
            </Grid>

          ))
        }
      </Grid>
    </Container>
    <CreateListingForm open={open} handleCloseFn={handleClose} token={props.token} fetchListingsFn={fetchListings}/>
    <PublishForm open={openAvail} handleCloseFn={handleAvailClose} token={props.token} channelToPublish={channelToPublish} fetchListingsFn={fetchListings} />
    <Routes>
      {
        userListingInfo.map((element) => {
          return (
            <Route key={element.listing.id} path={`/edit/${element.listing.id}`} element={
              <EditListingForm
                open={openEdit}
                handleCloseFn={handleCloseEdit}
                token={props.token}
                listingInfo={editableItems}
                fetchListingsFn={fetchListings} />
              }
            />
          )
        })
      }

    </Routes>
    </>
  )
}

HostedListings.propTypes = {
  token: PropTypes.string,
  currUserEmail: PropTypes.string,
};

export default HostedListings;
