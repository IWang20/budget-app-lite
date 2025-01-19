import {React, useState} from 'react';
import axios from "axios";
import './App.css'


const App = () => {
  const [transactions, setTransactions] = useState([]);
  const [month, setMonth] = useState("");
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

    const response = await axios.post("http://localhost:8000/upload_pdf/", formData, {headers: {"Content-Type": "multipart/form-data"}});
    // console.log(response);
    console.log(response["data"]["status"]);
    console.log(response["data"]["transactions"]);

    setTransactions(response["data"]["transactions"]);
    // this.setState({transactions: response.data});
  };

  const onTransactionSubmit = (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    // Iterate over the transactions
    transactions.forEach((_, index) => {
        // Find the selected radio button for this transaction index
        const jsonObject = {};
        const selectedOption = document.querySelector(`input[name="${index}"]:checked`);

        if (selectedOption) {
            // Add the index and selected option value to the array
            // transactionSelections.push({
            //     index: index,
            //     selection: selectedOption.id, // You can also use `selectedOption.value` if `value` is defined
            //     transaction: _
            // });
            const transaction = _;
            jsonObject["date"] = transaction[0];
            console.log(jsonObject["date"]);
            jsonObject["type"] = transaction[1];
            jsonObject["description"] = transaction[2];
            jsonObject["category"] = selectedOption.id;
            jsonObject["amount"] = transaction[3]
            const response = axios.post("http://localhost:8000/api/transaction/", jsonObject, {headers: {"Content-Type": "application/json"}});
            console.log(response);
        }
    });

    // jsonObject["transactionData"] = transactionSelections;
    // console.log(jsonObject);
    // const test = {"date": "2001-02-01", "type": "typeTest", "description":"testDescription", "category":"testCategory", "amount":30.1};
    
    // console.log(response["data"]);
    // jsonObject[]
    

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
          {
            transactions.map((transaction, index) => {
              return (
                <div class="flex-grid" key={index}> 
                  <div class="col">
                    <h3>{transaction[1]} {transaction[2]}</h3>
                  </div>
                  <div class="col">
                    <label>
                      <input type="radio" id="test1" name={index}/> test1
                    </label>
                    <label>
                      <input type="radio" id="test2" name={index}/> test2
                    </label>
                  </div>
                </div>
              )
              // return <li key={index}>{transaction[1]} {transaction[2]}</li>
            })
          }
          <button type="submit">Submit</button>
        </form> 
      </div>
    </div>
  );
};

export default App;