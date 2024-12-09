import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Header = () => {
    return (
    <Navbar expand="lg" className="custom-navbar">
        <Navbar.Brand href="#home" className="navbar-brand">
            <div class="m-3">
            <svg width="50" height="50" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M28.1251 25C28.1251 31.625 22.7709 36.9792 16.1459 36.9792C9.52091 36.9792 4.16675 31.625 4.16675 25C4.16675 18.375 9.52091 13.0208 16.1459 13.0208M20.8334 25C20.8334 18.1042 26.4376 12.5 33.3334 12.5C40.2292 12.5 45.8334 18.1042 45.8334 25C45.8334 31.8958 40.2292 37.5 33.3334 37.5" stroke="white" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
            </div>
            PoliLens
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="ms-auto">
            <Nav.Link as={Link} to="">Dashboard</Nav.Link>
            <Nav.Link as={Link} to="/politicians">Politicians</Nav.Link>
            <Nav.Link as={Link} to="/bills">Bills</Nav.Link>
            <Nav.Link as={Link} to="/connections">Connections</Nav.Link>
        </Nav>
        </Navbar.Collapse>
    </Navbar>
    )
}

export default Header;