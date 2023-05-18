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

import {SHOW_CONFIGS_URL, DEPLOYMENT_URL, CHECK_STATUS_URL, STOP_URL} from './constants.js'


const Config =()=>{
  let deployedConfigId = ''
  const [isDeployed, setIsDeployed] = useState(false);
  const checkStatus = ()=>{
    // let deployedConfigId_1 = document.getElementById('deploy_id').value;
    let url1= CHECK_STATUS_URL+deployedConfigId
    console.log(url1, ' ', deployedConfigId)
    fetch(url1)
      .then(response => response.json())
      .then(data=> {
        console.log(data['status'])
        if(data['status'] == 0){
          alert(deployedConfigId + ' is pending deployment ')
        }
        else if(data['status'] == 1){
          alert(deployedConfigId + ' is deployed successfully ')
        }
        else if(data ['status']== 2){
          alert(deployedConfigId + ' is deployment failed ')
        }
        else if(data['status'] == 3){
          alert(deployedConfigId + ' container is stopped')
        }
        else{
          alert('not yet deployed')
        }
      })
  }

  const handleChange= (event)=>{
    deployedConfigId = event.target.value;
    console.log(deployedConfigId)
  }

  const handleSubmit = ()=>{
    console.log(deployedConfigId)
    let url = DEPLOYMENT_URL+deployedConfigId
    console.log(url);

    const data = {
      'config-id': deployedConfigId
    }

    const jsonData = JSON.stringify(data)


    fetch(url, {
     method:'POST',
     headers: { 'Content-Type': 'application/json' },
     body: jsonData

      
       
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

    setIsDeployed(true);
  }

  const handleStop = ()=>{
    // setIsDeployed(false)
    let stop_url = STOP_URL+deployedConfigId

    const data = {
      'config-id': deployedConfigId
    }

    const jsonData = JSON.stringify(data)

    fetch(stop_url, {
     method:'POST',
     headers: { 'Content-Type': 'application/json' },
     body: jsonData

      
       
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));

    setIsDeployed(false);


  }

	// const handleSubmit= ()=>{
	// 	const data = {
	// 		'config-id': document.getElementById("configId").innerHTML.slice(10,document.getElementById("configId").innerHTML.length)
	// 	}
 //     // console.log(configId)
	// 	let configId = document.getElementById("configId").innerHTML.slice(10,document.getElementById("configId").innerHTML.length)
	// 	configId = configId.slice(2, configId.length - 1)

	// 	let url = 'http://192.168.0.241:8003/provision/'+configId
	// 	console.log(configId+ " "+ url)

	// 	const jsonData = JSON.stringify(data);


 //    	fetch(url, {
 //    	method:'POST',
 //    	headers: { 'Content-Type': 'application/json' },
 //    	body: jsonData

    	
    	 
 //    })
 //    .then(response => response.json())
 //    .then(data => console.log(data))
 //    .catch(error => console.error(error));

 //    deployedConfigId = configId;


	// }

//   useState(()=>{
//     fetch(SHOW_CONFIGS_URL)
//     .then(response => response.json())
//     .then(data => {
//       const cardContainer = document.querySelector('#card-container1');
//       for(let i = 0;i<data.length;i++){
//           const card = document.createElement('div');
//             card.classList.add('card');

//       // Create the card body element
//               const cardBody = document.createElement('div');
//               cardBody.classList.add('card-body');

      

//       cardBody.innerHTML = `
//         <Card className="card-style">
//       <Card.Body>
//         <p id = "templateId">template-id: ${data[i]['message']}</p>
//         <Card.Text>
          
//           <ListGroup>
//             <ListGroup.Item id="os">OS: ${data[i]['message']} </ListGroup.Item><br>
//             <ListGroup.Item id="language">Language: ${data[i]['message']}</ListGroup.Item><br>
//           </ListGroup>
//         </Card.Text>
//         <p> Here are the libraries</p>
        
//       </Card.Body>
//     </Card>`
// const listGroup = document.createElement('div');
//     listGroup.classList.add('list-group');
//     const items = ['Item 1', 'Item 2', 'Item 3'];

// items.forEach(item => {
//   const listItem = document.createElement('div');
//   listItem.classList.add('list-group-item');
//   listItem.textContent = item;
//   listGroup.appendChild(listItem);
// });

// cardBody.appendChild(listGroup);



// const button = document.createElement('button');
// button.classList.add('btn', 'btn-primary', 'submit-button');
// button.textContent = 'Submit';



// // cardBody.appendChild(button);

//     card.appendChild(cardBody);
//     cardContainer.appendChild(card);
//       }
//     })
//   }, [])


	useEffect(()=>{
    console.log(SHOW_CONFIGS_URL);
		fetch(SHOW_CONFIGS_URL)
			.then(response => response.json())
			.then(data=> {
        console.log(data);
				console.log(data['response'].length);
				
				const cardContainer = document.querySelector('#card-container1');
				for (let i = 0;i<data['response'].length;i++){
					// console.log(data[i])
         if(1 ){
					const card = document.createElement('div');
            		card.classList.add('card');

      // Create the card body element
              const cardBody = document.createElement('div');
              cardBody.classList.add('card-body');
              const items = data['response'][i]['languages'][0]['libraries']
              console.log(items)

      let configId = JSON.stringify(data['response'][i]['_id'])
      configId = configId.slice(8, configId.length-1)
      console.log(configId)

      cardBody.innerHTML = `
        <Card className="card-style">
      <Card.Body>
        <p id = "configId">config-id: ${configId}</p>
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

const button = document.createElement('button');
button.classList.add('btn', 'btn-primary', 'submit-button');
button.textContent = 'Deploy';
button.addEventListener('click', handleSubmit);




// Add the ListGroup to the Card Body
cardBody.appendChild(listGroup);
// cardBody.appendChild(button);
card.appendChild(cardBody);
cardContainer.appendChild(card);
}
				}
			})
	.catch(error => console.error(error));
	}, [])

	return(
		<div>
      <input type="text" class="deploy_id" id = "configid" placeholder="Please Enter the Config you want to deploy" onChange = {handleChange}/>
      <Button variant="contained" class = "submit config" onClick={handleSubmit}>Deploy</Button>

      <Button variant="contained" class = "check status button" onClick={checkStatus}>Check Status of deployed</Button>
      <Button variant="contained" class = "check status button" onClick={handleStop}>Stop</Button>

      <div id="card-container1" class="card-deck">
      
    </div>
    </div>
		);
}

export default Config;