#####################################################
# validation run script for 1D supersonic flow code #
# developed by: Ramkumar			    #
#####################################################

# runing first script and renaming the output
python3 script21.py
mv Data.csv Data21.csv

# runing 2nd script and renaming the output
python3 script41.py
mv Data.csv Data41.csv

# runing 3rd and renaming the output
python3 script81.py
mv Data.csv Data81.csv

# running validation script
python3 validator.py

echo "Done Computation"
