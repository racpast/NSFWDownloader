# **NSFW** Downloader

A program that can download **a large number of images of a certain type** from **a given database**, used for scraping images **to build a personal image hosting service**.

This project **references** the database **from** [**Mabbs · pixiv-index**](https://github.com/Mabbs/pixiv-index), and I will **update the database from time to time**.

*(Last update on Nov 17, 2024)*

Run `DownloadNSFW.py` in the same directory as the folder containing the json file to start the download. **If the program runs properly**, it will output logs in the console. Unparsed json files are stored by default in the folder specified by the `data_folder` variable. **If the image specified in a json file is successfully downloaded**, the json file is moved to the folder specified by the `data_downloaded_folder` variable. **Otherwise**, it will be moved to the folder specified by the `data_error_folder` variable. **All downloaded images are moved to the folder specified by the** `download_folder` **variable**.

In some cases, you may need to **change the address of the Pixiv image reverse proxy** manually. You can try using `https://i.pixiv.re`, but it seems that this proxy **will fail after receiving a constant flood of requests**, so the default `https://i.yuki.sh` is **the most stable** in my opinion. (I once ran a test with about **37,000** requests.)

The following is a table of **default values**:


| variable | default value |
| ------- | ------- |
| data_folder | data |
| data_error_folder | data_error |
| download_folder | download |
| data_downloaded_folder | data_downloaded |
| pixivimgrp | https://i.yuki.sh |


## 🚀 **Have fun!**
