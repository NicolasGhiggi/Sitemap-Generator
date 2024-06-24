# Sitemap Generator

## Introduction
This script is designed to automate the creation of sitemaps in XML format. Just provide the link of the website to be mapped and the script will do the rest. The sitemap files are generated and saved in a newly created folder within your computer's download directory. The name of this folder will be in the format *sitemap_dd-mm-yyy_hh-mm-ss*.

In addition, to ensure good organization and optimize performance, URLs are divided into several sitemaps. Each sitemap will contain a maximum of 10000 URLs, so as to avoid overly large sitemaps and facilitate indexing by search engines.



## Utilize technologies
```
Programming language: Python
```



## Installation & Execution
- Install Python on your computer. You can install it through Microsoft store or you can download the .exe file from the official site (The recommended version for this script is 3.12.4 or up).
Link for install python:

```
https://www.python.org/downloads/windows/
````


- Start the script you can open the script with the python compiler you installed in first point or you go on the position of script and either with the command on terminal:

```
py sitemap_generator.py 
```


- Enter the link to the site you want to map, example: 

```
https://example.com
```