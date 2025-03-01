import {React, useState, useEffect} from 'react';
import axios from "axios";
import { BarChart, Bar, PieChart, Pie, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, LabelList } from "recharts";
import './Summary.css'

// const data = [
//     { month: "January", itemA: 1000, itemB: 2000},
//     { month: "February", itemA: 1500, itemB: 1000, itemC: 500 },
//     { month: "March", itemA: 2000, itemB: 2500, itemC: 500 },
//     { month: "April", itemA: 2500, itemB: 3000, itemC: 1500 },
//     { month: "May", itemA: 3000, itemB: 2000, itemC: 1000 },
// ];

const colors = ["#E176C1",
                "#E19658",
                "#E1574E",
            " #7D7EE1",
                "#8EE077",
                "#E1C95F",
                "#9D68D1",
                "#6BB6CC"]
// const transactionsTest = [
//     {month: "January", "Uber Trip Help.Uber.Com": 98.87, "Spotify": 5.99},
//     {month: "Febuary", "Chipotle Online Chipotle.Com": 9.01, "Spotify": 5.99}
// ]

// prop passing undefined into loading 
const Bars = ({transactionData, loading}) => { 
    const transactions = transactionData;
    const uniqueDescriptions = new Set();
    console.log(transactions);
    console.log("<Chart/> " + loading);

    for (const month in transactions) { 
        for (const key in transactions[month]) {
            if (key !== "month") {
                uniqueDescriptions.add(key)
            }
        }
    }
    console.log(uniqueDescriptions);

    if (loading === "idle") {
        return (
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data="" margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="" />
                    <YAxis />
                    <Tooltip />
                </BarChart>
            </ResponsiveContainer>
        )
    }
    else if (loading === "fetching") {
        return <p>Loading...</p>;
    }
    else if (loading === "completed") {
        return (
            <div>
                <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={transactions} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis />
                        <Tooltip />
                        {
                            [...uniqueDescriptions].map((description, index) => {
                                console.log(description, index);
                                return (
                                    
                                    <Bar dataKey={description} stackId="a" fill={colors[index % 7]}>
                                        <LabelList dataKey={description} position="insideTop" fill="#fff" />
                                    </Bar>
                                )
                            })
                        }
                    </BarChart>
                </ResponsiveContainer>
            </div>
        )
    }
}

const Pies = ({transactionData, loading}) => { 
    const transactions = transactionData;
    const uniqueDescriptions = new Set();
    // const [year, setYear] = useState(yearText);
    console.log(transactions);
    console.log("<Chart/> " + loading);

    for (const month in transactions) { 
        for (const key in transactions[month]) {
            if (key !== "month") {
                uniqueDescriptions.add(key)
            }
        }
    }
    console.log(uniqueDescriptions);

    if (loading === "idle") {
        return (
            <ResponsiveContainer>
                <PieChart width={1000} height={1000}>
                    <Pie data={transactionData} dataKey="amount" nameKey="name" cx="70%" cy="70%" outerRadius={10} fill="#8884d8" />
                    {/* <Pie data={data02} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={60} outerRadius={80} fill="#82ca9d" label /> */}
                </PieChart>
            </ResponsiveContainer>
            
        )
    }
    else if (loading === "fetching") {
        return <p>Loading...</p>;
    }
    else if (loading === "completed") {
        return (
            <div>
                <PieChart width={730} height={250}>
                    <Pie data={transactionData} dataKey="amount" nameKey="name" cx="50%" cy="50%" outerRadius={50} fill="#8884d8" />
                    {/* <Pie data={data02} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={60} outerRadius={80} fill="#82ca9d" label /> */}
                </PieChart>
            </div>
        )
    }
}

const Summary = () => {
    const [years, setYears] = useState([]);
    const [currYear, setCurrYear] = useState(-1);
    const [yearText, setYearText] = useState("Select Year");
    const [analysisText, setAnalysisText] = useState("Total Transaction Cost");
    const [barData, setBarData] = useState([]);
    // const [pieData, setPieData] = useState([]);
    // const [lineData, setLineData] = useState([]);
    const [loadingStatus, setLoadingStatus] = useState("idle");


    useEffect(() => {
        const getYears = async() => {
            const response = await axios.get("http://localhost:8000/analysis/?type=list-years");
            setYears(response["data"]["years"]);
        }
        getYears();
    }, []);

    // get data
    // pause loading
    // return all types bar, pie, 
    //  set them
    // resume loading


    // REMEMBER TO GET ALL YEARS DATA, CURRENTLY setBarData(response[data][data]) doesn't work but adding [data][data][year] does for some reason
    // Takes a grouped data set from /analysis/ 
    // just look in analysis_type varible, no need to pass it into getTransactions
    async function getTransactions(event, year, analysis_type) {
        event.preventDefault();
        // setYearText(year);
        setAnalysisText(analysis_type);
        
        setLoadingStatus("fetching");
        const response = await axios.get("/analysis/?type=year-data&year=" + year);
        const allData = response["data"]["data"];
        var barTransactions = [];
        var pieTransactions = [];
        
        console.log(allData);
        
        allData[year].map((dict) => {
            var temp = {};
            Object.keys(dict).map((key) => {
                // console.log(dict[key]);
                if (key === "month") {
                    temp["month"] = dict[key];
                }
                else {
                    if (analysis_type === "Total Transaction Cost") {
                        temp[key] = dict[key][4];
                    }
                    else if (analysis_type === "Total Transaction Count") {
                        temp[key] = dict[key][5];
                    }
                    else {
                        console.log("invalid analysis type: " + analysis_type);
                    }
                    
                }
            })
            barTransactions.push(temp);
        });
        // console.log(barTransactions);
        
        // Pie
        // var temp = {};
        // allData[year].map((dict) => {
        //     Object.keys(dict).map((key) => {
        //         if (key !== "month") {
        //             if (!(key in temp)) {
        //                 temp[key] = [dict[key][4], dict[key][5]];
        //             }
        //             else {
        //                 temp[key][0] += dict[key][4];
        //                 temp[key][1] += dict[key][5];
        //                 console.log(temp[key]);
        //             }
                    
        //         }
        //     })
        // });
        // console.log(temp);

        // Object.keys(temp).map((transaction) => {
        //     var slice = {};
        //     slice["name"] = transaction;
        //     slice["amount"] = temp[transaction][0];
        //     slice["count"] = temp[transaction][1];
        //     pieTransactions.push(slice);
        // });
        // console.log(pieTransactions);

        
        setBarData(barTransactions);
        // setPieData(pieTransactions);
        setLoadingStatus("completed");
    }

    // states
    // 1. idle - on open
        // in Chart, render completely empty chart
    // 2. fetching data - getTransactions
        // in Chart, render loading screen
    // 3. return data - ? 
        // in Chart, render chart with transactions
    


    return (    
        <div>
            <h1>Welcome to the Summary Page! :3</h1>
            <div className="dropdown">
                <button className="dropbtn">{yearText}</button>
                <div className="dropdown-content">
                    <a href="/" onClick={(event) => {setYearText("All");
                                                    getTransactions(event, -1, analysisText);}}>All</a>
                    {years.map((year, index) => { 
                        return (
                            <a href="/" onClick={(event) => {setYearText(year);
                                                            getTransactions(event, year, analysisText);}} key={index}>{year}</a>
                        )
                    })}
                </div>
            </div>
            <div className="dropdown">
                <button className="dropbtn">{analysisText}</button>
                <div className="dropdown-content">
                    <a href="/" onClick={(event) => getTransactions(event, currYear, "Total Transaction Cost")}>Total Transaction Cost</a>
                    <a href="/" onClick={(event) => getTransactions(event, currYear, "Total Transaction Count")}>Total Transaction Count</a>
                </div>
            </div>
            <Bars transactionData={barData} loading={loadingStatus}/>
            {/* <Pies transactionData={pieData} loading={loadingStatus}/> */}
        </div>
    )
};

export default Summary;