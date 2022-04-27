var express=require('express')
var session=require('cookie-session')
var app=express.Router()
app.use(express.static(__dirname + '/public/login'));
app.use(express.urlencoded({extended:true}))
app.use(express.json())
app.use(session({secret:'hello123',resave:false,saveUninitialized:false}))
var sql=require('./getSql.js')
app.get('/login',(req,res)=>{
    res.render('login.ejs')
})

app.post('/login',(req,res)=>{
    uname=req.body.uname;
    password=req.body.password;
    if(!uname||!password)
    res.send("empty")
    else
    {
        var query="select * from users where name=? and password=?"
        vals=[]
        vals.push(uname)
        vals.push(password)
        sql.execute(query,vals,(err,result)=>{
            if(err)throw err
            else
            {
                if(result.length){
                res.send("ok")
                req.session.take=result[0].name
                console.log(result[0].name,req.session.take)
                }
                else
                res.send("not ok")
            }
        })
    }
})
module.exports=app