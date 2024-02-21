import { useEffect, useState } from "react";
import NavBottom from "./Nav";
import { Avatar, Button, Card, CardContent, DialogTitle, Modal, ModalDialog } from "@mui/joy";
import { secondsToTime } from "./common";

export default function Job() {
    const jobID = window.location.pathname.split("/")[2];
    const [job, setJob] = useState(null);
    const [user, setUser] = useState(null);
    const [applications, setApplications] = useState([]);

    const [showShareJobModal, setShowShareJobModal] = useState(false);

    useEffect(() => {
        fetch(process.env.REACT_APP_API_URL + "/jobs/view/" + jobID, {
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
            setJob(data.job);
        });

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
            setUser(data.account);
        });
    }, []);

    useEffect(()=>{
        if (!user || !job) return;
        if (user.username == job.created_by) {
            fetch(process.env.REACT_APP_API_URL + "/jobs/view/" + jobID + "/applications", {
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
                setApplications(data.applications);
            });
        }
    }, [user, job]);

    function applyToJob() {
        const quoted_amount = prompt("Enter quoted price for the job?");
        fetch(process.env.REACT_APP_API_URL + "/jobs/create/apply?jobId=" + jobID + "&quoted_amount=" + quoted_amount, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            }
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                alert(data.error);
                return;
            }
            alert("Applied to job");
        });
    }

    function markApplicationStatus(applicationId, status) {
        fetch(process.env.REACT_APP_API_URL + `/jobs/update/${jobID}/applications/${applicationId}/application_status`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
            body: JSON.stringify({ status: status }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                alert(data.error);
                return;
            }
            alert("Changed status to " + status);
        });
    }

    function setApplicantHired(workerUserId) {
        fetch(process.env.REACT_APP_API_URL + `/jobs/update/${jobID}/applications/${workerUserId}/hired`, {
            method: "PUT",
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
            alert("Hired");
        });
    }

    return (
        <div className="">
            <Modal open={showShareJobModal} onClose={() => {setShowShareJobModal(false);}}>
                <ModalDialog className="overflow-y-auto">
                    <DialogTitle>Share Job</DialogTitle>
                    <div className='flex gap-2 flex-wrap justify-evenly'>
                        <Button size="sm" className="cursor-pointer" onClick={() => {navigator.clipboard.writeText(window.location.href); setShowShareJobModal(false);}}>Copy Link</Button>
                        <Button size="sm" className="cursor-pointer" onClick={() => {if (!navigator.share) { alert("Share not supported"); return; } navigator.share({url: window.location.href}); setShowShareJobModal(false);}}>Share</Button>
                        <Button size="sm" variant="outlined" className="cursor-pointer" onClick={() => {setShowShareJobModal(false);}}>Cancel</Button>
                    </div>

                </ModalDialog>
            </Modal>
            {job && <div className="p-2">
                <div className="p-3">
                    <div className="text-2xl font-semibold">
                        {job.address}
                    </div>
                    <div className="flex gap-2 flex-wrap mt-2">
                        {job.tags.map((tag) => (
                            <div className="bg-gray-200 rounded-full px-3 py-1 text-sm">
                                {tag.name}
                            </div> 
                        ))}
                    </div>
                    <div className="flex gap-6 flex-wrap mt-2">
                        <div className="flex gap-1">
                            <img src="/icons/clock-circle.svg" className="w-5 h-5" />
                            {job.duration_range_start} - {job.duration_range_end} {job.duration_range_unit}
                        </div>
                        <div className="flex gap-1">
                            {job.currency} {job.price_range_start} - {job.price_range_end}
                        </div>
                        <div className="flex gap-1">
                            <img src="/icons/star.svg" className="w-4 h-4" />
                            <div>
                                {job.rating} / 5
                            </div>
                        </div>
                        <div>
                            Posted {secondsToTime(job.ago)} ago
                        </div>
                    </div>
                    {/* <embed className='m-2 h-[40vh] w-full' src={`https://www.google.com/maps/embed/v1/view?key=${process.env.REACT_APP_MAP_API_KEY}&center=${job.lat},${job.long}&zoom=15&maptype=satellite`} /> */}
                    <embed className="m-2 h-[40vh] w-full" src={`https://www.google.com/maps/embed/v1/place?key=${process.env.REACT_APP_MAP_API_KEY}&q=${job.address}`} />
                    <div className="mt-2 p-4">
                        {job.description}
                        {user && user.username == job.created_by &&
                            <>
                                <div className="font-semibold m-1">Job Applications</div>
                                <div className="mt-6 flex flex-col gap-2">
                                    {applications.map( (application, aid) => (
                                    <Card variant="outlined" className="cursor-pointer w-full" key={aid}>
                                        <CardContent className="text-xs">
                                            <div className="flex w-full justify-between items-center">
                                                <div className="flex gap-1 items-center" onClick={() => {window.location.href = `/profile/${application.applicant.id}`}}>
                                                    <Avatar src={application.applicant.profile_picture} sx={{ width: 30, height: 30 }}>{application.applicant.username}</Avatar>
                                                    {application.applicant.username}
                                                </div>
                                                <div className="flex gap-2 items-center">
                                                    <Button onClick={() => {markApplicationStatus(application.id, "shortlisted")}} color="warning" size="sm" variant="outlined">Shortlist</Button>
                                                    <Button onClick={() => {markApplicationStatus(application.id, "rejected")}} color="error" size="sm" variant="outlined">Reject</Button>
                                                    <Button onClick={() => {markApplicationStatus(application.id, "hired"); setApplicantHired(application.applicant.id)}} color="success" size="sm" variant="outlined">Hire</Button>
                                                </div>
                                                <div className="flex gap-2">
                                                    <Button onClick={() => {window.location.href = `/message/${application.applicant.id}?fromjob=${job.id}&role=poster_application_contact"`}} variant="outlined">Message</Button>
                                                    <Button>{application.status}</Button>
                                                </div>
                                            </div>
                                            <>
                                                Applied on {application.created_at} ({secondsToTime(application.ago / 60 / 60)} ago)
                                                <br />
                                                <div className="text-sm"><span className="font-semibold">Quoted Amount {job.currency}</span> {application.quoted_amount}</div>
                                            </>
                                        </CardContent>
                                    </Card>) )}
                                </div>
                            </>
                        }
                        {user && user.username != job.created_by && user.open_to_work &&
                            <div className="mt-6 flex flex-col gap-2">
                                <Button onClick={() => { applyToJob() }} className="w-full">Apply</Button>
                                <Button onClick={() => window.location.href = `/message/${job.created_by}?fromjob=${job.id}&role=applicant"`} variant="solid" className="w-full">Message</Button>
                            </div>
                        }
                        <div className="mt-6 flex flex-col gap-2">
                            <Button onClick={() => {setShowShareJobModal(true)}} variant="outlined" className="w-full">Share</Button>
                        </div>
                    </div>
                </div>
            </div>}

            <NavBottom />
        </div>
    )
}