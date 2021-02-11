import PyPDF4 as reader
import fitz  # this is pymupdf
import re
from stateDefinitions import templates 


def getPageSections (doc, start, end):
    text = ""
    bReadPage = False
    sTrans = ''
    nStart = None

    # print('[Get Pages][start]: ', start)
    # print('[Get Pages][end]: ', end)

    for page in doc:
        text = page.getText()

        # print('page start find: ', start[0]['find'])
        if not bReadPage:
            nStart = re.search(start[0]['find'], text)
            if nStart != None:
                bReadPage = True

        if bReadPage:
            sTrans += str(text)
        
        # print('page end find: ', end[0]['find'])
        if bReadPage:
            if re.search(end[0]['find'], text) != None:
                bReadPage = False 
    
    return sTrans


def findInString(finds, text, bStart):
    results = []
    for find in finds:
        if bStart: 
            results += [m.start() for m in re.finditer(find, text)]
        else:
            results += [m.end() for m in re.finditer(find, text)]
    return results


def filterByPositions(text, start, end):
    
    lines = text.splitlines()
    bInclude = False

    starts = findInString(start, text, True)
    ends = findInString(end, text, False)

    print(starts)
    print(ends)

    return
    i=0
    for i in range(len(starts)):
        if starts[i] != None:
            print(starts[i].end())
            if ends[i] != None:
                print(ends[i].end())
                # print(text[starts[i].end():ends[i].start()])
            else:
                # print(text[starts[i].end():])
                pass


def matchStyle(styles, style):
    # print(styles)
    # print(style)
    for key, value in styles.items():
        if value == style:
            return key
            break
    return None



def existsInArrayFind(text, finds):
    for find in finds:      # loop through array of dicts with {find: text , skip: 0}
        found = re.search(find['find'], text, re.IGNORECASE)
        if found != None:
            # if text.strip() in find['find']:
            return find['skip']
            break
    return -1


def valExistsNotEmpty(value, checkExists):
    if checkExists:
        return value != None and value != ''
    else:
        return value == None or value == ''
    return False
    




def backFillArray(backfill, value, values):
   
    if backfill != None:
        # print('-----------')
        # print(backfill)
        for fillField in backfill:
            
            valueInTrans = False
            if fillField in value:
                if valExistsNotEmpty(value[fillField], True):
                    valueInTrans = True

            valueInPrevTrans = False
            if len(values) > 0:
                if (fillField in values[-1]):
                    if valExistsNotEmpty(values[-1][fillField], True):
                        valueInPrevTrans = True
                        
            if valueInTrans and valueInPrevTrans: value[fillField] = values[-1][fillField]
    
    return value



# FRANK CC
startEnd = {'pageStart': [{"find":  "TRANSACTION DATE", 'skip': 0}],  
"pageEnd" : [{'find': "TOTAL AMOUNT DUE", 'skip': 0}], 
"sectionStart": [{"find": r"^LAST MONTH'S BALANCE", 'skip': 0}
], 
"sectionEnd": [{"find": r"^SUBTOTAL", 'skip': 0}
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
'transDebitForeign': ['date', 'amount', 'description', 'foreign', 'description',' ccyCode', 'description' ],
'transCreditForeign': ['date', 'amount', 'description', 'foreign', 'description',' ccyCode' ],
'transCreditLocal': ['date', 'amount', 'description', 'description', 'description',' ccyCode' ],
'payment': ['date', 'description', 'reference', 'amount'],
'transDebit': ['date', 'amount', 'description', 'description'],
'transDebit2': ['date', 'amount', 'description'],
}

backfill = []
account = {'accountStart' : [{'find': r'([0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4}[-]{1}[0-9]{4})', 'skip': 0}]}
ignore = [{'find': r'^\){1}$', 'skip': 0}]
template = {'name': 'ocbc_cc_frank', 'startEnds': startEnd, 'styles': styles, 'checks': checks, 'account': account, 'ignore': ignore, 'backfill': backfill}
templates.append(template)




thisDef = {'file': 'dbs-consolidated.pdf', 'template': 'dbs_cc'}  # 10
thisDef = {'file': 'eStatement200104151222728937696.pdf', 'template': 'scb_cc'} #55
thisDef = {'file': 'dbs-cashline.pdf', 'template': 'dbs_cl'}  # 5
thisDef = {'file': 'FRANK CREDIT CARD-5534-Dec-20.pdf', 'template': 'ocbc_cc_frank'}  # 11

trial = True
trial = False


def filterByLine(text, start, end, styles, checks, accountFind, ignore, backfill):
    
    
    lines = text.splitlines()
    transStyle = []
    lineType = None
    bRead = False
    skip = 0
    starts = 0
    i =0

    account = None
    values = []
    value = {}

    for line in lines:
        # if i==20: break
        i += 1


        # check if the account is found
        findAccount = existsInArrayFind(line, accountFind)
        if findAccount > -1:
            account=line

        # Check if the lineshould be read or skipped
        lineType = None
        if skip > 0: skip -= 1

        foundStart = existsInArrayFind(line, start)
        foundEnd = existsInArrayFind(line, end)

        if foundStart > -1:
            bRead = True
            skip = 1 + foundStart
            starts += 1
        
        elif foundEnd > -1:
            bRead = False

        # check if the line should be ignored
        ignoreLine = existsInArrayFind(line, ignore)
        if ignoreLine > -1:
            skip = 1 + ignoreLine


        # parse the line and check for attributes
        if (bRead) and (skip == 0):

            bFound = False

            # check if attribute found
            for field, check in checks.items():     # loop through field checks
                for chk in check:                    # loop through if field has multiple checks
                    if (not bFound) and (re.search(chk, line.strip(), re.IGNORECASE) != None):  
                        value[field]=line.strip()
                        lineType = field
                        bFound = True
                        break
                if bFound: break
            
            # if nothing found, check for date or mark blank / None
            if not bFound:
                if len(line.strip()) == 0:
                    lineType = 'blank'
                else:
                    lineType = None
                    
        
            # update the account or transaction style
            if (lineType == 'account'): 
                value['account']=line
            elif (lineType != None):
                transStyle.append(lineType)

            # if (len(transStyle) > 7):
            #     print(transStyle)
                
            if lineType != None:
                print(lineType + ': ' + line)
                pass

            # check if the transaction pattern matches
            #   and add to transaction array  
            matched = matchStyle(styles, transStyle)
            if matched != None:
                transStyle = []
                value['account'] = account

                # Backfill array with missing values
                value = backFillArray(backfill, value, values)

                values.append(value)
                value = {'account': account}

    return values    

    

# Read all applicable lines into an array
# Run through pattern array with most complex patterns first
#       Loop through transaction patterns and remove the pattern if found
#
# this way simple patterns won't be matched incorrectly


# ^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$
# compatible 
# ([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+) -> caters for thousand separators
# (.[0-9][0-9]) -> any decimals
# * + no. of matches
# ^ match must start at beginning of string
# $ match must end at end of string
# [] acceptable chars
# [^] not acceptable chars
# | or options
# ? optional
# {} length
# /i optional upper/lower
# [\t\f\n\r] whitespace
# /s all whitespace





def startNewDef (doc):
    for page in doc:
        text = page.getText()
        print(text)

    pass


def readTheFile(thisDef, trial):
    
    # print('----------reading file----------')
    # print('[Definition]:-')
    # print(thisDef)
    # print('[Trial]: ', trial )

    with fitz.open(thisDef['file']) as doc:

        if trial:
            start = "VISA CASHONE PLATINUM\n4300−9201−0161−3774\nTransaction Reference"
            end = "MINIMUM PAYMENT DUE"

            start = "DBS ALTITUDE AMERICAN EXPRESS CARD NO.: 3779 103413 17522"
            end = "MINIMUM PAYMENT DUE"

            start = "TRANSACTION ACTIVITY"
            end = "MINIMUM PAYMENT DUE"

            startNewDef(doc)
            # transPages = getPageSections(doc, start, end)
            # print(transPages)

            # start = ["BALANCE FROM PREVIOUS STATEMENT", "Currency Amount"]
            # end =["To be continued", "MINIMUM PAYMENT DUE"]

            # transClean = filterByLine(transPages, start, end)
            # print(transPages)

        else:
            print('[Finding Template]: ', thisDef['template'])

            for template in templates:
                # print('[Checking Template][looking for match]:', template['name'], thisDef['template'])
                if template['name'] == thisDef['template']:

                    print('[Start][Template Found]: ', template['name'])
                    
                    transPages = getPageSections(doc, template['startEnds']['pageStart'], template['startEnds']['pageEnd'])
                    if valExistsNotEmpty(transPages, False):
                        print('[Error] file content empty')
    
                    # print(transPages)

                    transClean = filterByLine(transPages, template['startEnds']['sectionStart'], template['startEnds']['sectionEnd'], template['styles'], template['checks'], template['account']['accountStart'], template['ignore'], template['backfill'] )
                    print(transClean)
                    
                    # print('Record count: ', len(transClean))
                    break


readTheFile(thisDef, trial)



    


## start -----------------------------
# YOUR CARD / PERSONAL LOANS TRANSACTIONS
# VISA CASHONE PLATINUM
# 4300−9201−0161−3774
# Transaction Reference
# SGD Amount
# Transaction
# Date
# Posting
# Date
# Description
# Currency Amount
# 37,313.73
# BALANCE FROM PREVIOUS STATEMENT


## two dates -----------------------------
# 74055269332296697800749
# JEWEL COFFEE        SINGAPORE   SG


# 29 Nov
# 28 Nov
#        5.58

## single date -----------------------------
# GUILT−FREE          SINGAPORE   SG

#       13.00

# 29 Nov
# 74890299332102888747531

## double date with currency -----------------------------
# 74889609329085120700012
# METAL LITE MC FORT  TAGUIG CITY PH
#     18900.00
# PHP
# 26 Nov
# 23 Nov
#      526.03

## payment -----------------------------
# PAYMENT − THANK YOU


# 13 Dec
# 13 Dec
#    1,260.00CR


## end of list 1 -----------------------------
# To be continued

# Ref No :
# Page: 4 of 7
# Statement Date: 24 Dec 2019
# Payment Due Date: 18 Jan 2020
# PARSONS BENJAMIN LEE
# YOUR CARD / PERSONAL LOANS TRANSACTIONS
# VISA CASHONE PLATINUM
# 4300−9201−0161−3774
# Transaction Reference
# SGD Amount
# Transaction
# Date
# Posting
# Date
# Description
# Currency Amount



## end of list final -----------------------------
# 1,280.60
# MINIMUM PAYMENT DUE
# NEW BALANCE
# 40,914.47




# print(text)

# def readPDF():
#     file = open(r'eStatement200104151222728937696.pdf','rb')
#     readfile = reader.PdfFileReader(file, strict=False)
#     # for text in readfile.getPage(0):
#     #     print(text)
#     page = readfile.getPage(0)
#     page_content = page.extractText()
#     print(page_content)
#     pagecount = readfile.getNumPages()
#     return {'data': pagecount}

# print(readPDF())