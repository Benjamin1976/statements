import PyPDF4 as reader
import fitz  # this is pymupdf
import re


def getPageSections (doc, start, end):
    text = ""
    # startTrans = "BALANCE FROM PREVIOUS STATEMENT"
    # endTrans = "MINIMUM PAYMENT DUE"
    bReadPage = False
    sTrans = ''
    nStart = None

    for page in doc:
        text = page.getText()

        
        if not bReadPage:
            nStart = re.search(start, text)
            if nStart != None:
                bReadPage = True

        if bReadPage:
            sTrans += str(text)
        
        if bReadPage:
            if re.search(end, text) != None:
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


styles = {
'transTwoDateRefStart': ['reference', 'description', 'blank', 'blank', 'date', 'date', 'amount'],
'transTwoDateRefEnd': ['description', 'blank', 'blank', 'date', 'date', 'amount', 'reference'],
'transOneDateRefStart': ['reference', 'description', 'blank',  'amount',  'blank', 'date', 'reference'],
'transOneDateRefEnd': ['description', 'blank',  'amount',  'blank', 'date', 'reference'],
'transTwoDatePlusCcy': ['reference', 'description', 'amount', 'ccyCode', 'date', 'date', 'amount'],
'transOneDatePlusCcy': ['reference', 'description', 'amount', 'ccyCode', 'blank', 'date', 'amount'],
'payment': ['description', 'blank', 'blank', 'date', 'date', 'amount'],
}


checks = {'reference': [r'(?:(?<!\d)\d{23}(?!\d))'], 'description': [r'^.{34}$', r'^.{19}$'], 
    'date': [r'^[0-9]{1,2}[\s]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|nec]{3}\s/i/g'],
    'amount': [r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])(CR|DR)+?', r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$'],
    'ccyCode': [r'^[A-Za-z]{3}$']
}





def matchStyle(styles, style):
    # print(styles)
    # print(style)
    for key, value in styles.items():
        if value == style:
            return key
            break
    return None


# def readValues(style, line):




def filterByLine(text, start, end):
    
    monthText = str( 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec')

    lines = text.splitlines()
    bInclude = False
    transStyle = []
    lineType = None
    bRead = False
    bFirstRead = True
    skip = 0
    starts = 0
    i =0

    fields = "date|description|amount|reference|ccyCode|ccyValue"
    ignore = 'PAYMENT − THANK YOU'
    values = []
    value = {}

    # value = {"reference": None, 'date': None, 'description' : None, 'amount': }

    for line in lines:
        # if i==20: break
        i += 1


        lineType = None
        if skip > 0: skip -= 1

        if line.strip() in start:
            bRead = True
            skip = 1
            if starts == 0 and line.strip() == 'Currency Amount': skip += 1
            starts += 1
    
        elif line.strip() in end:
            bRead = False
            skip = 1



        if (bRead) and (skip == 0):
            # print(line)
            bFound = False
            for field, check in checks.items():     # loop through field checks
                for ch in check:                    # loop through if field has multiple checks
                    if (not bFound) and (re.match(ch, line.strip()) != None):  
                        value[field]=line.strip()
                        lineType = field
                        bFound = True
                        break
                if bFound: break
                
            if not bFound:
                if monthText.find(line[-3:].lower()) > -1:
                    lineType = 'date'
                    value['date'] = line.strip()

                elif len(line.strip()) == 0:
                    lineType = 'blank'

                else:
                    lineType = None


            # if re.match(r'(?:(?<!\d)\d{23}(?!\d))', line) != None:
            #     lineType = 'reference'
            #     value['reference'] = line.strip()

            # elif re.match(r'^.{34}$', line) != None:
            #     lineType = 'description'
            #     value['description'] = line.strip()

            # elif re.match(r'^.{19}$', line) != None:
            #     lineType = 'description'
            #     value['description'] = line.strip()

            # elif re.match(r'^[0-9]{1,2}[\s]*[jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|nec]{3}\s/i/g',line.strip()) != None:
            #     lineType = 'date'
            #     value['date'] = line.strip()


            # elif re.match(r'\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])(CR|DR)+?',line.strip()) != None:
            #     lineType = 'amount'
            #     value['amount'] = line.strip()

            # elif re.match(r'^\$?([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+)(.[0-9][0-9])?$',line.strip()) != None:
            #     lineType = 'amount'
            #     value['amount'] = line.strip()

            # elif re.match(r'^[A-Za-z]{3}$', line.strip()) != None:
            # # elif len(line.strip()) == 3:
            #     lineType = 'ccyCode'
            #     value['ccyCode'] = line.strip()

            # elif monthText.find(line[-3:].lower()) > -1:
            #     lineType = 'date'
            #     value['date'] = line.strip()

            # elif len(line.strip()) == 0:
            #     lineType = 'blank'

            # else:
            #     lineType = None
            
            if lineType != None: transStyle.append(lineType)

            if (len(transStyle) > 7):
                print(transStyle)
                
            matched = matchStyle(styles, transStyle)
            if matched != None:
                transStyle = []
                values.append(value)
                value = {}

    return values            

    


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


with fitz.open("eStatement200104151222728937696.pdf") as doc:

    start = "VISA CASHONE PLATINUM\n4300−9201−0161−3774\nTransaction Reference"
    end = "MINIMUM PAYMENT DUE"

    transPages = getPageSections(doc, start, end)
    # print(transPages)

    start = ["BALANCE FROM PREVIOUS STATEMENT", "Currency Amount"]
    end =["To be continued", "MINIMUM PAYMENT DUE"]
    # print(transPages)
    # transClean = filterByPositions(transPages, start, end)
    transClean = filterByLine(transPages, start, end)
    print(transClean)


    


    # .splitlines()
    # print(trans)
    # for line in trans:
    #     if re.match(r'\b\d{15}\b', line):
    #         print(line)


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