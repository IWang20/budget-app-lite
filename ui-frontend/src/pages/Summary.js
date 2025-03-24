import {React, useState, useEffect} from 'react';
import axios from "axios";
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, LabelList } from "recharts";
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



const Bars = ({transactionData, loading}) => { 
    const transactions = transactionData;
    const uniqueDescriptions = new Set();
    // console.log(transactions);
    // console.log("<Chart/> " + loading);

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
                <ResponsiveContainer width="100%" height={500}>
                    <BarChart data={transactions} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="month" />
                        <YAxis />
                        <Tooltip />
                        {
                            
                            [...uniqueDescriptions].sort().map((description, index) => {
                                // console.log(description, index);
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
    const [activeIndex, setActiveIndex] = useState(-1);
    // console.log(transactions);
    // console.log("<Chart/> " + loading);
    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];
    const pie_width = 400;
    const pie_height = 400;

    const onPieEnter = (_, index) => {
        setActiveIndex(index);
    };

    if (loading === "idle") {
        return (
            <h1>No Data</h1>
        )
    }
    else if (loading === "fetching") {
        return <p>Loading...</p>;
    }
    else if (loading === "completed") {
        console.log(transactionData);
        return (
            <PieChart width={pie_width} height={pie_height}>
                <Pie
                    data={transactionData}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={150}
                    fill="#8884d8"
                    onMouseEnter={onPieEnter}
                    style={{ cursor: 'pointer', outline: 'none'}}
                >
                    <LabelList dataKey="name"/>
                    {Object.entries(transactionData).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
                </Pie>
                <Tooltip/>
            </PieChart>
        )
    }
}

const Summary = () => {
    const [years, setYears] = useState([]);
    const [transactionYear, setTransactionYear] = useState("All");
    const [transactionGroupType, setTransactionGroupType] = useState("Total Transaction Cost");
    const [barData, setBarData] = useState([]);
    const [categoryYear, setCategoryYear] = useState("All");
    const [categoryMonth, setCategoryMonth] = useState(["All", -1]);
    const [categoryAnalysisText, setCategoryAnalysisText] = useState("Total Transaction Cost");
    const [pieData, setPieData] = useState([]);
    const [barLoadingStatus, setBarLoadingStatus] = useState("idle");
    const [pieLoadingStatus, setPieLoadingStatus] = useState("idle");
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];


    useEffect(() => {
        const getYears = async() => {
            const response = await axios.get("http://localhost:8000/analysis/?type=list-years");
            setYears(response["data"]["years"]);
        }
        getYears();
    }, []);

    // pie gets loaded first because of this, 
    // I set this because the state needed to be set instantly before I make the get request
    useEffect(() => {
        getCategories(categoryYear, categoryMonth[1], categoryAnalysisText);
    }, [categoryYear, categoryMonth, categoryAnalysisText]);

    useEffect(() => {
        getTransactions(transactionYear, transactionGroupType);
    }, [transactionGroupType, transactionYear]);

    // could add the kind of group by category/transaction 
    async function getTransactions(year, total_type) {
        if (year === "All") {
            year = -1;
        }

        if (total_type === "Total Transaction Cost") {
            total_type = "total-cost";
        }
        else if (total_type === "Total Transaction Count") {
            total_type = "total-count";
        }
        
        setBarLoadingStatus("fetching");
        const response = await axios.get("/analysis/?type=year-data&year=" + year + "&total-type=" + total_type);
        const allData = response["data"]["transactions"];
        var barTransactions = [];
        
        console.log(allData);
        for (const dict of allData[year]) {
            var temp = {};
            for (const key of Object.keys(dict)) {
                if (key === "month") {
                    temp["month"] = dict[key];
                }
                else {
                    temp[key] = dict[key][4];
                }
            }
            barTransactions.push(temp);
        }
        // barTransactions.sort((a, b) => a[5]-b[5]);
        // console.log(barTransactions);
        setBarData(barTransactions);
        setBarLoadingStatus("completed");
    }

    // pull all data
    async function getCategories(year, month, analysis_type) {
        if (year === "All") {
            year = -1;
        }

        if (analysis_type === "Total Transaction Cost") {
            analysis_type = "total-cost"
        }
        else if (analysis_type === "Total Transaction Count") {
            analysis_type = "total-count"
        }
        else {
            console.log("invalid analysis type " + analysis_type);
        }

        const categories = [];
        
        setPieLoadingStatus("fetching");
        const response = await axios.get("/analysis/?type=category-data&year=" + year + "&month=" + month + "&total-type=" + analysis_type);
        const allData = response["data"]["transactions"];
        for (const key in allData) {
            const temp = {};
            temp['name'] = key;
            temp['value'] = allData[key];
            categories.push(temp);
        }
        console.log(categories);
        setPieData(categories);
        // regroup everything if it is all years
        // regroup things anyways, they aren't organized correctly 

        setPieLoadingStatus("completed");
    }

    return (    
        <div>
            <h1>Welcome to the Summary Page! :3</h1>
            <div className="dropdown">
                <button className="dropbtn">{transactionYear}</button>
                <div className="dropdown-content">
                    <a href="/" onClick={(event) => {setTransactionYear("All"); event.preventDefault();}}>All</a>
                    {years.map((year, index) => { 
                        return (
                            <a href="/" onClick={(event) => {setTransactionYear(year);
                                                            event.preventDefault();}} key={index}>{year}</a>
                        )
                    })}
                </div>
            </div>
            <div className="dropdown">
                <button className="dropbtn">{transactionGroupType}</button>
                <div className="dropdown-content">
                    <a href="/" onClick={(event) => {setTransactionGroupType("Total Transaction Cost");
                                                    event.preventDefault();}}>Total Transaction Cost</a>
                    <a href="/" onClick={(event) => {setTransactionGroupType("Total Transaction Count");
                                                    event.preventDefault();}}>Total Transaction Count</a>
                </div>
            </div>
            <Bars transactionData={barData} loading={barLoadingStatus}/>
            <div className="dropdown">
                <button className="dropbtn">{categoryYear}</button>
                <div className="dropdown-content">
                    <a href="/" onClick={(event) => {event.preventDefault();
                                                    setCategoryYear("All");}}>All</a>
                    {years.map((year, index) => { 
                        return (
                            <a href="/" onClick={(event) => {setCategoryYear(year);
                                                            event.preventDefault();}} key={index}>{year}</a>
                        )
                    })}
                </div>
            </div>
            <div className="dropdown">
                <button className="dropbtn">{categoryMonth[0]}</button>
                <div className="dropdown-content">
                    <a href="/" onClick={(event) => {setCategoryMonth(["All", -1]);
                                                    event.preventDefault();}}>All</a>
                    {
                        
                        Array.from({length:12}, (value, index) => index).map((index) => {
                            // console.log(index);
                            return (
                                <a href="/" onClick={(event) => {setCategoryMonth([months[index], index+1]);
                                                                event.preventDefault();}}>{months[index]}</a>
                            );
                        })
                    }
                </div>
            </div>
            <div className="dropdown">
                <button className="dropbtn">{categoryAnalysisText}</button>
                <div className="dropdown-content">
                    <a href="/" onClick={(event) => {setCategoryAnalysisText("Total Transaction Cost");
                                                    event.preventDefault();}}>Total Transaction Cost</a>
                    <a href="/" onClick={(event) => {setCategoryAnalysisText("Total Transaction Count");
                                                    event.preventDefault();}}>Total Transaction Count</a>
                </div>
            </div>
            <Pies transactionData={pieData} loading={pieLoadingStatus}/>
        </div>
    )
};

export default Summary;