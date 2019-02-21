# ctp-market

An program used to provide data-recording service


## Prepare the Environment
- vnpy installation

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[gateway](https://github.com/vnpy/vnpy)

- libraries 
```bash
git clone https://github.com/somewheve/ctp-market
cd ctp-market
pip install requirements.txt -i https://pypi.douban.com/simple
ln -s /home/username/anaconda2/bin/tcping /usr/bin/tcping
```

## Usage
```bash
    # warning :
    #    1, make sure the database connection info which you choose was provided in config.py
    #    2, you can create a new any setup py file , just ensure that this file was registered by App Instance  
    # An example program  was provided named run.py
    
    # recommandation :
    # read it before you run this file 
   
    cd ctp-market & python run.py

```





## 特点

- Support more than one database ['mysql', 'mongodb', 'redis']

- Easier to learn and alter  

- Support multiple market address and get the fastest one  

