var express=require('express')
var app=express.Router()
app.use(express.json())
app.use(express.urlencoded({extended:true}))
var fs = require('fs');
app.post('/fetch',(req,res)=>{
    if(fs.existsSync('forecast.json')&&fs.existsSync('anomly.json'))
    {
        data = fs.readFileSync('forecast.json');
        data = JSON.parse(data);
        data1= fs.readFileSync('anomly.json');
        data1=JSON.parse(data1);
        res.send(JSON.stringify({v1:data,v2:data1}))
    }
    else
    res.send("nok")
})
module.exports=app