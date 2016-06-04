# curltocsv
Simple tool that collects timing info from curl for obtaining index.html from a domain

Example:

    python curltocsv.py -f format.txt -d www.cnn.com -w cnn.csv

Above collects data from www.cnn.com and writes it to cnn.csv

Example:

    python curltocsv.py -f format.txt --domainfile domains.txt --outdir csvtest -n 100 -s 5 -j

Above runs for each domain in domains.txt, writes results to a directory called csvtest, writes results as json, runs the command 100 times for each domain, and sleeps 5 seconds between each command.

