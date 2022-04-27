function login()
{
    uname=document.getElementById("name").value;
    password=document.getElementById("password").value;
    if(!uname||!password)
    alert("check your inputs")
    else
    {
        $.ajax(
            {
                url:'/login',
                method:'POST',
                contentType:'application/json',
                data:JSON.stringify({uname:uname,password:password}),
                success:function(response)
                {
                    if(response=="empty")
                    alert("error 4 occured")
                    else if(response=="ok")
                    window.location="https://tarp-app-naman.herokuapp.com/home"
                    else
                    alert("Check credentials")
                },
                error:function()
                {
                    alert("error 6 occured")
                }
            }
        )
    }
}