# FIB-UPC-LP-python-16S

Python project for the course of LP at the FIB, UPC. Spring semester of 2016

The project consisted on:

- Getting information about Bicing stations in Barcelona from [the following server](http://wservice.viabicing.cat/v1/getstations.php?v=1)
- Extract as much information as possible from the `rdf` file about restaurants in Barcelona and format it in a `csv` file
- Be able to call the script with a query string to search among the restaurants' information
  - Disjunction (OR) queries are formated as a python list
  - Conjunction (AND) queries are formated as a tuple
- The results must be presented in the form of a table in an `html` file, with all the information extracted on any restaurant that matches the query, as well as the Bicing stations under 1km of distance, ordered from closest to farthest, with empty bike parking lots, and also the Bicing stations with available bikes

Extracting the restaurants' data is done in the [`rdf2csv.py`](../blob/master/rdf2csv.py) file. Reading the Bicing server, taking the information from the `csv` file, and putting everything in the form of a (rather ugly, I admit) table in an `html` file is done in the [`csv2html.py`](../blob/master/csv2html.py) file.
