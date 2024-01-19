import Button from "@mui/joy/Button";
import Input from "@mui/joy/Input";

export default function Login() {
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
                        <Input className="w-full h-[50px] rounded-sm" placeholder="Username" />
                        <Input type="password" className="w-full h-[50px] rounded-sm" placeholder="Password" />
                        <div className="mt-2 text-sm w-full text-right">
                            <a href="/forgot-password">
                                Forgot Password?
                            </a>
                        </div>
                        <Button className="mt-2 w-full h-[50px] rounded-sm" onClick={() => {}}>Login</Button>
                    </div>
                </div>
            </div>
        </div>
    )
}