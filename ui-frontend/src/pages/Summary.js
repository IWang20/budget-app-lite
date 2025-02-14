import {React, useState, useEffect} from 'react';
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, LabelList } from "recharts";
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
const Chart = ({transactionData, loading}) => { 
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


                        // it isn't returing properly
                        // could it be that the 
                        // for
                        //      for 
                        //              return 
                        // is messing up because technically its returning twice?
                        // 
                        // try getting a list of all the unique transactions, then rendering all the bars at once based on that list of key 
                        {
                            // transactions.map((dict) => {
                            //     Object.keys(dict).map((values) => {
                            //         if (values !== "month") {
                            //             console.log(values);
                            //             return (
                            //                 <Bar dataKey={values} stackId="a" fill="#ffc658">
                            //                     <LabelList dataKey={values} position="insideTop" fill="#fff" />
                            //                 </Bar>
                            //             )
                            //         }
                            //     })
                            // })
                            
                            [...uniqueDescriptions].map((description, index) => {
                                console.log(description, index);
                                return (
                                    
                                    <Bar dataKey={description} stackId="a" fill={colors[index % 7]}>
                                        <LabelList dataKey={description} position="insideTop" fill="#fff" />
                                    </Bar>
                                )
                            })
                        }
                        {/* <Bar dataKey={"Uber Trip Help.Uber.Com"} stackId="a" fill="#ffc658">
                            <LabelList dataKey={"Uber Trip Help.Uber.Com"} position="insideTop" fill="#fff" />
                        </Bar>
                        <Bar dataKey={"Chipotle Online Chipotle.Com"} stackId="a" fill="#00FF00">
                            <LabelList dataKey={"Chipotle Online Chipotle.Com"} position="insideTop" fill="#fff" />
                        </Bar>
                        <Bar dataKey={"Spotify"} stackId="a" fill="#00FFFF">
                            <LabelList dataKey={"Spotify"} position="insideTop" fill="#fff" />
                        </Bar> */}
                    </BarChart>
                </ResponsiveContainer>
            </div>
        )
    }
    

}



const Summary = () => {
    const [years, setYears] = useState([]);
    const [dropDownText, setDropDownText] = useState("Select Year");
    const [transactions, setTransactions] = useState([]);
    const [loadingStatus, setLoadingStatus] = useState("idle");


    useEffect(() => {
        const getYears = async() => {
            const response = await axios.get("http://localhost:8000/analysis/?type=list-years");
            setYears(response["data"]["years"]);
        }
        getYears();
    }, []);

    // useEffect(() => {
    //     console.log("render");
    // }, []);    

    // useEffect(() => {
    //     console.log(transactions);
    // }, [transactions]);

    // set transaction, set dropdown text
    async function getTransactions(event, year) {
        event.preventDefault();
        setLoadingStatus("fetching");
        const response = await axios.get("/analysis/?type=year-data&year=" + year);
        var formatted_transactions = []
        response["data"]["data"][year].map((dict) => {
            var temp = {};
            Object.keys(dict).map((key) => {
                console.log(dict[key]);
                if (key === "month") {
                    temp["month"] = dict[key];
                }
                else {
                    temp[key] = dict[key][4];
                }
            })
            formatted_transactions.push(temp);
        })
        const grouped_transactions = response["data"]["data"];
        // why doesn't grouped_transactions work?????
        setDropDownText(year);
        setTransactions(formatted_transactions);
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
                <button className="dropbtn">{dropDownText}</button>
                <div className="dropdown-content">
                    {years.map((year, index) => {
                        return (
                            <a href="/" onClick={(event) => getTransactions(event, year)} key={index}>{year}</a>
                        )
                    })}
                </div>
            </div>
            <Chart transactionData={transactions} loading={loadingStatus}/>
        </div>
    )
};

export default Summary;