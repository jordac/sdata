"""
##Purpose of this code is to gather listing data and present it into a CSV file for management
#The script first reads 2 files one for errors and one for lister #'s
#it then compares the number of occurences that match the listers name within each file
#it then applys conversions based off numbers given on paper by lead's
#class ListerDetail is used to take in name of lister and compare against data
"""
#imported operator for sorting of dictionary for po output
import operator
#imported csv for file handeling
import csv

#Make sure file is in same directory as script.
#Open's file of current listing detail for 1 week
CURRENTLISTINGDATA=open("currentlistingdetail.csv", "rb")
data = csv.reader(CURRENTLISTINGDATA, delimiter=",")
data = [row for row in data]
rowdata = [field for field in data]
rowdata.pop(0)
ALLLISTERS = [rows[18] for rows in rowdata]
#Open's file of current errors and parses data, 
ERRORSLIST = open("currenterrorlist.csv", "rb")
Edata = csv.reader(ERRORSLIST, delimiter=",")
Edata = [row for row in Edata]
Erowdata = [field for field in Edata]

#Returns new list of ListerDetail intances for each name in currentlistingdata
def createNewListerDetail(namelist):
    """
    Creates an instance of ListerDetail for every name in CURRENTLISTINGDATA
    for the purpose of writing to a csv file.
    """
    global listerNames
    listerNames = []
    for name in namelist:
        splitname = name.split(" ",1)
        firstinitials = splitname[0][0]+splitname[-1][0]
        print "New Lister Instance:  " + str(firstinitials)
        firstinitials = ListerDetail(name)
        print firstinitials.name
        listerNames.append(firstinitials)
    return listerNames
    
        
def masterWriteToCsv(objectlist):
    """
    Relys on writeCsvFile to append each converted lister detail to outfile
    """
    for lister in objectlist:
        #conditional to only write to outfile if lister is in san Diego conditional can be applied in above
        #function should be tested further for runtime preformance
        if "San Diego" in lister.listerLocation:
            print lister.name
            writeCsvFile(outfile, [[lister.name]+datatocsv], [lister.listedbyweek()], [lister.errorratedata(),lister.listedbystockweekly(), lister.POdatabylister(),list([" "])])
            print "new lister data added to file!"
    writeCsvFile(outfile, [""], [masterobj.POtotalnumberforall()], [""])
    print "Completed lister detail... see output file for results"
##writeCsvFile(outfile, OGdatatocsv, [OG.listedbyweek()], [OG.errorratedata()])
    

#My data is 2 lists returned by a func, need to add the header list to the two lists
def writeCsvFile(fname, data, data2, data3, *args, **kwargs):
    """
    @param fname: string, name of file to write
    @param data: list of list of items

    Write data to file
    """
    mycsv = csv.writer(open(fname, 'ab'), *args, **kwargs)
    for row in data:
        mycsv.writerow(row)
    for row2 in data2:
        mycsv.writerows(row2)
    for row3 in data3:
        mycsv.writerows(row3)




#Plot every lister's weekly numbers in plot for team henry, can be refactored for HenrysTeam require variable tean
def PlotTeam():
    """
    Requires import matplotlib for call
    plots teamHenry on graph
    refactor for each team or listers by adding intake of ListerDetail.name to graph individuals or teams
    """
    global HenrysTeam
    count = 0
    days = []
    listerlist = []
    namelist = []
    plt.title("Lister Detail for the week")
    for name in HenrysTeam:
        namelist.append(name)
        currentlister = ListerDetail(name)
        listerlist.append(currentlister)
        numbers = currentlister.listedbyweek()[1]       
        days = [1,2,3,4,5,6]
        count += 1
        plt.subplot()
        #print len(days),len(numbers)
        plt.plot(days,numbers, label=name)
        plt.ylabel(name)
        plt.xlabel("Shoes Listed")     
    plt.legend()    
    plt.show()

#Object to contain lister name and data
class ListerDetail(object):
    """
    Class takes in lister name and renders data
    lister name is first and last name with a comma seperation
    datarendered = a converted CURRENTLISTERDATA row by row

    """
    def __init__(self, name, datarendered=rowdata, errordata=Erowdata):
        self.name = name
        self.datarendered = datarendered
        self.datarendered1 = [rows for rows in datarendered if self.name in rows]
        self.errordata = errordata
        self.datesInListerData = set([rows[3] for rows in datarendered])
        self.listerLocation = set([rows[19] for rows in datarendered if self.name in rows])
        """
        create a function for the below 2 datasets to count items listed under each PO# and one for stocks.
        """
        self.posAllWorkedOn = set([rows[0] for rows in datarendered])
        self.posListerworkedOn = set([rows[0] for rows in datarendered if self.name in rows])
        self.stockTypesWorkedOn = set([rows[1] for rows in self.datarendered1])
    
    def POdatabylister(self):
        listerPOdict = {}
        for item in self.posListerworkedOn:
            listerPOdict[item] = 0
        for rows in self.datarendered:
            if rows[18] == self.name:
                currentvalue = listerPOdict[rows[0]]
                listerPOdict[rows[0]] = currentvalue + int(rows[4])
        listerPOdictSorted = sorted(listerPOdict.iteritems(), key= operator.itemgetter(1))
        return [("PO","Items Listed")]+listerPOdictSorted[::-1]

            
    def POtotalnumberforall(self):
        weeksPOdict = {}
        for item in self.posAllWorkedOn:
            weeksPOdict[item] = 0
        for rows in self.datarendered:
            if rows[19] == "San Diego":
                currentvalue = weeksPOdict[rows[0]]
                weeksPOdict[rows[0]] = currentvalue+int(rows[4])
        weeksPOdictSorted = sorted(weeksPOdict.iteritems(), key=operator.itemgetter(1))
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print " Finished writing PO data to output file "
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        #return [weeksPoDictSorted.keys(), weeksPoDictSorted.values()]
        return [("PO", "# of items")]+weeksPOdictSorted[::-1]

    def listedbystockweekly(self):
        weekstockdict = {}
        for item in self.stockTypesWorkedOn:
            weekstockdict[item] = 0
        for rows in self.datarendered:
            if self.name in rows[18]:
                currentvalue = weekstockdict[rows[1]]
                weekstockdict[rows[1]] = currentvalue+int(rows[4])
        return [weekstockdict.keys(), weekstockdict.values()]

    def errorbylister(self):
        """
        uses firstName data from CURRENTLISTINGDATA to compare against ERRORSLIST names
        """
        count = 0
        #excluded code for no need to manipulate data further for runtime preformance
        #if self.datesInListerData[-1] == "dates":
            #self.datesInListerData.pop(-1)
        
        firstName = self.name.split(" ",1)
        #print firstName[0] 
        for rows in self.errordata:
            if firstName[0].lower() in rows[1].lower():
                #print rows[6].split("/")[0]
                datesSplit = rows[6].split("/")
                #print datesSplit
                if len(datesSplit[0]) == len("1"):
                    #print "single month"
                    convertedMonth = str("0")+str(datesSplit[0])
                    datesSplit[0] = convertedMonth
                if len(datesSplit[1]) == len("1"):
                    convertedDay = str("0")+str(datesSplit[1])
                    datesSplit[1] = convertedDay
                convertedDate = str(datesSplit[2])+str("-")+str(datesSplit[0])+str("-")+str(datesSplit[1])
                if convertedDate in self.datesActiveListing:
                    count += 1
                
        return count
        #Test 1 Success
        #print "You should have 46" + str(count)
#Grabs percentage by dividing total errors for active days listing / total shoes for the week converted        
    def errorratebylister(self):
        """
        Returns weekly error rate by dividing errors found on active days listing and divding that...
        against totalForTheWeekConverted number for individual lister
        """
        totalForTheWeekConverted = sum(self.listedbyweek()[1])
        if totalForTheWeekConverted > 0:
            weeklyErrorRate = float(self.errorbylister()) / float(totalForTheWeekConverted)
        else:
            weeklyErrorRate = 0  
        return str(round(weeklyErrorRate,4)*100)+str("%")
        
#Returns 1 list of string data to parse into file        
    def errorratedata(self):
        """
        Adds header and presents code for write to CSV
        """
        header = ["Errors", "Total Shoes Listed", "Error Percentage Rate"]
        return [header, [str(self.errorbylister()), str(sum(self.listedbyweek()[1])), str(self.errorratebylister())]]

#Pulls all items based on name    
    def filterbyname(self):
        """
        filters shoes "soley"(haha) upon condition that it was given a lot without conversions
        """
        shoesListed=0
        for rows in self.datarendered:
            if self.name in rows[18]:
                shoesListed+=1
        print "Shoes Listed by s"+str(self.name)+" "+str(shoesListed)
        
#Pulls all items listed under a current day returns number
    def filterbyday(self, date):
        """
        Filters shoes listed per day for lister based on date given and if lister.name is in datarendered from...
        CURRENTLISTINGDATA
        """
        listedOnDay = 0
        for rows in self.datarendered:
            if self.name in rows[18]:
                if date in rows[3]:
                    listedOnDay+=1
        #print listedOnDay
        day_numbers = [[date],[listedOnDay]]
        return listedOnDay
    
#prototype not for use
    def filterbyweek1(self, data=rowdata):
        """
        MUST BE RUN BEFORE ERROR DATA COLLECTED!
        THIS IS FOR ACTIVATION OF self.activeDaysListing
        This method gathers date data as well as number of items listed per date
        This method returns two lists dates(I.E[date,date,date...],[#,##,###,]
        """
        listedOnCurrentDate = 0
        listedOnDate = []
        dates = []
        previousdate = None
        for rows in self.datarendered:
            for date in rows[3]:
                if self.name in rows[18]:
                    currentdate = rows[3]
                    if currentdate != previousdate:
                        dates.append(currentdate)
                        listedOnDate.append(listedOnCurrentDate)
                        listedOnCurrentDate=0
                    else:
                        listedOnCurrentDate += 1
                    previousdate = currentdate
        return dates, listedOnDate
#returns 2 lists, 1 of dates for week other for numbers assosciated with name.        
    def listedbyweek(self):
        """
        Returns dates,numbers for lister I.E [2/10/2014],[127]... each a pair an individual list
        """
        dates = []
        numbersByDate = []
        previousdate = None
        for rows in self.datarendered:
            for date in rows[3]:
                currentdate = rows[3]
                if currentdate != previousdate:
                    dates.append(currentdate)
                previousdate = currentdate
        for date in dates:
            numbersByDate.append(self.filterbystock(date))
        if numbersByDate[-1] == 0:
            dates.pop(-1)
            numbersByDate.pop(-1)
        self.datesActiveListing = dates
        print dates
        return dates,numbersByDate
    
    def plotweeknumbers(self):
        """
        Requires import matplotlib
        Plots numbers for team for 1 week
        """
        numbers = self.listedbyweek()[1]
        days_list = ['Monday','Tuesday','Wednesday', 'Thursday','Friday','Saturday']
        count = 1
        days = []
        for date in self.listedbyweek()[0]:
            days.append(count)
            count += 1
        plt.plot(days,numbers,"green")
        return plt.show()
    
                
                        
    
#Pulls type of stock and iterates through file adding to total    
    def filterbystock(self,date):
        """
        Filters items based on stocktype
        """
        stockTypeDict = {}
        count = 0
        missedStock = 0
        convertedTotal = 0
        for rows in self.datarendered:
            if self.name in rows[18]:
                if date in rows[3]:
                    #print date
                    if rows[1] not in stockTypeDict.iterkeys():
                        stockTypeDict[rows[1]] = 1
                    else:
                        current_val = stockTypeDict[rows[1]]
                        stockTypeDict[rows[1]] = current_val+int(rows[4])
                        #print rows[4]
            if self.name in rows[18]:
                if date in rows[3]:
                    if "Boots" in rows[11]:
                        convertedTotal += 1.2
                        stockTypeDict[rows[1]] -= 1
                        print "BOOTS!"
        for types in stockTypeDict:
            #print types
            #print stockTypeDict[types]
            #print type(types)
            print self.name+" listed "+str(types)+" shoes "+str(stockTypeDict[types])+" times."
            if types == "Returns" or types == "Loose":
                 convertedTotal += stockTypeDict[types] * 1.4
                 print "Returns or loose added"
            elif types == "Bulkstock" or types == "Storestock":
                convertedTotal += stockTypeDict[types] * 1
            elif types == "Closeout" or types == "Inline":
                convertedTotal += stockTypeDict[types] * .167
            else:
                print "Did not convert, didn't properly specify stocktypes.!"
                missedStock += 1
                print missedStock
                print "YOU NEED A CONDITIONAL FOR!: " +str(types)
        return convertedTotal
            
    def filterbydaywithhours(self, date, hours=7.5):
        print "Total hourly average for "+str(date)+" with "+str(hours)+" considered listing is "+str(int(self.filterbyday(date))/hours)
        
                 
                    
JC = ListerDetail('Jordan Cullen')
LL = ListerDetail('Lori Lerma')
#JC.filterbystock("2014-02-10")
#print JC.name
#print JC.filterbyname()
#print JC.filterbyday("2014-01-27")
#print JC.datarendered1
#print JC.filterbydaywithhours("2014-01-27", 7.5)
#print JC.filterbystock()
#print LL.filterbystock()
#print LL.filterbyweek()
#print LL.name+str(" numbers for the week ")+str(LL.listedbyweek())
#For each day we want a list and a seperate list for the numbers
#Use list of 2 lists... list 1 is called day_numbers others are day and numbers
#Then plot in matplotlib using lists day, numbers.
#LL.plotweeknumbers()
#JC.plotweeknumbers()


CURRENTLISTINGDATA.close()
ERRORSLIST.close()


def test_filterbydaywithhours(totallisted,hours,date):
    sampleL = ListerDetail("Lister1")
    print "Total hourly " + str(totallisted/hours)
    sampleL.filterbydaywithhours("2014-01-27", 7.5)
        
    
#print test_filterbydaywithhours(133, 7.5, 0)


#JCdatatocsv=[["Dates","Shoes Listed", JC.name]]

outfile = r'output.csv'
datatocsv = ["Dates", "Shoes Listed", ]

#writeCsvFile(outfile, JCdatatocsv, [JC.listedbyweek()], [JC.errorratedata()])
#writeCsvFile(outfile, LLdatatocsv, [LL.listedbyweek()], [LL.errorratedata()])
#writeCsvFile(outfile, OGdatatocsv, [OG.listedbyweek()], [OG.errorratedata()])
#writeCsvFile(outfile, MGdatatocsv, [MG.listedbyweek()], [MG.errorratedata()])
#writeCsvFile(outfile, DRdatatocsv, [DR.listedbyweek()], [DR.errorratedata()])
#writeCsvFile(outfile, LRdatatocsv, [LR.listedbyweek()], [LR.errorratedata()])
#PlotTeam()
#print "Jordan".lower()
#print Erowdata[1][1]
##print JC.errorbylister()
##int LL.errorbylister()
#print JC.errorratebylister()
#print LL.errorratebylister()
#print sum(JC.listedbyweek()[1])
#print JC.datesActiveListing
#print DR.errorratedata()
#print DR.name
###
###
"""
Master function call below
uses masterWriteToCsv with list generated from CURRENTLISTINGDATA of lister names within company
"""
masterobj = ListerDetail("Master, Admin")
masterWriteToCsv(createNewListerDetail(set(ALLLISTERS)))
#print JC.posListerworkedOn
#print JC.stockTypesWorkedOn
#print JC.listedbystockweekly()
#print LL.listedbystockweekly()
##print JC.listedbyweek()
#print JC.errorratedata()