#!/usr/bin/env python
import numpy as np
from Constants import *
import stockGatherer
import pprint

"""
The backend database for the CashYou hackathon project.
"""

LOOKUP_TABLE = {"Visa Inc.":"V", "UnitedHealth Group Incorporated":"UNH", "Procter & Gamble Company [The]":"PG", "Coca-Cola Company [The]":"KO", "Goldman Sachs Group Inc. [The]":"GS", "Wal-Mart Stores Inc.":"WMT", "Merck & Company Inc.":"MRK", "Verizon Communications Inc.":"VZ", "United Technologies Corporation":"UTX", "The Travelers Companies Inc.":"TRV",
                "Walt Disney Company (The)":"DIS", "Boeing Company (The)":"BA", "General Electric Company":"GE", "Home Depot Inc. (The)":"HD", "3M Company":"MMM", "Pfizer Inc":"PFE", "Nike Inc.":"NKE", "McDonald's Corporation":"MCD", "JP Morgan Chase & Co.":"JPM", "Intel Corporation":"INTC",
                "Cisco Systems Inc.":"CSCO", "Chevron Corporation":"CVX", "Caterpillar, Inc.":"CAT", "American Express Company":"AXP", "Johnson & Johnson":"JNJ", "Exxon Mobil Corporation":"XOM", "Microsoft Corporation":"MSFT", "International Business Machines Corporation":"IBM", "Apple Inc.":"AAPL"}

#Dictionary for file names to get stock info
FILE_NAMES = {}
for x in LOOKUP_TABLE:
    FILE_NAMES[x] = LOOKUP_TABLE[x] + ".p"

GROUP_ID = "groupID"
ADMINSHIP = "adminship"
CREATORSHIP = "creatorship"
AMOUNT_INVESTED = "amountInvested"
#max number of members per group
MAX_MEMBERS = 20


class InvestGroup(object):
	""" Class that defines the attributes and operations possible with a single investment group.
		Creator, members, and advisors are all lists of groupMember s"""
	def __new__(self, name, creator, members, advisors = None, desc = " ", stocksTracked = []):
		if type(name) is not str or type(desc) is not str:
			print("Error creating group.")
			return None
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
				pass # Email advisor/advisor choice code
		return
	def __del__(self):
		return "Deleting group."

	def updateMembers(self, addingMember = False, member_id = None, member = None):
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
					#Check if # of members is too large (DDOS)
					if len(self.members) >= MAX_MEMBERS:
						return "Too many group members. Please form a new group."
					else:
						self.members.append(member)
			else:
				return "Invalid member ID."
			return
		except:
			return "Error updating member list."
	def updatePrevPerform(self): # FFFFFFF - Update with code
		"""Updates previous performance with new value"""
		#Nick's code
		pass
	def getCurrRating(self):
		"""Returns current rating."""
		return self.rating
	def updateRating(self, newRating):
		"""Returns updated 0 to 5 star rating"""
		if newRating > 5.0:
			return "Invalid Input"

		if self.rating is None:
			rating = 0.0
		else:
			rating = self.rating

		self.rating = (rating * self.numRaters + newRating) / (self.numRaters + 1)
		self.numRaters = self.numRaters + 1
		return self.rating
	# def deleteGroup(self): # FFFFFF - Not deleting object instance currently- handle with groupData manager function?
	# 	"""When group is deleted, deletes all associated data or stores it in the stack for later deletion"""
	# 	del self
	# 	return

class groupMember(object):
	"""Stores groupmember specific data attributes for each user.
	Each member will have an unique id that we will assign.
	TODO: CHANGE AUTHORIZE TO OUTSIDE OF THIS"""
	#List of idcts that give information
	# activeGroups = [{(groupID:(str), adminship:(bool), creatorship:(bool), amountInvested:(int))}]
	#				 [(string,    F/T		, T/F)]
	#same for prevGroups
	def __init__(self, userID, activeGroups, prevGroups, preferredStocks = []):
		#permissions
		self.id = userID
		self.current_groups = activeGroups
		self.old_groups = prevGroups
		self.preferredStocks = preferredStocks
		# user.dev = isdev	   #True gives dev permissions

	def __str__(self):
		full = ("User ID: %s \nCurrent Groups: " % self.id) + str(self.current_groups) + "\nOld Groups" + str(self.old_groups) + "\npreferred stocks:" + str(self.preferredStocks)
		return full

	#group = {(groupID:(str), adminship:(bool), creatorship:(bool), amountInvested:(int))}
	def addGroup(self, group):
		self.current_groups.append(group)
	#groupID is a group ID
	def removeGroup(self, groupID):
		for x in range(0, len(self.current_groups)):
			if self.current_groups[x][GROUP_ID] == groupID:
				self.old_groups.append(self.current_groups.pop(x))
				return

	#stock is what it would show up with in our dictionary (e.g. V for Visa)
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
					self.current_groups[x][AMOUNT_INVESTED]+= deltaInvested
				else:
					print("Invalid investment request.")

class groupData(object):
	""" Instantiates all groups. The backbone of our database. """
	def __init__(self):
		self.groups = dict()
		self.investGroups = []
		self.default_group_num = 0
		self.advisors = "Advisors"
		self.members = "Members"
		self.creators = "Creators"
		self.descript = "Description"
		self.stocksTracked = "Tracking"
	def launchSite(self):
		for groupID in self.groups:
			self.investGroups.append(InvestGroup(name = groupID, creator = self.groups[groupID][self.creators], members = self.groups[groupID][self.members], advisors = self.groups[groupID][self.advisors],
				desc = self.groups[groupID][self.descript], stocksTracked = self.groups[groupID][self.stocksTracked]))
			# print(self.returnActiveMembers())
			# print(self.returnActiveAdvisors())
	def spawnGroup(self, name = None, creator = [], membersIn = [], advisorsIn = [], description = "", stocks = []):
		#membersin and advnisorsin both lists of member objects
		if name and name not in self.groups:
			self.groups[name] = {self.creators:creator, self.members:membersIn, self.advisors:advisorsIn, self.descript:description, self.stocksTracked:stocks}
		else:
			name = str(self.default_group_num)
			self.default_group_num+=1
			self.groups[name] = {self.creators:creator, self.members:membersIn, self.advisors:advisorsIn, self.descript:description, self.stocksTracked:stocks}

		for x in membersIn:
			dict_to_add = {GROUP_ID:name, ADMINSHIP:False, CREATORSHIP:False, AMOUNT_INVESTED:0.0}
			x.addGroup(dict_to_add)
		for y in advisorsIn:
			dict_to_add = {GROUP_ID:name, ADMINSHIP:True, CREATORSHIP:False, AMOUNT_INVESTED:0.0}
			y.addGroup(dict_to_add)
		for z in creator:
			dict_to_add = {GROUP_ID:name, ADMINSHIP:False, CREATORSHIP:True, AMOUNT_INVESTED:0.0}
			z.addGroup(dict_to_add)
	def deleteGroup(self, groupName):
		self.groups.pop(groupName, None)
	def returnActiveGroups(self):
		allGroups = []
		for x in self.groups:
			allGroups.append(x)
		return allGroups
	def returnActiveMembers(self, groupID):
		return self.groups[groupID][self.members]
	def returnActiveAdvisors(self, groupID):
		return self.groups[groupID][self.advisors]
	def lookupGroup(self, groupID): #Return data on a requested group.
		return self.groups[groupID]

#handles user's information
#TODO: @Yichen
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
	description_test = "A group devoted to investing in cashews."
	site = groupData()
	test_users = []
	for x in range(0, 10):
		temp = groupMember(x, [], [], preferredStocks = [])
		if temp:
			test_users.append(temp)
	pp = pprint.PrettyPrinter(indent=4)
	for x in test_users:
		print(x)

	site.spawnGroup(creator = test_users[0], membersIn = test_users[1:9], advisorsIn = [test_users[9:]], description = description_test)
	print(site)
	# site.spawnGroup("Test",)
	# site.launchSite()
	# print(site.returnActiveMembers())

	# A = InvestGroup("CashYou", 12345, 98765, description)
	# A.updateMembers(True, 23456)
	# A.updateMembers(False, 12345)
	# print(A.members)
	# A.deleteGroup()
