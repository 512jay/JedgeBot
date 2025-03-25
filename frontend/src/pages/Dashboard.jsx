// /frontend/src/pages/Dashboard.jsx
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import Sidebar from "../components/layout/Sidebar";
import {
  MDBContainer,
  MDBRow,
  MDBCol,
  MDBCard,
  MDBCardBody,
  MDBCardText,
  MDBCardTitle,
} from "mdb-react-ui-kit";

const Dashboard = () => {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (!loading) {
      if (!user) {
        navigate("/login");
      } else if (!["free", "client", "manager", "enterprise"].includes(user.role)) {
        navigate("/unauthorized");
      }
    }
  }, [user, loading, navigate]);

  if (loading || !user) return null;

  return (
    <div style={{ display: "flex", height: "100vh", width: "100vw" }}>
      <Sidebar />

      <div style={{ flex: 1, backgroundColor: "#6495ED", padding: "2rem", overflowY: "auto" }}>
        <h1 style={{ fontSize: "2.5rem", fontWeight: "600", marginBottom: "2rem", color: "white" }}>
          Welcome to your dashboard
        </h1>

        <MDBContainer fluid style={{ paddingLeft: "2rem", paddingRight: "2rem" }}>
          <MDBRow className="mb-4">
            <MDBCol md="12">
              <MDBCard>
                <MDBCardBody>
                  <MDBCardTitle>Portfolio Overview</MDBCardTitle>
                  <MDBCardText>Total Balance: $125,000</MDBCardText>
                  <MDBCardText className="text-success">Net P&amp;L: +5.2%</MDBCardText>
                </MDBCardBody>
              </MDBCard>
            </MDBCol>
          </MDBRow>

          <MDBRow className="mb-4">
            <MDBCol md="12">
              <MDBCard>
                <MDBCardBody>
                  <MDBCardTitle>Recent Activity</MDBCardTitle>
                  <ul className="ms-3">
                    <li>Executed order: 100 shares of AAPL</li>
                    <li>New client added: John Doe</li>
                    <li>Portfolio rebalanced</li>
                  </ul>
                </MDBCardBody>
              </MDBCard>
            </MDBCol>
          </MDBRow>

          <MDBRow>
            <MDBCol md="12">
              <MDBCard>
                <MDBCardBody>
                  <MDBCardTitle>Market Insights</MDBCardTitle>
                  <MDBCardText>S&amp;P 500: +1.8%</MDBCardText>
                  <MDBCardText className="text-primary">Top Gainer: TSLA +7.4%</MDBCardText>
                </MDBCardBody>
              </MDBCard>
            </MDBCol>
          </MDBRow>
        </MDBContainer>
      </div>
    </div>
  );
};

export default Dashboard;
