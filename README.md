# Stock Futures Analysis

## Introduction
This repository contains tools and scripts for analyzing stock futures. The goal is to provide insights and predictions based on historical data and various financial indicators.

## Features
- Data collection from Shioaji APIs
 https://sinotrade.github.io/zh_TW/

- Test with jupyter notebook

## Installation
To use the tools in this repository, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/zongyiu/stock_futures.git
    ```
2. Navigate to the project directory:
    ```bash
    cd stock_futures
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
### Install Talib

https://github.com/TA-Lib/ta-lib-python

#### Step 1 prepare c library
```
$ wget https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz/download -O ta-lib-0.4.0-src.tar.gz
$ tar -xzf ta-lib-0.4.0-src.tar.gz
$ cd ta-lib/
$ ./configure --prefix=/usr
$ make
$ sudo make install
```
#### Step 2 pip install

$ pip install TA-Lib



## Usage
1. Load DB from my private resource:
    ```
    ./db/future_kbars.db
    ```
2. Workstation:
    ```
    ./workstation
    ```
3. Source Code:
    ```
    ./source
    ```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For any questions or suggestions, please open an issue or contact [your email](mailto:zongyiu.ho@gmail.com).
