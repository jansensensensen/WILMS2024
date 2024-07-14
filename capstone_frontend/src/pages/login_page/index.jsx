import React from "react";
import TextField from "@mui/material/TextField";
import { Button, Box, Typography, Snackbar, Alert } from "@mui/material";
import { ButtonStyle1, loginstyle, fields, logo } from "./styles";
import { useState } from "react";
import Wild from "../../images/w4.png";
import bg from "../../images/basebg.jpg";
import { useContext } from "react";
import AuthContext from "../../context/AuthContext";
import { useEffect } from "react";

import { useNavigate } from "react-router-dom";

const Login = () => {
  const [open, setOpen] = React.useState(false);
  let { loginUser, loginError, setLoginError, user } = useContext(AuthContext);

  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      setOpen(false);
      setLoginError(null);

      // return;
    }

    // setOpen(false);
  };
  const navigate = useNavigate();
  const [accounts, setAccount] = useState([]);
  const [accountlogin, setAccountlogin] = useState({
    username: "",
    password: "",
  });

  const { username, password } = accountlogin;
  const onInputChange = (e) => {
    setAccountlogin({ ...accountlogin, [e.target.name]: e.target.value });
  };
  useEffect(() => {
    if (loginError === null) {
      setOpen(false);
    } else {
      setOpen(true);
    }
  }, [loginError]);
  if (user !== null) {
    navigate("/booking/calendar");
  } else {
    return (
      <div
        style={{
          backgroundImage: `url(${bg})`,
          backgroundRepeat: "no-repeat",
          backgroundSize: "cover",
          height: "100vh",
          width: "100vw",
          display: "flex",
          // justifyContent: "center",
          // alignItems: "center",
          flexDirection: "column",
        }}
      >
        <Box marginTop={5}>
          <a href="http://127.0.0.1:8000/">
            <img
              src={Wild}
              alt="logo"
              width={300}
              height={100}
              // style={{
              //   position: "absolute",
              //   top: 120,
              //   left: 700,
              // }}
            />
            <Snackbar
              open={open}
              autoHideDuration={6000}
              onClose={handleClose}
              anchorOrigin={{ horizontal: "center", vertical: "bottom" }}
            >
              <Alert
                onClose={handleClose}
                severity="error"
                sx={{ width: "100%" }}
              >
                {loginError}
              </Alert>
            </Snackbar>
          </a>
        </Box>
        <Box>
          <Box
            style={loginstyle}
            sx={{ p: 5, width: 300, height: "auto", align: "center" }}
          >
            <Typography
              sx={{ fontWeight: "bold" }}
              id="modal-modal-title"
              variant="h4"
              component="h2"
              fontFamily="Poppins"
              color="black"
            >
              {" "}
              USER LOGIN
            </Typography>
            <br /> <br />
            <TextField
              label={"Email"}
              id="username"
              name="username"
              onChange={(e) => onInputChange(e)}
              style={fields}
            />{" "}
            <br />
            <br />
            <TextField
              label={"Password"}
              id="pw"
              name="password"
              type="password"
              onChange={(e) => onInputChange(e)}
              style={fields}
            />
            <br />
            <br />
            <Button
              variant="contained"
              color="primary"
              style={ButtonStyle1}
              onClick={() => {
                loginUser(accountlogin.username, accountlogin.password);
              }}
            >
              Login
            </Button>
            <br />
          </Box>
        </Box>
      </div>
    );
  }
};

export default Login;
