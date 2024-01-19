import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./Home";
import { CssVarsProvider, extendTheme } from "@mui/joy/styles";
import Login from "./Login";
import Register from "./Register";

function App() {
    const theme = extendTheme({
        colorSchemes: {
            dark: {
                palette: {
                    "primary": { // TODO: Create Palette
                        "50": "#33363F",
                        "100": "#33363F",
                        "200": "#33363F",
                        "300": "#33363F",
                        "400": "#33363F",
                        "500": "#33363F",
                        "600": "#33363F",
                        "700": "#33363F",
                        "800": "#33363F",
                        "900": "#33363F"
                    }
                },
            },
            light: {
                palette: {
                    "primary": {
                        "50": "#33363F",
                        "100": "#33363F",
                        "200": "#33363F",
                        "300": "#33363F",
                        "400": "#33363F",
                        "500": "#33363F",
                        "600": "#33363F",
                        "700": "#33363F",
                        "800": "#33363F",
                        "900": "#33363F"
                    }
                },
            },
        },
    });

    return (
        <CssVarsProvider theme={theme}>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                </Routes>
            </BrowserRouter>
        </CssVarsProvider>
    );
}

export default App;
