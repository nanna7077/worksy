import { Avatar, Button, Input, LinearProgress } from "@mui/joy";
import NavBottom from "./Nav";
import { useEffect, useState } from "react";

export default function Messages() {
    const [showLoader, setShowLoader] = useState(false);
    const [showSidebar, setShowSidebar] = useState(true);
    const [user, setUser] = useState(null);
    const [messages, setMessages] = useState([]);
    const [conversations, setConversations] = useState([]);
    const [currentConversation, setCurrentConversation] = useState(null);
    const [currentMessage, setCurrentMessage] = useState("");

    useEffect(() => {
        setShowLoader(true);
        fetch(process.env.REACT_APP_API_URL + "/accounts/view/self", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            setShowLoader(false);
            if (data.error != undefined) {
                return;
            }
            setUser(data.account);
        });

        setShowLoader(true);
        fetch(process.env.REACT_APP_API_URL + "/messages/view/conversations", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            setShowLoader(false);
            if (data.error != undefined) {
                return;
            }
            setConversations(data.conversations);
        });

        if (window.location.href.split("/").length == 5) {
            setShowLoader(true);
            fetch(process.env.REACT_APP_API_URL + "/messages/create/conversation/new", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
                },
                body: JSON.stringify({
                    receiver_id: window.location.href.split("/").at(-1).split("?")[0],
                }),
            })
            .then((response) => response.json())
            .then((data) => {
                setShowLoader(false);
                if (data.error != undefined) {
                    return;
                }
                setCurrentConversation(data.conversation);
            });
        }
        
    }, [])

    useEffect(() => {
        if (!currentConversation) return;

        setShowLoader(true);
        fetch(process.env.REACT_APP_API_URL + "/messages/view/conversations/" + currentConversation.id + "/messages", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            setShowLoader(false);
            if (data.error != undefined) {
                return;
            }
            setMessages(data.messages);
        });
    }, [currentConversation])

    function searchUser(value) {
        value = value.replace(/\s/g, "");
        if (!value || value.length == 0) return;
        var conversations_ = [];
        for (let i = 0; i < conversations.length; i++) {
            try {
                if (conversations[i].sender.username.contains(value)) {
                    conversations_.push(conversations[i]);
                }
            } catch { continue; }
        }
        if (conversations_.length != 0) setConversations(conversations_);

        setShowLoader(true);
        fetch(process.env.REACT_APP_API_URL + "/messages/view/conversations/search/" + value, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
        })
        .then((response) => response.json())
        .then((data) => {
            setShowLoader(false);
            if (data.error != undefined) {
                return;
            }
            if (data.conversations.length != 0) {setConversations(data.conversations); return;}

            setShowLoader(true);
            fetch(process.env.REACT_APP_API_URL + "/messages/create/conversation/new", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
                },
                body: JSON.stringify({
                    receiver_username: value
                }),
            })
            .then((response) => response.json())
            .then((data) => {
                setShowLoader(false);
                if (data.error != undefined) {
                    return;
                }
                if (!data.conversation) {setConversations([]); return;}
                setConversations([data.conversation]);
            });

        });
        
    }

    function openChat(conversation) {
        setCurrentConversation(conversation);
    }

    function sendMessage() {
        if (!currentConversation) return;

        setShowLoader(true);
        fetch(process.env.REACT_APP_API_URL + `/messages/create/conversation/${currentConversation.id}/new`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
            body: JSON.stringify({
                content: currentMessage,
                receiverAccountId: currentConversation.id
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            setShowLoader(false);
            if (data.error != undefined) {
                return;
            }
            setMessages([data.message, ...messages]);
            setCurrentMessage("");
        });
    }

    return (
        <div className="p-2">
            {showLoader && <LinearProgress />}
            {user && <div className="flex w-full h-[89vh]">
                <img src="icons/hamburger-menu.svg" className={"w-6 h-6 fixed top-3 z-10" + (showSidebar ? " md:hidden" : "")} onClick={() => {setShowSidebar(!showSidebar)}} />
                {showSidebar && <div className="flex flex-col h-full w-full gap-2 md:w-[20vw] overflow-x-scroll cursor-pointer">
                    <div className="flex gap-1 items-center justify-center">
                        {showSidebar && <Input placeholder="Search User" onChange={(e) => {searchUser(e.target.value)}} />}
                    </div>
                    {conversations.map((conversation, ci) => (
                    <div className="h-[8%] w-full bg-gray-200 flex gap-2 p-2 items-center" key={ci} onClick={() => {openChat(conversation)}}>
                        <Avatar variant="solid" src={conversation.receiver.id == user.id ? conversation.sender.profile_picture : conversation.receiver.profile_picture} color="primary">{conversation.receiver.id == user.id ? conversation.sender.username : conversation.receiver.username}</Avatar>
                        <div className="flex justify-between items-center w-full">
                            <div className="text-base">{conversation.receiver.id == user.id ? conversation.sender.username : conversation.receiver.username}</div>
                            {/* {(conversation.messageCount != undefined) && <div className="text-sm rounded-full font-semibold px-2">{conversation.messageCount}</div>} */}
                        </div>
                    </div>))}
                    {conversations.length == 0 && <div className="h-[8%] w-full bg-gray-200 flex gap-2 p-2 items-center">
                        <div className="text-base w-full text-center">
                            No conversations yet.<br/>
                            <span className="text-sm">Search for a user.</span>
                        </div>
                    </div>}
                </div>}
                <div className={"h-full w-full md:w-[80vw] m-2 md:block" + (showSidebar ? " hidden" : "")}>
                    <div className="h-[7%] mb-2 bg-slate-200 p-2 flex items-center">
                        <h1 className="text-xl font-semibold">{currentConversation ? <div className="flex items-center gap-2" onClick={() => {window.location.href = "/profile/" + (currentConversation.receiver.id == user.id ? currentConversation.sender.id : currentConversation.receiver.id)}}><Avatar variant="solid" src={currentConversation.receiver.id == user.id ? currentConversation.sender.profile_picture : currentConversation.receiver.profile_picture} color="primary">{currentConversation.receiver.id == user.id ? currentConversation.sender.username : currentConversation.receiver.username}</Avatar><div className="text-lg">{currentConversation.receiver.id == user.id ? currentConversation.sender.username : currentConversation.receiver.username}</div></div> : "Messages"}</h1>
                    </div>
                    {currentConversation && <div className="h-[85%] sticky bottom-0 bg-slate-200 flex flex-col-reverse overflow-y-scroll gap-3 p-4 mb-3">
                        {messages.map((message, index) => (
                            <div key={index} className={"flex flex-col items-end"  + (message.sender_id == user.id ? " self-end" : "self-start")}>
                                <div className="w-fit h-fit rounded-sm p-2 bg-slate-400 text-base">
                                    {message.content}
                                </div>
                                <div className="text-xs">{message.created_at}</div>
                            </div>
                        ))}
                    </div>}
                    {!currentConversation && <div className="h-[85%] sticky bottom-0 bg-slate-200 flex overflow-y-scroll gap-3 items-center justify-center p-4 mb-3">
                        <div className="w-fit h-fit rounded-sm p-6 bg-slate-300 text-base font-semibold">
                            Select a conversation
                        </div>
                    </div>}
                    {currentConversation && <div className="flex gap-2">
                        <Input variant="soft" placeholder="Type a message..." className="w-full" value={currentMessage} onChange={(e) => {setCurrentMessage(e.target.value)}} />
                        <Button onClick={() => {sendMessage()}}>Send</Button>
                    </div>}
                </div>
            </div>}

            <NavBottom />
        </div>
    )
}