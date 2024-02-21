import { useEffect, useState } from "react";
import LinearProgress from '@mui/joy/LinearProgress';

export default function NavBottom() {
    const [refresh, setRefresh] = useState(false);
    const [user, setUser] = useState(null);
    const [notificationCount, setNotificationCount] = useState(0);

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
                return;
            }
            console.log(data.user)
            setUser(data.account);
        });

        fetch(process.env.REACT_APP_API_URL + "/notifications/view/count", {
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
            setNotificationCount(data.count);
        });
    }, [refresh])

    function toggleSelfVisibility() {
        fetch(`${process.env.REACT_APP_API_URL}/accounts/update/visibility/${user.is_available ? 0 : 1}`, {
            method: "PUT",
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
            setUser(data.account);
            setRefresh(!refresh);
        });
    }

    return (
        <>
            {user ? 
            <div className="w-full h-16 border-gray-200 flex items-center justify-evenly fixed bottom-0 bg-[rgba(255,255,255,0.8)] text-xs">
                {user.is_available ? 
                <div className="flex items-center flex-col bg-[rgba(255,255,255,0.2)] cursor-pointer" onClick={toggleSelfVisibility}>
                    <img className="h-8" src="/icons/eye-scan.svg" />
                    Visible
                </div> :
                <div className="flex items-center flex-col bg-[rgba(255,255,255,0.2)] cursor-pointer" onClick={toggleSelfVisibility}>
                    <img className="h-8" src="/icons/eye-closed.svg" />
                    Invisible
                </div>
                }

                <div className="flex items-center flex-col bg-[rgba(255,255,255,0.2)] cursor-pointer" onClick={()=>{window.location.href="/"}}>
                    <img className="h-8" src="/icons/point-on-map.svg" />
                    View Map
                </div>
                
                <div className="flex items-center flex-col bg-[rgba(255,255,255,0.2)] cursor-pointer" onClick={()=>{window.location.href="/history"}}>
                    <img className="h-8" src="/icons/history.svg" />
                    History
                </div>

                <div className="flex items-center flex-col bg-[rgba(255,255,255,0.2)] cursor-pointer" onClick={()=>{window.location.href="/jobs/create"}}>
                    <img className="h-8" src="/icons/add-square.svg" />
                    Create Job
                </div>

                <div className="flex items-center flex-col bg-[rgba(255,255,255,0.2)] cursor-pointer" onClick={()=>{window.location.href="/notifications"}}>
                    <img className="h-8" src="/icons/bell.svg" />
                    Notifications
                    {(notificationCount>0) && <div className="text-xs">{notificationCount} New Notification</div>}
                </div>

                <div className="flex items-center flex-col bg-[rgba(255,255,255,0.2)] cursor-pointer" onClick={()=>{window.location.href="/messages"}}>
                    <img className="h-8" src="/icons/chat-unread.svg" />
                    Messages
                </div>

                <div className="flex items-center flex-col bg-[rgba(255,255,255,0.2)] cursor-pointer" onClick={()=>{window.location.href="/profile/" + user.id;}}>
                    <img className="h-8" src="/icons/user-circle.svg" />
                    Profile
                </div>
            </div> :
            <LinearProgress />
            }
        </>
    )
}