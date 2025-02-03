import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route} from "react-router";
import './index.css';
import App from './pages/App';
import Summary from './pages/Summary';
import reportWebVitals from './reportWebVitals';

export default function Main() {
  return (
    <BrowserRouter>
      <Routes>
          <Route index element={<App/>}/>
          <Route path="/summary" element={<Summary/>}/>
      </Routes>
      {/* <Switch>
        <Route path="/">
          <App/>
        </Route>
      </Switch> */}
    </BrowserRouter>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
console.log(root);
root.render(
  // <React.StrictMode>
    <Main />
  // </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
