from dialog_tag import DialogTag
import json
import os
import datetime
import time
#Before everything, we load the model.


def printresults(dataoutput):
    print("Showing results for file", dataoutput[0])
    print("Old Dictionary Looks Like This:", dataoutput[1])
    print("Model Dictionary Looks Like This:", dataoutput[2])
    print("Base Dictionary Looks Like This:", dataoutput[3])
    print("Accuracy is ", dataoutput[5], "out of", dataoutput[4])

def savemetadata(dataoutputcompiled,filename):
    accbase = 0
    totalbase = 0
    f = open(filename, "a")
    for file in dataoutputcompiled:
        accbase += file[5]
        totalbase += file[4]
    f.write("Now the file has more content!")
    print("Total Accuracy is ", totalbase, "Number found is", accbase)
    #f.close()


#Converts from switchboards standard to the DSARMD Standard. Input is a string, output is a string.
def wordconversion(stringinput):
    dict = {
        "Statement-non-opinion" : "Assertion-Opinion",
        "Statement-opinion" : "Assertion-Opinion",
        "Repeat-phrase" : "Assertion-Opinion",
        "Collaborative Completion" : "Assertion-Opinion",
        "Quotation" : "Assertion-Opinion",
        "Or-Clause" : "Assertion-Opinion",
        "Acknowledge (Backchannel)" :"Acknowledge",
        "Appreciation" :"Acknowledge",
        "Response Acknowledgement": "Acknowledge",
        "Maybe/Accept-Part" : "Agree-Accept",
        "Agree/Accept" : "Agree-Accept",
        "Yes Answers" : "Agree-Accept",
        "Dispreferred answers" : "Response-Answer",
        "Affirmative Non-yes Answers" : "Response-Answer",
        "Response" : "Response-Non-Answer",
        "Hold Before Answer/Agreement" : "Response-Non-Answer",
        "Hedge": "Response-Non-Answer",
        "Reject" : "Disagree-Reject",
        "Negative Non-no Answers" : "Disagree-Reject",
        "No Answers": "Disagree-Reject",
        "Conventional-opening":"Conventional-Opening",
        "Signal-non-understanding": "Signal-Non-Understanding",
        "Conventional-closing":"Conventional-Closing",
        "Wh-Question" : "Information-Request",
        "Declarative Yes-No-Question" : "Information-Request",
        "Yes-No-Question" : "Information-Request",
        "Open-Question" : "Information-Request",
        "Rhetorical-Question" : "Information-Request",
        "Tag-Question" : "Information-Request",
        "Summarize/Reformulate"  : "Confirmation-Request",
        "Backchannel in Question Form" : "Confirmation-Request",
        "Offers, Options Commits":"Offer-Commit",
        "Action-directive":"Action-Directive",
        "Abandoned"  : "Other-Conventional-Phrase",
        "Turn-exit"  : "Other-Conventional-Phrase",
        "Other"  : "Other-Conventional-Phrase",
        "Downplayer" : "Other-Conventional-Phrase",
        "Apology"  : "Other-Conventional-Phrase",
        "Other"  : "Other-Conventional-Phrase",
        "Thanking"  : "Other-Conventional-Phrase",
        "Non-Verbal" :"Delete Line",
        "Uninterpretable" : "Delete Line",
        "Self-talk" : "Delete Line" ,
        "3rd-Party Talk" : "Delete Line"
    }
    if stringinput in dict.keys():
        stringoutput = dict[stringinput]
    else:
        print(stringinput)
        stringoutput = ""
#Exception, uncomment for testing.
#    if stringoutput == "":
#        raise Exception("Output not found")
    return stringoutput

def testaccuracyall(path):
    print("Running Accuracy Scan")
    directory = path
    outputlist = []
    for entry in os.scandir(directory):
        if (entry.path.endswith(".json")):
            print("Testing Accuracy For ", entry.path)
            outputlist.append(testjsonaccuracy(entry.path))
    return outputlist



def testjsonaccuracy(filename):
    input = {}
    with open(filename) as read_file:
        input = json.load(read_file)
    parsed = inputtodict(input)
    output = []
    output.append(filename)
    outputdict = {}
    oldoccurances = {}
    modeloccurances = {}
    baseoccurances = {}
    totalutterances = 0
    correcttags = 0
    for i in parsed:
        if i[0] == None:
            continue
        totalutterances +=1
        #Print("i0 is ",i[0])
        #Run preprocess on i[0]
        #Insert preprocessing here.
        theirtag = model.predict_tag(i[0])
        oldtag = theirtag
        theirtag = wordconversion(theirtag)
        ourtag = i[1]
        if ourtag == '':
            totalutterances -= 1
            continue
        tag = ourtag
        #print("Tag is",tag)
        #tagparts = ourtag.split(':')
        #print(tagparts)
        #tag = tagparts[1]
        if(theirtag == tag):
            correcttags += 1
        else:
            print("Theirtag: ", theirtag, "Oldtag", oldtag, "Tag: ", tag)
        if oldtag not in oldoccurances.keys():
            oldoccurances[oldtag] = 1
        else:
            oldoccurances[oldtag] += 1
        if theirtag not in modeloccurances.keys():
            modeloccurances[theirtag] = 1
        else:
            modeloccurances[theirtag] += 1
        if tag not in baseoccurances.keys():
            baseoccurances[tag] = 1
        else:
            baseoccurances[tag] += 1
    output.append(oldoccurances)
    output.append(modeloccurances)
    output.append(baseoccurances)
    output.append(totalutterances)
    output.append(correcttags)
    return output

#Takes in an input of a list turns with dicts inside of it.
def inputtodict(inputdict):
    turns = inputdict["turns"]
    dictlist = []
    outputlist = []
    # Turns is a list of interactions.
    for i in turns:
        dictlist.append(i["text"])
        # print(i["text"])
        dictlist.append(i["dialog_act"])
        # print(i["dialog_act"])
        appendlist = dictlist.copy()
        outputlist.append(appendlist)
        dictlist.clear()
    #print(outputlist)
    return outputlist


#Run the main.
# K is a list of all possible tags, useful for later.
model = DialogTag('distilbert-base-uncased')


#make sure to set yourpath properly.
allresults = testaccuracyall(r'YourPath')
for i in allresults:
    printresults(i)

modeloccurancesoutput = {}
baseoccurancesoutput = {}
print(allresults)
'''
for i in allresults.keys():
    if i not in modeloccurancesoutput.keys():
        modeloccurancesoutput[i] = allresults[2][i]
    else:
        modeloccurancesoutput[i] += allresults[2][i]
'''



#savemetadata(allresults, "results.txt")


#for i in allresults:
#    for k in i[2]:
#        modeloccurancesoutput

#    printresults(i)


