from pypdf import PdfReader
import json

TRANSACTION_TYPES = [
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
      data = {}
      entries = []
      entry, flag = [], False
      for line in source:
        line = line.strip()
        if line == "STATEMENT OF ACCOUNT":
          if flag: entries.append([] + entry)
          entry, flag = [], False
          continue
        tokens = line.split(" ")
        if len(tokens) > 4 and any(map(lambda e: " ".join(tokens[4:]).startswith(e), TRANSACTION_TYPES)):
          if flag: entries.append([] + entry)
          entry, flag = [], True
        if "BALANCE B/F" in line:
          data["initial_value"] = line.replace("BALANCE B/F", "").strip()
          continue
        if "BALANCE C/F" in line:
          if flag: entries.append([] + entry)
          break
        if not flag: continue
        entry.append(line)
      data["entries"] = entries
      output.write(json.dumps(data, indent=4))

def consolidated_payment_4():
  with open("data/consolidated_payment_3.json", "r") as source:
    with open("data/consolidated_payment_4.json", "w") as output:
      data = json.loads(source.read())
      previous_running_balance = round(float(data["initial_value"].replace(",", "")) * 100)
      processed = []
      for entry in data["entries"]:
        processed_entry = {}
        tokens = entry[0].split(" ")
        date = " ".join(tokens[:2])
        transaction_type = list(filter(lambda e: " ".join(tokens[4:]).startswith(e), TRANSACTION_TYPES))[0]
        amount = round(float(tokens[2].replace(",", "")) * 100)
        running_balance = round(float(tokens[3].replace(",", "")) * 100)
        if previous_running_balance - amount == running_balance: amount *= -1
        entry[-1] = entry[-1].replace(date, "").strip()
        previous_running_balance = running_balance
        processed_entry["date"] = date
        processed_entry["transaction_type"] = transaction_type
        processed_entry["amount"] = amount / 100.0
        processed_entry["running_balance"] = running_balance / 100.0
        processed_entry["description"] = " ".join(entry[1:])
        processed.append(processed_entry)
      output.write(json.dumps(processed, indent=4))

consolidated_payment_1()
consolidated_payment_2()
consolidated_payment_3()
consolidated_payment_4()
