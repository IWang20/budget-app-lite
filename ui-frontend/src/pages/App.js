import {React, useState} from 'react';
import axios from "axios";
import './App.css'


const Form = ({transactionData, loading_state}) => {
  console.log(transactionData);

  if (loading_state === "idle") {
    <h1>No Data</h1>
  }
  else if (loading_state === "fetching") {
    <h1>Loading</h1>
  }
  else {
    // combine similar transactions and display them, embed them in the form using a hidden input 
    return (
      transactionData.map((transaction, index) => {
        return (
          <div class="flex-grid" key={index}>
            <div class="col">
              <h3>{transaction[2]}</h3>
              <p>{transaction[1]} </p>
            </div>
            <div class="col">
              <label>
                <input type="radio" id="dining" name={index}/> dining
              </label>
              <label>
                <input type="radio" id="personal" name={index}/> personal
              </label>
              <label>
                <input type="radio" id="rent/utilities" name={index}/> rent/utilities
              </label>
              <label>
                <input type="radio" id="groceries" name={index}/> groceries
              </label>
              <label>
                <input type="radio" id="transporation" name={index}/> transporation
              </label>
              <label>
                <input type="radio" id="other" name={index}/> other
              </label>
            </div>
          </div>
        )
      })
    )
  }
}

const App = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState("idle");
  // const [month, setMonth] = useState("");
  const [fileName, setFileName] = useState("");
  const [file, setFile] = useState();



  const onFileChange = (event) => {
    setFile(event.target.files[0]);
    setFileName(event.target.files[1]);
  };

  const onFileUpload = async() => {
    const formData = new FormData();

    formData.append(
      "pdf",
      file,
      fileName
    );

    // Details of the uploaded file
    setLoading("fetching");
    const response = await axios.post("http://localhost:8000/upload_pdf/", formData, {headers: {"Content-Type": "multipart/form-data"}});
    // console.log(response);
    console.log(response["data"]["status"]);
    console.log(response["data"]["transactions"]);

    setTransactions(response["data"]["transactions"]);
    setLoading("completed");
    // this.setState({transactions: response.data});
  };

  const sendTransaction = async(jsonObject) => {
    const response = await axios.post("http://localhost:8000/api/transaction/", jsonObject, {headers: {"Content-Type": "application/json"}});
    // console.log(response);
  };

  const unCheckAll = () => {
    const radios = document.querySelectorAll("input[type='radio']");
    radios.forEach((input) => {
      input.checked = false;
    });
  };

  const onTransactionSubmit = (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    const selectedTransactions = new Set();

    transactions.forEach((transaction, index) => {
        const jsonObject = {};
        const selectedOption = document.querySelector(`input[name="${index}"]:checked`);

        if (selectedOption) {
            // const transaction = _;
            jsonObject["date"] = transaction[0];
            console.log(jsonObject["date"]);
            jsonObject["type"] = transaction[1];
            jsonObject["description"] = transaction[2];
            jsonObject["category"] = selectedOption.id;
            jsonObject["amount"] = transaction[3];
            sendTransaction(jsonObject);
            console.log(index);
            selectedTransactions.add(transaction);
        }
    });

    console.log(selectedTransactions);
    setTransactions((items) => items.filter((t) => !(selectedTransactions.has(t))));
    console.log(transactions);
    unCheckAll();
    // selectedTransactions.clear();
  };


  return (
    <div>
      <h3>File Upload using React!</h3>
      <div>
        <input type="file" onChange={onFileChange} />
        <button onClick={onFileUpload}>
          Upload!
        </button>
      </div>
      <div>
      <form onSubmit={onTransactionSubmit}>
        <Form transactionData={transactions} loading_state={loading}/>
        <button type="submit">Submit</button>
      </form>
      </div>
    </div>
  );
};

export default App;