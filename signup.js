var express=require('express')
var session=require('cookie-session')
var app=express.Router()
app.use(express.static(__dirname + '/public/signup'));
app.use(express.urlencoded({extended:true}))
app.use(express.json())
app.use(session({secret:'hello123',resave:false,saveUninitialized:false}))
var sql=require('./getSql.js')
app.get('/',(req,res)=>{
    res.render('index.ejs')
})

app.post('/signup',(req,res)=>{
    uname=req.body.uname;
    password=req.body.password;
    vals=[]
    vals.push(uname)
    vals.push(password)
    if(!uname||!password)
    res.send("empty")
    else
    {
        var query="insert into users(name,password)values(?,?);"
        sql.execute(query,vals,(err,result)=>{
            if(err)throw err
            else
            res.send("ok")
        })
    }
})
module.exports=app