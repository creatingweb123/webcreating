import express from "express";
import axios from "axios";;

const app = express();
const port = 3000;
const API_URL = "https://secrets-api.appbrewery.com/";
//TODO 1: Fill in your values for the 3 types of auth.
const yourUsername = "123";
const yourPassword = "123";
const yourAPIKey = "a1cd5fe8-cbd8-4927-9676-adec873c1d6c";
const yourBearerToken = "ea14a823-0203-4ddc-87e7-d94c3b00f829";

app.get("/", (req, res) => {
  res.render("index.ejs", { content: "API Response." });
});

app.get("/noAuth", (req, res) => {
  axios.get(`${API_URL}random`)
  .then(function(response){
    var data = JSON.stringify(response.data);
    res.render("index.ejs",{content:data})
  })
  .catch(function(error){
    console.error("Failed to make request:", error.message);
  });
});

app.get("/basicAuth", (req, res) => {
  axios.get(`${API_URL}all`,{
    auth:{
      username: yourUsername,
      password: yourPassword
    },
    parmas:{
      page:1
    }
  })
  .then(function(response){
    var data = JSON.stringify(response.data);
    res.render("index.ejs",{content:data})
  })
  .catch(function(error){
    console.error("Failed to make request:", error.message);
  });

});

app.get("/apiKey", (req, res) => {
  axios.get(`${API_URL}filter`,{
    params:{
      apiKey:yourAPIKey,
      score:5
    }
  })
  .then(function(response){
    var data_api = JSON.stringify(response.data);
    res.render("index.ejs",{content:data_api})
  })
  .catch(function(error){
    console.error("Failed to make request:", error.message);
  });
});

app.get("/bearerToken", (req, res) => {
  axios.get(API_URL+"secrets/1",{
    headers: { 
      Authorization: `Bearer ${yourBearerToken}` 
    },
  })
  .then(function(response){
    var data_token = JSON.stringify(response.data);
    res.render("index.ejs",{content:data_token})
  })
  .catch(function(error){
    console.error("Failed to make request:", error.message);
  });

});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});


// axios.post(`${API_URL}register`,{
//   data:{
//     username:"123",
//     password:"123"
//   }
// })
// .then(function(response){

// })
// .catch(function())