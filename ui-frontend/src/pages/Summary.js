import {React, useState} from 'react';
import axios from "axios";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, LabelList } from "recharts";

const data = [
    { month: "January", itemA: 1000, itemB: 2000, itemC: 1000 },
    { month: "February", itemA: 1500, itemB: 1000, itemC: 500 },
    { month: "March", itemA: 2000, itemB: 2500, itemC: 500 },
    { month: "April", itemA: 2500, itemB: 3000, itemC: 1500 },
    { month: "May", itemA: 3000, itemB: 2000, itemC: 1000 },
];
  


const Summary = () => {
    const [transactions, setTransactions] = useState("");
    const getTransactions = async() => {
        const response = await axios.get("http://localhost:8000/api/transaction/");
        // console.log(response["data"]);
        setTransactions(response["data"]);
    };

    // getTransactions();

    return (    
        <div>
            <h1>Welcome to the Summary Page! :3</h1>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="month" />
                    <YAxis />
                    <Tooltip />
                    {/* <Bar dataKey="sales" fill="#8884d8" barSize={50} /> */}
                    {/* <Bar dataKey="itemA" stackId="a" fill="#8884d8">
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