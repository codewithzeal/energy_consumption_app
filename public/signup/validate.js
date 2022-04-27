function validate()
{
    uname=document.getElementById("uname").value;
    password=document.getElementById("password").value;
    if(!uname||!password)
    alert("check your inputs")
    else
    {
        $.ajax(
            {
                url:'/signup',
                method:'POST',
                contentType:'application/json',
                data:JSON.stringify({uname:uname,password:password}),
                success:function(response)
                {
                    if(response=="empty")
                    alert("error 1 occured")
                    else if(response=="ok")
                    alert("registered")
                    else
                    alert("error 2 occured")
                },
                error:function()
                {
                    alert("error 3 occured")
                }
            }
        )
    }
}