#!/usr/bin/env python
import numpy as np

"""
The backend database for the CashYou hackathon project.
"""
import constants

class InvestGroup(object):
	""" Class that defines the attributes and operations possible with a single investment group."""
	def __init__(self, name, creator, members, advisors = None, desc = " ", stocksTracked = []):
		if type(name) is not str or type(desc) is not str:
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
				pass # Email advisor/advisor choice code
		return

	def __del__(self):
		return "Deleting group."
	def updateMembers(self, addingMember = False, member_id = None):
		""" Updates the list of members in a group."""
		try:
			if (addingMember is False) and (type(member_id) is int and member_id is not None):
				for num in range(0, len(self.members)):
					if self.members[num] == member_id:
						try:
							np.delete(self.members,num)
						except:
							return "Error deleting member."
				#search for member in list of members & delete
				return
			elif (addingMember is True) and (type(member_id) is int and member_id is not None):
				#Check if # of members is too large (DDOS)
				if len(self.members) > self.maxMembers:
					return "Too many group members. Please form a new group."
				else:
					np.append(self.members,member_id)
				return
			else:
				return "Invalid member ID."
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
	Each member will have an unique id that we will assign."""
	#List of idcts that give information
	# activeGroups = [{(groupID:(str), adminship:(bool), creatorship:(bool), amountInvested:(int))}]
	#				 [(string,    F/T		, T/F)]
	#same for prevGroups
	def __init__(self, userID, activeGroups, prevGroups, preferredStocks = [], auth = False):
		if auth:
			#permissions
			self.id = userID
			self.current_groups = activeGroups
			self.old_groups = prevGroups
			self.preferredStocks = preferredStocks
			# user.dev = isdev	   #True gives dev permissions
		else:
			return "You're not logged in! Please log in and try again."

	#group is a dict in the form given above
	def addGroup(self, group):
		self.current_groups.append(group)
	#groupID is a group ID
	def removeGroup(self, groupID):
		for x in range(0, len(self.current_groups)):
			if self.current_groups[x]["groupID"] == groupID:
				self.old_groups.append(self.current_groups.pop(x))
				return

	#stock is what it would show up with in our dictionary (e.g. V for Visa)
	def addPreferredStock(self, stock):
		preferredStocks.append(stock)
	def removePreferredStock(self, stock):
		preferredStocks.remove(stock)

	def updateGroupID(self, groupID, changedGroupID):
		for x in range(0, len(self.current_groups)):
			if self.current_groups[x]["groupID"] == groupID:
				self.current_groups[x]["groupID"] = changedGroupID
	def updateGroupAdminship(self, groupID, adminship):
		for x in range(0, len(self.current_groups)):
			if self.current_groups[x]["groupID"] == groupID:
				self.current_groups[x]["adminship"] = adminship
	def updateGroupInvestment(self, groupID, deltaInvested):
		for x in range(0, len(self.current_groups)):
			if self.current_groups[x]["groupID"] == groupID:
				if self.current_groups[x]["amountInvested"] + deltaInvested > 0:
					self.current_groups[x]["amountInvested"]+= deltaInvested
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
		pass
	def launchSite(self):
		for groupID in self.groups:
			self.investGroups.append(InvestGroup(name = groupID, creator = self.groups[groupID][self.creators], members = self.groups[groupID][self.members], advisors = self.groups[groupID][self.advisors],
				desc = self.groups[groupID][self.descript], stocksTracked = self.groups[groupID][self.stocksTracked]))
			# print(self.returnActiveMembers())
			# print(self.returnActiveAdvisors())
	def spawnGroup(self, name = None, creator = None, membersIn = [], advisorsIn = [], description = "", stocks = []):
		#membersin and advnisorsin both lists of member objects
		if name and name not in self.groups:
			self.groups[name] = {self.creators:creator, self.members:membersIn, self.advisors:advisorsIn, self.descript:description, self.stocksTracked:stocks}
		else:
			name = str(self.default_group_num)
			self.default_group_num+=1
			self.groups[name] = {self.creators:creator, self.members:membersIn, self.advisors:advisorsIn, self.descript:description, self.stocksTracked:stocks}
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

# if __name__ == "__main__":
# 	description = "A group devoted to investing in cashews."
# 	site = groupData()
# 	site.launchSite()
# 	print(site.returnActiveMembers())

	# A = InvestGroup("CashYou", 12345, 98765, description)
	# A.updateMembers(True, 23456)
	# A.updateMembers(False, 12345)
	# print(A.members)
	# A.deleteGroup()
