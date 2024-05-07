# Analyzing-laptop-sold-on-Tiki
This is my personal project aimed at analyzing data of laptops sold on the Tiki website. I use Python to collect data through APIs, perform data cleaning, and utilize Power Bi for data visualization and analysis.

# Crawl data
Make sure your laptop/PC have Python installed. Steps to crawl data:
+ Open Command Prompt at the folder. Run file "crawl_id.py" first to obtain the id of each product on Tiki's laptop page.
Command: `python crawl_id.py`
+ Run "crawl_product.py" next to gather all the information about each laptop.
Command: `python crawl_product.py`
+ Run "crawl_comment.py" to retrieve comments.
Command: `python crawl_comment.py`

# Clean data
There is a jupyter notebook "clean_data.ipynb" containing the code for data cleaning.

# Visualize data
Open the PowerBi report file "report_tiki.pbix" to view my visualizations.

# Analytics
A Word file "tiki_report.docx" contains my analysis.
