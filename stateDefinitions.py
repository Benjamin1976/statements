
templates = []






# ANZ CC
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
template = {'name': 'bankwest', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': False, 'matchByStyles': True}
templates.append(template)



# ANZ SAV - new
startEnd = {'pageStart': [{"find":  "OPENING BALANCE", 'skip': 0}],  
"pageEnd" : [{"find": "TOTALS AT END OF PAGE", 'skip': 0}], 
"sectionStart": [
    {"find": r"OPENING BALANCE$", 'skip': 3}, 
], 
"sectionEnd": [
 {"find": r"^TOTALS AT END OF PAGE$", 'skip': 0}
]}
checks = {
    'blank' : [r"^blank$"],
    'year' : [r'^[1-2]{1}[90]{1}[9012]{1}[0-9]{1}$'],
    'date': [r'^[0-9]{2}[ ]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}'],
    'account' : [r'[0-9]{4}[-]{1}[0-9]{5}', r'([0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4})'],
    'amount': [r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])[\s]+(CR|DR)+?', r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$'],
    'description': [r'^.+$']
}

styles = {
'transCredit3Desc': ['date', 'description', 'description', 'description', 'blank', 'amount', 'amount'],
'transDedit3Desc': ['date', 'description', 'description', 'description', 'amount', 'blank',  'amount'],
'transCredit2Desc': ['date',  'description', 'description', 'blank', 'amount', 'amount'],
'transDredit2Desc': ['date',  'description', 'description', 'amount', 'blank', 'amount'],
'payment': ['date', 'description', 'reference', 'amount'],
}
# 'transCredit1Desc': ['date', 'description', 'description', 'description', 'blank', 'amount', 'balance'],
# 'payment': ['date', 'description', 'reference', 'amount', 'date', 'amount'],
backfill = []
account = {'accountStart' : [{'find': r'[0-9]{4}[ ]{1}[0-9]{6}[ ]{1}[0-9]{5}', 'skip': 0}, {'find': r'([0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4})', 'skip': 0}]}
ignore = []
template = {'name': 'anz_sav', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': True, 'matchByStyles': True}
templates.append(template)


# ANZ SAV - old
startEnd = {'pageStart': [{"find":  "OPENING BALANCE", 'skip': 0}],  
"pageEnd" : [{"find": "TOTALS AT END OF PAGE", 'skip': 0}], 
"sectionStart": [
    {"find": r"OPENING BALANCE$", 'skip': 3}, 
], 
"sectionEnd": [
 {"find": r"^TOTALS AT END OF PAGE$", 'skip': 0}
]}
# checks = [
#     {'field' : ['blank'], 'find': [r"^blank$"]},
#     {'field' : ['year'], 'find': [r'^[1-2]{1}[90]{1}[9012]{1}[0-9]{1}$']},
#     {'field' : ['date', 'description'], 'find': [r'^[0-9]{2}[ ]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}']},
#     {'field' : ['account'], 'find': [r'[0-9]{4}[-]{1}[0-9]{5}', r'([0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4})']},
#     {'field' : ['amount'], 'find': [r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])[\s]+(CR|DR)+?', r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$']},
#     {'field' : ['description'], 'find': [r'^.+$']}
# ]
checks = {
    'blank' : [r"^blank$"],
    'year' : [r'^[1-2]{1}[90]{1}[9012]{1}[0-9]{1}$'],
    'date': [r'^[0-9]{2}[ ]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}'],
    'date': [r'^[0-9]{2}[ ]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}'],
    'account' : [r'[0-9]{4}[-]{1}[0-9]{5}', r'([0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4})'],
    'amount': [r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])[\s]+(CR|DR)+?', r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$'],
    'description': [r'^.+$']
}

styles = {
'transCredit3Desc': ['date', 'description', 'description', 'description', 'blank', 'amount', 'amount'],
'transDedit3Desc': ['date', 'description', 'description', 'description', 'amount', 'blank',  'amount'],
'transCredit2Desc': ['date',  'description', 'description', 'blank', 'amount', 'amount'],
'transDredit2Desc': ['date',  'description', 'description', 'amount', 'blank', 'amount'],
'payment': ['date', 'description', 'reference', 'amount'],
}
# 'transCredit1Desc': ['date', 'description', 'description', 'description', 'blank', 'amount', 'balance'],
# 'payment': ['date', 'description', 'reference', 'amount', 'date', 'amount'],
backfill = []
account = {'accountStart' : [{'find': r'[0-9]{4}[ ]{1}[0-9]{6}[ ]{1}[0-9]{5}', 'skip': 0}, {'find': r'([0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4})', 'skip': 0}]}
ignore = []
template = {'name': 'anz_sav_old', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': True, 'matchByStyles': True}
templates.append(template)



# BANKWEST
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
template = {'name': 'bankwest', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': False, 'matchByStyles': True}
templates.append(template)



# Visa CashOne
startEnd = {'pageStart': [{"find":  "VISA CASHONE PLATINUM\n4300−9201−0161−3774\nTransaction Reference", 'skip': 0}],  
"pageEnd" : [{'find': "MINIMUM PAYMENT DUE", 'skip': 0}], 
"sectionStart": [{"find": r"BALANCE FROM PREVIOUS STATEMENT", 'skip': 0}, {"find": r"Currency Amount", 'skip': 1}], 
"sectionEnd": [{"find": r"To be continued", 'skip': 0}, {"find": r"MINIMUM PAYMENT DUE", 'skip': 0}]}

startEnd = {'pageStart': [{"find":  "VISA CASHONE PLATINUM\n4300−9201−0161−3774\nTransaction Reference", 'skip': 0}],  
"pageEnd" : [{'find': "MINIMUM PAYMENT DUE", 'skip': 0}], 
"sectionStart": [{"find": r"BALANCE FROM PREVIOUS STATEMENT", 'skip': 0}], 
"sectionEnd": [{"find": r"MINIMUM PAYMENT DUE", 'skip': -1}]}

# checks = {'reference': [r'(?:(?<!\d)\d{23}(?!\d))'], 
#     'description': [r'^.{34}$', r'^.{19}$', r'INTEREST'],
#     'date': [r'^[0-9]{2}[\s]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}'],
#     'amount': [r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])(CR|DR)+?', r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$'],
#     'ccyCode': [r'^[A-Za-z]{3}$']
# }

# styles = {
# 'transTwoDateRefStart': ['reference', 'description', 'blank', 'blank', 'date', 'date', 'amount'],
# 'transTwoDatePlusCcy': ['reference', 'description', 'amount', 'ccyCode', 'date', 'date', 'amount'],
# 'transOneDateRefEnd': ['description', 'blank',  'amount',  'blank', 'date', 'reference'],
# 'payment': ['description', 'blank', 'blank', 'date', 'date', 'amount']
# }

checks = { 
    'description': [r'^.{34}$', r'^.{19}$', r'INTEREST'],
    'date': [r'^[0-9]{2}[\s]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}'],
    'amount': [r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])(CR|DR)+?', r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$'],
    'ccyCode': [r'^[A-Za-z]{3}$']
}

styles = {
'transTwoDateRefStart': ['description', 'blank', 'blank', 'date', 'date', 'amount'],
'transTwoDatePlusCcy': ['description', 'amount', 'ccyCode', 'date', 'date', 'amount'],
'transOneDateRefEnd': ['description', 'blank',  'amount',  'blank', 'date']
}
# 'payment': ['description', 'blank', 'blank', 'date', 'date', 'amount']

backfill = []
account = {'accountStart' : [{'find': r'VISA CASHONE PLATINUM', 'skip': 0}, {'find': r'([0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4})', 'skip': 0}]}
ignore = [{'find': r'^REF NO:', 'skip': 0}]
ignore = [
    {'find': r'[0-9]{23}', 'skip': 0},
    {'find': r'Ref No :', 'skip': 0}
    ]
# template = {'name': 'scb_cc', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': False, 'matchByStyles': False}
template = {'name': 'scb_cc', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': False, 'matchByStyles': True}
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
template = {'name': 'dbs_cl', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': False, 'matchByStyles': True}
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
template = {'name': 'dbs_cc', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': False, 'matchByStyles': True}
templates.append(template)








# FRANK CC
startEnd = {'pageStart': [{"find":  "TRANSACTION DATE", 'skip': 0}],  
"pageEnd" : [{'find': "TOTAL AMOUNT DUE", 'skip': 0}], 
"sectionStart": [{"find": r"^LAST MONTH'S BALANCE", 'skip': 0}
], 
"sectionEnd": [{"find": r"^SUBTOTAL", 'skip': -1}
]}
checks = { 
    'date': [r'^[0-9]{2}[/]{1}[0-9]{2}'],
    'foreign': [r'^FOREIGN CURRENCY'],
    'ccyCode': [r'^[A-z]{2}$'],
    'account' : [r'([0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4})'],
    'amount': [r'^\(?[0-9,\.]+\)?$'],
    'description': [r'^.+$']
}

styles = {
'transDebitForeign': ['date', 'amount', 'description', 'foreign', 'description','ccyCode', 'description' ],
'transCreditForeign': ['date', 'amount', 'description', 'foreign', 'description','ccyCode' ],
'transCreditLocal': ['date', 'amount', 'description', 'description','ccyCode' ],
'payment': ['date', 'description', 'reference', 'amount'],
'transDebit': ['date', 'amount', 'description', 'description'],
'transDebit2': ['date', 'amount', 'description'],
}

backfill = []
account = {'accountStart' : [{'find': r'([0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4})', 'skip': 0}]}
ignore = [{'find': r'^\){1}$', 'skip': 0}]
template = {'name': 'ocbc_cc_frank', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': False, 'matchByStyles': True}
templates.append(template)



# CITI CC
startEnd = {'pageStart': [{"find":  "BALANCE PREVIOUS STATEMENT", 'skip': 0}],  
"pageEnd" : [{'find': "TOTAL AMOUNT DUE", 'skip': 0}], 
"sectionStart": [
    {"find": r"^BALANCE PREVIOUS STATEMENT$", 'skip': 1},
    {"find": r"^CITI PREMIERMILES CARD 4147 4630 0394 6163 - PARSONS BENJAMIN LEE$", 'skip': 0},
    {"find": r"^AMOUNT \(SGD\)$", 'skip': 0}
], 
"sectionEnd": [
    {"find": r"^SUB-TOTAL:$", 'skip': 0},
    {"find": r"^CITI PREMIERMILES CARD 4147 4630 0394 6163$", 'skip': -1},
    {"find": r"^Payment Due Date", 'skip': 0}
]}

checks = { 
    'date': [r'^[0-9]{2}[ ]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec]{3}'],
    'ccyCode': [r'^[A-z]{2}$'],
    'account' : [r'([0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4}[ ]{1}[0-9]{4})'],
    'amount': [r'^\(?[0-9,\.]+\)?$'],
    'description': [r'^.+$']
}

styles = {
'transCCY2Desc': ['date', 'description', 'description', 'ccyCode', 'amount' ],
'transCCY1Desc': ['date', 'description', 'ccyCode', 'amount' ],
'trans': ['date', 'description', 'description', 'amount' ],
'payment': ['date', 'description', 'amount' ],
}
# 'transDebitForeign': ['date', 'amount', 'description', 'foreign', 'description','ccyCode', 'description' ],
# 'transCreditForeign': ['date', 'amount', 'description', 'foreign', 'description','ccyCode' ],
# 'transCreditLocal': ['date', 'amount', 'description', 'description','ccyCode' ],
# 'payment': ['date', 'description', 'reference', 'amount'],
# 'transDebit': ['date', 'amount', 'description', 'description'],

backfill = []
account = {'accountStart' : [{'find': r'([0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4})', 'skip': 0}]}
ignore = []
template = {'name': 'citi_cc', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': False, 'matchByStyles': True}
templates.append(template)




# HSBC CC
startEnd = {'pageStart': [{"find":  "TRANSACTION DATE", 'skip': 0}],  
"pageEnd" : [{'find': "TOTAL AMOUNT DUE", 'skip': 0}], 
"sectionStart": [{"find": r"^LAST MONTH'S BALANCE", 'skip': 0}
], 
"sectionEnd": [{"find": r"^SUBTOTAL", 'skip': -1}
]}
checks = { 
    'date': [r'^[0-9]{2}[/]{1}[0-9]{2}'],
    'foreign': [r'^FOREIGN CURRENCY'],
    'ccyCode': [r'^[A-z]{2}$'],
    'account' : [r'([0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4})'],
    'amount': [r'^\(?[0-9,\.]+\)?$'],
    'description': [r'^.+$']
}

styles = {
'transDebitForeign': ['date', 'amount', 'description', 'foreign', 'description','ccyCode', 'description' ],
'transCreditForeign': ['date', 'amount', 'description', 'foreign', 'description','ccyCode' ],
'transCreditLocal': ['date', 'amount', 'description', 'description','ccyCode' ],
'payment': ['date', 'description', 'reference', 'amount'],
'transDebit': ['date', 'amount', 'description', 'description'],
'transDebit2': ['date', 'amount', 'description'],
}

backfill = []
account = {'accountStart' : [{'find': r'([0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4})', 'skip': 0}]}
ignore = [{'find': r'^\){1}$', 'skip': 0}]
template = {'name': 'hsbc_cc', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill, 'includeBlanks': False, 'matchByStyles': True}
templates.append(template)
