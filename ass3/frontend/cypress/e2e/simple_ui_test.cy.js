describe('AirBrb Happy Path', () => {
  it('should navigate to home screen successfully', () => {
    cy.visit('localhost:3000/');
    cy.url().should('include', 'localhost:3000');
  });

  it('should navigate to the register screen successfully', () => {
    cy.get('[name="registerButton"]')
      .click();
    cy.url().should('include', 'localhost:3000/register');
  })

  it('should register successfully', () => {
    cy.get('[id=emailInput]')
      .focus()
      .type('anEmail@email.com');

    cy.get('[id=passInput]')
      .focus()
      .type('randompassword');

    cy.get('[id=passConfirmInput]')
      .focus()
      .type('randompassword');

    cy.get('[id=nameInput]')
      .focus()
      .type('user1');

    cy.get('[name=submitRegisterButton]')
      .click()

    cy.url().should('include', 'localhost:3000/');
  })

  it('should create a new listing', () => {
    cy.get('[name=hostedListingsButton]')
      .click();

    cy.url().should('include', 'localhost:3000/hosted');

    cy.get('[name=addListingButton]')
      .click();

    cy.get('[id=listingTitle]')
      .focus()
      .type('Listing1');

    cy.get('[id=listingAddress]')
      .focus()
      .type('3 Listing Address');

    cy.get('[id=listingPrice]')
      .focus()
      .type('250');

    cy.get('[id=propertyType]')
      .focus()
      .type('House');

    cy.get('[id=numberOfBathrooms]')
      .focus()
      .type('3');

    cy.get('[id=numberOfBedrooms]')
      .focus()
      .type('4');

    cy.get('[id=numberOfBeds]')
      .focus()
      .type('5');

    cy.get('[id=propertyAmenities]')
      .focus()
      .type('Indoor pool');

    cy.get('[name=listingThumbnailUpload]')
      .selectFile('src/assets/house.png')

    cy.get('[name=listingCreateButton]')
      .click()

    cy.url().should('include', 'localhost:3000/');
  });

  it('should publish the created listing', () => {
    cy.get('[name=publishButton]')
      .click()

    cy.get('[name=fromDatepicker]')
      .focus()
      .clear()
      .type('11012022')

    cy.get('[name=toDatepicker]')
      .focus()
      .clear()
      .type('11302022')

    cy.get('[name=addAvailButton]')
      .click()

    cy.get('[name=publishConfirmButton]')
      .click()
  })

  it('should unpublish the published listing', () => {
    cy.get('[name=unpublishButton]')
      .click();
  })

  it('should logout', () => {
    cy.get('[name=logoutButton]')
      .click();
  })

  it('should log back in', () => {
    cy.get('[name=loginButton]')
      .click()

    cy.get('[id=emailInput]')
      .focus()
      .type('anEmail@email.com')

    cy.get('[id=passInput]')
      .focus()
      .type('randompassword')

    cy.get('[name=loginConfirmButton]')
      .click()
  })
});
