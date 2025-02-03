import {React, useState, useEffect} from 'react';
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, LabelList } from "recharts";
import './Summary.css'

const data = [
    { month: "January", itemA: 1000, itemB: 2000, itemC: 1000 },
    { month: "February", itemA: 1500, itemB: 1000, itemC: 500 },
    { month: "March", itemA: 2000, itemB: 2500, itemC: 500 },
    { month: "April", itemA: 2500, itemB: 3000, itemC: 1500 },
    { month: "May", itemA: 3000, itemB: 2000, itemC: 1000 },
];
  


const Summary = () => {
    const [transactions, setTransactions] = useState([]);
    const [dropDownText, setDropDownText] = useState("Select Year")
    const [years, setYears] = useState([]);

    useEffect(() => {
        const getYears = async() => {
            const response = await axios.get("http://localhost:8000/analysis/?type=list-years");
            setYears(response["data"]["years"]);
            // console.log(response);
            // console.log(transactions);
        }
        getYears();
    }, []);

    // set transaction, set dropdown text
    async function getTransactions(event, year) {
        event.preventDefault();
        const response = await axios.get("/analysis/?type=year-data&year=" + year);
        setDropDownText(year)
        setTransactions(response["data"])
        console.log(response["data"]);
    }


    return (    
        <div>
            <h1>Welcome to the Summary Page! :3</h1>
            <div className="dropdown">
                <button className="dropbtn">{dropDownText}</button>
                <div className="dropdown-content">
                    {years.map((year, index) => {
                        return (
                            <a href="#" onClick={(event) => getTransactions(event, year)} key={index}>{year}</a>
                        )
                    })}
                </div>
            </div>

            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    {/* <Bar dataKey="sales" fill="#8884d8" barSize={50} />
                    <Bar dataKey="itemA" stackId="a" fill="#8884d8">
                        <LabelList dataKey="itemA" position="insideTop" fill="#fff" />
                    </Bar>
                    <Bar dataKey="itemB" stackId="a" fill="#82ca9d">
                        <LabelList dataKey="itemB" position="insideTop" fill="#fff" />
                    </Bar>
                    <Bar dataKey="itemC" stackId="a" fill="#ffc658">
                        <LabelList dataKey="itemC" position="insideTop" fill="#fff" />
                    </Bar> */}
                </BarChart>
            </ResponsiveContainer>
        </div>
    )
};

export default Summary;