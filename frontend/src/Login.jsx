import Button from "@mui/joy/Button";
import Input from "@mui/joy/Input";
import { useEffect, useState } from "react";

export default function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    useEffect(() => {
        fetch(process.env.REACT_APP_API_URL + "/accounts/view/self", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                if (data.error == "UnAuthorized") {
                    return;
                }
                alert(data.error);
                return;
            }
            window.location.href = "/";
        });
    }, [])

    function login() {
        fetch(process.env.REACT_APP_API_URL + "/accounts/create/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                if (data.error == "Unauthorized") {
                    return;
                }
                alert(data.error);
                return;
            }
            window.localStorage.setItem("sessionkey", data.sessionkey);
            window.location.href = "/";
        });
    }

    return (
        <div className="">
            <div className="w-full flex gap-2 p-2 bg-[#33363F] text-white justify-center items-center">
                <span className="text-xl font-bold">Worksy</span>
                <span className="text-xl">|</span>
                <span>
                    Don't have an account? <a className="underline" href="/register">Register</a>
                </span>
            </div>
            <div className="flex h-screen justify-center items-center">
                <div className="w-full flex flex-col items-center">
                    <img src="logo.png" alt="logo" />
                    <div className="mt-6">Log into your account</div>
                    <div className="w-full mt-6 flex gap-2 flex-col items-center p-4">
                        <Input type="username" className="w-full h-[50px] rounded-sm" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
                        <Input type="password" className="w-full h-[50px] rounded-sm" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
                        <div className="mt-2 text-sm w-full text-right">
                            <a href="/forgot-password">
                                Forgot Password?
                            </a>
                        </div>
                        <Button className="mt-2 w-full h-[50px] rounded-sm" onClick={login}>Login</Button>
                    </div>
                </div>
            </div>
        </div>
    )
}