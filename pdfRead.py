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
    return None


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



# 'date,description,amount,
#  date,description,description,ccyCode,amount,
#  date,description,description,amount,
#  date,description,description,amount,
#  date,description,ccyCode,amount,
#  date,description,ccyCode,amount,
#  date,description,ccyCode,amount,
#  date,description,ccyCode,amount,
#  date,description,ccyCode,amount,
#  date,description,ccyCode,amount,
#  date,description,description,ccyCode,amount,
#  date,description,description,ccyCode,amount,
#  date,description,description,ccyCode,amount,
#  date,description,description,ccyCode,amount,
#  date,description,description,ccyCode,amount,
#  date,description,ccyCode,amount'

# styles = {
# 'transCCY2Desc': ['date', 'description', 'description', 'ccyCode', 'amount' ],
# 'transCCY1Desc': ['date', 'description', 'ccyCode', 'amount' ],
# 'trans': ['date', 'description', 'description', 'amount' ],
# 'payment': ['date', 'description', 'amount' ],
# }

def matchPatternsByStyles(styles, transStyles, values):

    newValues = []

    # loop through the styles   
    for name, style in styles.items():
        allStylesFound = ",".join(transStyles)              # create a string of all the style fields
        styleToFind = ','.join(style)                       # create a string of the style pattern to match
        itemsInStyle = len(style)                           # count the number of items in the style pattern
        matches = re.finditer(r'\b%s\b' % styleToFind, allStylesFound, re.MULTILINE)    # find the style pattern in all trans pattern

        # loop through all the matches in reverse to find the trans style pattern
        for matchNum, match in reversed(list(enumerate(matches, start=1))):
            
            # find the transaction style in the overall styles found
            transStart = allStylesFound[1:match.start()]        # take the start of the style list to the match position
            arrayStart = len(re.findall(r',', transStart))      # count the commas / array index @ match
            arrayEnd = arrayStart + itemsInStyle

            trans = values[arrayStart: arrayEnd]                # extract the actual field values
            newValues.append(trans)                             # add to the new Transactions array
            # print(trans)
            # print('[Found Style] ', name, 'starting at', arrayStart)

            # remove the items from the style lists
            del values[arrayStart: arrayEnd] 
            del transStyles[arrayStart: arrayEnd] 
            # print(transStyles)

    print('[Missed Styles]:', transStyles)
    print('[Missed Values]:', values)

    return newValues


def matchPatternsByLines(styles, transStyles, values):

    newValues = []
    tempStyle = []

    for style in transStyles:

        matched = matchStyle(styles, tempStyle)
        if matched != None:
            newTran = values[0:len(tempStyle)]
            newValues.append(newTran)
            del values[0:len(tempStyle)]
            tempStyle = []
        else:
            tempStyle.append(style)

        if len(tempStyle) > 7:
            print('Not matched')

    return newValues

    # # loop through the styles   
    # for name, style in styles.items():
    #     allStylesFound = ",".join(transStyles)              # create a string of all the style fields
    #     styleToFind = ','.join(style)                       # create a string of the style pattern to match
    #     itemsInStyle = len(style)                           # count the number of items in the style pattern
    #     matches = re.finditer(r'\b%s\b' % styleToFind, allStylesFound, re.MULTILINE)    # find the style pattern in all trans pattern

    #     # loop through all the matches in reverse to find the trans style pattern
    #     for matchNum, match in reversed(list(enumerate(matches, start=1))):
            
    #         # find the transaction style in the overall styles found
    #         transStart = allStylesFound[1:match.start()]        # take the start of the style list to the match position
    #         arrayStart = len(re.findall(r',', transStart))      # count the commas / array index @ match
    #         arrayEnd = arrayStart + itemsInStyle

    #         trans = values[arrayStart: arrayEnd]                # extract the actual field values
    #         newValues.append(trans)                             # add to the new Transactions array
    #         print(trans)
    #         # print('[Found Style] ', name, 'starting at', arrayStart)

    #         # remove the items from the style lists
    #         del values[arrayStart: arrayEnd] 
    #         del transStyles[arrayStart: arrayEnd] 
    #         # print(transStyles)

    # return newValues





thisDef = {'file': 'FRANK CREDIT CARD-5534-Dec-20.pdf', 'template': 'ocbc_cc_frank'}  # 11
thisDef = {'file': 'dbs-cashline.pdf', 'template': 'dbs_cl'}  # 5
thisDef = {'file': 'dbs-consolidated.pdf', 'template': 'dbs_cc'}  # 10
thisDef = {'file': 'CardStatement_012021.pdf', 'template': 'citi_cc'} #
thisDef = {'file': 'eStatement200104151222728937696.pdf', 'template': 'scb_cc'} #55


thisDef = {'file': '2021-01-07_Statement.pdf', 'template': 'hsbc_cc'} # doesn't work, images only
thisDef = {'file': '11512aa8-e77d-4f46-90b9-cd1dea1c7fd3.pdf', 'template': 'anz_sav_old'} # old format didn't work - not full content


thisDef = {'file': 'estatement (1).pdf', 'template': 'bankwest'} # 

thisDef = {'file': 'estatement (60).pdf', 'template': 'bankwest'} # 


thisDef = {'file': '2b776bd1-9e10-4520-a56a-431131983879.pdf', 'template': 'anz_cc'} #

thisDef = {'file': 'f1feb0a8-a88a-4ac5-ac30-b34e691029dc.pdf', 'template': 'anz_sav'} # works, new format with single trans
thisDef = {'file': '1f9c0d7a-feae-4976-aeed-0787d11730a8.pdf', 'template': 'anz_sav'} # checking with new format with multiple page


trial = True
trial = False



def filterByLine(text, start, end, styles, checks, accountFind, ignore, backfill, matchByStyles, includeBlanks):
    
    lines = text.splitlines()
    transStyles = []
    lineType = None
    bRead = False
    skip = 0
    starts = 0
    i =0

    account = None
    values = []
    newValues = []
    value = {}

    for line in lines:
        # if i==20: break
        i += 1


        # check if the account is found
        findAccount = existsInArrayFind(line, accountFind)
        if findAccount != None:
            account=line

        # Check if the lineshould be read or skipped
        lineType = None
        if skip > 0: skip -= 1

        print(line)
        if line.strip() == "09 DEC OPENING BALANCE":
            print(line)

        foundStart = existsInArrayFind(line.strip(), start)
        foundEnd = existsInArrayFind(line.strip(), end)

        if foundStart != None:
            bRead = True
            skip = 1 + foundStart
            starts += 1
        
        elif foundEnd != None:
            bRead = False
            if foundEnd < 0:
                del values[foundEnd:]

        # check if the line should be ignored
        ignoreLine = existsInArrayFind(line, ignore)
        if ignoreLine != None:
            skip = 1 + ignoreLine


        # print (ignoreLine != None, ': ', line )

        # parse the line and check for attributes
        if (bRead) and (skip == 0):

            # check if attribute found
            bFound = False
            for field, check in checks.items():     # loop through field checks
                for chk in check:                    # loop through if field has multiple checks
                    if (not bFound) and (re.search(chk, line.strip(), re.IGNORECASE) != None):  
                        # value=line.strip()
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


            if (lineType != None) and (lineType != 'blank'):
                print('[', lineType, "]:", line)
                    

            if (lineType != 'account') and (lineType != None):
                transStyles.append(lineType)
                values.append(value)
                value = {}
               
    if matchByStyles:
        newValues = matchPatternsByStyles(styles, transStyles, values)
    else:
        newValues = matchPatternsByLines(styles, transStyles, values)

    # print('[Found Values]:', newValues)
    print('[Found Styles]:', len(newValues))
    return newValues    

    

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

                    transClean = filterByLine(transPages, template['startEnds']['sectionStart'], template['startEnds']['sectionEnd'], template['styles'], template['checks'], template['account']['accountStart'], template['ignore'], template['backfill'], template['matchByStyles'], template['includeBlanks'] )
                    print(transClean)
                    
                    # print('Record count: ', len(transClean))
                    break


readTheFile(thisDef, trial)

# transStyles = ['date', 'description', 'amount', 
# 'date', 'description', 'amount', 
# 'date', 'description', 'amount', 
# 'date', 'description', 'amount', 'currency', 'description',
# 'date', 'description', 'amount', 'currency', 'description',
# 'date', 'description', 'amount', 
# 'date', 'description', 'amount', 
# 'date', 'description', 'amount', 'currency', 'description',
# 'date', 'description', 'amount', 'currency', 'description',
# 'date', 'description', 'amount', 'currency', 'description',
# 'date', 'description', 'amount', 
# ]

# transStyles2 = ['1', '2', '3', 
# '4', '5', '6', 
# '7', '8', '9', 
# '10', '11', '12', 'currency', 'description',
# 'date', 'description', 'amount', 'currency', 'description',
# 'date', 'description', 'amount', 
# '121', '878', '989', 
# 'date', 'description', 'amount', 'currency', 'description',
# 'date', 'description', 'amount', 'currency', 'description',
# '15', '16', '17', '18', '19',
# 'date', 'description', 'amount', 
# ]

# # 1st @ 9

# styles = { 'style1' : ['date', 'description', 'amount', 'currency', 'description'],
#             'style2' : ['date', 'description', 'amount']
#             }






# for style in styles:
#     if style in list1:
#         print('found')



