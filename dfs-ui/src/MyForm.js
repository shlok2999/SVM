import React, { useState, useEffect } from "react";
import Button from '@mui/material/Button';
import './App.css';
import {useNavigate} from 'react-router-dom';
import Card from 'react-bootstrap/Card';
import Select from 'react-select';

import {SAVE_TO_CONFIG_URL} from './constants.js'

const MyForm = ()=>{
	
	const [selectedOption, setSelectedOption] = useState(""); // State to store selected option
  	const [library, setLibrary] = useState([]);
  	const [count, setCount] = useState(0);
    const [osSelected, setOsSelected] = useState("");	

  	const navigate = useNavigate();


    const options = [
    { value: 'option1', label: 'Option 1' },
    { value: 'option2', label: 'Option 2' },
    { value: 'option3', label: 'Option 3' },
  ];

  const [selectedOptions, setSelectedOptions] = useState([]);
  const [selectedOptionsList, setSelectedOptionsList] = useState([]);



  const handleSelectChange = (selectedOptions) => {
    setSelectedOptions(selectedOptions);
    // console.log(selectedOptions)
  };


  	const handleDropdownChange = (event) => {
    console.log("language selected is " + event.target.value)
    const temp_selected  = event.target.value
    setSelectedOption(temp_selected); // Update selected option in state

    
    setCount(count+1)
    
    // console.log(count)



  };

  const handleOsDropdownChange = (event) =>{
    console.log("os selected is " + event.target.value)
    const temp_selected  = event.target.value
    setOsSelected(temp_selected); 
  }

  useEffect(()=> {
      // setLibrary(library);
      // console.log("first element is ", libraries[0]);
      // setCount((count)=>count+1);

      // console.log("Selected option: ", selectedOption);
      console.log(SAVE_TO_CONFIG_URL);
      const libraries = []

    if(selectedOption == "python"){

      libraries.push({value: "tensorflow", label:"tensorflow"});
      libraries.push({value: "scikit-learn", label:"scikit-learn"});
      libraries.push({value: "numpy", label:"numpy"});
      libraries.push({value: "pandas", label:"pandas"});

    }
    else if(selectedOption == "node.js"){ 
      libraries.push({value: "express", label:"express"});
      libraries.push({value: "gulp", label:"gulp"});
      libraries.push({value: "async-js", label:"async-js"});
      libraries.push({value: "request", label:"request"});
    }
    console.log(osSelected)
    let url = 'http://127.0.0.1:8001/library/os/' + osSelected

    console.log(url)

    fetch('http://127.0.0.1:8001/templates')
      .then(response => response.json())
      .then(data => {
        console.log(data)


      })
      .catch(error => console.error(error));

    fetch(url)
      .then(response => response.json())
      .then(data => {
        console.log('templates are '+ data)


      })
      .catch(error => console.error(error));
  
    // console.log("Helllp world")
    // console.log(libraries[0])
      setLibrary(libraries)
      setSelectedOptionsList(selectedOptions.map(option => option.value));
      // console.log(library)
      // console.log(selectedOptionsList)

    },[selectedOptions, osSelected, selectedOption]);


    const handleSubmit = (event) => {
    event.preventDefault();
    var form = event.target;
    // console.log("#################################################################################")

    // Handle form submission here with selectedOption value
    console.log(form.cpu.value);
    console.log(form.gpu.value);
    console.log(form.ram.value);
    console.log(form.storage.value);
    console.log(library, ' ', selectedOption)

    // const data = {
    // 	cpu: form.cpu.value,
    // 		gpu: form.gpu.value,
    // 		memory: form.memory.value,
    // 		library: selectedOptionsList,
    //     os: form.os.value
    // 	};

      const data = {
        os: form.os.value,
        

        languages:[
           {
          'language-name': selectedOption,
          'libraries': selectedOptionsList
         }
        ],
        resources:{
          cpu: form.cpu.value,
          gpu : form.gpu.value,
          ram: form.ram.value
        },
        'port-publish':[
          {
            external: {
              ports: form.external.value
            },
            internal:{
              ports: form.internal.value,
              protocol: form.protocol.value
            }
          }
        ],
        'dataset':{
          'version':form.dsVersion.value,
          'filename': form.filename.value,
          'bucketname': form.bucket.value
        },
        'storage':[
          {
            lifecycle: form.storageType.value,
            size: form.storage.value,
            target: '/target'
          },

        ],
        'env-name':form.envname.value,
        'version': form.version.value
      };
    const jsonData = JSON.stringify(data);

    //send form data to server
    fetch(SAVE_TO_CONFIG_URL, {
    	method:'POST',
    	headers: { 'Content-Type': 'application/json' },
    	body: jsonData

    	
    	 
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

  };

  const handleInputChange = (event)=>{
    event.preventDefault();
    // console.log(event.target.value)

    var dropdown = document.getElementById('libraries');
    dropdown.addEventListener('change', function(){
        console.log(dropdown.value)
    });

  }

  const onBack = ()=> {
  	navigate(-1)
  }

  return(
  	   <div>
  	   	<Button variant="contained" onClick = {onBack}>Back</Button>
  		<form class="form-container" onSubmit={handleSubmit}>
    		<input type="text" class="form-input" id = "cpu" placeholder="Please Enter the CPU Requirements"/>
    	 	<input type="text" class="form-input" id = "gpu" placeholder="Please Enter the GPU Requirements"/>
    		<input type="text" class="form-input" id = "ram" placeholder="Please Enter the RAM Requirements"/>
    		<input type="text" class="form-input" id = "storage" placeholder="Please Enter the Storage Requirements"/>
        <input type="text" class="form-input" id = "storageType" placeholder="Please Enter the Storage LifeCycle"/>

        <input type="text" class="form-input" id = "external" placeholder="Please Enter the External Port"/>
        <input type="text" class="form-input" id = "internal" placeholder="Please Enter the Internal Port"/>
        <input type="text" class="form-input" id = "protocol" placeholder="Please Enter the Protocol"/>

        <input type="text" class="form-input" id = "dsVersion" placeholder="Please Enter the DS Version"/>
        <input type="text" class="form-input" id = "bucket" placeholder="Please Enter the Bucket"/>
        <input type="text" class="form-input" id = "filename" placeholder="Please Enter the Filename"/>

        <input type="text" class="form-input" id = "envname" placeholder="Please Enter the Environment name"/>
        <input type="text" class="form-input" id = "version" placeholder="Please Enter the Version name"/>


    		<select id = "os" class="form-dropdown" onChange={handleOsDropdownChange} value={osSelected}>
    			<option value="" selected disabled>Please Select an OS to work on</option>
    			<option value="ubuntu">ubuntu</option>
    			<option value="alpine">alpine</option>
    		</select>
    		<select class="form-dropdown" onChange={handleDropdownChange} value={selectedOption}>
    			<option value="" selected disabled>Please select a Programming Language</option>
    			<option value="python">python</option>
    			// <option value="node.js">node.js</option>
    			// <option value="goLang">goLang</option>
    		</select>
      
    		

        <Select
        options={library}
        value={selectedOptions}
        isMulti={true}
        onChange={handleSelectChange}
        placeholder="Please select a Libraries to work with"
      />

    		
   			 <button type="submit" class="form-submit" >Submit</button>
   		 </form>
   		</div>
  );
};






export default MyForm;