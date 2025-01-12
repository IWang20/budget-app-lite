

// const transactions = [
//   {
//       "id": 1,
//       "date": "2025-01-09",
//       "type": "django test",
//       "description": "up' down left right # z",
//       "category": "groceries",
//       "amount": 1000.0
//   },
//   { 
//     "id": 2,
//     "date": "2025-01-10",
//     "type": "django test 2",
//     "description": "awerhjawoeurh aiue ",
//     "category": "rent",
//     "amount": 1000.0
//   },
// ]

import React from 'react';
import axios from "axios";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedFile: null,
    };
  }

  onFileChange = event => {
    this.setState({ selectedFile: event.target.files[0] });
  };

  onFileUpload = () => {
    const formData = new FormData();

    formData.append(
      "myFile",
      this.state.selectedFile,
      this.state.selectedFile.name
    );

    // Details of the uploaded file
    console.log(this.state.selectedFile);

    axios.post("http://localhost:8000/upload_pdf/", formData, {headers: {"Content-Type": "multipart/form-data"}});
  };

  render() {
    return (
      <div>
        <h3>File Upload using React!</h3>
        <div>
          <input type="file" onChange={this.onFileChange} />
          <button onClick={this.onFileUpload}>
            Upload!
          </button>
        </div>
      </div>
    );
  }
}

export default App;