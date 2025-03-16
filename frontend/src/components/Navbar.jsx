import React from "react";
import { MDBNavbar, MDBContainer, MDBNavbarBrand, MDBIcon } from "mdb-react-ui-kit";

const Navbar = () => {
  return (
    <MDBNavbar light bgColor="light" className="shadow-sm">
      <MDBContainer fluid>
        <MDBNavbarBrand>
          <MDBIcon fas icon="chart-line" className="me-2" />
          JedgeBot Dashboard
        </MDBNavbarBrand>
      </MDBContainer>
    </MDBNavbar>
  );
};

export default Navbar;
