var db=require('./database_connect.js')
sql=db.connect((err)=>{
    if(err)
    {
        console.log('There was an error');
    }
   console.log("connected sucessfully")
})
/* query="INSERT INTO `users` (`s_id`, `name`, `password`, `date`) VALUES(1, 'kareem', '1234', '2022-04-21');"
sql.query(query,(err,result)=>{
    console.log(err)
}) */
module.exports=sql; 