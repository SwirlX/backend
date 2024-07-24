import React from 'react';
import { Button, Container, Grid, Card, CardMedia, CardContent, CardActions, Typography, TextField, IconButton } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { makeStyles } from '@mui/styles';
import { Routes, Route, useNavigate } from 'react-router-dom';
import PropTypes from 'prop-types';
import { getBookedListingsId, fetchListingInfo, fetchAllListings } from '../helpers';
import FilterByForm from '../components/FilterByForm';
import ViewListing from './ViewListing';

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

Home.propTypes = {
  token: PropTypes.string,
  currUserEmail: PropTypes.string,
};

function Home (props) {
  const defaultBedroomRange = [0, 20];
  const defaultPriceRange = [0, 2000];

  const navigate = useNavigate();

  const classes = useStyles();

  const [liveListingInfo, setLiveListingInfo] = React.useState([]);
  const [allLiveListings, setAllLiveListings] = React.useState([]);
  const [openFilterForm, setOpenFilterForm] = React.useState(false);

  const [bedroomRange, setBedroomRange] = React.useState(defaultBedroomRange);
  const [priceRange, setPriceRange] = React.useState(defaultPriceRange);
  const [from, setFrom] = React.useState();
  const [to, setTo] = React.useState();

  let filtersApplied = false;

  React.useEffect(() => {
    fetchLiveListings();
  }, [])

  // Called when filter button is clicked
  const handleFilterBtn = () => {
    setOpenFilterForm(true);
  }

  // Called when close button is clicked in the filter form
  const handleCloseFilterForm = () => {
    setOpenFilterForm(false);
  }

  // Called when apply button clicked in the filter form
  const handleFilterApply = () => {
    handleCloseFilterForm();
    filtersApplied = (true);
    doFilter();
  }

  // Called when discard button clicked in the filter form and discards all applied filters
  const handleDiscardFilters = () => {
    handleCloseFilterForm();
    filtersApplied = (false);
    setBedroomRange(defaultBedroomRange);
    setPriceRange(defaultPriceRange);
    setFrom();
    setTo();
    setLiveListingInfo(allLiveListings);
  }

  // Apply filters when filter apply is clicked
  const doFilter = () => {
    const filterByBedrooms = (element) => {
      const bedrooms = element.listing.metadata.numberOfBedrooms;
      return (bedroomRange[0] <= bedrooms) && (bedrooms <= bedroomRange[1])
    }

    const filterByDateRange = (element) => {
      const fromDate = new Date(from);
      const toDate = new Date(to);

      for (const availRange of element.listing.availability) {
        const startDate = new Date(availRange.start)
        const endDate = new Date(availRange.end)
        if (startDate <= fromDate && toDate <= endDate) {
          return true;
        }
      }

      return false;
    }

    const filterByPriceRange = (element) => {
      const price = element.listing.price;
      return (priceRange[0] <= price) && (price <= priceRange[1])
    }

    if (filtersApplied) {
      let filteredListings = []
      filteredListings = allLiveListings.filter(filterByBedrooms)
      if ((typeof from !== 'undefined') && (typeof to !== 'undefined')) {
        filteredListings = filteredListings.filter(filterByDateRange);
      }
      filteredListings = filteredListings.filter(filterByPriceRange);
      setLiveListingInfo(filteredListings);
    } else {
      setLiveListingInfo(allLiveListings);
    }
  }

  // Filters listings based on query put into the search bar
  const handleQuery = (query) => {
    if (query === '') {
      fetchLiveListings();
      return;
    }

    const filteredListings = liveListingInfo.filter((element) => {
      return element.listing.title
        .toLowerCase()
        .startsWith(query.toLowerCase());
    });
    setLiveListingInfo(filteredListings);
  }

  // Opens the required paged to view a listing
  // when clicked
  const handleViewBtn = (listingId) => {
    navigate(`/listing/${listingId}`);
  }

  // Get all the published (live) listings and sorts accordingly
  const fetchLiveListings = async () => {
    const data = await fetchAllListings(props.token);

    // Attaches an id key-value pair to the listings
    const userListingData = []
    for (const userListing of data.listings) {
      const listingData = await fetchListingInfo(userListing.id, props.token);
      listingData.listing.id = userListing.id;
      userListingData.push(listingData);
    }

    // Filter all listings to only live listings
    let liveListings = userListingData.filter((element) => element.listing.published)

    // Sort listings alphabetically
    liveListings.sort((l, r) => {
      if (l.listing.title < r.listing.title) {
        return -1;
      }

      if (l.listing.title > r.listing.title) {
        return 1;
      }

      return 0;
    });

    // Shows all booked listings first if user is logged in
    if (props.token) {
      const bookedListingsId = await getBookedListingsId(props.currUserEmail, props.token);
      console.log(bookedListingsId);
      let liveListingsCopy = [...liveListings];
      for (const individualListing of liveListings) {
        if (bookedListingsId.includes(individualListing.listing.id.toString())) {
          liveListingsCopy = liveListingsCopy.filter(element => element !== individualListing);
          liveListingsCopy.unshift(individualListing);
          console.log(liveListingsCopy);
        }
      }
      liveListings = liveListingsCopy;
    }
    setLiveListingInfo(liveListings);
    setAllLiveListings(liveListings);
  }

  return (
    <>
    <Button sx={ { margin: '0 10px' } } variant='contained' onClick={handleFilterBtn}>
      Filter By
    </Button>
    <TextField
      id="search-bar"
      className="text"
      onChange={(e) => {
        handleQuery(e.target.value);
      }}
      label="Search Listings"
      variant="outlined"
      placeholder="Search..."
      size="small"
    />

    <IconButton type="submit" aria-label="search">
      <SearchIcon style={{ fill: 'blue' }} />
    </IconButton>

    <Container maxWidth='lg' className={classes.cardGrid} >
      <Grid container spacing={4}>
        {
          liveListingInfo.map((element) => {
            return (
              <Grid key={element.listing.id} item>
                <Card className={classes.card}>
                  <CardMedia
                    className={classes.cardMedia}
                    image= {element.listing.thumbnail}
                    title='Image title'
                  />
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
                      <Button size='small' color='primary' onClick={() => handleViewBtn(element.listing.id)} >View</Button>
                    </CardActions>
                  </CardContent>
                </Card>
              </Grid>
            )
          })
        }
      </Grid>
    </Container>
    <FilterByForm
      open={openFilterForm}
      handleCloseFn={handleCloseFilterForm}
      bedroomRange={bedroomRange}
      setBedroomRangeFn={setBedroomRange}
      priceRange={priceRange}
      setPriceRangeFn={setPriceRange}
      from={from}
      setFromFn={setFrom}
      to={to}
      setToFn={setTo}
      handleFilterApplyFn={handleFilterApply}
      handleDiscardFiltersFn={handleDiscardFilters}
    />
    <Routes>
      {
        allLiveListings.map((element) => {
          return (
            <Route
              key={`/listing/${element.listing.id}`}
              path={`/listing/${element.listing.id}`}
              element={
                <ViewListing listingInfo={element.listing} />
              }
            />
          )
        })
      }
    </Routes>
    </>
  )
}

export default Home;
