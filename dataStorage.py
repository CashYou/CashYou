#!/usr/bin/env python
import numpy as np
from Constants import *
import stockGatherer
import pprint
import random
import pickle

"""
The backend database for the CashYou hackathon project.
"""

LOOKUP_TABLE = {"Visa Inc.": "V", "UnitedHealth Group Incorporated": "UNH", "Procter & Gamble Company [The]": "PG", "Coca-Cola Company [The]": "KO", "Goldman Sachs Group Inc. [The]": "GS", "Wal-Mart Stores Inc.": "WMT", "Merck & Company Inc.": "MRK", "Verizon Communications Inc.": "VZ", "United Technologies Corporation": "UTX", "The Travelers Companies Inc.": "TRV",
                "Walt Disney Company (The)": "DIS", "Boeing Company (The)": "BA", "General Electric Company": "GE", "Home Depot Inc. (The)": "HD", "3M Company": "MMM", "Pfizer Inc": "PFE", "Nike Inc.": "NKE", "McDonald's Corporation": "MCD", "JP Morgan Chase & Co.": "JPM", "Intel Corporation": "INTC",
                "Cisco Systems Inc.": "CSCO", "Chevron Corporation": "CVX", "Caterpillar, Inc.": "CAT", "American Express Company": "AXP", "Johnson & Johnson": "JNJ", "Exxon Mobil Corporation": "XOM", "Microsoft Corporation": "MSFT", "International Business Machines Corporation": "IBM", "Apple Inc.": "AAPL"}

# Dictionary for file names to get stock info
FILE_NAMES = {}
for x in LOOKUP_TABLE:
    FILE_NAMES[x] = LOOKUP_TABLE[x] + ".p"

GROUP_ID = "groupID"
ADMINSHIP = "adminship"
CREATORSHIP = "creatorship"
AMOUNT_INVESTED = "amountInvested"
# max number of members per group
MAX_MEMBERS = 20


class InvestGroup(object):
    """ Class that defines the attributes and operations possible with a single investment group.
            Creator, members, and advisors are all lists of groupMember s"""

    def __init__(self, name, creator, members, advisors=None, desc=" ", stocksTracked=[]):
        if type(name) is not str and type(desc) is not str:
            print("Error creating group.")
        else:
            self.name = name
            self.desc = desc
            self.rating = None
            self.numRaters = 0
            self.totalCash = 0
            self.members = members
            self.creator = creator
            self.stocksTracked = stocksTracked

            if advisors is not None:
                self.advisors = advisors
            else:
                pass  # Email advisor/advisor choice code

    def __del__(self):
        return "Deleting group."

    def __str__(self):
        final_string = "THE MEMBERS ARE: "
        for x in self.members:
            final_string += (str(x) + "\n")
        final_string += "\n\nTHE CREATOR/S IS/ARE:"
        for y in self.creator:
            final_string += (str(y) + "\n")
        final_string += ("Total Cash: " + str(self.totalCash) + "\n")
        final_string += ("Tracked stocks: \n")
        for x in self.stocksTracked:
            final_string += (x + "\n")
        return final_string + "\n\n\n"

    def updateMembers(self, addingMember=False, member_id=None, member=None):
        """ Updates the list of members in a group.
                addingMember = boolean, member_id = (something, as long as it's consistent)
                member = groupMember"""
        try:
            if member_id and (type(member_id) is int):
                if (addingMember is False):
                    for num in range(0, len(self.members)):
                        if self.members[num].id == member_id:
                            try:
                                self.members.pop(num)
                                break
                            except:
                                return "Error deleting member."
                elif (addingMember is True) and member:
                    # Check if # of members is too large (DDOS)
                    if len(self.members) >= MAX_MEMBERS:
                        return "Too many group members. Please form a new group."
                    else:
                        self.members.append(member)
            else:
                return "Invalid member ID."
            return
        except:
            return "Error updating member list."

    def updatePrevPerform(self):  # FFFFFFF - Update with code
        """Updates previous performance with new value"""
        # Nick's code
        # N/A for this weekend
        pass

    def getCurrRating(self):
        """Returns current rating."""
        return self.rating

    def getAdvisors(self):
        return self.advisors

    def updateRating(self, newRating):
        """Returns updated 0 to 5 star rating"""
        if newRating > 5.0:
            return "Invalid Input"
        if self.rating is None:
            rating = 0.0
        else:
            rating = self.rating
        self.rating = (rating * self.numRaters + newRating) / \
            (self.numRaters + 1)
        self.numRaters = self.numRaters + 1
        return self.rating

    def addStocksTracked(self, stock):
        stocksTracked.append(stock)

    def deleteStocksTracked(self, stock):
        stocksTracked.remove(stock)

    def currentFunds(self):
        curr_funds = 0
        for z in [self.members, self.advisors]:
            for x in self.members:
                for y in x.current_groups:
                    if y["groupID"] == self.name:
                        curr_funds += y["amountInvested"]
        self.totalCash = curr_funds

    def fundsChange(self, amt):
        self.totalCash += amt

    def getInfo(self):
        tracked = ""
        for x in range(0, len(self.stocksTracked)):
            if x > 0:
                tracked += ", " + self.stocksTracked[x]
            else:
                tracked += " " + self.stocksTracked[x]
        return "We are " + self.name + ". " + self.desc + " We prefer to trade:" + tracked + "."

    #takes in member name
    def removeMember(self, member):
        print(member)
        for x in self.members:
            print(str(x))
            print(x.name)
            if str(x.name) == str(member):
                x.removeGroup(self.name)
                self.members.remove(x)
                return True
        return None

    #takes in an actual groupMember
    def addMember(self, member):
        self.members.append(member)
        member.addGroup({"groupID":self.name, "adminship":False, "creatorship":False, "amountInvested":0})

class groupMember(object):
    """Stores groupmember specific data attributes for each user.
    Each member will have an unique id that we will assign.
    TODO: CHANGE AUTHORIZE TO OUTSIDE OF THIS"""
    # List of dicts that give information
    # activeGroups = [{(groupID:(str), adminship:(bool), creatorship:(bool), amountInvested:(int))}]
    #				 [(string,    F/T		, T/F)]
    # same for prevGroups
    def __init__(self, userID, name, activeGroups, prevGroups, preferredStocks=[]):
        # permissions
        self.id = userID
        self.name = name
        self.current_groups = activeGroups
        self.old_groups = prevGroups
        self.preferredStocks = preferredStocks
        # user.dev = isdev	   #True gives dev permissions

    def __str__(self):
        full = ("User ID: %s \nName: %s \nCurrent Groups: " % (self.id, self.name) ) + str(self.current_groups) + "\nOld Groups: " + \
            str(self.old_groups) + "\nPreferred stocks: " + \
            str(self.preferredStocks) + "\n"
        return full

    # group = {(groupID:(str), adminship:(bool), creatorship:(bool), amountInvested:(int))}
    def addGroup(self, group):
        self.current_groups.append(group)
    # groupID is a group ID

    def removeGroup(self, groupID):
        for x in range(0, len(self.current_groups)):
            if self.current_groups[x][GROUP_ID] == groupID:
                self.old_groups.append(self.current_groups.pop(x))
                return

    # stock is what it would show up with in our dictionary (e.g. V for Visa)
    def addPreferredStock(self, stock):
        preferredStocks.append(stock)

    def removePreferredStock(self, stock):
        preferredStocks.remove(stock)

    def updateGroupID(self, groupID, changedGroupID):
        for x in range(0, len(self.current_groups)):
            if self.current_groups[x][GROUP_ID] == groupID:
                self.current_groups[x][GROUP_ID] = changedGroupID

    def updateGroupAdminship(self, groupID, adminship):
        for x in range(0, len(self.current_groups)):
            if self.current_groups[x][GROUP_ID] == groupID:
                self.current_groups[x][ADMINSHIP] = adminship

    def updateGroupInvestment(self, groupID, deltaInvested):
        for x in range(0, len(self.current_groups)):
            if self.current_groups[x][GROUP_ID] == groupID:
                if self.current_groups[x][AMOUNT_INVESTED] + deltaInvested > 0:
                    self.current_groups[x][AMOUNT_INVESTED] += deltaInvested
                else:
                    print("Invalid investment request.")


class groupData(object):
    """ Instantiates all groups. The backbone of our database. """

    def __init__(self):
        self.all_Users = []
        self.groups = dict()
        self.investGroups = []
        self.default_group_num = 1
        self.advisors = "Advisors"
        self.members = "Members"
        self.creators = "Creators"
        self.descript = "Description"
        self.stocksTracked = "Tracking"

    def __str__(self):
        full_str = ""
        for x in self.groups:
            for y in self.groups[x]:
                if type(self.groups[x][y]) is list:
                    for z in self.groups[x][y]:
                        full_str += str(z) + "\n"
                else:
                    full_str += str(self.groups[x][y]) + "\n"
        full_str += "\n"
        for y in self.investGroups:
            full_str += str(y) + "\n\n"
        return full_str

    def launchSite(self):
        for groupID in self.groups:
            testNewGroup = InvestGroup(name=groupID, creator=self.groups[groupID][self.creators], members=self.groups[groupID][self.members], advisors=self.groups[groupID][self.advisors],
                                       desc=self.groups[groupID][self.descript], stocksTracked=self.groups[groupID][self.stocksTracked])
            self.investGroups.append(testNewGroup)

    def spawnGroup(self, name=None, creator=[], membersIn=[], advisorsIn=[], description="", stocks=[]):
        if name and name not in self.groups:
            self.groups[name] = {self.creators: creator, self.members: membersIn,
                                 self.advisors: advisorsIn, self.descript: description, self.stocksTracked: stocks}
        else:
            name = str(self.default_group_num)
            self.default_group_num += 1
            self.groups[name] = {self.creators: creator, self.members: membersIn,
                                 self.advisors: advisorsIn, self.descript: description, self.stocksTracked: stocks}

        # TODO: CHECK TO SEE IF DICT ALREADY IN MEMBERS THING AND UPDATE MEMBER IF IT IS
        for x in membersIn:
            dict_to_add = {GROUP_ID: name, ADMINSHIP: False,
                           CREATORSHIP: False, AMOUNT_INVESTED: 0.0}
            for a in x.current_groups:
                if a[GROUP_ID] == name:
                    pass
                else:
                    x.addGroup(dict_to_add)
            for b in x.old_groups:
                if a[GROUP_ID] == name:
                    x.old_groups.remove(b)
        for y in advisorsIn:
            dict_to_add = {GROUP_ID: name, ADMINSHIP: True,
                           CREATORSHIP: False, AMOUNT_INVESTED: 0.0}
            for a in y.current_groups:
                if a[GROUP_ID] == name:
                    pass
                else:
                    y.addGroup(dict_to_add)
            for b in y.old_groups:
                if a[GROUP_ID] == name:
                    y.old_groups.remove(b)
        for z in creator:
            dict_to_add = {GROUP_ID: name, ADMINSHIP: False,
                           CREATORSHIP: True, AMOUNT_INVESTED: 0.0}
            for a in z.current_groups:
                if a[GROUP_ID] == name:
                    pass
                else:
                    z.addGroup(dict_to_add)
            for b in x.old_groups:
                if a[GROUP_ID] == name:
                    z.old_groups.remove(b)

        favored_stocks = dict()
        for y in [self.creators, self.members, self.advisors]:
            for x in self.groups[name][y]:
                for z in x.preferredStocks:
                    if z in favored_stocks:
                        favored_stocks[z] += 1
                    else:
                        favored_stocks[z] = 1
        top_stocks = []
        highest = 0
        highest_Stock = ""
        for z in range(0, 3):
            for x in favored_stocks:
                if x not in top_stocks:
                    if favored_stocks[x] > highest:
                        highest = favored_stocks[x]
                        highest_Stock = x
            top_stocks.append(highest_Stock)
            highest = 0
            highest_Stock = ""
        self.groups[name][self.stocksTracked] = top_stocks

    def deleteGroup(self, groupName):
        if groupName in self.groups:
            for x in [self.members, self.creators, self.advisors]:
                for y in self.groups[groupName][x]:
                    y.removeGroup(groupName)
            self.groups.pop(groupName, None)
        else:
            print("Invalid group.")

    def returnActiveGroups(self):
        allGroups = []
        for x in self.groups:
            allGroups.append(x)
        return allGroups

    def returnActiveMembers(self, groupID):
        return self.groups[groupID][self.members]

    def returnActiveAdvisors(self, groupID):
        return self.groups[groupID][self.advisors]

    def lookupGroup(self, groupID):  # Return data on a requested group.
        return self.groups[groupID]

    def newGroupAdvisor(self, groupID, newAdvisorID, onlyAdmin=False):
        return

    def removeGroupAdvisor(self, groupID, oldAdvisorID):
        return

    #name is a string
    def findMemberByName(self, name):
        for x in self.members:
            if str(x.name) == str(name):
                return x

    def findAdvisorByName(self, name):
        for x in self.advisors:
            if str(x.name) == str(name):
                return x


# handles user's information
# TODO: @Yichen


class userData(object):
    def __init__(self, userID, groups):
        pass

    def createGroup(self):
        pass

    def joinGroup(self):
        groupMember(12345, self.activeGroups, self.prevGroups, True, False)

    def leaveGroup(self):
        pass

    def becomeAdvisor(self, groupID):
        pass


if __name__ == "__main__":
    remake = False
    if remake:
        description_test = "A group devoted to investing in cashews."
        site = groupData()
        test_users = []
        test_user_names = ["John", "Sherlock", "Watson", "Holmes", "Lydia", "Nicholas", "Victoria", "Yichen", "Prava", "Gracey", "Emily", "Sam"]
        test_dict = {0: ["V", "UNH", "TRV"], 1: ["MSFT", "JPM", "PG"], 2: ["APPL", "GE", "UNH"], 3: ["V", "MSFT", "XOM"],
                     4: ["HD", "GE", "VZ"], 5: ["CVX", "AXP", "BA"], 6: ["V", "MSFT", "APPL"], 7: ["UNH", "PG", "KO"]}
        for x in range(0, 10):
            temp_int = random.randint(0, 6)
            temp = groupMember(x, test_user_names[x], [], [], preferredStocks=test_dict[temp_int])
            if temp:
                test_users.append(temp)
        site.all_Users = test_users
        site.spawnGroup(name = "Cashoo", creator=[test_users[0]], membersIn=test_users[0:9],
                        advisorsIn=test_users[9:], description=description_test)
        site.spawnGroup(name = "Gesundheit", creator=[test_users[1]], membersIn=test_users[3:7],
                        advisorsIn=test_users[2:3], description="A group dedicated to cashewing in on the stock market.")
        site.launchSite()
        pickle.dump(site, open("ALL_GROUPS.p", "wb"))
    newsite = pickle.load(open("ALL_GROUPS.p", "rb"))




    # print(newsite.investGroups[0].getInfo())
    # print(newsite.investGroups[1].getInfo())
    # hi = newsite.investGroups[0].removeMember("John")
    # if hi:
    #     print("He's gone, Jim")
    # else:
    #     print("wrong name.")
    # newsite.investGroups[0].addMember(newsite.all_Users[0])
    # hi = newsite.investGroups[0].removeMember("John")
    # if hi:
    #     print("He's gone, Jim")
    # else:
    #     print("wrong name.")

    # print(site)
    # site.deleteGroup('1')
    # print("\n\n POST DELETE:")
    # print(site)
    # print("\n\n RETURN ACTIVE ADVISORS")
    # print(site.returnActiveAdvisors('2'))
    # print("\n\n RETURN ACTIVE MEMBERS:")
    # print(site.returnActiveMembers('2'))
