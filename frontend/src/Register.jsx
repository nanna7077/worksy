import Button from "@mui/joy/Button";
import Input from "@mui/joy/Input";
import { useState } from "react";
import PhoneInputWithCountrySelect from "react-phone-number-input";
import "react-phone-number-input/style.css";

export default function Register() {
    const [fullName, setFullName] = useState("");
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [phone, setPhone] = useState("");

    const register = () => {
        fetch(process.env.REACT_APP_API_URL + "/accounts/create/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                fullName: fullName,
                username: username,
                email: email,
                password: password,
                phone: phone,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                alert(data.error);
                return;
            }
            window.location.href = "/login";
        });
    }

    return (
        <div className="">
            <div className="w-full flex gap-2 p-2 bg-[#33363F] text-white justify-center items-center">
                <span className="text-xl font-bold">Worksy</span>
                <span className="text-xl">|</span>
                <span>
                    Already have an account?{" "}
                    <a className="underline" href="/login">
                        Login
                    </a>
                </span>
            </div>
            <div className="flex h-screen justify-center items-center">
                <div className="w-full flex flex-col items-center">
                    <img src="logo.png" alt="logo" />
                    <div className="mt-6">Create a new account</div>
                    <div className="w-full mt-6 flex gap-2 flex-col items-center p-4">
                        <Input
                            className="w-full h-[50px] rounded-sm"
                            placeholder="Full name"
                            onChange={(e) => {setFullName(e.target.value)}}
                        />
                        <Input
                            type="username"
                            className="w-full h-[50px] rounded-sm"
                            placeholder="Username"
                            onChange={(e) => {setUsername(e.target.value)}}
                        />
                        <Input
                            type="email"
                            className="w-full h-[50px] rounded-sm"
                            placeholder="Email Address"
                            onChange={(e) => {setEmail(e.target.value)}}
                        />
                        <Input
                            type="password"
                            className="w-full h-[50px] rounded-sm"
                            placeholder="Password"
                            onChange={(e) => {setPassword(e.target.value)}}
                        />
                        <PhoneInputWithCountrySelect
                            placeholder="Phone Number"
                            onChange={(v) => {
                                setPhone(v);
                            }}
                            international
                            defaultCountry="IN"
                            value={phone}
                            className="w-full h-[50px] rounded-sm"
                        />
                        <Button
                            className="mt-2 w-full h-[50px] rounded-sm"
                            onClick={() => {
                                register();
                            }}
                        >
                            Register
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}
