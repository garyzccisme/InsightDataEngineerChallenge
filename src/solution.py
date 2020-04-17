import csv
from datetime import datetime
import sys
import time


class Solution:
    def __init__(self, read_path: str, write_path: str):
        self.read_path = read_path
        self.write_path = write_path

        # Define some intermediate variables
        self.raw = {}
        self.mid = {}
        self.final = None

    def pipeline(self):
        """
        This is the only method that users are supposed to run.
        """
        self._read_csv()
        self._initialize()
        self._process()
        self._sort()
        self._write_csv()

    def _read_csv(self):
        """
        Read csv file, filter out unrelated columns and transfer the data into dictionary, stored in self.raw.
        Schema: {Complaint ID: [Product, Date received, Company]}
        """
        with open(self.read_path, 'r', encoding='UTF-8') as file:
            csv_file = csv.DictReader(file)
            keys = ['Complaint ID', 'Product', 'Date received', 'Company']
            for i, row in enumerate(csv_file):
                tem_dict = dict(row)
                record = [tem_dict.get(x) for x in keys]

                # Check Validation
                if not all(record):
                    continue
                self.raw[record[0]] = list(map(str.lower, record[1:]))

    # TODO: Could use HEAP data structure here to gain more efficiency
    def _initialize(self):
        """
        Get primary key (Product, Year), set it as dictionary key to generate new dictionary, stored in self.mid.
        Schema: {(Product, Year): [Complaints_number, Complaints_company_number, dict(company, counts)]}
        """
        if self.raw == {}:
            raise SyntaxError("Invalid Syntax: self.raw is not initialized.")

        for index, record in self.raw.items():

            # (Product, Year) should be output table's primary key
            pk = (record[0], datetime.strptime(record[1], '%Y-%m-%d').year)
            if pk not in self.mid:
                complaint_counts = 1
                company_counts = 1
                company = {record[2]: 1}
                self.mid[pk] = [complaint_counts, company_counts, company]
            else:
                self.mid[pk][0] += 1

                # Check if the company has shown before
                if record[2] not in self.mid[pk][2]:
                    self.mid[pk][1] += 1
                    self.mid[pk][2][record[2]] = 1
                else:
                    self.mid[pk][2][record[2]] += 1

    def _process(self):
        """
        Focus on the dict(company, counts) in self.mid, get max value and calculate percentage, updated in self.mid.
        Schema: {(Product, Year): [Complaints_number, Complaints_company_number, max_complaints_percent_by_company]}
        """
        if self.mid == {}:
            raise SyntaxError("Invalid Syntax: self.mid is not initialized.")
        items = list(self.mid.items())
        for pk, target in items:
            max_percent = int(round(max(target[-1].values()) / target[0] * 100, 0))
            self.mid[pk][-1] = max_percent

    def _sort(self):
        """
        Reconstruct self.mid into list, sort it by primary key, stored in self.final.
        Schema: [[Product, Year, Complaints_number, Complaints_company_number, max_complaints_percent_by_company]]
        """
        if self.mid == {}:
            raise SyntaxError("Invalid Syntax: self.mid is not initialized.")
        self.final = [[*pk, *target] for pk, target in self.mid.items()]
        self.final.sort(key=lambda x: (x[0], x[1]))

    def _write_csv(self):
        """
        Write self.final into csv file.
        """
        with open(self.write_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in self.final:
                csv_writer.writerow(row)


if __name__ == "__main__":
    start = time.time()
    print("Start on {}.".format(datetime.fromtimestamp(start).strftime('%c')))
    solution = Solution(*sys.argv[1:])
    solution.pipeline()
    end = time.time()
    print("Finish on {}, totally {} s.".format(datetime.fromtimestamp(end).strftime('%c'), round(end - start, 2)))
