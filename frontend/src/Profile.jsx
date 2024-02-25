import { Avatar, Button, Chip, ChipDelete, DialogTitle, Input, LinearProgress, Modal, ModalDialog } from "@mui/joy";
import { useEffect } from "react";
import { useState } from "react";
import NavBottom from "./Nav";

export default function Profile() {
    const [isLoading, setIsLoading] = useState(false);
    const [refresh, setRefresh] = useState(false);

    const profileID = window.location.pathname.split("/")[2];
    const [user, setUser] = useState(null);
    const [skills, setSkills] = useState([]);

    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmNewPassword, setConfirmNewPassword] = useState("");

    const [showSkillAddModal, setShowSkillAddModal] = useState(false);

    useEffect(() => {
        setIsLoading(true);

        fetch(process.env.REACT_APP_API_URL + "/accounts/view/" + profileID, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            setIsLoading(false);
            if (data.error != undefined) {
                return;
            }
            setUser(data.account);
        });

        fetch(process.env.REACT_APP_API_URL + "/jobs/view/tags/list/all", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            setIsLoading(false);
            if (data.error != undefined) {
                return;
            }
            setSkills(data.tags);
        });

        setRefresh(false);
    }, [refresh])

    function resetPassword() {
        if (newPassword != confirmNewPassword) {
            alert("Passwords do not match");
            setIsLoading(false);
            return;
        }
        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + "/accounts/update/password", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
            body: JSON.stringify({
                password: newPassword,
                confirm_password: confirmNewPassword,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            setIsLoading(false);
            if (data.error != undefined) {
                return;
            }
            alert("Password reset successful");
        });
    }

    function updateFullname() {
        const fullname = prompt("What's your full name?");
        if (fullname == null) {
            return;
        }
        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + "/accounts/update/fullname", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
            body: JSON.stringify({
                fullname: fullname,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            setIsLoading(false);
            if (data.error != undefined) {
                return;
            }
            setRefresh(true);
        });
    }

    function updateEmail() {
        const email = prompt("What's your email?");
        if (email == null) {
            return;
        }
        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + "/accounts/update/email", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
            body: JSON.stringify({
                email: email,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            setIsLoading(false);
            if (data.error != undefined) {
                return;
            }
            setCurrentPassword("");
            setNewPassword("");
            setConfirmNewPassword("");
            setRefresh(true);
        });
    }

    function updatePhone() {
        const phone = prompt("What's your phone number?");
        if (phone == null) {
            return;
        }
        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + "/accounts/update/phone", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
            body: JSON.stringify({
                phone: phone,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            setIsLoading(false);
            if (data.error != undefined) {
                return;
            }
            setRefresh(true);
        });
    }

    function updateOpenToWork() {
        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + "/accounts/update/open_to_work", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            setIsLoading(false);
            if (data.error != undefined) {
                return;
            }
            setRefresh(true);
        });
    }

    function logout() {
        fetch(process.env.REACT_APP_API_URL + "/accounts/update/logout", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                return;
            }
            window.localStorage.removeItem("sessionkey").then(() => {
                window.location.href = "/";
            })
        });
    }

    return (<div className="">
        {isLoading && <LinearProgress color="primary" />}
        <Modal open={showSkillAddModal} onClose={() => {setShowSkillAddModal(false);}}>
            <ModalDialog className="overflow-y-auto">
                <DialogTitle>Add Skill</DialogTitle>
                <div className='flex gap-2 flex-wrap justify-evenly'>
                    {skills.map((skill, sid) => (
                        <Chip
                            key={sid}
                            color="primary"
                            className="!text-white"
                            variant="soft"
                            onClick={() => {
                                fetch(process.env.REACT_APP_API_URL + "/accounts/update/tags/add", {
                                    method: "POST",
                                    headers: {
                                        "Content-Type": "application/json",
                                        "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
                                    },
                                    body: JSON.stringify({
                                        "tagId": skill.id
                                    }),
                                })
                                setShowSkillAddModal(false);
                                setRefresh(true);
                            }}
                        >
                            {skill.name}
                        </Chip>
                    ))}
                </div>

            </ModalDialog>
        </Modal>
        <div className="flex flex-col">
            <div style={{background: "rgba(255, 255, 255, .4)"}} className="m-2 p-2 backdrop-blur-lg">
                {user && 
                <div className="flex w-full justify-center items-center gap-3">
                    <Avatar src={user.profile_picture} onClick={() => {window.open("https://gravatar.com/profile/avatars", "_blank")}} sx={{width: 150, height: 150}}>{user.username}</Avatar>
                    <div className="flex flex-col items-center">
                        <div className="text-2xl font-bold" onClick={() => {if(!user.is_self) return; updateFullname()}}>{user.fullname} <span className="text-sm">({user.username})</span> </div>
                        {user.is_self && <div className="text-sm"><span onClick={() => {if(!user.is_self) return; updateEmail()}}>{user.email}</span> | <span onClick={() => {if(!user.is_self) return; updatePhone()}}>{user.phone}</span></div>}
                        <div className="flex-break mt-3"></div>
                        <div className="flex gap-3">
                            <div className="flex gap-1 items-center">
                                <img src="/icons/star.svg" className="w-4 h-4" />
                                <div>
                                    {user.rating} / 5
                                </div>
                            </div>
                            <Button size="sm" onClick={() => {if(!user.is_self) return; updateOpenToWork()}} className="!text-xs" variant="solid" color="primary">{user.open_to_work ? "Open to work" : "Not open to work"}</Button>
                            {user.open_to_work && <Button size="sm" className="!text-xs" variant="solid" color="primary">{user.is_available ? "Available Now" : "Not Available Now"}</Button>}
                            <Button size="sm" onClick={() => {window.location.href = "/messages/" + profileID}} className="!text-xs" variant="solid" color="primary">Message</Button>
                        </div>
                    </div>
                </div>}
            </div>
            <div className="p-4 flex flex-col gap-2">
                <Button className="w-full" onClick={logout} variant="outlined">Logout</Button>
            </div>
            <div style={{background: "rgba(255, 255, 255, .4)"}} className="m-2 p-2 backdrop-blur-lg flex flex-col gap-2">
                <div className="flex gap-2 items-center">
                    <div className="font-semibold">Skills</div>
                    <div className="flex-grow"></div>
                    {user && user.is_self && <Button size="sm" onClick={() => {setShowSkillAddModal(true)}} className="!text-xs" variant="solid" color="primary">Add Skill</Button>}
                </div>
                <div className="flex flex-wrap gap-2">
                    {user && user.tags.map((skill, index) => <Chip key={index} color="primary" className="!text-white" variant="soft"label={skill.name}>{skill.name} <ChipDelete className="!text-white" onDelete={() => {
                        setIsLoading(true);
                        fetch(process.env.REACT_APP_API_URL + "/accounts/update/tags/remove", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
                            },
                            body: JSON.stringify({
                                "tagId": skill.id
                            }),
                        })
                        .then((response) => response.json())
                        .then((data) => {
                            setIsLoading(false);
                            if (data.error != undefined) {
                                return;
                            }
                            setRefresh(true);
                        })
                    }} /></Chip>)}
                    <div className="flex-break mt-2 w-full"></div>
                    {user && user.tags.length == 0 && <div className="text-sm">No skills added yet</div>}
                </div>
            </div>
            {user && user.is_self && <div style={{background: "rgba(255, 255, 255, .4)"}} className="m-2 mt-0 p-2 backdrop-blur-lg">
                <div className="flex flex-col">
                    <div className="text-xl font-bold">Reset Password</div>
                    <div className="flex-break mt-3"></div>
                    <div className="text-base">Current Password</div>
                    <Input type="password" defaultValue={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} />
                    <div className="flex-break mt-1"></div>
                    <div className="text-base">New Password</div>
                    <Input type="password" defaultValue={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
                    <div className="flex-break mt-1"></div>
                    <div className="text-base">Confirm New Password</div>
                    <Input type="password" defaultValue={confirmNewPassword} onChange={(e) => setConfirmNewPassword(e.target.value)} />
                    <div className="flex-break mt-3"></div>
                    <Button className="w-fit" variant="outlined" color="primary" onClick={() => {resetPassword()}}>Change Password</Button>
                </div>
            </div>}
        </div>

        <NavBottom />
    </div>)
}