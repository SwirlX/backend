import moment from 'moment';

// Given all parameters, makes a request to the backend API
// and returns a promise with the data
export const makeRequest = (route, method, headers, body) => {
  const options = {
    method,
    headers,
  };

  if (body !== undefined) {
    options.body = JSON.stringify(body);
  }

  return new Promise((resolve, reject) => {
    fetch('http://localhost:5005' + route, options).then((res) => {
      return res.json();
    }).then((data) => {
      if (data.error) {
        reject(data);
      } else {
        resolve(data);
      }
    });
  })
}

// Converts a file to a base64 URL
export function fileToDataUrl (file) {
  const validFileTypes = ['image/jpeg', 'image/png', 'image/jpg']
  const valid = validFileTypes.find(type => type === file.type);

  if (!valid) {
    throw Error('provided file is not a png, jpg or jpeg image.');
  }

  const reader = new FileReader();
  const dataUrlPromise = new Promise((resolve, reject) => {
    reader.onerror = reject;
    reader.onload = () => resolve(reader.result);
  });
  reader.readAsDataURL(file);
  return dataUrlPromise;
}

// Gets the booked listings of a given user
export async function getBookedListingsId (userEmail, token) {
  const bookingsRequest = makeRequest('/bookings', 'GET', {
    'Content-type': 'application/JSON',
    Authorization: `Bearer ${token}`
  });

  let bookingsList = null;
  try {
    bookingsList = await bookingsRequest;
  } catch (error) {
    alert(error.error);
    return;
  }
  const userBookedListingsId = []
  for (const booking of bookingsList.bookings) {
    if (booking.owner === userEmail) {
      userBookedListingsId.push(booking.listingId);
    }
  }
  return userBookedListingsId;
}

// Gets information a given listings from the backend
export const fetchListingInfo = async (listingId, token) => {
  const listingRes = makeRequest(`/listings/${listingId}`, 'GET', {
    'Content-type': 'application/JSON',
    Authorization: `Bearer ${token}`
  });

  try {
    const data = await listingRes;
    return data;
  } catch (error) {
    alert(error.error);
  }
}

// Gets all listings from the backend
export const fetchAllListings = async (token) => {
  const response = makeRequest('/listings', 'GET',
    {
      'Content-type': 'application/JSON',
      Authorization: `Bearer ${token}`
    },
  )
  try {
    const data = await response;
    return data;
  } catch (error) {
    alert(error.error);
  }
}

// Compute number of nights staying at listing and total price
export const getPriceFromNightsStayed = (from, to, pricePerNight) => {
  const startDateMoment = moment(new Date(from));
  const endDateMoment = moment(new Date(to));
  const numberOfNights = endDateMoment.diff(startDateMoment, 'days', true);
  return numberOfNights * pricePerNight;
}
