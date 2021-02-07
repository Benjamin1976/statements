
templates = []


# Visa CashOne
startEnd = {'pageStart': [{"find":  "VISA CASHONE PLATINUM\n4300−9201−0161−3774\nTransaction Reference", 'skip': 0}],  
"pageEnd" : [{'find': "MINIMUM PAYMENT DUE", 'skip': 0}], 
"sectionStart": [{"find": r"BALANCE FROM PREVIOUS STATEMENT", 'skip': 0}, {"find": r"Currency Amount", 'skip': 1}], 
"sectionEnd": [{"find": r"To be continued", 'skip': 0}, {"find": r"MINIMUM PAYMENT DUE", 'skip': 0}]}

checks = {'reference': [r'(?:(?<!\d)\d{23}(?!\d))'], 
    'description': [r'^.{34}$', r'^.{19}$'],
    'date': [r'^[0-9]{1,2}[\s]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}\s'],
    'amount': [r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])(CR|DR)+?', r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$'],
    'ccyCode': [r'^[A-Za-z]{3}$']
}

styles = {
'transTwoDateRefStart': ['reference', 'description', 'blank', 'blank', 'date', 'date', 'amount'],
'transTwoDateRefEnd': ['description', 'blank', 'blank', 'date', 'date', 'amount', 'reference'],
'transOneDateRefStart': ['reference', 'description', 'blank',  'amount',  'blank', 'date', 'reference'],
'transOneDateRefEnd': ['description', 'blank',  'amount',  'blank', 'date', 'reference'],
'transTwoDatePlusCcy': ['reference', 'description', 'amount', 'ccyCode', 'date', 'date', 'amount'],
'transOneDatePlusCcy': ['reference', 'description', 'amount', 'ccyCode', 'blank', 'date', 'amount'],
'payment': ['description', 'blank', 'blank', 'date', 'date', 'amount'],
}
backfill = []
account = {'accountStart' : [{'find': r'VISA CASHONE PLATINUM', 'skip': 0}, {'find': r'([0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4})', 'skip': 0}]}
ignore = []
template = {'name': 'scb_cc', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill}
templates.append(template)

# DBS Cashline
startEnd = {'pageStart': [{"find":  "TRANSACTION ACTIVITY", 'skip': 0}],  
"pageEnd" : [{'find': "MINIMUM PAYMENT DUE", 'skip': 0}], 
"sectionStart": [
    {"find": r"PREVIOUS BALANCE", 'skip': 1},
    {"find": r"NEW TRANSACTIONS", 'skip': 0}
], 
"sectionEnd": [
    {"find": r"SUB-TOTAL", 'skip': 0},
    {"find": r"CLOSING BALANCE", 'skip': 0}
    ]}

checks = { 
    'date': [r'^[0-9]{1,2}[\s]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}[\s]*[0-9]{4}'],
    'description': [r'^.{37}$', r'^.{20}$', r'^.{33}$'],
    'amount': [r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])( CR| DR)+?', r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$'],
    'ccyCode': [r'^[A-Za-z]{3}$']
}

styles = {
'transDate': ['date', 'description', 'amount'],
'transNoDate': ['description', 'amount'],
'payment': ['date', 'description', 'amount'],
}
backfill = ['date']
account = {'accountStart' : [{'find': r'PARSONS BENJAMIN LEE\'S  DBS CASHLINE ACCOUNT NO.  082-585507-0', 'skip': 0}]}
ignore = []
template = {'name': 'dbs_cl', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill}
templates.append(template)



# DBS ALTITUDE AMERICAN EXPRESS CARD NO.: 3779 103413 17522
startEnd = {'pageStart': [{"find":  "CARD NO.:", 'skip': 0}],  
"pageEnd" : [{'find': "INSTALMENT PLANS SUMMARY", 'skip': 0}], 
"sectionStart": [{"find": r"^NEW TRANSACTIONS PARSONS BENJAMIN LEE", 'skip': 0}
, {"find": r"^SUB-TOTAL:", 'skip': 1}
, {"find": r"^PREVIOUS BALANCE", 'skip': 1}
], 
"sectionEnd": [{"find": r"^SUB-TOTAL:", 'skip': 0}
, {"find": r"^TOTAL:", 'skip': 0}
, {"find": r"^PARSONS BENJAMIN LEE", 'skip': 0}
]}
checks = {'reference': [r'^REF NO:'], 
    'account' : [r'[0-9]{4}[ ]{1}[0-9]{6}[ ]{1}[0-9]{5}', r'([0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4})'],
    'date': [r'^[0-9]{2}[ ]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}'],
    'amount': [r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])[\s]+(CR|DR)+?', r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$'],
    'description': [r'^.+$']
}

styles = {
'trans': ['date', 'description', 'amount'],
'payment': ['date', 'description', 'reference', 'amount'],
}
# 'payment': ['date', 'description', 'reference', 'amount', 'date', 'amount'],
backfill = []
account = {'accountStart' : [{'find': r'[0-9]{4}[ ]{1}[0-9]{6}[ ]{1}[0-9]{5}', 'skip': 0}, {'find': r'([0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4})', 'skip': 0}]}
ignore = [{'find': r"^PREVIOUS BALANCE$", 'skip': 1}]
template = {'name': 'dbs_cc', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill}
templates.append(template)
