import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./Home";
import { CssVarsProvider, extendTheme } from "@mui/joy/styles";
import Login from "./Login";
import Register from "./Register";
import JobCreate from "./JobCreate";
import History from "./History";
import Profile from "./Profile";
import Notifications from "./Notifications";
import Job from "./Job";
import Messages from "./Messages";
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDbia_Y0J5mQ9JAe5xBJXTj1MIEsfcaeK8",
  authDomain: "worksy-fff70.firebaseapp.com",
  projectId: "worksy-fff70",
  storageBucket: "worksy-fff70.appspot.com",
  messagingSenderId: "517208843814",
  appId: "1:517208843814:web:ec9baef6da3e65e903a8e7",
  measurementId: "G-87Y3FL3E4R"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

function App() {
    const theme = extendTheme({
        colorSchemes: {
            dark: {
                palette: {
                    primary: {
                        // TODO: Create Palette
                        50: "#33363F",
                        100: "#33363F",
                        200: "#33363F",
                        300: "#33363F",
                        400: "#33363F",
                        500: "#33363F",
                        600: "#33363F",
                        700: "#33363F",
                        800: "#33363F",
                        900: "#33363F",
                    },
                },
            },
            light: {
                palette: {
                    primary: {
                        50: "#33363F",
                        100: "#33363F",
                        200: "#33363F",
                        300: "#33363F",
                        400: "#33363F",
                        500: "#33363F",
                        600: "#33363F",
                        700: "#33363F",
                        800: "#33363F",
                        900: "#33363F",
                    },
                },
            },
        },
    });

    return (
        <CssVarsProvider theme={theme}>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/profile/:id" element={<Profile />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/jobs/create" element={<JobCreate />} />
                    <Route path="/history" element={<History />} />
                    <Route path="/notifications" element={<Notifications />} />
                    <Route path="/job/:id" element={<Job />} />
                    <Route path="/messages" element={<Messages />} />
                    <Route path="/messages/:id" element={<Messages />} />
                </Routes>
            </BrowserRouter>
        </CssVarsProvider>
    );
}

export default App;
