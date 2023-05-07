from pypdf import PdfReader
import json

def consolidated_payment_1():
  reader = PdfReader("data/consolidated_payment.pdf")
  number_of_pages = len(reader.pages)
  print(number_of_pages)

  with open("data/consolidated_payment_1.txt", "w") as output:
    for page in reader.pages:
      text = page.extract_text()
      if "Account No." not in text: continue
      output.write(text)
      output.write("\n")

def consolidated_payment_2():
  with open("data/consolidated_payment_1.txt", "r") as source:
    with open("data/consolidated_payment_2.txt", "w") as output:
      for line in source:
        line = line.strip()
        while "  " in line:
          line = line.strip().replace("  ", " ")
        output.write(line)
        output.write("\n")

def consolidated_payment_3():
  with open("data/consolidated_payment_2.txt", "r") as source:
    with open("data/consolidated_payment_3.json", "w") as output:
      transaction_types = [
        "BILL PAYMENT INB",
        "BONUS INTEREST",
        "DEBIT PURCHASE",
        "FAST PAYMENT",
        "FUND TRANSFER",
        "GIRO - SALARY",
        "INTEREST CREDIT",
        "NETS QR",
        "PAYMENT /TRANSFER",
        "POS PURCHASE NETS",
      ]
      entries = []
      entry, flag = [], False
      for line in source:
        line = line.strip()
        if line == "STATEMENT OF ACCOUNT":
          flag = False
          continue
        if any(map(lambda transaction_type: line.endswith(transaction_type), transaction_types)):
          if flag: entries.append([] + entry)
          entry, flag = [], True
        if not flag: continue
        if "BALANCE B/F" in line: continue
        entry.append(line)
      output.write(json.dumps(entries, indent=4))

# consolidated_payment_1()
# consolidated_payment_2()
consolidated_payment_3()
