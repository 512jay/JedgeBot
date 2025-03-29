// /frontend/src/features/profile/Profile.jsx

import React from "react";
import { useAuth } from "@/context/useAuth";
import {
  MDBContainer,
  MDBCard,
  MDBCardBody,
  MDBCardTitle,
  MDBCardText,
  MDBRow,
  MDBCol,
  MDBBtn,
} from "mdb-react-ui-kit";
import { useNavigate } from "react-router-dom";

const Profile = () => {
  const { user, loading } = useAuth();
  const navigate = useNavigate();

  if (loading || !user) return null;

  return (
    <MDBContainer className="pt-4">
      <MDBRow className="justify-content-center">
        <MDBCol md="8" lg="6">
          <MDBCard className="shadow-3">
            <MDBCardBody>
              <MDBCardTitle className="mb-3">Your Profile</MDBCardTitle>

              <MDBCardText>
                <strong>Username:</strong> {user.username}
              </MDBCardText>
              <MDBCardText>
                <strong>Email:</strong> {user.email}
              </MDBCardText>
              <MDBCardText>
                <strong>Role:</strong> {user.role}
              </MDBCardText>

              {user.status && (
                <MDBCardText>
                  <strong>Status:</strong> {user.status}
                </MDBCardText>
              )}

              {/* ✅ Reset Password Button */}
              <MDBBtn
                color="primary"
                className="mt-3"
                onClick={() => navigate("/forgot-password")}
              >
                Reset Password
              </MDBBtn>
            </MDBCardBody>
          </MDBCard>
        </MDBCol>
      </MDBRow>
    </MDBContainer>
  );
};

export default Profile;
