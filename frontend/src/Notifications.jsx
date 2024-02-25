import { useState } from "react";
import NavBottom from "./Nav";
import { useEffect } from "react";
import { secondsToTime } from "./common";

export default function Notifications() {

    const [user, setUser] = useState(null);
    const [readNotifications, setReadNotifications] = useState([]);
    const [readNotificationsLastOffset, setReadNotificationsLastOffset] = useState(0);
    const [unreadNotifications, setUnreadNotifications] = useState([]);
    const [unreadNotificationsLastOffset, setUnreadNotificationsLastOffset] = useState(0);

    function read_notifications() {
        fetch(process.env.REACT_APP_API_URL + `/notifications/view/read?offset=${readNotificationsLastOffset}&limit=10`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                alert(data.error);
                return;
            }
            if (!readNotifications) {
                setReadNotifications(data.notifications);
            } else { setReadNotifications(readNotifications.concat(data.notifications)); }
            setReadNotificationsLastOffset(readNotificationsLastOffset + 10);
        });
    }

    function unread_notificatons() {
        fetch(process.env.REACT_APP_API_URL + `/notifications/view/unread?offset=${unreadNotificationsLastOffset}&limit=10`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                alert(data.error);
                return;
            }
            if (!unreadNotifications) {
                setUnreadNotifications(data.notifications);
            } else { setUnreadNotifications(unreadNotifications.concat(data.notifications)); }
            setUnreadNotificationsLastOffset(unreadNotificationsLastOffset + 10);
        });
    }

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
                alert(data.error);
                return;
            }
            setUser(data.user);

            read_notifications();
            unread_notificatons();
        });

    }, []);

    return (
        <div className="p-2">
            <h1 className="font-semibold text-lg">Notifications</h1>

            <div className="flex flex-col gap-4 items-center">
                <p>No notifications yet.</p>

                <div className="mt-4 mb-8 flex flex-col gap-4 max-h-[50vh] overflow-y-auto w-full p-2">
                {readNotifications.map((notification, nid) => (
                    <div className="cursor-pointer bg-[rgba(255,255,255,.5)] shadow-md items-center p-4 rounded-lg w-full" key={nid}>
                        <div className="flex justify-between w-full">
                            <div className="text-lg">
                                {notification.message}
                            </div>

                            <div className="text-sm">
                                {secondsToTime(notification.ago)} ago ({notification.created_at})
                            </div>
                        </div>
                    </div>
                ))}
                </div>
            </div>

            <h1 className="font-semibold text-lg">Previous Notifications</h1>

            <div className="flex flex-col gap-4 items-center">
                <p>No notifications yet.</p>

                <div className="mt-4 mb-8 flex flex-col gap-4 max-h-[50vh] overflow-y-auto w-full p-2">
                    {unreadNotifications.map((notification, nid) => (
                    <div className="cursor-pointer bg-[rgba(255,255,255,.3)] shadow-md items-center p-4 rounded-lg w-full" key={nid}>
                        <div className="flex justify-between w-full">
                            <div className="text-lg">
                                {notification.message}
                            </div>

                            <div className="text-sm">
                                {secondsToTime(notification.ago)} ago ({notification.created_at})
                            </div>
                        </div>
                    </div>))}
                </div>
            </div>

            <NavBottom />
        </div>
    );
}