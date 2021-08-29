from os import system, name

def clear():
    if name == 'nt':
        x = system('cls')
    else:
        x = system('clear')


class Admin:
    """ THIS CLASS CONTAINS ALL SENSITIVE DATA AND CAN BE ONLY ACCESSD BY ADMINS. """
    _branches = {}
    _c_Blood = ["A+", "A-", "B+", "O+", "O-"]
    _rareBlood = {"B-": 0, "AB+": 0, "AB-": 0}

    def __init__(self):
        with open('CommonBlood.txt', 'r') as f:
            lines = f.readlines()
            if len(lines) != 0:
                with open('branch.txt', 'r') as f:
                    key = f.readlines()[:-1]

                for i in range(len(key) // 2 + 1):
                    vals = []
                    for val in lines[5 * i:5 * i + 5]:
                        vals.append(int(val[:-1]))
                    self._branches.update({key[2 * i]: vals})

        with open('RareBlood.txt', 'r') as rf:
            lines = rf.readlines()
            self._rareBlood["B-"] = int(lines[0][:-1])
            self._rareBlood["AB+"] = int(lines[1][:-1])
            self._rareBlood["AB-"] = int(lines[2][:-1])

    def saveData(self):
        with open('CommonBlood.txt', 'w') as f:
            with open('branch.txt', 'w') as f1:
                key = self._branches.keys()
                for k in key:
                    f1.write(k + "\n")
                    for j in range(5):
                        f.write(str(self._branches[k][j]) + "\n")

        with open('RareBlood.txt', 'w') as rf:
            rf.write(str(self._rareBlood["B-"])+"\n")
            rf.write(str(self._rareBlood["AB+"])+"\n")
            rf.write(str(self._rareBlood["AB-"])+"\n")

    # TAKING SAMPLE IN ORDER OF A+ A- B+ O+ O- (COMMON BLOOD GROUP) B- AB+ AB-
    def addBranch(self, name, samples=[0, 0, 0, 0, 0]):
        if type(samples) == list:
            if len(samples) != 5:
                samples = [0, 0, 0, 0, 0]
            self._branches.update({name+"\n": samples})
            print("Branch Added")
        else:
            print("Branch Not Added")

    def getBranches(self):
        print("Available Branches")
        for i in self._branches.keys():
            print(i, end="")

    def display(self):
        keys = self._branches.keys()
        for key in keys:
            print("\n\nBranch : ",key)
            blood = self._branches[key]
            for i in range(5):
                print(self._c_Blood[i], " >> ", blood[i], end="     ")

        print("\n\nRare Blood")
        print("B- >> ", self._rareBlood["B-"])
        print("AB+ >> ", self._rareBlood["AB+"])
        print("AB- >> ", self._rareBlood["AB-"])
        print("\n")

    def update(self, branch, data):
        if branch in self._branches.keys():
            self._branches[branch] = data
            print("Updated")
        else:
            print("Can't Updated!!! Branch not found")


class donor(Admin):
    def __init__(self):
        self.registered = True

    def __donate(self, bloodGroup, branch):  # PRIVATE FUNCTION WIL BE CALLED BY selectBranch()
        """ DONATING BLOOD """
        self.rare = bloodGroup // 5
        self.pos = bloodGroup % 5

        if self.rare == 1:
            R = ["B-", "AB+", "AB-"]
            self._rareBlood[R[self.pos]] += 1
        else:
            self._branches[branch][self.pos] += 1
        print("Thanks For Donating...")

    def selectBranch(self, branchName):
        if self.registered == True:
            try:
                print("Choose from the below Blood Groups : ")
                print(
                    "1. A_POSITIVE\n2. B_POSITIVE\n3. O_POSITIVE\n4. A_NEGATIVE\n5. O_NEGATIVE\n6. B_NEGATIVE\n7. AB_POSITIVE\n8. AB_NEGATIVE")
                self.bg = int(input())
                while self.bg not in range(1, 9):
                    print("Invalid Selection   \nPlease Make Valid Selection ")
                    self.bg = int(input())
                self.__donate(self.bg - 1, branchName)

            except:
                print("INVALID BRANCH")
        else:
            print("Name Unregistered")


class patient(Admin):
    def __init__(self):
        self.registered = True

    def requestForBlood(self):
        if self.registered == True:
            print(
                "1. A_POSITIVE\n2. A_NEGATIVE\n3. B_POSITIVE\n4. O_POSITIVE\n5. O_NEGATIVE\n6. B_NEGATIVE\n7. AB_POSITIVE\n8. AB_NEGATIVE")
            self.bg = int(input("Enter the blood group required : "))
            while self.bg not in range(1, 9):
                print("Invalid Selection   \nPlease Make Valid Selection ")
                self.bg = int(input())
            print("Searching in bloodBank ...")
            self.rare = (self.bg - 1) // 5
            self.pos = (self.bg - 1) % 5
            if self.rare == 1:
                R = ["B-", "AB+", "AB-"]
                if self._rareBlood[R[self.pos]] != 0:
                    self._rareBlood[R[self.pos]] -= 1
                    print("Congratulations  Blood Found And Request Approved ")
                else:
                    print("Sorry Blood not available")
            else:
                keys = self._branches.keys()
                for key in keys:
                    if self._branches[key][self.pos] != 0:
                        self._branches[key][self.pos] -= 1
                        print("Congratulations  Blood Found in Branch " + key[:-1] + " And Request Approved ")
                        return
                print("Sorry Blood not available")

def adminMenu(ad):
    run = True
    while run:
        print(">>>>>> ADMIN MENU <<<<<<")
        print("________________________")
        print("1. ADD BRANCH\n2. BRANCHES\n3. UPDATE BRANCH\n4. STOCK\n5. BACK")
        user = input("Enter (1-5) : ")
        if user == '1':
            clear()
            print(">>>>> ADD BRANCH <<<<<\n")
            bName = input("Enter Branch Name : ")
            temp = list(input("Blood Quantity in Order of A+ A- B+ O+ O- (Comma Separated) : ").split(','))
            bdata = []
            for i in temp:
                bdata.append(int(i))
            ad.addBranch(bName,bdata)
        elif user == '2':
            clear()
            print(">>>>> BRANCHES <<<<<\n")
            ad.getBranches()
        elif user == '3':
            clear()
            print(">>>>> UPDATE BRANCH <<<<<\n")
            bName = input("Enter Branch Name : ")
            temp = list(input("Blood Quantity in Order of A+ A- B+ O+ O- (Comma Separated) : ").split(','))
            bdata = []
            for i in temp:
                bdata.append(int(i))
            ad.update(bName, bdata)
        elif user == '4':
            clear()
            print(">>>>> STOCK <<<<<\n")
            ad.display()
        else:
            run = False

def patientMenu(pat):
    run = True
    while run:
        print(">>>>>> PATIENT MENU <<<<<<")
        print("________________________")
        print("1. REQUEST FOR BLOOD\n2. BACK")
        user = input("Enter (1-2) : ")
        if user == '1':
            clear()
            print(">>>>> BLOOD REQUEST <<<<<\n")
            pat.requestForBlood()
        else:
            run = False

def donorMenu(don):
    run = True
    while run:
        print(">>>>>> PATIENT MENU <<<<<<")
        print("________________________")
        print("1. VIEW BRANCHES\n2. DONATE\n3. BACK")
        user = input("Enter (1-3) : ")
        if user == '1':
            clear()
            print(">>>>> VIEW BRANCHES <<<<<\n")
            don.getBranches()
        elif user == '2':
            clear()
            print(">>>>> DONATE <<<<<\n")
            branch = input("Enter Branch Name : ")
            don.selectBranch(branch+"\n")
        else:
            run = False

if __name__ == '__main__':
    admin = Admin()
    pat = patient()
    don = donor()
    run = True
    while run:
        clear()
        print("\n\n***************************************** Welcome to Blood Managment System - Company XYZ *****************************************\n")
        print("Login to blood managment system as :")
        print("1.Admin\n2.Donor\n3.Acceptor\n4.Exit")
        user = input("Enter (1-4) : ")

        if user == '1':
            clear()
            adminMenu(admin)
        elif user == '2':
            clear()
            donorMenu(don)
        elif user == '3':
            clear()
            patientMenu(pat)
        else:
            run = False



    admin.saveData()