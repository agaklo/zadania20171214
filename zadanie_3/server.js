var express = require('express');
var url = require('url');
var app = express();

function validate_number(value, valueDescription){
    if( !/^[0-9]+$/.test(value)){ 
        throw Error("Wrong format of "+valueDescription) 
    }
    var valueAsInt = parseInt(value, 10);
    if( isNaN(valueAsInt) ){
        throw Error("Value "+valueDescription+" is not a number") 
    }
    return valueAsInt;
}

app.use(express.static('public'));
app.get('/', function (req, res) {
    var params = url.parse(req.url, true);
    var query = params.query;
    console.log("Input parameters: " + JSON.stringify(query));
    try{
        var a = validate_number(query.a, "input value a");
        var b = validate_number(query.b, "input value b");
        var result = a+b        
        console.log("Result: "+result.toString());
        res.end(result.toString());
    }catch(e){
        console.log(e);
        res.status(404).end(e.message);
    }
})

var server = app.listen(8080, function () {
   console.log('Listening on port: ' + server.address().port);
})
