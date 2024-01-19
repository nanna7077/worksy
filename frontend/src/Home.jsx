import Button from "@mui/joy/Button";

export default function Home() {
    return (
        <div className="">
            <div className="flex h-screen justify-center items-center">
                <div className="w-full flex flex-col items-center">
                    <img src="logo.png" alt="logo" />
                    <div className="w-full mt-[100px] flex gap-2 flex-col items-center">
                        <Button className="w-[50vw] h-[50px] rounded-sm" onClick={() => {window.location.href = '/login'}}>Login</Button>
                        <Button className="w-[50vw] h-[50px] rounded-sm" onClick={() => {window.location.href = '/register'}}>Register</Button>
                    </div>
                </div>
            </div>
        </div>
    )
}