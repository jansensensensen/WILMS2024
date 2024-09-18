import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";

import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";

import MenuIcon from "@mui/icons-material/Menu";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Button, Icon } from "@mui/material";
import HomeIcon from "@mui/icons-material/Home";
import DashboardIcon from "@mui/icons-material/Dashboard";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import BookIcon from "@mui/icons-material/Book";
import ListIcon from "@mui/icons-material/List";
import Wild from "../../images/wild.png";
import bgcover from "../../images/basebg.PNG";
import admin from "../../images/admin3.png";
import { useNavigate, useLocation, Link } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import { useContext, useState } from "react";
import { BASE_URL } from "../../links";


const drawerWidth = 277;

export default function DashBoardTemplate(props) {
  const { user } = useContext(AuthContext);
  const { window } = props;
  const [mobileOpen, setMobileOpen] = React.useState(false);
  const { logoutUser } = React.useContext(AuthContext);
  const [role, setRole] = useState("admin"); //default role
  const navigate = useNavigate();

  // admin appbar navigate to other apps
  const mainNavItems = [
    { name: "Home", path: "/wallet" },
    { name: "Facility", path: "/facility/facilitymanagement" },
    { name: "Booking", path: "/booking/calendar" },
    { name: "Wallet", path: "/wallet/dashboard/" },
    { name: "Crowd Control", path: "/wiladmin/admindashboard" },
    
  ];

  //admin sidenav
  const adminNavItems = [
    // { name: "Home", icon: HomeIcon, path: "/" },
    { name: "Tracker", icon: DashboardIcon, path: "/booking/tracker" },
    { name: "Calendar", icon: CalendarMonthIcon, path: "/booking/calendar" },
    { name: "Logs", icon: BookIcon, path: "/booking/logs" },
    { name: "Bookings", icon: ListIcon, path: "/booking/bookings" },
    { name: "About", path: "/booking/about" },
  ];

  //user sidenav
  const userNavItems = [
    // { name: "Home", icon: HomeIcon, path: "/home" },
    { name: "Calendar", icon: CalendarMonthIcon, path: "/booking/calendar" },
    { name: "Bookings", icon: ListIcon, path: "/booking/bookings" },
    { name: "About", path: "/booking/about" },
  ];

  const NavItems = user?.role === "admin" ? adminNavItems : userNavItems;
  const isUser = user?.role === "user";
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const selectedStyle = {
    backgroundColor: "#fecc00",
    borderRadius: "5px",
    color: "white",
  };
  const unselectedStyle = {
    backgroundColor: "transparent",
    color: "black",
    transition: "background 0.7s, color 0.7s",
    borderRadius: "5px",
    "&:hover": {
      bgcolor: "#fecc00",
    },
    // fontWeight: 700,
    // fontSize: '1.4rem'
  };

  const logoutButtonStyle = {
    backgroundColor: "transparent",
    color: "red",
    transition: "background 0.7s, color 0.7s",
    fontSize: "1.5rem",
    fontWeight: 770,
    "&:hover": {
      bgcolor: "transparent",
      textDecoration: "none",
      borderBottom: "1px solid black",
      paddingBottom: "1px",
      color: "red",
      transition: "color 0.1s",
      fontFamily: "Poppins",
    },
  };

  const location = useLocation();

  const Navigation = () => {
    if (user?.role !== "admin") {
      return null;
    }

    return (
      <List
        sx={{
          marginLeft: "auto",
          display: "flex",
          fontSize: "1.2rem",
        }}
      >
        {mainNavItems.map((item, index) => (
          <Button
            key={index}
            className="adminapps"
            sx={{
              ...(item.path === location.pathname
                ? selectedStyle
                : unselectedStyle),
              "&:hover": {
                bgcolor: "transparent",
                textDecoration: "none",
                borderBottom: "1px solid black",
                paddingBottom: "1px",
                color: "white",
                transition: "color 0.1s",
                fontWeight: 770,
                fontSize: "1.4rem",
                fontFamily: "Poppins",
              },
            }}
            href={
              item.path.startsWith("http") || item.name === "Booking"
                ? item.path
                : `${BASE_URL}${item.path}`
            }
            target="_blank" //opens in a new tab
          >
            <ListItemButton>
              <ListItemText
                primary={item.name}
                primaryTypographyProps={{
                  style: {
                    fontWeight: 770,
                    fontSize: "1.4rem",
                    fontFamily: "Poppins",
                  },
                }}
              />
            </ListItemButton>
          </Button>
        ))}
        <Button sx={logoutButtonStyle} onClick={() => logoutUser()}>
          <Typography fontFamily="Poppins">Logout</Typography>
        </Button>
      </List>
    );
  };

  const drawer = (
    // sidenav sidenavbar
    <div>
      <Toolbar
        sx={{
          backgroundColor: "#fecc00",
          height: "112px",
          alignItems: "center",
        }}
      >
        <img src={Wild} alt="logo" width={300} height={70} />
      </Toolbar>
      {/* <Divider sx={{ backgroundColor: "white" }} /> */}
      {/* sidenav color */}
      {user?.role === "admin" ? (
        <div> 
          <img src={admin} alt="Admin" width={92} height={90} style={{marginTop: "20px"}}/>
          <Typography sx={{ fontFamily: "Poppins", color: "white" }}>
            Admin
          </Typography>
        </div>
      ) : user?.role === "user" ? (
        <Typography sx={{ fontFamily: "Poppins", color: "white", fontSize: "25px" }}>
          Booking System
        </Typography>
      ) : null}
      <List
        sx={{
          backgroundColor: "black",
          paddingBottom: "5px",
          display: "column",
          height: "auto",
          fontSize: "1.2rem",
        }}
      >
        {NavItems.map((item, index) => (
          <ListItem
            sx={{
              ...(item.path === location.pathname
                ? {
                    ...selectedStyle,
                    borderRadius: "10px",
                    borderBottomRightRadius: "18px",
                    borderTopLeftRadius: "18px",
                    borderRadius: "5px",
                  }
                : {
                    ...unselectedStyle,
                    backgroundColor: "#333333",
                    borderBottomRightRadius: "18px",
                    borderTopLeftRadius: "18px",
                    borderRadius: "5px",
                  }),
              padding: "5px",
              margin: "13px",
              width: "auto",
            }}
            key={index}
            disablePadding
          >
            <ListItemButton onClick={() => navigate(item.path)}>
              <ListItemText
                sx={{
                  color: "white",
                  fontWeight: "bold",
                  fontFamily: "Poppins",
                  alignItems: "center",
                  textAlign: "center",
                  fontSize: "1.2rem",
                }}
                fontWeight= "strong"
                primary={item.name}
              />
            </ListItemButton>
          </ListItem>
        ))}
        <br />

        {isUser && (
          <ListItem
            disablePadding
            sx={{ display: "flex", justifyContent: "center", paddingTop: 40 }}
          >
            <Button
              variant="contained"
              sx={{
                backgroundColor: "#fecc00",
                borderColor: "#fecc00",
                width: "80%",
                color: "black",
                ":hover": {
                  bgcolor: "#9c7b16",
                  color: "white",
                },
                borderRadius: "10px",
              }}
              onClick={() => {
                logoutUser();
              }}
            >
              <Typography fontFamily="Poppins" fontWeight="bold">
                Logout
              </Typography>
            </Button>
          </ListItem>
        )}
      </List>
    </div>
  );

  const container = window !== undefined ? () => window().document.body : undefined;

  return (
    // main nav
    <Box
      sx={{
      display:'flex',
      backgroundImage: `url(${bgcover})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
      width:'100%',
      height: '100%',
      "@media (max-width: 815px)": {
                  width:'100vh',

                },
      }}
    >
      <CssBaseline />
      <AppBar
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar sx={{ backgroundColor: "#fecc00", height: "112px" }}>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: "none" } }}
          >
            <MenuIcon />
          </IconButton>
          {/* Roboto Slab */}
          <Typography
            variant="h4"
            noWrap
            component="div"
            fontFamily="Poppins"
            color="black"
            fontWeight="bold"
          >
          </Typography>
          <Navigation />
        </Toolbar>
      </AppBar>

      <AppBar
        sx={{
          position: "absolute",
          backgroundColor: "#fecc00",
          top: "150px",
          left: "50%",
          transform: "translateX(-50%)",
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          height: '9vh',
          width: '75%',
          borderRadius: '1px',
          marginLeft: '135px',
          zIndex: 0,
          "@media (max-width: 768px)": {
            width: '90%',
            marginLeft: '5%',
          },
        }}
      >
        <Box sx={{ width: '100%', textAlign: 'left' , marginLeft: "7px" }}>
        <Typography
          variant="h4"
          noWrap
          component="div"
          fontFamily="Poppins"
          color="black"
          fontWeight="bold"
          margin="auto"
          sx={{ padding: '10px' }}
          //textAlign="left"
        >
          {props.title}
        </Typography>
        </Box>
      </AppBar>

      <Box
        component="nav"
        sx={{
          width: { sm: drawerWidth },
          flexShrink: { sm: 0 },
          backgroundColor: "black",
        }}
        aria-label="mailbox folders"
      >
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <Drawer
          PaperProps={{
            sx: {
              backgroundColor: "black",
            },
          }}
          container={container}
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: "block", sm: "none" },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              width: drawerWidth,
            },
            border: "none",
          }}
        >
          {drawer}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: "none", sm: "block" },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              width: drawerWidth,
              border: "none",
              // sidenav color
              backgroundColor: "black",
            },
          }}
          PaperProps={{
            sx: {
              backgroundColor: "#white",
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 0,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
        }}
      >
        <Toolbar />
        <Typography paragraph>{/* eraseable */}</Typography>
        {props.children}
      </Box>
    </Box>
  );
}
