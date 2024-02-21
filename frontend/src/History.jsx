import Input from "@mui/joy/Input";
import Button from "@mui/joy/Button";
import { useEffect, useState } from "react";
import NavBottom from "./Nav";

export default function History() {
    const [reload, setReload] = useState(true);
    const [user, setUser] = useState(null);
    const [selfpostedJobs, setSelfpostedJobs] = useState([]);
    const [applications, setApplications] = useState([]);
    const [applicationLastOffset, setApplicationLastOffset] = useState(0);
    const [previousJobs, setPreviousJobs] = useState([]);
    const [previousJobsLastOffset, setPreviousJobsLastOffset] = useState(0);

    function loadPreviousJobs() {
        fetch(process.env.REACT_APP_API_URL + `/jobs/view/history/previous_jobs?offset=${previousJobsLastOffset}&limit=10`, {
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
            if (!previousJobs) {
                setPreviousJobs(data.prevJobs);
            } else { setPreviousJobs(previousJobs.concat(data.prevJobs)); }
            setPreviousJobsLastOffset(previousJobsLastOffset + 10);
        });
    }

    function loadApplications() {
        fetch(process.env.REACT_APP_API_URL + `/jobs/view/history/applications?offset=${applicationLastOffset}&limit=10`, {
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
            if (!applications) {
                setApplications(data.applications);
            } else { setApplications(applications.concat(data.applications)); }
            setApplicationLastOffset(applicationLastOffset + 10);
        });
    }

    function markComplete(jobId) {
        var rating = prompt("Please enter a rating between 1 and 5");

        if (rating == null || rating == "" || rating > 5 || rating < 1) {
            return;
        }

        fetch(process.env.REACT_APP_API_URL + `/jobs/update/${jobId}/markComplete`, {
            method: 'PUT',
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
            body: JSON.stringify({ rating: rating }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                alert(data.error);
                return;
            }
            window.location.reload();
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
                return;
            }
            setUser(data.account);
        });

        fetch(process.env.REACT_APP_API_URL + "/jobs/view/selfposted/list/all", {
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
            setSelfpostedJobs(data.jobs);
        });
        setReload(false);

        loadPreviousJobs();
        loadApplications();

    }, [reload])

    return (
        <div className="">
            {
                user &&
                
                <div className="flex h-full justify-center items-center">

                    <div className="w-full p-8">
                        <div className="font-bold">Previous Work</div>
                        {previousJobs.length == 0 &&
                            <div className="text-center">
                                No previous work
                            </div>
                        }

                        {previousJobs.map((job, jid) => (
                            <div className="mt-4 mb-8 flex flex-col gap-4 max-h-[30vh] overflow-y-auto" key={jid}>
                                <div className="cursor-pointer bg-[rgba(255,255,255,.5)] shadow-md items-center p-4 rounded-lg">
                                    <div className="flex justify-between w-full">
                                        <div className="text-lg">
                                            <div>{job.job.address}</div>
                                            <div className="text-xs">Posted By {job.poster.fullname}</div>
                                        </div>
                                        <Button size="sm" variant="outlined">{job.status}</Button>
                                    </div>
                                    <div className="flex gap-2 items-center flex-col md:flex-row mt-2 mb-2">
                                        <div className="text-xs">
                                            Started At: {job.created_at}
                                        </div>
                                        { (job.finished_at != null) && <div className="text-xs">
                                            Finished At: {job.finished_at}
                                        </div>}
                                        { (job.duration != null) && <div className="text-xs">
                                            Duration: {job.duration} Hours
                                        </div>}
                                    </div>
                                    <div className="w-full flex gap-4 text-sm flex-col items-center md:flex-row">
                                        <div className="flex gap-1 mt-1 items-center">
                                            <div className="flex items-center gap-1">
                                                Worker <img src="/icons/star.svg" className="w-6 h-6" />
                                            </div>
                                            <div className="flex items-center gap-1 font-base">
                                                <Input value={job.worker_rating} type="number" size="sm" onChange={(e)=>{
                                                    if (!(e.target.value > 5 || e.target.value < 1)) {
                                                        fetch(process.env.REACT_APP_API_URL + `/jobs/update/${job.id}/workerRating`, {
                                                            method: 'PUT',
                                                            headers: {
                                                                "Content-Type": "application/json",
                                                                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
                                                            },
                                                            body: JSON.stringify({ rating: e.target.value}),
                                                        })
                                                        .then((response) => response.json())
                                                        .then((data) => {
                                                            if (data.error != undefined) {
                                                                alert(data.error);
                                                                return;
                                                            }
                                                            window.location.reload();
                                                        });
                                                    }
                                                }} /> / 5
                                            </div>
                                        </div>
                                        <div className="flex gap-1 mt-1">
                                            <div className="font-semibold">
                                                {job.currency}
                                            </div>
                                            <div>
                                                {job.amount}
                                            </div>
                                        </div>
                                        {job.status == "started" &&
                                            <Button size="sm" variant="outlined" onClick={() => markComplete(job.id)}>Mark Completed</Button>
                                        }
                                    </div>
                                </div>
                            </div>
                        ))}


                        <div className="font-bold">Applications</div>
                        {applications.length == 0 &&
                            <div className="text-center">
                                You have not applied for any job yet
                            </div>
                        }

                        {applications.map((appl, aid) => (
                        <div className="mt-4 mb-8 flex flex-col gap-4 max-h-[30vh] overflow-y-auto" key={aid}>
                            <div className="cursor-pointer bg-[rgba(255,255,255,.5)] shadow-md items-center p-4 rounded-lg">
                                <div className="flex justify-between w-full">
                                    <div className="text-lg">
                                        {appl.job.address}
                                    </div>
                                    <div className="flex gap-2 items-center">
                                        <div className="text-xs">
                                            Applied On: {appl.created_at}
                                        </div>
                                        <Button size="sm" variant="outlined">{appl.status}</Button>
                                    </div>
                                </div>
                                <div className="w-full flex gap-4 text-sm flex-col items-center md:flex-row">
                                    <div className="flex gap-1 mt-1">
                                        <img className="w-5" src="/icons/clock-circle.svg"/>
                                        <div>
                                            {appl.job.duration_range_start} - 
                                            {appl.job.duration_range_end} {appl.job.duration_range_unit}
                                        </div>
                                    </div>
                                    <div className="flex gap-1 mt-1">
                                        <div className="font-semibold">
                                            Quoted Amount {appl.job.currency}
                                        </div>
                                        {appl.quoted_amount}
                                    </div>
                                    <div className="flex gap-1 mt-1">
                                        <div className="font-semibold">
                                            {appl.job.currency}
                                        </div>
                                        <div>
                                            {appl.job.price_range_start} - 
                                            {appl.job.price_range_end}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>))}
                        
                        <div className="font-bold">Previous Postings</div>
                            {selfpostedJobs.length == 0 &&
                                <div className="text-center">
                                    You have not posted any job yet
                                </div>
                            }

                        <div className="mt-4 mb-8 flex flex-col gap-4 max-h-[30vh] overflow-y-auto">

                            {selfpostedJobs.map((job, jid) => (
                                <div className="cursor-pointer bg-[rgba(255,255,255,.5)] shadow-md items-center p-4 rounded-lg" key={jid} onClick={()=>{window.location.href="/job/"+job.id}}>
                                    <div className="flex justify-between w-full">
                                        <div className="text-lg">
                                            {job.address}
                                        </div>
                                        <div className="text-xs">
                                            {job.created_at}
                                        </div>
                                    </div>
                                    <div className="w-full flex gap-4 text-sm">
                                        <div className="flex gap-1 mt-1">
                                            <img className="w-5" src="/icons/clock-circle.svg"/>
                                            <div>
                                                {job.duration_range_start} - 
                                                {job.duration_range_end} {job.duration_range_unit}
                                            </div>
                                        </div>
                                        <div className="flex gap-1 mt-1">
                                            <div className="font-semibold">
                                                {job.currency}
                                            </div>
                                            <div>
                                                {job.price_range_start} - 
                                                {job.price_range_end}
                                            </div>
                                        </div>
                                    </div>
                                    {job.tags.map((tag, tid) => 
                                        (<div className="w-full flex flex-wrap mt-3">
                                            <div className="w-fit bg-[rgba(0,0,0,0.1)] text-xs p-1 flex gap-2 justify-center align-center">
                                                {tag.name}
                                            </div>
                                        </div>)
                                    )}
                                </div>)
                            )
                            }

                        </div>
                    </div>

                    <NavBottom />
                </div>
            }
        </div>
    )
}