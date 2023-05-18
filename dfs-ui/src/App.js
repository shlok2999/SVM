import logo from './logo.svg';
import './App.css';
import MyForm from './MyForm'
import React, { useState, useEffect } from "react";
// import Button from '@material-ui/core/Button';
import Button from '@mui/material/Button';
import {useNavigate} from 'react-router-dom';
import ListGroup from 'react-bootstrap/ListGroup';
import Card from 'react-bootstrap/Card';




const App = () => {
  const [selectedOption, setSelectedOption] = useState(""); // State to store selected option
  const [library, setLibrary] = useState([]);
  const [count, setCount] = useState(0);
  

  const navigate = useNavigate();

  let node_monitor_ip = ''
  let dfs_server_ip = ''
    let node_monitor_port = ''
    let dfs_server_port = ''

  // let libraries_ds = ['tensorflow', 'scikit-learn' 'numpy', 'pandas']
  const ds_obj = {
    libraries:['tensorflow', 'scikit-learn', 'numpy', 'pandas'],
    language: 'Python',
    OS: 'Ubuntu'
  }

  const web_dev_obj = {
    libraries:['express', 'gulp', 'async-js', 'request'],
    language:'Node.js',
    OS:'Ubuntu'
  }
  
  // const libraries = []



  const handleDropdownChange = (event) => {
    console.log(event.target.value)
    const temp_selected  = event.target.value
    setSelectedOption(temp_selected); // Update selected option in state

    
    setCount(count+1)
    
    // console.log(count)



  };

  useEffect(()=> {
      // setLibrary(library);
      // console.log("first element is ", libraries[0]);
      // setCount((count)=>count+1);

    //   fetch('cfg.json')
    // .then(response => {
    //   const clonedResponse = response.clone();
    //   console.log(clonedResponse)
    //   return Promise.all([response.json(), clonedResponse.json()]);
    // })
    // .then(json => {
    //   console.log(json)
    //   dfs_server_ip = json.configs.dfs_server_ip;
    //   console.log(dfs_server_ip)

    //   dfs_server_port = json.configs.dfs_server_port;
    //   console.log(dfs_server_port)

    //   node_monitor_ip = json.configs.node_monitor_ip
    //   console.log(node_monitor_ip)

    //   node_monitor_port = json.configs.node_monitor_port
    //   console.log(node_monitor_port)


    // }).catch(error => console.log(error))

      console.log("Selected option: ", selectedOption);
    const libraries = []

    if(selectedOption == "Python"){

      libraries.push({value: "tensorflow", label:"tensorflow"});
      libraries.push({value: "scikit-learn", label:"scikit-learn"});
      libraries.push({value: "numpy", label:"numpy"});
      libraries.push({value: "pandas", label:"pandas"});

    }
    else if(selectedOption == "Node.js"){
      libraries.push({value: "express", label:"express"});
      libraries.push({value: "gulp", label:"gulp"});
      libraries.push({value: "async-js", label:"async-js"});
      libraries.push({value: "request", label:"request"});
    }
    // console.log("Helllp world")
    // console.log(libraries[0])
      setLibrary(libraries)
      console.log(library)

    },[selectedOption, count]);


  

  

  // console.log(count);

  const handleSubmit = (event) => {
    event.preventDefault();
    var form = event.target;

    // Handle form submission here with selectedOption value
    console.log(form.cpu.value);
    console.log(form.gpu.value);
    console.log(form.memory.value);
    console.log(form.storage.value);
    console.log(library, ' ', selectedOption)
  };

  const handleInputChange = (event)=>{
    event.preventDefault();
    // console.log(event.target.value)

    var dropdown = document.getElementById('libraries');
    dropdown.addEventListener('change', function(){
        console.log(dropdown.value)
    });

  }

  const navigateToCustomTemplate = ()=>{
    navigate('/form')
  }

  const navigateToConfig = ()=>{
    navigate('/config')
  }

  const navigateToDSTemplate = ()=>{
    navigate('/saved_templates',{
      state:{
        obj:ds_obj,
      }
    });
  };

  const navigateToWebDevTemplate = ()=>{
    navigate('/saved_templates',{
      state:{
        obj:web_dev_obj,
      }
    });
  };


  

  return (
    <div>
    <div className="main-div">
      <h1>Welcome to SVM D-cloud</h1>
      <p>Make your own Environment</p>
      
    </div>
    <Button variant="contained" class = "data-science-button" onClick={navigateToConfig}>Check Saved Configurations</Button>
      <Button variant="contained" class = "web-devlopment-button" onClick={navigateToWebDevTemplate}>Check Saved Templates</Button>
      <Button variant="contained" class = "custom-template-button" onClick={navigateToCustomTemplate}>Custom Template</Button>
      </div>

  );
};

function Library(props){
  return(
      <select class="form-dropdown">
        <option value="" selected disabled>Please select a Library to work with</option>
        {props.library_list.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
      </select>
    );
}

export default App;

