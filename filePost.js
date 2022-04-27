var fs = require('fs');
var express=require('express')
const { v4: uuidv4 } = require('uuid');
const session = require('cookie-session') 
window=require('buffer')
var app=express.Router()
var sql=require('./getSql')
fs = require('fs');
app.use(express.json())
app.use(express.urlencoded({extended:true}))
var formidable = require('formidable');
const { writeFile } = require('fs');
app.use(session({secret: 'Your_Secret_Key',resave:false,saveUninitialized:false}))
app.post('/filePost',(req,res)=>{

    async function b642ab(base64string){
        return Buffer.from(base64string,'base64')
      }

    function trainModel(fname)
    {
        
        console.log('here')
        const { spawn } = require('child_process');
        const child = spawn('python', ['model.py',fname], {shell: true});
        child.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
        if(data=="done")
        {
            console.log("done")
            res.send("ok")
        }
        });

        child.stderr.on('data', (data) => {
            console.log(`stdout: ${data}`);
            });

        child.on('error',(err)=>{
            console.log(err)
        })
        child.on('exit',(code)=>{
             console.log('exit')
             data = fs.readFileSync('train_accuracy_visual.json');
             data = JSON.parse(data);
             data1= fs.readFileSync('prediction_visual.json');
             data1=JSON.parse(data1);
             const child1 = spawn('python', ['visualization.py',fname], {shell: true});
             child1.on('exit',(code)=>{
             res.send(JSON.stringify({v1:data,v2:data1}))
            })
        })
    }


    //console.log("Ye toh theek hai")
    const form = new formidable.IncomingForm();
    form.maxFileSize = 300 * 1024 * 1024;
    form.parse(req, async function(err, fields, files){
        fname=fields['fname']
        uname=fields['user']
        filedata=fields['filedata']
        ext=fields['ext']
        fs.writeFileSync('public//home//uploads/'+fname, filedata, 'base64');
        trainModel(fname)
    })
})

module.exports=app