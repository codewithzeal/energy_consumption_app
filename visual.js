var express=require('express')
var app=express.Router()
app.use(express.json())
app.use(express.urlencoded({extended:true}))
var fs = require('fs');
app.use(express.static(__dirname+'/public/visual'))
app.get('/visual',(req,res)=>{
    if(fs.existsSync('forecast.json')&&fs.existsSync('anomly.json'))
    res.render('visual.ejs')
    else
    res.redirect('/home')
})
module.exports=app