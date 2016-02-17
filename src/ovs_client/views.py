from django.shortcuts import render

# Create your views here.

import socket
import json

buffer = 65536

def ovsdb_list_dbs(request, ovs_address):
    address = ovs_address.split(":")
    ip = address[0]
    port = int(address[1])
    values = {"list_dbs":[],
              "ovs_address":ovs_address,
              }
    try:
        s = ovsdb_connect(ip, port)
        values["list_dbs"] = get_list_dbs(s)
    except Exception as e:
        values["list_dbs"] = [e]
    return render(request, 'ovs_client/ovsdb_list_dbs.html', values)

def ovsdb_table_list(request, ovs_address, db_name):
    address = ovs_address.split(":")
    ip = address[0]
    port = int(address[1])
    values = {"schema":[],
              "ovs_address":ovs_address,
              "db_name":db_name,
              }
    try:
        s = ovsdb_connect(ip, port)
        schema_list = get_tables(s, db_name)
        table_list = schema_list['tables'].keys()
        values["table_list"] = table_list
    except Exception as e:
        values["schema"] = [e]
    return render(request, 'ovs_client/ovsdb_table_list.html', values)

def ovsdb_table_data(request, ovs_address, db_name, table_name):
    address = ovs_address.split(":")
    ip = address[0]
    port = int(address[1])
    values = {"schema":[],
              "ovs_address":ovs_address,
              "db_name":db_name,
              "table_name":table_name,
              }
    s = ovsdb_connect(ip, port)
    table_data = get_table_data(s, db_name, table_name)
    table_data = table_data[0]['rows']
    values['table_data'] = table_data
    try:
        values['key_values'] = table_data[0].keys()
    except Exception as e:
        print e
        values['datas'] = list()
        return render(request, 'ovs_client/ovsdb_table_data.html', values)
        
    values['datas'] = list()
    for data in table_data:
        values['datas'].append(data.values())
    
    return render(request, 'ovs_client/ovsdb_table_data.html', values)


def ovsdb_connect(ovsdb_ip, ovsdb_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ovsdb_ip, ovsdb_port))
    except Exception as e:
        raise e
    return s

def get_list_dbs(s):
    query_json = {
                    "method": "list_dbs",
                    "params":[],
                    "id": 2003
                }
    query_string = json.dumps(query_json)
    s.send(query_string)
    response = s.recv(buffer)
    json_dump = json.loads(response)
#     print json.dumps(json_dump, indent=4)
    return json_dump["result"]

def get_tables(s, db_name):
    query_json = {
                    "method": "get_schema",
                    "params":[db_name],
                    "id": 2003
                }
    query_string = json.dumps(query_json)
    s.send(query_string)
    response = s.recv(buffer)
    json_dump = json.loads(response)
#     print json.dumps(json_dump, indent=4)
    return json_dump["result"]

def get_table_data(s, db_name, table_name):
    query_json = {
                        "method": "transact",
                        "params":[
                                    db_name,
                                    {
                                        "op": "select",
                                        "table": table_name,
                                        "where" :[]
                                    }
                        ],
                        "id": 2003
                    }
#         query_json["params"][1]["columns"] = list()
#         query_json["params"][1]["columns"].append("name")
    query_string = json.dumps(query_json)
    s.send(query_string)
    response = s.recv(buffer)
    json_dump = json.loads(response)
#     print json.dumps(json_dump, indent=4)
    return json_dump['result']

def print_column(column):
    print "-----------"
    print len(column)
    for name in column:
        print name 