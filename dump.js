async function visualize()
    {
        var val1
        var val2
        fs.readFile("prediction_visual.json", "utf8", (err, jsonString) => {
          if (err) {
            console.log("Error reading file from disk:", err);
            return;
          }
          try {
            val1 = JSON.parse(jsonString);


            fs.readFile("train_accuracy_visual.json", "utf8", (err, jsonString) => {
                if (err) {
                  console.log("Error reading file from disk:", err);
                  return;
                }
                try {
                  val2 = JSON.parse(jsonString);
                  res.send(JSON.stringify({v1:val1,v2:val2}))
                  return "ff"
                  //console.log("Customer address is:", customer.address); // => "Customer address is: Infinity Loop Drive"
                } catch (err) {
                  console.log("Error parsing JSON string:", err);
                }
              });


            //console.log("Customer address is:", customer.address); // => "Customer address is: Infinity Loop Drive"
          } catch (err) {
            console.log("Error parsing JSON string:", err);
          }
        });

        
         
    }