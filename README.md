# LSCD DATA FETCH 康文署活動資料
Fetch the activities in the [LSCD website]( http://www.lcsd.gov.hk/tc/programmes/enrolment/enrolmentrsp.html)

## Getting Started

**Configurate Config.json**
> Set true in storage attribute when you use the storage system
```
{
"storage":{
"file":false, //use file to save the data
"mysql":true, //use mysql to save the data
"mongo":false //use mongodb to save the data
},
"storage_file":{
"path":"" //path to save the data
},
"mysql":{
"host":"xxx.xxx.xxx.xxx",//IP or the host of the mysql 
"port":3306, //default port is 3306 
"database":"lscd", 
"username":"username",
"password":"your password"
},"mongo":{ 
"host":"xxx.xxx.xxx.xxx",//IP or the host of the mongo 
"port":27017, //default port is 27017 
"database":"lscd"
},
"lang":{ //not using
"tc":"b5",
"sc":"b5&sc=sc",
"en":"en"
}
}
```

**Quick Start**
```
python act_fetcher.py
```

### Prerequisites

**Mac OS**
Python 2.7 (Default)

Install **[brew](https://brew.sh/)**
```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Install pip
``` 
$ sudo easy_install pip
```
Install MYSQL Driver
```
$ brew install mysql-connector-c
$ pip install mysql-python
```
Install Mongodb Driver
```
$ python -m pip install pymongo
```

### Installing
> clone the project to your project directory
```
$ git clone https://github.com/lokmannicholas/openapi_lscd_data_collector.git "project directory"
```

## Deployment

>System could be deploy on MacOS , Ubuntu, Debian , etc.

## Contributing

Please contact to know more

## Versioning

latest version [v1.0](https://github.com/lokmannicholas/openapi_lscd_data_collector/tags). 

## Authors

* **Lokmannicholas ng** - *Code building* - [Lokmannicholas](https://github.com/lokmannicholas)

See also the list of [contributors](https://github.com/lokmannicholas/openapi_lscd_data_collector/graphs/contributors) who participated in this project.

## Reference
* [康文署]( http://www.lcsd.gov.hk/) 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
