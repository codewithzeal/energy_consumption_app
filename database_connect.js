const mysql=require('mysql2');
var mydb
var log={
    connect:function()
    {
    
    var config=
    {
        host:"" ,    
	    port:"3306",
        user: '',
        password: '',
        database: 'tarp'
    }
    const db=mysql.createConnection(config);
    return db;
}
}
module.exports=log;