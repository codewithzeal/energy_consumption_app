function check()
{
  $.ajax(
    {
      url:'/check',
      method:'POST',
      contentType:'application/json',
      success:function(res)
      {
        if(res!="nok")
        {
          plot(res)
          plot1(res)
        }
      },
      error:function()
      {
        alert("error 2atq occured")
      }
    }
  )
}
async function plot(res)
{
  res=JSON.parse(res)
  x11=res.v1['loss']
  x12=res.v1['val_loss']
  var trace1 = {
    x: [0,5,10,15,20,25,30],
    y: x11,
    type: 'scatter',
    name:'train'
  };
  
  var trace2 = {
    x: [0,5,10,15,20,25,30],
    y: x12,
    type: 'scatter',
    name:'test'
  };
  
  var data = [trace1, trace2];
  
  Plotly.newPlot('myPlot', data);
  return
// Display using Plotly
}


async function plot1(res)
{
  res=JSON.parse(res)
  x11=res.v2['y1']
  x12=res.v2['y2']
  var trace1 = {
    x: res.v2['x_values'],
    y: x11,
    type: 'scatter',
    name:'actual'
  };
  
  var trace2 = {
    x: res.v2['x_values'],
    y: x12,
    type: 'scatter',
    name:'prediction'
  };
  
  var data = [trace1, trace2];
  
  Plotly.newPlot('myPlot1', data);
  return
}


async function plot2()
{
  
}

function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
      x.className += " responsive";
    } else {
      x.className = "topnav";
    }
  }

function perform()
{
  document.getElementById('formFile').click();
}

function readFile(file){
  return new Promise((s,r)=>{
    fr=new FileReader()
    fr.readAsDataURL(file);
    fr.onload=async (e)=>
    {
        s(e.target.result.toString())
    }
  })
}

async function doUpload()
{
  var files=document.getElementById("formFile").files;
  file=files[0]
  await readFile(files[0]).then(async (fasb64)=>
  {
    fname=file.name
    a=fasb64
    ac=fasb64
    a=a.substring(a.indexOf(',')+1)
    bext=ac
    bext=bext.substr(0,bext.indexOf(',')+1)
    makeUpload(fname,a,bext)
  })
}

function makeUpload(fname,a,bext)
{
  document.getElementById("status").innerHTML="Loading..."
  var fd=new FormData()
  fd.append('user',getMyInfo())
  fd.append("fname",fname)
  fd.append("filedata",a)
  fd.append("ext",bext)
  $.ajax({
    url:'/filePost',
    method:'POST',
    contentType:false,
    processData:false,
    data:fd,
    success:async function(res)
    {
      if(res=="error")
      alert("some error occured please refresh")
      else
      {
        await plot(res)
        await plot1(res)
        document.getElementById("status").innerHTML="Your forecast"
      }
    },
    error:function(res)
    {
      alert("error occured please refresh")
      console.log(res)
    }
  })
}