#!/usr/bin/env python
import numpy as np

"""
The backend database for the CashYou hackathon project.
"""

class InvestGroup(object):
	""" Class that defines the attributes and operations possible with a single investment group."""
	def __init__(self, name, creator, adv = None, desc = " ", prevPerform = []):
		if type(name) is not str and type(desc) is not str:
			print("Error creating group.")
			return
		else:
			self.name = name
			self.desc = desc

			self.rating = None
			self.numRaters = 0 
			self.members = np.array([creator])
			self.maxMembers = 2

			if adv is not None:
				self.adv = adv
			else:
				pass # Email advisor/advisor choice code
			return

	def __del__(self):
		return "Deleting group."

	def updateMembers(self,addingMember = False, member_id = None):
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
	"""Stores groupmember specific data attributes for each user."""
	def __init__(self, userID, activeGroups, prevGroups, amountInvested, auth = False, isadmin = False, isdev = False):
		if auth:
			#permissions
			self.advisor = isadmin #True gives superuser permissions
			user.dev = isdev	   #True gives dev permissions
			self.invested = amountInvested
		else:
			return "You're not logged in! Please log in and try again."

class groupData(object):
	""" Instantiates all groups. The backbone of our database. """
	def __init__(self):
		self.groups = np.array(["A", "B"])
		pass
	def launchSite(self):
		for groupID in self.groups:
			groupID = InvestGroup("CashYou", 12345, 98765, description)
			print(groupID.members)
	def spawnGroup(self):
		pass
	def deleteGroup(self):
		pass
	def returnActiveGroups(self):
		return self.groups
	def returnActiveMembers(self):
		for group in self.groups:
			return group.members
	def lookupGroup(self, groupID): #Return data on a requested group.
		pass

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
	description = "A group devoted to investing in cashews."
	site = groupData()
	site.launchSite()
	print(site.returnActiveMembers())

	# A = InvestGroup("CashYou", 12345, 98765, description)
	# A.updateMembers(True, 23456)
	# A.updateMembers(False, 12345)
	# print(A.members)
	# A.deleteGroup()