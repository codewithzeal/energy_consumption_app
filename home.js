var express=require('express')
var app=express.Router()
app.use(express.json())
app.use(express.urlencoded({extended:true}))
app.use(express.static(__dirname+'/public/home'))
var sql=require('./getSql.js')
var session=require('cookie-session')
app.use(session({secret:'hello123',resave:false,saveUninitialized:false}))
app.get('/home',(req,res)=>{
    res.render('home.ejs',{uid:req.session.name})
})
module.exports=app