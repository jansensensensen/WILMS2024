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
} from "@mui/material";
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

export default function Logs(props) {
  const [venueSelected, setVenueSelected] = useState("Coworking Space");
  const [facilities, setFacilities] = useState([]);
  const [venueId, setVenueId] = useState(1);
  const [searchText, setSearchText] = useState("");
  const [filteredEvents, setFilteredEvents] = useState([]);
  const [events, setEvents] = useState([]);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [page, setPage] = useState(0);
  const navigate = useNavigate();
  const { user, logoutUser } = useContext(AuthContext);

  useEffect(() => {
    axios
      .get(`${BASE_URL}/api/getAllAttendance/`)
      .then((response) => {
        setEvents(response.data);
        setFilteredEvents(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data", error);
      });
  }, []);

  useEffect(() => {
    axios.get(`${BASE_URL}/facility/get-facility/`).then((res) => {
      setFacilities(res?.data);
      var indx0 = res?.data[0];
      setVenueSelected(indx0?.facility_name);
      setVenueId(indx0?.facility_id);
    });
  }, []);

  useEffect(() => {
    const filtered = events.filter((item) => item.venueId === venueId);
    setFilteredEvents(filtered);
  }, [venueSelected, events]);

  const handleSearchTextChange = (e) => {
    const searchText = e.target.value;
    setSearchText(searchText);

    if (searchText === "") {
      const filtered = events.filter((item) => {
        return (
          (item.venueId === venueId &&
            item.name.toLowerCase().includes(searchText.toLowerCase())) ||
          (item.venueId === venueId &&
            item.date.toString().includes(searchText))
        );
      });
      setFilteredEvents(filtered);
    } else {
      const filtered = events.filter((item) => {
        return (
          (item.venueId === venueId &&
            item.name.toLowerCase().includes(searchText.toLowerCase())) ||
          (item.venueId === venueId &&
            item.date.toString().includes(searchText))
        );
      });
      setFilteredEvents(filtered);
    }
  };

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  if (!user || user.role !== "admin") {
    navigate("/booking/login");
    return null;
  } else {
    return (
      <div style={{ position: "relative", backgroundColor: "#fff", }}>
        <DashBoardTemplate title="ATTENDANCE LOGS">
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

              }}
            >
              <div style={{marginLeft: "auto"}}>
                <Box
                  sx={{
                    flexGrow: 1,
                    display: "flex",
                    border: "1px solid rgba(0, 0, 0.5, 0.1)",
                    marginLeft: "auto",
                    alignItems: "center",
                    justifyContent: "space-between",
                    position: "relative",
                    paddingLeft: 2,
                    width: "100%",
                    backgroundColor: "white",
                    borderRadius: 2,
                  }}
                >
                  <StyledInputBase
                    placeholder="Search..."
                    value={searchText}
                    onChange={handleSearchTextChange}
                    inputProps={{ "aria-label": "search" }}
                  />
                  <SearchIconWrapper>
                    <SearchIcon />
                  </SearchIconWrapper>

                </Box>
              </div>

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
                <ButtonGroup sx={{ marginBottom: 2 }}>
                  {facilities.map((item, index) => (
                    <Button
                      key={index}
                      sx={
                        venueSelected === item?.facility_name
                          ? selectedStyle
                          : unselectedStyle
                      }
                      onClick={() => {
                        setVenueSelected(item?.facility_name);
                        setVenueId(item?.facility_id);
                      }}
                    >
                      {item?.facility_name}
                    </Button>
                  ))}
                </ButtonGroup>

                <TableContainer>
                  <Table
                    style={{
                      backgroundColor: "white",
                      width: "100%",
                      textAlign: "center",
                      fontFamily: "Oswald",
                      "@media (max-width: 600px)": {
                        fontSize: "14px",
                      },
                      "@media (max-width: 400px)": {
                        fontSize: "12px",
                      },
                    }}
                  >
                    <TableHead>
                      <TableRow>
                        <StyledTableCell align="center">Name</StyledTableCell>
                        <StyledTableCell align="center">Loggedin</StyledTableCell>
                        <StyledTableCell align="center">Overstaying</StyledTableCell>
                        <StyledTableCell align="center">Date</StyledTableCell>
                        <StyledTableCell align="center">Login Time</StyledTableCell>
                        <StyledTableCell align="center">Logout Time</StyledTableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {filteredEvents
                        .slice(page * rowsPerPage, (page + 1) * rowsPerPage)
                        .map((event, index) => (
                          <StyledTableRow key={index}>
                            <StyledTableCell
                              component="th"
                              scope="row"
                              align="center"
                            >
                              {event?.name}
                            </StyledTableCell>
                            <StyledTableCell align="center">
                              {event.isSignedIn === true ? "Yes" : "No"}
                            </StyledTableCell>
                            <StyledTableCell align="center">
                              {event.isOverstaying === true ? "Yes" : "No"}
                            </StyledTableCell>
                            <StyledTableCell align="center">
                              {event?.date}
                            </StyledTableCell>
                            <StyledTableCell align="center">
                              {event?.signInTime}
                            </StyledTableCell>
                            <StyledTableCell align="center">
                              {event?.signOutTime}
                            </StyledTableCell>
                          </StyledTableRow>
                        ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </Box>
            </Box>
          </Container>
        </DashBoardTemplate>
      </div>
    );
  }
}
