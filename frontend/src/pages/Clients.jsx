import React, { useState } from "react";
import { MDBTable, MDBTableHead, MDBTableBody, MDBBtn, MDBIcon, MDBInputGroup, MDBInput } from "mdb-react-ui-kit";

const Clients = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [clients, setClients] = useState([
    { id: 1, name: "Client A", accounts: 3, portfolioValue: "$500,000", risk: "Low" },
    { id: 2, name: "Client B", accounts: 2, portfolioValue: "$300,000", risk: "Medium" },
    { id: 3, name: "Client C", accounts: 5, portfolioValue: "$800,000", risk: "High" }
  ]);

  const filteredClients = clients.filter(client =>
    client.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="container mt-4">
      <h2>Clients</h2>

      {/* Search Bar */}
      <MDBInputGroup className="mb-3">
        <MDBInput label="Search clients..." onChange={(e) => setSearchTerm(e.target.value)} />
        <MDBBtn color="primary">
          <MDBIcon fas icon="search" />
        </MDBBtn>
      </MDBInputGroup>

      {/* Clients Table */}
      <MDBTable align="middle">
        <MDBTableHead>
          <tr>
            <th>Client Name</th>
            <th>Accounts</th>
            <th>Portfolio Value</th>
            <th>Risk Level</th>
            <th>Actions</th>
          </tr>
        </MDBTableHead>
        <MDBTableBody>
          {filteredClients.map((client) => (
            <tr key={client.id}>
              <td>{client.name}</td>
              <td>{client.accounts}</td>
              <td>{client.portfolioValue}</td>
              <td>{client.risk}</td>
              <td>
                <MDBBtn color="info" size="sm">
                  <MDBIcon fas icon="eye" className="me-1" /> View
                </MDBBtn>
                <MDBBtn color="danger" size="sm" className="ms-2">
                  <MDBIcon fas icon="trash-alt" className="me-1" /> Delete
                </MDBBtn>
              </td>
            </tr>
          ))}
        </MDBTableBody>
      </MDBTable>
    </div>
  );
};

export default Clients;
