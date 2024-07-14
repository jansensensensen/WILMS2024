import DashBoardTemplate from "../containers/dashboard_template";
import { BASE_URL } from "../../links";

import {
  Box,
  Grid,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Container,
  CardContent,
  Paper,
} from "@mui/material";
import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import axios from "axios";
import * as React from "react";
import AuthContext from "../../context/AuthContext";
import { StyledTableCell, StyledTableRow, ResponsiveContainer } from "./styles";

export default function Tracker(props) {
  //const [ratingFilter, setRatingFilter] = useState([0, 5]);
  const [data, setData] = useState([]);
  let { user, setUser, authenticated } = useContext(AuthContext);
  const title = ["ONGOING", "EXPECTED", "WAITING", "OVERSTAYING"];
  const navigate = useNavigate();

  const [containerDetails, setContainerDetails] = useState(
    title.map((title) => ({
      title,
      contents: [],
    }))
  );

  useEffect(() => {
    const fetchData = async () => {
      const endpoints = [
        `${BASE_URL}/api/getOngoing/`,
        `${BASE_URL}/api/getExpected/`,
        `${BASE_URL}/api/getWaiting/`,
        `${BASE_URL}/api/getOverstaying/`,
      ];

      const updatedContainerDetails = [...containerDetails];

      try {
        for (let i = 0; i < endpoints.length; i++) {
          const response = await axios.get(endpoints[i]);
          if (response.status === 200) {
            const data = response.data;

            if (Array.isArray(data)) {
              updatedContainerDetails[i].contents = data.map((facility) => ({
                name: facility.facility_name,
                count: facility.count,
              }));
            } else {
              console.error(`Invalid data format for ${endpoints[i]}`);
            }
          } else {
            console.error(`Failed to fetch data from ${endpoints[i]}`);
          }
        }

        setContainerDetails(updatedContainerDetails);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    axios
      .get(`${BASE_URL}/api/getSignedIn/`)
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data", error);
      });
  }, []);

  if (user === null && user.role !== "admin") {
    navigate("/booking/login");
  } else if (user.role === "user"){
    navigate("/booking/calendar");
  } else if (user.role === "admin"){
    return (
      <div style={{ position: "relative", backgroundColor: "#fff" }}>
        <DashBoardTemplate title="TRACKER">
          <Container sx={{ paddingTop: "50px", width: "100%",  }}>
            <Box
              backgroundColor="white"
              display="flex"
              alignItems="center"
              justifyContent="center" // Center the content horizontally
              flexDirection="column"
              p={2}
              borderRadius={1}
              mt={5}
              marginTop={14}
              padding={{ xs: 2, md: 2 }}
              width="100%"
              // sx={{overflow:'auto'}}
            >
              <div>
                <Container
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    maxWidth: "100%",
                  }}
                >
                  <Box sx={{ flexGrow: 1 }}>
                  <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "start",
                  }}
                >
                  <Typography
                    sx={{
                      paddingLeft: -195,
                      color: "lightblack",
                      position: "flex-start",
                      fontSize: 30,
                      fontWeight: "bold",
                      marginTop: 2,
                    }}
                    fontFamily="Poppins"
                  >
                    Activity Tracker
                  </Typography>
                </div>
                    <Grid container spacing={2} >

                      {containerDetails.map((card, index) => (
                        <Grid key={index} item xs={12} sm={6} md={4} lg={3}>
                          <Paper
                            elevation={3}
                            sx={{
                              minWidth: { xs: 100, sm: 150 },
                              minWidth: 195,
                              width: "auto",
                              minHeight: 287,
                              height: "auto",
                              display: "relative",
                              background: "#ffe836",
                              border: "1px solid #fecc00",
                              marginBottom: 7,
                            }}
                          >
                            <CardContent>
                              <Typography
                                sx={{
                                  fontSize: { xs: 16, md: 20 },
                                  fontWeight: "bold",
                                  fontFamily: "Poppins",
                                }}
                                color="text.primary"
                              >
                                {card.title}
                              </Typography>
                              <Typography
                                variant="body2"
                                color="text.primary"
                                textAlign="left"
                                fontFamily="Poppins"
                                fontSize={{ xs: 14, md: 17 }}
                              >
                                {card.contents.map((content, i) => (
                                  <div
                                    key={i}
                                    style={{
                                      display: "flex",
                                      alignItems: "center",
                                    }}
                                  >
                                    <div style={{ flex: 1 }}>{content.name}</div>
                                    <div
                                      style={{
                                        width: "25px",
                                        marginLeft: "8px",
                                      }}
                                    >
                                      [{content.count}]
                                    </div>
                                    <br />
                                    <br />
                                  </div>
                                ))}
                              </Typography>
                            </CardContent>
                          </Paper>
                        </Grid>
                      ))}
                    </Grid>
                  </Box>
                </Container>

                {/* Logged in USERS */}
                <div
                  style={{
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "start",
                  }}
                >
                  <Typography
                    sx={{
                      paddingLeft: -195,
                      color: "lightblack",
                      position: "flex-start",
                      fontSize: 30,
                      fontWeight: "bold",
                    }}
                    fontFamily="Poppins"
                  >
                    Currently Logged in users
                  </Typography>
                </div>
                <Container
                  sx={{
                    marginBottom: 5,
                    backgroundColor: "f5fffa",
                    borderRadius: 3,
                    width: "100%", // Adjust width as needed
                  }}
                >
                  <TableContainer
                    sx={{
                      minWidth: 50,
                      display: "flex",
                      justifyContent: "center",
                      borderStyle: "groove",
                      borderRadius: 2,
                    }}
                  >
                    <Table>
                      <TableHead>
                        <StyledTableRow>
                          <StyledTableCell align="center">Booking ID</StyledTableCell>
                          <StyledTableCell align="center">Name</StyledTableCell>
                          <StyledTableCell align="center">Venue</StyledTableCell>
                          <StyledTableCell align="center">Time Signed in</StyledTableCell>
                        </StyledTableRow>
                      </TableHead>
                      <TableBody>
                        {data.map((row, index) => (
                          <StyledTableRow key={index}>
                            <StyledTableCell align="center">{row.booking}</StyledTableCell>
                            <StyledTableCell align="center">{row.name}</StyledTableCell>
                            <StyledTableCell align="center">{row.venueId}</StyledTableCell>
                            <StyledTableCell align="center">{row.signInTime}</StyledTableCell>
                          </StyledTableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                </Container>
              </div>
            </Box>
          </Container>
        </DashBoardTemplate>
      </div>
    );
  }
}