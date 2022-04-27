var express=require('express')
var app=express.Router()
app.use(express.json())
app.use(express.urlencoded({extended:true}))
var fs = require('fs');
app.post('/check',(req,res)=>{
    const fs = require("fs");
    if(fs.existsSync('prediction_visual.json')&&fs.existsSync('train_accuracy_visual.json'))
    {
        data = fs.readFileSync('train_accuracy_visual.json');
        data = JSON.parse(data);
        data1= fs.readFileSync('prediction_visual.json');
        data1=JSON.parse(data1);
        res.send(JSON.stringify({v1:data,v2:data1}))
    }
    else
    res.send("nok")
})
module.exports=app