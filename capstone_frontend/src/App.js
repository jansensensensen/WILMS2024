import './App.css';
import {
  BrowserRouter, Routes,
  Route, Redirect, Link,
} from 'react-router-dom';
// import wild from "../../images/wil.png";
import {AuthProvider} from './context/AuthContext';
import Tracker from './pages/dashboard';
import Calendar from './pages/calendar_page';
import MyReservations from './pages/my_reservations';
import AttendanceLogs from './pages/attendance_logs';
import Attendance from './pages/attendance';
import Login from './pages/login_page';
import About from './pages/about';

function App() {
  return (
    <div className="App">
     
        <BrowserRouter>
        <AuthProvider>
          <Routes>
            <Route exact path="/booking/login" element={<Login />} />
            {/* <Route exact path="/" element={<Login />} /> */}
            <Route exact path="/booking/tracker" element={<Tracker />} />
            <Route exact path="/booking/calendar" element={<Calendar />} />
            <Route exact path="/booking/logs" element={<AttendanceLogs />} />
            <Route exact path="/booking/bookings" element={<MyReservations />} />
            <Route exact path="/booking/about" element={<About />} />

            {/* <Route exact path="/attendance" element={<Attendance />} /> */}
            <Route exact path="/booking/attendance" element={<Attendance />} />
          </Routes>
          </AuthProvider>
        </BrowserRouter>
      
    </div>
  );
}

export default App;
