# Programming with Python — Assignment 1

Solutions for the 10 questions in the B.Tech Information Technology, Semester V
Programming with Python (202044504) assignment.

## Requirements
- Python 3.10 or newer
- Q1–Q9 use the Python standard library.
- Q10 uses Tkinter, normally included with desktop Python installations.

## Run
Run each script from a terminal:

```bash
python Q1_Campus_Merit_Analyzer.py < input.txt
python Q2_Password_Audit.py < input.txt
python Q3_Expression_Engine.py < input.txt
python Q4_CSV_Transaction_Splitter.py transactions.csv
python Q5_Bank_Settlement_System.py < input.txt
python Q6_Module_Dependency_Resolver.py < input.txt
python Q7_Formula_Validator.py
python Q8_Compressed_Log_Index.py < input.txt
python Q9_Threaded_Job_Scheduler.py < input.txt
python Q10_Assignment_Tracker.py
```

For Q4, the input CSV header must contain `transaction_id,account_id,type,amount,timestamp`.
Q8 BUILD input format: `BUILD folder_path archive.zip`.
Q8 SEARCH input format: `SEARCH index.pkl q token1 ... tokenq`.
Q7 accepts one formula or assignment per line; enter `quit` to exit.
Q10 saves records in `assignment_data.json` in the working directory and exports CSV through the GUI.

## Notes
- Read and understand each program before submission.
- Test using the assignment's sample input plus at least three additional cases.
- Do not include private data in the repository.
