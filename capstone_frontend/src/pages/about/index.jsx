import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import DashBoardTemplate from "../containers/dashboard_template";
import {
  Box,
  Button,
  ButtonGroup,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Container,
  Grid,
  Typography,
  Paper
} from "@mui/material";
import Wild from "../../images/wild.png";
import SearchIcon from "@mui/icons-material/Search";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import {
  selectedStyle,
  unselectedStyle,
  StyledTableCell,
  StyledTableRow,
  SearchIconWrapper,
  StyledInputBase,
  Search,
} from "./styles";
import { useNavigate } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import { BASE_URL } from "../../links";
import bgpic from "../../images/reception2.jpg";
import richdwine from "../../images/rich.jpg";
import joann from "../../images/joann.jpg";
import pam from "../../images/pam.jpg";
import junie from "../../images/junie.png";
import belle from "../../images/belle.jpg";

export default function About(props) {
  const navigate = useNavigate();
  const { user, logoutUser } = useContext(AuthContext);
  const textStyles = {
    fontFamily: 'Poppins, sans-serif', // Use Poppins as the font family
  };


  if (user === null) {
    navigate("/booking/login");
  }  else {
    return (
      <div style={{ position: "relative", backgroundColor: "#fff", }}>
        <DashBoardTemplate title="About">
          <Container sx={{ minHeight: "1000px", height: "auto", paddingTop: "50px" }}>
            <Box
              backgroundColor="white"
              display="flex"
              alignItems="center"
              flexDirection="column"
              p={2}
              borderRadius={1}
              mt={5}
              marginTop={14}
              justifyContent="center"
              //padding="30px"
              sx={{
                width: "100%",
                "@media (max-width: 2560px)": {
                  padding: "10px",
                },
                fontFamily: "Poppins",
              }}
            >
         <Box m={2}>
  <Paper elevation={3} style={{ padding: '16px' }}>
    <Grid container spacing={2} alignItems="center">
      {/* Image on the left */}
      <Grid item xs={12} md={6}>
        <img
          src={bgpic}
          alt="Your Image"
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </Grid>

      {/* Text on the right */}
      <Grid item xs={12} md={6}>
        <Typography variant="h4" gutterBottom style={textStyles}>
          WILMS Booking
        </Typography>
        <Typography variant="body2" style={textStyles}>
          Wildcats Innovation Laboratory (WIL) booking system development project is to create
          a web-based system that will automate the booking process for both online and offline users,
          improve the efficiency of personnel in managing appointments, track attendance, and provide a feedback and review system.
          Ultimately, the WIL booking system aims to improve the overall productivity of the WIL system by streamlining the booking process
          and enhancing the user experience.
        </Typography>
      </Grid>
    </Grid>
  </Paper>

  <Box sx={{
  backgroundColor: '#ffd700', // Yellow background color
  padding: '16px',
  margin: '50px',
  borderRadius: '8px', // Optional: Add rounded corners for a card-like appearance
  boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)', // Optional: Add a subtle shadow for depth
  '&:hover': {
    boxShadow: '0 8px 16px rgba(0, 0, 0, 0.2)', // Optional: Increase shadow on hover for a pop effect
  },
}}>
    <Typography variant="h4">
        Our Team
    </Typography>
</Box>
  {/* Team Members Section */}
  <Grid container spacing={2} justify="space-between">
     <Grid container spacing={3} justify="space-between">
      {/* Team Member 1 */}
      <Grid item xs={12} md={4}>
        <Paper elevation={3} style={{ padding: '16px', textAlign: 'center' }}>
          <img
            src={belle} // Replace with the actual image URL
            alt="Team Member 1"
            style={{ width: '100%', height: '350px', marginBottom: '8px' }}
          />
          <Typography variant="h6" gutterBottom>
            Team Member 1
          </Typography>
          <Typography variant="body2">
            Name: Belle Hannah Sebial
            <br />
            Role: Project Manager
            <br />
            Contact: bellehannah.sebial@cit.edu
          </Typography>
        </Paper>
      </Grid>

      {/* Team Member 2 */}
      <Grid item xs={12} md={4}>
        <Paper elevation={3} style={{ padding: '16px', textAlign: 'center' }}>
        <img
            src={joann} // Replace with the actual image URL
            alt="Team Member 1"
            style={{ width: '100%', height: '350px', marginBottom: '8px' }}
          />
          <Typography variant="h6" gutterBottom>
            Team Member 2
          </Typography>
          <Typography variant="body2">
            Name: Joann Alfante
            <br />
            Role: Resource Manager
            <br />
            Contact: joann.alfante@cit.edu
          </Typography>
        </Paper>
      </Grid>

      {/* Team Member 3 */}
      <Grid item xs={12} md={4}>
        <Paper elevation={3} style={{ padding: '16px', textAlign: 'center' }}>
        <img
            src={richdwine} // Replace with the actual image URL
            alt="Team Member 1"
            style={{ width: '100%', height: '350px', marginBottom: '8px' }}
          />
          <Typography variant="h6" gutterBottom>
            Team Member 3
          </Typography>
          <Typography variant="body2">
            Name: Francis Dwine Bendulo
            <br />
            Role: Full Stack Developer
            <br />
            Contact: francisdwine.bendulo@cit.edu
          </Typography>
        </Paper>
      </Grid>

      {/* Team Member 4 */}
      <Grid item xs={12} md={4}>
        <Paper elevation={3} style={{ padding: '16px', textAlign: 'center' }}>
        <img
            src={pam} // Replace with the actual image URL
            alt="Team Member 1"
            style={{ width: '100%', height: '350px', marginBottom: '8px' }}
          />
          <Typography variant="h6" gutterBottom>
            Team Member 4
          </Typography>
          <Typography variant="body2">
            Name: Pamela Cañedo
            <br />
            Role: Front-end Developer
            <br />
            Contact: pamela.canedo@cit.edu
          </Typography>
        </Paper>
      </Grid>

      {/* Team Member 5 */}
      <Grid item xs={12} md={4}>
        <Paper elevation={3} style={{ padding: '16px', textAlign: 'center' }}>
        <img
            src={junie} // Replace with the actual image URL
            alt="Team Member 1"
            style={{ width: '100%', height: '350px', marginBottom: '8px' }}
          />
          <Typography variant="h6" gutterBottom>
            Team Member 5
          </Typography>
          <Typography variant="body2">
            Name: Junie John Roldan
            <br />
            Role: Tester and Front-end Developer
            <br />
            Contact: juniejohn.roldan@cit.edu
          </Typography>
        </Paper>
      </Grid>
    </Grid>
  </Grid>
</Box>;





              <Box
                sx={{
                  p: "0px 0px 0px 0px",
                  width: "100%",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "flex-start",
                  minHeight: "500px",
                  height: "auto",
                  overflowX: "auto",
                  maxWidth:'97%',
                }}
              >



              </Box>
            </Box>
          </Container>
        </DashBoardTemplate>
      </div>
    );
  }
}
