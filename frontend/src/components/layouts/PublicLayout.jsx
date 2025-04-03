// /frontend/src/components/layouts/PublicLayout.jsx

import React, { useEffect } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { Container, Row, Col } from 'react-bootstrap';
import { useAuth } from "@hooks/useAuth";
import Header from "./Header";
import Footer from "./Footer";

export default function PublicLayout({
  pageTitle = "Fordis Ludus",
  children,
  hideHeader = false,
  hideFooter = false,
  debug = false,
  hero = false,
}) {
  const location = useLocation();
  const { user } = useAuth?.() || {};

  useEffect(() => {
    document.title = pageTitle;
  }, [pageTitle]);

  return (
    <div
      className={`d-flex flex-column min-vh-100 ${hero ? "hero-layout" : "bg-mutedRose"}`}
      style={{
        backgroundColor: '#9A616D',
        overflowX: 'hidden'
      }}
    >
      {!hideHeader && <Header />}

      <main className="flex-grow-1 d-flex align-items-center justify-content-center">
        <Container>
          <Row className="justify-content-center">
            <Col xs={12} md={10} lg={8} xl={6}>
              {children || <Outlet />}
            </Col>
          </Row>
        </Container>
      </main>

      {debug && (
        <pre className="text-muted small text-center">
          Debug: path={location.pathname}, auth={user?.isAuthenticated ? "yes" : "no"}
        </pre>
      )}

      {!hideFooter && <Footer />}
    </div>
  );
}
