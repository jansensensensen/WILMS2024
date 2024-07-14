import React, { useState, useEffect, useRef } from "react";
import { BASE_URL } from "../../links";
import axios from "axios";
import Modal from "@mui/material/Modal";
import { Box, Button, Typography, TextField, Snackbar } from "@mui/material";
import MuiAlert from "@mui/material/Alert";
import { modalHeaderStyle, ButtonStyle1 } from "./styles";
import { CustomAlert } from "../calendar_page";

export default function Attendance(props) {
  const [attendance, setAttendance] = useState(false);
  const [isVenueModalOpen, setVenueModal] = useState(false);
  const [userLoggedIn, setUserLoggedIn] = useState(false);
  const [lastBooking, setLastBooking] = useState(null);
  const [isLoggedOutModalOpen, setLoggedOutModal] = useState(false);
  const [tapInput, setTapInput] = useState("");
  const [scannedNumber, setScannedNumber] = useState("");
  const [avail, setAvail] = useState(true);
  const [warningMessage, setWarningMessage] = useState("");
  const scannedNumberRef = useRef(scannedNumber);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [alertSuccess, setAlertSuccess] = useState(false);
  const [alertMessage, setAlertMessage] = useState("");
  const [alertOpen, setAlertOpen] = useState(false);

  const handleAlertClose = () => {
    setAlertOpen(false);
  };

  const openAttendanceModal = () => {
    setAttendance(true);
  };

  const closeModal = () => {
    setAttendance(false);
  };

  const closeLoggedOutModal = () => {
    setLoggedOutModal(false);
  };

  const WelcomeModal = () => {
    setVenueModal(false);
  };

  const handleSnackbarClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }

    setSnackbarOpen(false);
  };

  const handleChange = (e) => {
    const newScannedNumber = e.target.value;
    console.log('Scanned Number:', newScannedNumber);
    setTapInput(newScannedNumber);
    if (newScannedNumber.length === 10 && /^\d+$/.test(newScannedNumber)) {
      console.log('Handling save...');
      scannedNumberRef.current = newScannedNumber;
    }
  };
  
  useEffect(() => {
    const intervalId = setInterval(() => {
      //assign interval to a variable to clear it.
      setAvail(true);
    }, 5000);
    return () => clearInterval(intervalId);
  }, [avail]);

  const handleSave = (scannedNumber) => {
    if (avail === true) {
      const data = { rfid: scannedNumber };
      console.log(data);
      axios
        .post(`${BASE_URL}/api/logAttendance/`, data)
        .then((response) => {
          if (response.data.state === "login") {
            console.log("Data saved successfully", response.data);
            setUserLoggedIn(true);
            setLastBooking(response.data);
            setVenueModal(true);
            closeModal();
          } else if (response.data.state === "noBooking") {
            setAvail(false);
            setAlertMessage("You Have No Booking within 30 minutes!");
            setAlertOpen(true);
            setAlertSuccess(true);
          } else if (response.data.state === "notFound") {
            setAvail(false);
            setAlertMessage("ID is not found or is unregistered");
            setAlertOpen(true);
            setAlertSuccess(true);
          } else {
            setLoggedOutModal(true);
          }
          setTapInput("")
        })
        .catch((error) => {
          console.error("Error saving data", error);
          setAlertOpen(true);
        });
    }
  };  

  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.key === 'Enter') {
        const currentScannedNumber = scannedNumberRef.current;
        console.log('Handling save...', currentScannedNumber);
        handleSave(currentScannedNumber);
        setTapInput("");
        console.log('Scanned Number:', scannedNumberRef.current);
        console.log('Tap Input:', tapInput);
        
      }
    };

    document.addEventListener('keypress', handleKeyPress);

    return () => {
      document.removeEventListener('keypress', handleKeyPress);
    };
  }, [handleSave]);
  

  return (
    <div>
      {alertOpen && (
        <CustomAlert
        open={alertOpen}
        onClose={handleAlertClose}
        message={alertMessage}
        color={alertSuccess ? "#e74c3c" : "#e74c3c"}
      />
      )}

      <div style={{ margin: "80px" }}></div>
      <Modal
        open={true}
        onClose={closeModal}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 400,
            bgcolor: "background.paper",
            border: "2px solid #000",
            boxShadow: 24,
            p: 4,
            fontFamily: "Poppins",
          }}
        >
          <h2 sx={{ modalHeaderStyle }}>Tap Here</h2>
          <Typography
            sx={{ fontFamily: "Poppins", fontSize: 30, fontWeight: "bold" }}
          >
            Please tap your ID:
          </Typography>
          <div style={{ margin: "20px" }}></div>
          <TextField
            label="ID Number"
            variant="outlined"
            fullWidth
            value={tapInput}
            onChange={handleChange}
            sx={{ fontFamily: "Poppins" }}
            autoFocus
          />
          <Box sx={{ justifyContent: "space-between" }}>
            <div style={{ margin: "20px" }}></div>
            {/* <Button
              variant="contained"
              sx={ButtonStyle1}
              style={{ marginRight: "15px" }}
              onClick={() => {
                handleSave();
              }}
            >
              Tap In
            </Button>
            <Button
              variant="contained"
              sx={ButtonStyle2}
              onClick={closeModal}
            >
              Cancel
            </Button> */}
          </Box>
        </Box>
      </Modal>

      <Modal
        open={isVenueModalOpen && userLoggedIn}
        onClose={() => setVenueModal(true)}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 400,
            bgcolor: "background.paper",
            border: "2px solid #000",
            boxShadow: 24,
            p: 4,
          }}
        >
          <h2 sx={{ modalHeaderStyle }}>Welcome!</h2>
          <Typography>
            Your attendance has been logged, you can now proceed!
          </Typography>
          <div style={{ margin: "20px" }}></div>
          <Button
            variant="contained"
            sx={ButtonStyle1}
            style={{ marginRight: "15px" }}
            onClick={WelcomeModal}
          >
            Okay
          </Button>
        </Box>
      </Modal>
      <Modal
        open={isLoggedOutModalOpen}
        onClose={closeLoggedOutModal}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box
          sx={{
            position: "absolute",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            width: 400,
            bgcolor: "background.paper",
            border: "2px solid #000",
            boxShadow: 24,
            p: 4,
          }}
        >
          <h2 sx={{ modalHeaderStyle }}>You are Now Logged Out</h2>
          <Typography>You have been successfully logged out.</Typography>
          <div style={{ margin: "20px" }}></div>
          <Button
            variant="contained"
            sx={ButtonStyle1}
            style={{ marginRight: "15px" }}
            onClick={closeLoggedOutModal}
          >
            OK
          </Button>
        </Box>
      </Modal>
    </div>
  );
}
