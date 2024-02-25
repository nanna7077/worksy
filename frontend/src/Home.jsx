import GoogleMapReact from 'google-map-react';
import Button from "@mui/joy/Button";
import { Modal, ModalDialog, DialogTitle, Card, CardContent, Slider, Input, Box } from "@mui/joy";
import { useEffect, useState } from "react";
import NavBottom from "./Nav";
import LinearProgress from '@mui/joy/LinearProgress';
import { secondsToTime } from './common';

export default function Home() {
    const [isLoading, setIsLoading] = useState(false);
    const [user, setUser] = useState(null);
    const [mapsDefaultProps, setMapsDefaultProps] = useState(null)
    const [mapsCurrentBounds, setMapsCurrentBounds] = useState(null);
    const [mapVal, setMapVal] = useState([null, null]);
    const [currentMarkers, setCurrentMarkers] = useState([]);
    const [currentViewJobs, setCurrentViewJobs] = useState([]);

    const [showMoreJobsModal, setShowMoreJobsModal] = useState(false);
    const [showMoreJobsModal_radius, setShowMoreJobsModal_radius] = useState(5); // KiloMeters
    const [showMoreJobsModal_jobs, setShowMoreJobsModal_jobs] = useState([]);

    const [showSearchResults, setShowSearchResults] = useState(false);
    const [showSearchResults_search, setShowSearchResults_search] = useState("");
    const [showSearchResults_jobs, setShowSearchResults_jobs] = useState([]);
    const [showSearchResults_workers, setShowSearchResults_workers] = useState([]);

    const [showSpeakWithWorksyModal, setShowSpeakWithWorksyModal] = useState(false);
    const [showSpeakWithWorksyModal_messages, setShowSpeakWithWorksyModal_messages] = useState([]);
    const [showSpeakWithWorksyModal_messagefield, setShowSpeakWithWorksyModal_messagefield] = useState("");
    const [showSpeakWithWorksyModal_context, setShowSpeakWithWorksyModal_context] = useState(null);

    useEffect(() => {
        navigator.geolocation.getCurrentPosition((position) => {
            setMapsDefaultProps(
                {
                center: {
                    lat: 11.96181368, lng: 79.207205
                },
                zoom: 11
                }
            )
            // setMapsDefaultProps(
            //     { center: {
            //         lat: position.coords.latitude, lng: position.coords.longitude
            //     },
            //     zoom: 11
            //     }
            // );
        });
    }, [])

    useEffect(() => {
        if (!mapsDefaultProps) {
            fetch(process.env.REACT_APP_API_URL + `/accounts/view/self`, {
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
                    if (data.error == "Unauthorized") {
                        window.location.href = "/login";
                    }
                    return;
                }
                setUser(data.account);
            });    
            ; return};
        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + `/accounts/view/self?lat=${mapsDefaultProps.center.lat}&long=${mapsDefaultProps.center.lng}`, {
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
    }, [mapsDefaultProps]);

    function renderMapContent(){
        const [maps, map] = mapVal;
        if (maps == null) return;
        
        for (const m in currentMarkers) {
            currentMarkers[m].setMap(null);
        }

        var markers = [];
        
        markers.push(new maps.Marker({
            position: {
                lat: mapsDefaultProps.center.lat,
                lng: mapsDefaultProps.center.lng
            },
            map,
            title: 'You'
        }))

        for (const m in currentViewJobs) {
            var newmarker = new maps.Marker({
                position: {
                    lat: currentViewJobs[m].lat,
                    lng: currentViewJobs[m].long
                },
                map,
                title: `Posted ${secondsToTime(currentViewJobs[m].ago)} ago\nEst. Duration: ${currentViewJobs[m].duration_range_start} - ${currentViewJobs[m].duration_range_end} ${currentViewJobs[m].duration_range_unit}\n${currentViewJobs[m].currency} ${currentViewJobs[m].price_range_start}-${currentViewJobs[m].price_range_end}`,
            })
            newmarker.addListener('click', function() {
                showJobPreview(currentViewJobs[m].id);
            });
            markers.push(newmarker)
        }

        setCurrentMarkers(markers);
    }

    useEffect(() => {
        if (!mapsDefaultProps || !mapsCurrentBounds) {return};

        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + "/jobs/view/list/by/boundary", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
            body: JSON.stringify({"mapsCurrentBounds": mapsCurrentBounds}),
        })
        .then((response) => response.json())
        .then((data) => {
            setIsLoading(false);
            if (data.error != undefined) {
                return;
            }
            setCurrentViewJobs(data.jobs);
        });
        renderMapContent();
    }, [mapVal, mapsCurrentBounds])

    useEffect(() => {
        if (!mapsDefaultProps) return;
        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + `/jobs/view/list/by/radius?radius=${showMoreJobsModal_radius}&lat=${mapsDefaultProps.center.lat}&long=${mapsDefaultProps.center.lng}`, {
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
            setShowMoreJobsModal_jobs(data.jobs);
        });
    }, [showMoreJobsModal, showMoreJobsModal_radius])
    
    useEffect(() => {
        if (!mapsDefaultProps) return;
        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + `/search/jobs?query=${showSearchResults_search}&lat=${mapsDefaultProps.center.lat}&long=${mapsDefaultProps.center.lng}`, {
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
            setShowSearchResults_jobs(data.jobs);
        });

        fetch(process.env.REACT_APP_API_URL + `/search/workers?query=${showSearchResults_search}&lat=${mapsDefaultProps.center.lat}&long=${mapsDefaultProps.center.lng}`, {
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
            setShowSearchResults_workers(data.workers);
        });
    }, [showSearchResults, showSearchResults_search])

    function showJobPreview(jobID) {
        // Show a modal with the job details
        window.location.href='/job/' + jobID;
    }

    function showSpeakWithWorksyModal_sendToWorksyAI() {
        setIsLoading(true);
        fetch(process.env.REACT_APP_API_URL + (showSpeakWithWorksyModal_context ? `/genai/conversation?question=${showSpeakWithWorksyModal_messagefield}&context=${showSpeakWithWorksyModal_context}` : `/genai/conversation?question=${showSpeakWithWorksyModal_messagefield}`), {
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
            const usrMsg = {"content": `${showSpeakWithWorksyModal_messagefield}`, role: "user", "createdOn": (new Date()).toISOString()};
            const botMsg = {"content": data.response, role: "assistant", "createdOn": (new Date()).toISOString()}
            setShowSpeakWithWorksyModal_messages([usrMsg, ...showSpeakWithWorksyModal_messages]);
            setShowSpeakWithWorksyModal_messages([botMsg, ...showSpeakWithWorksyModal_messages]);
            setShowSpeakWithWorksyModal_messagefield("");
            setShowSpeakWithWorksyModal_context(data.context);
        });
    }

    return (
        <div className="">
            <Modal open={showMoreJobsModal} onClose={() => {setShowMoreJobsModal(false);}}>
                <ModalDialog className="overflow-y-auto">
                    <DialogTitle>Jobs around you</DialogTitle>
                    <div className='flex gap-3 text-xs items-center'>
                        <b>Radius</b>
                        <Slider defaultValue={showMoreJobsModal_radius} min={1} max={500} step={1} onChange={(e) => {setShowMoreJobsModal_radius(e.target.value)}} />
                        <div>
                            {showMoreJobsModal_radius} Kilometers
                        </div>
                    </div>
                    <div className='flex gap-2 flex-wrap justify-evenly'>
                        {showMoreJobsModal_jobs.map((job, jid) => (   
                            <Card key={jid} variant="outlined" className="w-fit cursor-pointer" onClick={() => showJobPreview(job.id)}>
                                <CardContent className="text-xs">
                                    <span className='w-[200px] text-sm'>{job.address}</span>
                                    <br/>
                                    {job.currency} {job.price_range_start} - {job.price_range_end}<br/>
                                    Est. Duration {job.duration_range_start} - {job.duration_range_end} {job.duration_range_unit}<br/>
                                    Posted {secondsToTime(job.ago)} ago
                                </CardContent>
                            </Card>
                        ))}
                    </div>

                </ModalDialog>
            </Modal>
            <Modal open={showSearchResults} onClose={() => setShowSearchResults(false)}>
                <ModalDialog className="overflow-y-auto w-[100vw] h-[100vh]">
                    <Input placeholder="Search for Jobs, Workers and more" onKeyDown={(e) => {setShowSearchResults_search(e.target.value)}} />
                    <Box className='m-1 backdrop-blur-sm rounded-sm p-1 border-black flex flex-col gap-1 max-h-[400px] overflow-y-auto cursor-pointer'>
                        <div className='flex justify-between'>
                            <span className='text-md font-bold'>Jobs</span>
                        </div>
                        <div className='flex flex-col gap-1 max-h-[40vh] overflow-y-auto'>
                            {showSearchResults_jobs.length == 0 ? <div>No Jobs Found</div> : null}
                            {showSearchResults_jobs.map((job, jid) =>(
                            <Box className='bg-[rgba(235,243,255,.8)] m-1 p-1 rounded-sm text-sm flex flex-col gap-2' onClick={() => showJobPreview(job.id)} key={jid}>
                                <div className='flex justify-between gap-2 items-center max-md:flex-col'>
                                    <div className='text-base'>{job.address}</div>
                                    <div className='text-xs'>{job.created_at} ({secondsToTime(job.ago)} ago)</div>
                                </div>
                                <div className='flex gap-2 items-center text-xs flex-wrap'>
                                    <div className='flex gap-1'>
                                        <img src='/icons/clock-circle.svg' className='w-4 h-4'/>
                                        {job.duration_range_start} - {job.duration_range_end} {job.duration_range_unit}
                                    </div>
                                    <div className='flex gap-1'>
                                        {job.currency} {job.price_range_start} - {job.price_range_end}
                                    </div>
                                    <div className='flex gap-1'>
                                        <img src="/icons/star.svg" className="w-4 h-4" />
                                        <div>
                                            {job.rating} / 5
                                        </div>
                                    </div>
                                    <div className='flex gap-1 flex-wrap'>
                                        {job.tags.map((tag, tagid) => (
                                            <div className="w-fit bg-[rgba(0,0,0,0.1)] text-xs p-1 flex gap-2 justify-center align-center rounded-base" key={tagid}>
                                                {tag.name}
                                            </div>
                                        ))}
                                    </div>
                                </div>
                            </Box>))}
                            
                        </div>

                        <br />

                        <span className='text-md font-bold'>Available Workers</span>
                        <div className='flex flex-col gap-1 max-h-[40vh] overflow-y-auto'>
                            {showSearchResults_workers.length == 0 ? <div>No Workers Found</div> : null}
                            {showSearchResults_workers.map((worker, wid) => (
                                <Box className='bg-[rgba(235,243,255,.8)] m-1 p-1 rounded-sm text-sm flex flex-col gap-1' key={wid} onClick={() => {window.location.href = "/profile/1"}}>
                                <div className='flex justify-between items-center'>
                                    <div className='text-base'>{worker.fullname}</div>
                                </div>
                                <div className='flex gap-2 items-center text-xs'>
                                    <div className='flex gap-1'>
                                        Average Rate {worker.price_average}
                                    </div>
                                    <div className='flex gap-1'>
                                        <img src="/icons/star.svg" className="w-4 h-4" />
                                        <div>
                                            {worker.rating} / 5
                                        </div>
                                    </div>
                                </div>
                            </Box>
                            ))}
                        </div>
                    </Box>
                </ModalDialog>
            </Modal>
            <Modal open={showSpeakWithWorksyModal} onClose={() => setShowSpeakWithWorksyModal(false)}>
                <ModalDialog className="overflow-y-auto w-[100vw] h-[90vh]">
                    <Box className='m-1 backdrop-blur-sm rounded-sm p-1 border-black flex flex-col gap-1 h-[100vh] overflow-y-auto cursor-pointer'>
                        <div className='flex justify-between'>
                            <span className='text-md font-bold'>Speak with Worksy</span>
                        </div>
                        <div className='flex flex-col-reverse h-full p-4 bg-blue-50 overflow-y-scroll gap-3'>
                            {showSpeakWithWorksyModal_messages.map((message, mid) =>
                                (<div className={"flex flex-col items-end"  + (message.role == 'user' ? " self-end" : " self-start")} key={mid}>
                                    <div className="w-fit h-fit rounded-sm p-2 bg-slate-400 text-base">
                                        {message.content}
                                    </div>
                                    <div className="text-xs">{message.createdOn}</div>
                                    </div>
                                ))
                            }
                        </div>
                        <div className='flex gap-2 w-full'>
                            <Input placeholder="Message" className='w-full' value={showSpeakWithWorksyModal_messagefield} onChange={(e) => {setShowSpeakWithWorksyModal_messagefield(e.target.value)}} />
                            <Button onClick={() => {showSpeakWithWorksyModal_sendToWorksyAI()}}>Send</Button>
                        </div>
                    </Box>
                </ModalDialog>
            </Modal>
            {isLoading && <LinearProgress />}
            {
                user ?
                
                <div>
                    {mapsDefaultProps && <div className='h-[100vh] w-full'>
                        <GoogleMapReact
                            bootstrapURLKeys={{key: process.env.REACT_APP_MAP_API_KEY}}
                            defaultCenter={mapsDefaultProps.center}
                            defaultZoom={mapsDefaultProps.zoom}
                            onChange={(e) => {
                                setMapsCurrentBounds(e.bounds);
                            }}
                            onGoogleApiLoaded={({map, maps}) => {
                                setMapVal([maps, map])
                            }}
                        >
                        </GoogleMapReact>
                    </div>}
                    <div className='fixed bottom-16 p-2 flex gap-2'>
                        <div className='bg-[#EBF3FF] rounded-md p-2 text-xs cursor-pointer' onClick={() => {setShowMoreJobsModal(true)}}>
                            More Jobs
                        </div>
                        <div className='bg-[#EBF3FF] rounded-md p-2 text-xs cursor-pointer' onClick={() => {setShowSearchResults(true)}}>
                            Search
                        </div>
                        <div className='bg-[#EBF3FF] rounded-md p-2 text-xs cursor-pointer' onClick={() => {setShowSpeakWithWorksyModal(true)}}>
                            Speak with Worksy
                        </div>
                    </div>
                    <NavBottom />
                </div> :

                <div className="flex h-screen justify-center items-center">
                    <div className="w-full flex flex-col items-center">
                        <img src="logo.png" alt="logo" />
                        <div className="w-full mt-[100px] flex gap-2 flex-col items-center">
                            <Button className="w-[50vw] h-[50px] rounded-sm" onClick={() => {window.location.href = '/login'}}>Login</Button>
                            <Button className="w-[50vw] h-[50px] rounded-sm" onClick={() => {window.location.href = '/register'}}>Register</Button>
                        </div>
                    </div>
                </div>
            }
        </div>
    )
}