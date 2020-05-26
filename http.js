//
//  Mobile Food Facility Permit
//
//  Reads a CSV file (Mobile_Food_Facility_Permit.csv) that contains Food Truck
//  info.
//  The following URL is supported.
//
//      GET http://localhost:8080/food_trucks/?latitude:string?longitude:string
//
//          Returns (in JSON) Food Truck details for the given location.
//


var assert = require('assert');

var fs = require('fs');

const http = require('http');

const lineReader = require('line-reader');

var urlp = require('url');


var food_trucks = [];
var column_names = [];

const file_name = 'Mobile_Food_Facility_Permit.csv';
var row = 0;
lineReader.eachLine(file_name, function(line) {
    if (row == 0) {
        console.log();
        console.log(line + "\n");
        column_names = line.split(",");
        console.log('column_names.length = ' + column_names.length);
    } else {
        var words = line.split(",");
        var values = {};

        for (var index = 0; index < column_names.length; index++) {
            values[column_names[index]] = words[index];
        }

        food_trucks.push(values);
    }

    row++;
});


function parse_query(query_str) {
    // console.log();
    // console.log('parse_query(START) query_str = "' + query_str + '"');

    var obj = {};

    if (query_str.length == 0) {
        console.log('parse_query(END) null query');
        return obj;
    }

    var queries = query_str.split("?");
    // console.log('parse_query() queries.length = ' + queries.length);

    for (var index1 = 0; index1 < queries.length; index1++) {
        if (queries[index1].length > 0) {
            query = queries[index1].split("=");

            if (query.length != 2)
                throw new Error('ERROR : invalid query = ' +
                                queries[index1] + '\n' +
                                'A query must be of the form "tag : value"');

            obj[query[0]] = query[1];
        }
    }

    for (key in obj) {
        // console.log('parse_query() obj[' + key + '] = ' + obj[key]);
    }

    // console.log('parse_query(END)');
    return obj;
}


//
//  Display a object of HTTP headers.
//

function print_object(headers)
{
    for (key in headers)
        console.log('    ' + key + ' : ' + headers[key]);
}


//
//  Service the "food_trucks" query.
//
//  /food_trucks/<query>
//
//  Show Food Trucks for a given {latitude, longitude}.
//  Where <query> = "?latitude:string" and "?longitude:string".
//
//  Arguments:
//    search = query string.
//    items = object of parameters.
//    response = HTTP Response ptr for user output.
//

function process_food_trucks(search, items, response)
{
    // Debug.

    // console.log();

    // console.log('process_food_trucks(START)');
    // console.log('process_food_trucks() search = ' + search);
    // console.log('process_food_trucks() items = ');

    num_items = 0;
    for (key in items) {
        // console.log('    ' + key + ' : ' + items[key]);
        num_items += 1;
    }

    if (num_items == 0) {
        throw new Error('ERROR : missing query.');
    } else if (num_items != 2) {
        throw new Error('ERROR : invalid number of queries (2 required).');
    } else if (! ('latitude' in items)) {
        throw new Error('ERROR : missing "latitude" parameter.');
    } else if (! ('longitude' in items)) {
        throw new Error('ERROR : missing "longitude" parameter.');
    }

    // Run the SELECT query.

    response.write('{\n');
    response.write('    "latitude" : "' + items['latitude'] + '",\n');
    response.write('    "longitude" : "' + items['longitude'] + '",\n');
    response.write('    "trucks" : [\n');

    var found = 0;
    for (var index1 = 0; index1 < food_trucks.length; index1++) {
        if (food_trucks[index1]['Latitude'] != items['latitude']) {
            ;
        } else if (food_trucks[index1]['Longitude'] != items['longitude']) {
            ;
        } else {
            if ((index1 > 0) && (found == 1)) {
                response.write(',\n');
            }

            found = 1;
            response.write('        {\n');
            for (var index2 = 0; index2 < column_names.length; index2++) {
                if (index2 > 0) {
                    response.write(',\n');
                }

                name = column_names[index2];
                response.write('            "' + name + '" : "' +
                               food_trucks[index1][name] + '"');
            }
            response.write('\n');
            response.write('        }');
        }
    }

    response.write('\n');
    response.write('    ]\n');
    response.write('}\n');

    // Done.

    response.end();
    // console.log('process_food_trucks(END)');
}


//
//  Create a HTTP server.
//

http.createServer((request, response) =>
{
    var start = new Date();

    console.log();
    console.log('createServer(START) ' + start);

    const { headers, method, url } = request;

    console.log('createServer() headers = ');
    print_object(headers);
    console.log('createServer() method = ' + method);
    console.log('createServer() url = ' + url);

    let body = [];

    request.on('error', (err) => {
        console.error(err);
    }).on('data', (chunk) => {
        body.push(chunk);
    }).on('end', () => {
        body = Buffer.concat(body).toString();
        console.log('createServer() body = ' + body);

        response.on('error', (err) => {
            console.error(err);
        });

        var query = urlp.parse(url, true);

        console.log('createServer() pathname = ' + query.pathname);
        console.log('createServer() search = ' + query.search);

        try {
            query_dict = parse_query(query.search);

            if (query.pathname == '/food_trucks') {
                process_food_trucks(query.search, query_dict, response);
            } else if (query.pathname == '/food_trucks/') {
                process_food_trucks(query.search, query_dict, response);
            } else {
                response.write('Unknown action = ' + query.pathname);
                response.end();
            }
        } catch (ex) {
           response.write(ex.message);
            response.end();
        }
    });

    var end = new Date();
    console.log('createServer(END) ' + end);
}).listen(8080);


