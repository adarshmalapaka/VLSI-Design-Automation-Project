# EC704-VLSI Design Automation Project


## Partitioning

### KL Algorithm

To run KL partitioning:<br/>

`python kl_algorithm.py <ISC_FILENAME> <RANDOM>`
 
Arguments:  <br/>
 
* `<ISC_FILENAME>` 
  * Input ISC file with extension. Ex: s298.isc 
* `<RANDOM>` 
  * ‘1’ for initial partitioning the nodes randomly.  
  * ‘0’ for initial partitioning the nodes in the order in which they appear in `<ISC_FILENAME>`. 
  * Default value is ‘0’  

For Example: <br/>
`python kl_algorithm.py s298.isc 0` 

### SA Algorithm

To run SA partitioning: <br/>

`python sa_algorithm.py <ISC_FILENAME> <RANDOM>`
 
Arguments:  <br/>
 
* `<ISC_FILENAME>` 
  * Input ISC file with extension. Ex: s298.isc 
* `<RANDOM>` 
  * ‘1’ for initial partitioning the nodes randomly.  
  * ‘0’ for initial partitioning the nodes in the order in which they appear in `<ISC_FILENAME>`. 
  * Default value is ‘0’ 
           
For Example: <br/>
`python sa_algorithm.py s298.isc 1`

