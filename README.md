# InsightDataEngineerChallenge

## Summary
My solution's logic is very simple and clear, which can be find at `./src/consumer_complaints.py`. 
The key point is to get the primary key of output table, which is (Product, Year).
Since third party packages are not allowed here, I adopt `Dictionary` data structure to deal with the data manipulation.
Other explanations can be found in the code docstrings and comments.

## Run Instruction
In the `run.sh` file, there are totally three code lines: 
- **Test Code 1** (Commented), the test dataset (small size) is provided by default repo.
- **Test Code 2** (Commented), the test dataset (modest size) is provided by original repo's `README.md`. While the file
 is too large to push to repo, so I cut it up and push a subset (10000 lines) into `test_2` folder. The original dataset
  can be
  find at [Here](http://files.consumerfinance.gov/ccdb/complaints.csv.zip).
- **Final Code** (Uncommented), the practical code for evaluation. Please make sure you create the `complaints.csv` in
 `input` folder. Otherwise it will come out with file not found Error.
 
 ## Improvement
 When running `_initialize()` method for `Solution` class, we can design a Heap data structure for company counts
  instead of store all companies counts in extra dictionary then find max count.  