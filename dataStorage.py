#!/usr/bin/env python

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
			self.numraters = 0 
			self.members = [creator]

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
					print(type(self.members[num]), type(member_id), num)
					if self.members[num] == member_id: 
						members[num] = None
						print("Hoi")
				#search for member in list of members & delete
				return
			elif (addingMember is True) and (type(member_id) is int and member_id is not None):
				#Check if # of members is too large (DOS)
				self.members.append(member_id)
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
		return self.rating

	def updateRating(self, newRating):
		"""Returns updated 0 to 5 star rating"""
		if newRating > 5:
			return "Invalid Input"

		if self.rating is None:
			rating = 0
		else:
			rating = self.rating

		self.rating = (rating * self.numraters + newRating) / (self.numraters + 1)
		self.numraters = self.numraters + 1
		return self.rating

	def deleteGroup(self): # FFFFFF - Not deleting object instance currently
		"""When group is deleted, deletes all associated data or stores it in the stack for later deletion"""
		del self
		return

class groupMember(object):
	def __init__(self, username, password, isadmin = False, isdev = False):
		self.username = username # May be handled by FB?
		self.password = password

		#permissions
		self.admin = isadmin #True gives superuser permissions
		self.dev = isdev
		self.activeGroups = []
		self.prevGroups = []


class groupData(object):
	def __init__(self, name, adv = None, desc = " ", prevPerform = [], ):
		pass

class userData(object):
	def __init__(self, userID):
		pass

if __name__ == "__main__":
	description = "A group devoted to investing in cashews."
	A = InvestGroup("CashYou", 12345, 98765, description)
	A.updateMembers(False, 12345)
	print(A.members)
	# A.deleteGroup()