import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import MyForm from './MyForm.js'
import Templates from './Templates.js'
import Config from './Config.js'
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  // <React.StrictMode>
  //   <App />
  //   <MyForm/>
  // </React.StrictMode>

  <BrowserRouter>
  	<Routes>
    <Route path="/" element={<App/>}/>
    <Route path = "/form" element={<MyForm/>}/>
    <Route path = "/saved_templates" element={<Templates/>}/>
    <Route path = "/config" element={<Config/>}/>
    </Routes>
  </BrowserRouter>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
