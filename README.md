# Future Citation Count Prediction

We survey and compare different approaches that have been suggested in the past to solve the problem of predicting the future citation count of a scientific article after a given time interval of its publication. Further, we present a comparative evaluation of the popular h-index and p-rank(a PageRank inspired model for assessing author impact) metrics.

## Getting Started

### DATASET

We adopted the popular [Aminer dataset](https://aminer.org/citation).
The citation data is extracted from DBLP, ACM, and other sources. Each paper is associated with abstract, authors, year, venue, and title.


### Prerequisites  
`cd src`  

Download the dataset  

`
$./download_dataset.sh
`

##Pre-process the dataset  

`
$./pre-process.sh
`

### Train the model  


`
$python feats2seq.py
$python SAS.py
`

##RESULTS  
Check [Final_Report](https://github.com/sreekarcheg/Citation-Count-Prediction/blob/master/Final_Report.pdf) for results

## Built With

* [Keras](www.keras.io)  

* [seq2seq](https://github.com/farizrahman4u/seq2seq) - sequence to sequence learning add-on for the python deep learning library Keras  



## Authors

**Sree Ram Sreekar**   cs13b1008@iith.ac.in  
**Akshita Mittel**     cs13b1040@iith.ac.in  
**Surya Teja Chavali** cs13b1028@iith.ac.in  


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


