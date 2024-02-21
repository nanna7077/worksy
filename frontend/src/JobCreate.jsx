import Button from "@mui/joy/Button";
import { useEffect, useState } from "react";
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';
import { geocodeByAddress, getLatLng, geocodeByLatLng } from 'react-google-places-autocomplete';
import NavBottom from "./Nav";

export default function JobCreate() {
    const [user, setUser] = useState(null);
    const [tags, setTags] = useState([]);
    const [currencies, setCurrencies] = useState([]);
    
    const [selectedTags, setSelectedTags] = useState([]);
    const [description, setDescription] = useState("");
    const [address, setAddress] = useState("");
    const [position, setPosition] = useState({ latitude: null, longitude: null });
    const [duration_range_start, setDurationRangeStart] = useState(0);
    const [duration_range_end, setDurationRangeEnd] = useState(0);
    const [duration_range_unit, setDurationRangeUnit] = useState('hours');
    const [price_currency, setPriceCurrency] = useState('INR');
    const [price_range_start, setPriceRangeStart] = useState(0);
    const [price_range_end, setPriceRangeEnd] = useState(0);


    function getPosition() {
        navigator.geolocation.getCurrentPosition((position) => {
            setPosition({ latitude: position.coords.latitude, longitude: position.coords.longitude });
        });
        geocodeByLatLng({ lat: position.latitude, lng: position.longitude })
        .then(results => {
            console.log(results)
            setAddress(results[0].formatted_address);
        })
        .catch(error => console.error('Error', error));
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
                if (data.error == "UnAuthorized") {
                    window.location.href = "/login";
                }
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
            if (data.error != undefined) {
                return;
            }
            setTags(data.tags);
        });

        fetch(process.env.REACT_APP_API_URL + "/common/currencies", {
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
            setCurrencies(Object.entries(data));
        });

        getPosition();

    }, [])

    useEffect(() => {
        geocodeByAddress(
            { address: address },
        )
        .then((results) => {
            const { lat, lng } = getLatLng(results[0]);
            console.log(lat, lng);
            setPosition({ latitude: lat, longitude: lng });
        })
        .catch((error) => console.error("Error", error));
    }, [address])

    function createJob() {
        fetch(process.env.REACT_APP_API_URL + "/jobs/create/new", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + window.localStorage.getItem("sessionkey"),
            },
            body: JSON.stringify({
                description: description,
                address: address,
                position: position,
                duration_range_start: duration_range_start,
                duration_range_end: duration_range_end,
                duration_range_unit: duration_range_unit,
                price_currency: price_currency,
                price_range_start: price_range_start,
                price_range_end: price_range_end,
                tags: selectedTags,
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.error != undefined) {
                return;
            }
            alert("Job created successfully");
            window.location.href = "/";
        });
    }

    return (
        <div className="">
            {
                user &&

                <div className="flex h-screen justify-center items-center">
                    <div className="w-1/2">
                        <h1 className="text-3xl font-bold mb-4">Create Job</h1>

                        <div className="mb-4">
                            <label
                                className="block text-gray-700 text-sm font-bold mb-2"
                                htmlFor="skills"
                            >
                                Required Skills
                            </label>

                            <div className="text-sm" id="skills">
                                <span className="mr-2 mb-2">Selected</span>
                                <div className="flex gap-2 flex-wrap mb-2">
                                    {selectedTags.map((tag) => (
                                        <div className="w-fit bg-[rgba(0,0,0,0.1)] text-xs p-1 flex gap-2 justify-center align-center" key={tag.id}>
                                            {tag.name}
                                            <div className="cursor-pointer" onClick={() => setSelectedTags(selectedTags.filter((t) => t.id != tag.id))}>x</div>
                                        </div>
                                    ))}
                                </div>

                                <span className="mr-2 mb-2">Available Tags</span>
                                <div className="flex gap-2 flex-wrap mb-2">
                                    {tags.map((tag) => (
                                        <div className="w-fit bg-[rgba(0,0,0,0.1)] text-xs p-1 flex gap-2 justify-center align-center" key={tag.id}>
                                            {tag.name}
                                            <div className="cursor-pointer" onClick={() => {if (selectedTags.includes(tag)) return; setSelectedTags([...selectedTags, tag])}}>+</div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        <div className="mb-4">
                            <label
                                className="block text-gray-700 text-sm font-bold mb-2"
                                htmlFor="description"
                            >
                                Description
                            </label>
                            <textarea
                                className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                id="description"
                                rows={4}
                                type="text"
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                placeholder="Description"
                            />
                        </div>

                        <div className="mb-4">
                            <label
                                className="block text-gray-700 text-sm font-bold mb-2"
                                htmlFor="address"
                            >
                                Address
                            </label>
                            <div className="flex gap-2 justify-center align-center items-center">
                                {!address && <GooglePlacesAutocomplete
                                    placeholder="Search Address"
                                    apiKey={process.env.REACT_APP_GOOGLE_MAPS_API_KEY}
                                    selectProps={{
                                        address,
                                        onChange: (e) => {console.log(e); setAddress(e.label)}
                                    }}
                                    className="w-full"
                                />}
                                {address && <input
                                    className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                    id="address"
                                    type="text"
                                    value={address}
                                    onChange={(e) => setAddress(e.target.value)}
                                    placeholder="Address"
                                />}
                                <img src="/icons/target.svg" className="cursor-pointer h-[30px]" onClick={getPosition} />
                            </div>
                            <div className="flex gap-2">
                                {position.latitude && <p className="text-sm text-gray-500">Latitude: {position.latitude}</p>}
                                {position.longitude && <p className="text-sm text-gray-500">Longitude: {position.longitude}</p>}
                            </div>

                        </div>

                        <div className="mb-4">
                            <label
                                className="block text-gray-700 text-sm font-bold mb-2"
                                htmlFor="duration"
                            >
                                Duration Range
                            </label>
                            <div className="flex gap-2 justify-between" id="duration">
                                <input
                                    className="shadow appearance-none border rounded w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                    type="text"
                                    value={duration_range_start}
                                    onChange={(e) => setDurationRangeStart(e.target.value)}
                                    placeholder="Duration Range Start"
                                />
                                -
                                <input
                                    className="shadow appearance-none border rounded w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                    type="text"
                                    value={duration_range_end}
                                    onChange={(e) => setDurationRangeEnd(e.target.value)}
                                    placeholder="Duration Range End"
                                />
                            </div>
                            <div className="flex justify-around mt-2 items-center">
                                <div>
                                    Selected Duration: <span className="font-bold capitalize">{duration_range_unit}</span>
                                </div>
                                <Button size="sm" onClick={() => setDurationRangeUnit("hours")}>Hours</Button>
                                <Button size="sm" onClick={() => setDurationRangeUnit("days")}>Days</Button>
                                <Button size="sm" onClick={() => setDurationRangeUnit("weeks")}>Weeks</Button>
                                <Button size="sm" onClick={() => setDurationRangeUnit("months")}>Months</Button>
                                <Button size="sm" onClick={() => setDurationRangeUnit("years")}>Years</Button>
                            </div>

                        </div>

                        <div className="mb-4">
                            <label
                                className="block text-gray-700 text-sm font-bold mb-2"
                                htmlFor="price"
                            >
                                Price Range
                            </label>
                            <div className="flex gap-2 justify-between" id="price">
                                <select className="shadow appearance-none border rounded w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline bg-[#ffffff]" onChange={(e) => setPriceCurrency(e.target.value)}>
                                    {currencies.map((currency, c) => (
                                        <option key={c} value={currency[0]}>{currency[0]} ({currency[1].name})</option>
                                    ))}
                                </select>
                                <input
                                    className="shadow appearance-none border rounded w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                    type="text"
                                    value={price_range_start}
                                    onChange={(e) => setPriceRangeStart(e.target.value)}
                                    placeholder="Price Range Start"
                                />
                                -
                                <input
                                    className="shadow appearance-none border rounded w-1/2 py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                                    type="text"
                                    value={price_range_end}
                                    onChange={(e) => setPriceRangeEnd(e.target.value)}
                                    placeholder="Price Range End"
                                />
                            </div>
                        </div>

                        <div className="flex items-center justify-center">
                            <button
                                className="bg-[#33363f] hover:bg-[#2f3136] w-full text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                                type="button"
                                onClick={createJob}
                            >
                                Create
                            </button>
                        </div>

                    </div>
                </div>
            }
                
            <div>
                <NavBottom />
            </div>
        </div>
    )
}