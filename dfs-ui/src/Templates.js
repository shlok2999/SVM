import React, { useState, useEffect } from "react";
// import Button from '@material-ui/core/Button';
import Button from '@mui/material/Button';

import ListGroup from 'react-bootstrap/ListGroup';
import Card from 'react-bootstrap/Card';
import { useLocation, useNavigate } from "react-router-dom";
import './App.css';
import { ProgressBar } from 'react-bootstrap';
import { Spinner } from 'react-bootstrap';

import { Modal, Form } from 'react-bootstrap';
import {SHOW_TEMPLATES_URL, SAVE_TO_CONFIG_URL} from './constants.js'

const Templates = ()=>{

	const navigate = useNavigate();
    const location = useLocation();
    const items = location.state.obj.libraries;
    const [loading, setLoading] = useState(false);

    const [isTemplate, setIsTemplate] = useState(true)

    const [externlPort, setExternlPort] = useState('');
    const [internalPort, setInternalPort] = useState('');
    const [protocol, setProtocol] = useState('');

    const [cardData, setCardData] = useState({});
    let temp_external_port = ''
    let temp_internal_port = ''
    let temp_protocol = ''

    let temp_dsVersion = ''
    let temp_fileName = ''
    let temp_bucketName = ''

    let temp_cpu = ''
    let temp_gpu = ''
    let temp_memory = ''
    let temp_storage = ''
    let temp_storage_lc = ''
    let temp_storage_target = '/target'

    let temp_env_name  = ''
    let temp_version = ''

    let node_monitor_ip = ''
    let dfs_server_ip = ''
    let node_monitor_port = ''
    let dfs_server_port = ''

// Define the onChange event handler for each input element
      const handleExternalChange = (event) => {
        const temp_selected  = event.target.value
        // console.log(temp_selected)
        setExternlPort(temp_selected);
        temp_external_port = temp_selected
        console.log(temp_external_port)
      }

    const handleInternalChange = (event) => {
      const temp_selected  = event.target.value
      // console.log(temp_selected)
      setInternalPort(temp_selected);
      temp_internal_port = temp_selected
      console.log(temp_internal_port)
    }

    const handleProtocolChange = (event) => {
      const temp_selected  = event.target.value
      // console.log(temp_selected);
      setProtocol(temp_selected);
      temp_protocol = temp_selected
      console.log(temp_protocol)
    }

    const handleDSVersionChange = (event)=>{
        temp_dsVersion = event.target.value;
    }

    const handleFileNameChange = (event)=>{
      temp_fileName = event.target.value;
    }

    const handleBucketNameChange = (event) =>{
        temp_bucketName = event.target.value;
    }

    const handleCPUChange = (event) =>{
        temp_cpu = event.target.value
    }

    const handleGPUChange = (event)=>{
      temp_gpu = event.target.value
     }

     const handleMemoryChange = (event)=>{
      temp_memory = event.target.value
     }

     const handleStorageChange = (event)=>{
      temp_storage = event.target.value
     }

     const handleStorageLifeCycleChange = (event)=>{
      temp_storage_lc = event.target.value
     }

     const handleEnvironmentNameChange = (event)=>{
      temp_env_name = event.target.value
     }

     const handleVersionChange = (event)=>{
      temp_version = event.target.value
     }

    
    console.log(items)

    const handleSubmit = (event)=>{
    	// console.log(document.getElementById("storage").innerHTML.slice(9,document.getElementById("storage").innerHTML.length));
      event.preventDefault();
      var form = event.target;
      // console.log(form.external_port)
      // console.log(form)

      console.log(temp_bucketName + " " + temp_fileName + " " + temp_dsVersion);
      

    	const data = {
        os: document.getElementById("os").innerHTML.slice(4,document.getElementById("os").innerHTML.length),
    		
        'isTemplate' : 1,
        'template-id' : document.getElementById("templateId").innerHTML.slice(13,document.getElementById("templateId").innerHTML.length-1),

        languages:[
           {
          'language-name': document.getElementById("language").innerHTML.slice(10,document.getElementById("language").innerHTML.length),
          'libraries': items
         }
        ],
        resources:{
          cpu: temp_cpu,
          gpu : temp_gpu,
          ram: temp_memory
        },
        'port-publish':[
          {
            external: {
              ports: temp_external_port
            },
            internal:{
              ports: temp_internal_port,
              protocol: temp_protocol
            }
          }
        ],
        'dataset':{
          'version':temp_dsVersion,
          'filename': temp_fileName,
          'bucketname': temp_bucketName
        },
          'env-name': temp_env_name,
          'version': temp_version
    	};
    	const jsonData = JSON.stringify(data);

      const config_save_url = SAVE_TO_CONFIG_URL;

    	fetch(config_save_url, {
    	method:'POST',
    	headers: { 'Content-Type': 'application/json' },
    	body: jsonData

    	
    	 
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

      setLoading(true);
    }


    

  


  useEffect(() => {


    const template_url = SHOW_TEMPLATES_URL;

    console.log(template_url + " "+SAVE_TO_CONFIG_URL)

    fetch(template_url)
     .then(response => response.json())
      .then(data => {
        console.log(data);
        const cardContainer = document.querySelector('#card-container');
          for(let i = 0;i<data['response'].length;i++){
            const card = document.createElement('div');
            card.classList.add('card');

      // Create the card body element
              const cardBody = document.createElement('div');
              cardBody.classList.add('card-body');

      

    //   cardBody.innerHTML = `
    //     <Card className="card-style">
    //   <Card.Body>
    //     <p id = "templateId">template-id: ${data[i]['message']}</p>
    //     <Card.Text>
          
    //       <ListGroup>
    //         <ListGroup.Item id="os">OS: ${data[i]['message']} </ListGroup.Item><br>
    //         <ListGroup.Item id="language">Language: ${data[i]['message']}</ListGroup.Item><br>
    //       </ListGroup>
    //     </Card.Text>
    //     <p> Here are the libraries</p>
        
    //   </Card.Body>
    // </Card>
      // `

    // const card = document.createElement('div');
    //   card.classList.add('card');

      // Create the card body element
              // const cardBody = document.createElement('div');
              // cardBody.classList.add('card-body');
              const items = data['response'][i]['languages'][0]['libraries']
              console.log(items)

      let configId = JSON.stringify(data['response'][i]['_id'])
      configId = configId.slice(8, configId.length-1)

      cardBody.innerHTML = `
        <Card className="card-style">
      <Card.Body>
        <p id = "templateId">templateId: ${configId}</p>
        <Card.Text>
          
          <ListGroup>
            <ListGroup.Item id="os">OS: ${data['response'][i]['os']} </ListGroup.Item><br>
            <ListGroup.Item id="cpu">CPU: ${data['response'][i]['resources']['cpu']} </ListGroup.Item><br>
            <ListGroup.Item id="gpu">GPU: ${data['response'][i]['resources']['gpu']}</ListGroup.Item><br>
            <ListGroup.Item id="memory">memory: ${data['response'][i]['resources']['ram']}</ListGroup.Item><br>
            <ListGroup.Item id="language">Language: ${data['response'][i]['languages'][0]['language-name']}</ListGroup.Item><br>
          </ListGroup>
        </Card.Text>
        <p> Here are the libraries</p>
        
      </Card.Body>
    </Card>
      `

      const listGroup = document.createElement('div');
    listGroup.classList.add('list-group');

// Create the list items
// const items = ['Item 1', 'Item 2', 'Item 3'];

items.forEach(item => {
  const listItem = document.createElement('div');
  listItem.classList.add('list-group-item');
  listItem.textContent = item;
  listGroup.appendChild(listItem);
});

// Add the ListGroup to the Card Body
cardBody.appendChild(listGroup);

const inputGroup = document.createElement('FORM');
// inputGroup.classList.add('input-group', 'mb-3');
cardContainer.appendChild(inputGroup);


const input1 = document.createElement('input');
input1.setAttribute('type', 'text');
input1.setAttribute('placeholder', 'External Port');
input1.setAttribute('id', 'external_port');
// input1.classList.add('form-control');
input1.addEventListener('change', handleExternalChange);

const input2 = document.createElement('input');
input2.setAttribute('type', 'text');
input2.setAttribute('placeholder', 'Internal Port');
input2.setAttribute('id', 'internal_port');
// input2.classList.add('form-control');
input2.addEventListener('change', handleInternalChange);

const input3 = document.createElement('input');
input3.setAttribute('type', 'text');
input3.setAttribute('placeholder', 'Protocol');
input3.setAttribute('id', 'protocol');
// input3.classList.add('form-control');
input3.addEventListener('change', handleProtocolChange);

// Add the input elements to the Card Body
inputGroup.appendChild(input1);
inputGroup.appendChild(input2);
inputGroup.appendChild(input3);

const datasetInputGroup = document.createElement('FORM');
// inputGroup.classList.add('input-group', 'mb-3');
cardContainer.appendChild(datasetInputGroup);

const input4 = document.createElement('input');
input4.setAttribute('type', 'text');
input4.setAttribute('placeholder', 'Dataset Version Number');
// input4.setAttribute('id', 'external_port');
// input1.classList.add('form-control');
input4.addEventListener('change', handleDSVersionChange);

const input5 = document.createElement('input');
input5.setAttribute('type', 'text');
input5.setAttribute('placeholder', 'File name');
// input5.setAttribute('id', 'internal_port');
// input2.classList.add('form-control');
input5.addEventListener('change', handleFileNameChange);

const input6 = document.createElement('input');
input6.setAttribute('type', 'text');
input6.setAttribute('placeholder', 'Bucket Name');
// input6.setAttribute('id', 'protocol');
// input3.classList.add('form-control');
input6.addEventListener('change', handleBucketNameChange);

// Add the input elements to the Card Body
datasetInputGroup.appendChild(input4);
datasetInputGroup.appendChild(input5);
datasetInputGroup.appendChild(input6);

// const resoucesGroup = document.createElement('FORM');
// // inputGroup.classList.add('input-group', 'mb-3');
// cardContainer.appendChild(resoucesGroup);

// const input7 = document.createElement('input');
// input7.setAttribute('type', 'text');
// input7.setAttribute('placeholder', 'CPU');
// input7.addEventListener('change', handleCPUChange);

// const input8 = document.createElement('input');
// input8.setAttribute('type', 'text');
// input8.setAttribute('placeholder', 'GPU');

// input8.addEventListener('change', handleGPUChange);

// const input9 = document.createElement('input');
// input9.setAttribute('type', 'text');
// input9.setAttribute('placeholder', 'Memory');

// input9.addEventListener('change', handleMemoryChange);

// const input10 = document.createElement('input');
// input10.setAttribute('type', 'text');
// input10.setAttribute('placeholder', 'Storage ');

// input10.addEventListener('change', handleStorageChange);

// const input11 = document.createElement('input');
// input11.setAttribute('type', 'text');
// input11.setAttribute('placeholder', 'Storage Lifecycle');

// input11.addEventListener('change', handleStorageLifeCycleChange);

// const input12 = document.createElement('input');
// input12.setAttribute('type', 'text');
// input12.setAttribute('placeholder', 'Storage Target');

// // input12.addEventListener('change', handleStorageTargetChange);

// // Add the input elements to the Card Body
// resoucesGroup.appendChild(input7);
// resoucesGroup.appendChild(input8);
// resoucesGroup.appendChild(input9);
// resoucesGroup.appendChild(input10);
// resoucesGroup.appendChild(input11);
// resoucesGroup.appendChild(input12);

const inputGroup_extras = document.createElement('FORM');
// inputGroup.classList.add('input-group', 'mb-3');
cardContainer.appendChild(inputGroup_extras);

const envname = document.createElement('input');
envname.setAttribute('type', 'text');
envname.setAttribute('placeholder', 'Environment name');

envname.addEventListener('change', handleEnvironmentNameChange);

const version = document.createElement('input');
version.setAttribute('type', 'text');
version.setAttribute('placeholder', 'Version');

version.addEventListener('change', handleVersionChange);

inputGroup_extras.appendChild(envname);
inputGroup_extras.appendChild(version);








const button = document.createElement('button');
button.classList.add('btn', 'btn-primary', 'submit-button');
button.textContent = 'Submit';
button.addEventListener('click', handleSubmit);


cardBody.appendChild(button);
// inputGroup.appendChild(s);

console.log(cardBody)


card.appendChild(cardBody);
       // card.appendChild(inputGroup)
console.log(card)




      
      cardContainer.appendChild(card);
      
          }
    })
      .catch(error => console.error(error));
  }, []);


	return(
		<div>
      {loading && <div>

        <p> it is loading...</p>

        </div>}
			
    <div id="card-container" class="card-deck">

    
      
    </div>
    </div>
		);
}



export default Templates;