import os,Classes,json
from Classes import *


##### Things that this program can do

#####  - Can currently read through a sentence and tell the user how many times each word was used
#####    in a certain position in the sentence 



## ok lets make an ai thati can relate words to other words
## it'll probably use a graph that has different grids for different types of words
## the Ai will have a structure that decides what type of word it is going to 
## say next. It will then look in the relevant grid ton its word type and 
## choose a random word 

## Iteration 1 make an ai that can recognize different types of word and 
## can recognize them if they are stored in its database 
## or use a single value to decide which ype of word the words are 

## single value doesn't works for double meaning words
## e.g. badger and badger fuckin idiot i am lol
## so each word will have a list of values that determine what type of word they are 
## There will be a cutoff that a value will have to be above to be included in a 
## graph and be catagorized as that kind of word based on sentance analysis

## Iteration 2 or 0 The Ai must be able to look at a sentance and say what type of 
## word it is currently looking at and which word is most likely to come 
## next 

## Note on how i think im gonna do word selection 
## The ai will look into its sentance structure banks for which
## word is the most likely to come next 
## it will then look in the graph for a word that is as close as possible 
## to other words of its kind in the sentance 
## certain types of words will be closer together in the graph 
## or the  angle will be smaller or something i don't know i totally forgot 
## 


## Total samples taken is going to be the Total number of  
## known Words is the dictionary of possible words that have been seen by the AI 


TotalSamplesTaken = 0 

KnownWords = {}

TestingMode = "By File"

SentanceAnalyst = SentanceDataPoint()
Punc = Punctuation("No Idea",0)
Wordie= Word("Words",False)
    
##### Section For Test Subprograms im going to be making 

SuccessList={}
TestResults=[0,0,0]

def UpdateSuccessList(TestName,Result):
  while(TestName in SuccessList):
    TestName=TestName+str(int(TestName[len(TestName)-1])+1)
  SuccessList[TestName]=Result

def PrintTest(PrintingItem):
  print(PrintingItem)
  Successful=input("was this test Successful?")
  if(Successful.lower().startswith("y")):
    UpdateSuccessList("PrintTest0","Test Successful")
    TestResults[0]+=1
  elif(Successful.lower().startswith("n")):
    UpdateSuccessList("PrintTest0","Test Failed")
    TestResults[1]+=1
  else:
    UpdateSuccessList("PrintTest0","Test Inconclusive")
    TestResults[2]+=1
  os.system("clear")

def TestReview():
  for term in SuccessList:
    print("{} was {}".format(term,SuccessList[term]))
  print("{} Test Cases Ran".format(len(SuccessList)))
  print("{} Test Cases Successful".format(TestResults[0]))
  print("{} Test Cases Failed".format(TestResults[1]))
  print("{} Test Cases Inconclusive".format(TestResults[2]))
  input()
  os.system("clear")
      
## uses teh dictionary search system to check if a 
## word has been seen by the system or not before 

def SearchKnown(SearchTerm):
  if(len(KnownWords)==0):
    return(False)
  else:
    if(SearchTerm.lower() not in KnownWords):
      return(False)
    else:
      return(True)

def CheckCapitalization(SearchTerm):
  if(len(SearchTerm.WordName)>=1):
    if(64<=ord(SearchTerm.WordName[0])<=90):
      ## result being that the word is Capitalized
      SearchTerm.SetCapital(True)
    elif(96<=ord(SearchTerm.WordName[0])<=122):
      ## result being that the word is not Capitalized
      SearchTerm.SetCapital(False)

def DetermineWordType(TheWord,WordPosition):
  ## the below function should return the word types
  ## that the analyzed word is most likely to be 
  UpdateWordTypeValues(TheWord,WordPosition)
  MostCommonTypesList={}
  ## the below loop should look at all the different types of words
  ## the word being looked at could be 
  ## the most common types of which will be added to the MostCommonTypesList
  for term in TheWord.WordType:
    if(len(MostCommonTypesList)==0):
      ## adds the first term to the list the term being the type of word
      ## and the percentage of how often its type is seen
      MostCommonTypesList[term]=TheWord.WordType[term]//TheWord.InstancesRecorded
    else:
      ## checks if the term it wants to add to the dict is bigger than the smallest
      ## term in this dict 
      if(len(MostCommonTypesList)==3):
        if((TheWord.WordType[term]//TheWord.InstancesRecorded)>=min(MostCommonTypesList.values())):
          MostCommonTypesList.pop(min(MostCommonTypesList.Values()))
          MostCommonTypesList[term]=TheWord.WordType[term]
      else:
        MostCommonTypesList[term]=TheWord.WordType[term]
  return(MostCommonTypesList)
  
def UserWordTypeOpinion(TheWord):  
  if(len(TheWord.WordName)>=1):
    print("What type of word is the following word?")
    print(""" 0-  Noun
    1- Verb
    2- Adjective
    3- Adverb
    4- Pronoun
    5- Prepesition 
    6- Conjunctions   
    7- Article
    8- Interjection""")
    print(TheWord.WordName)
    UserOpinion=input()
    os.system("clear")
    if(UserOpinion=="Aa1"):
      AddWordToTrainingDataFile(TheWord.WordName)
      UserOpinion=UserWordTypeOpinion(TheWord)
    elif(0>int(UserOpinion)<7):
      UserWordTypeOpinion(TheWord)
    ## Aa1 is the code that im going to use to add new testing data to the TestData file
    
    return(int(UserOpinion))
  
def UpdateWordTypeValues(TheWord,WordPosition):
  if(TestingMode=="By Hand"):
    UserWordTypeOpinion(TheWord)
  else:
    WordToValueTranslator={"noun":0,"verb":1,"adjective":2,"adverb":3,"pronoun":4,"preposition":5,"conjunction":6,"article":7,"interjection":8}
    WordFile=FindMatches(TheWord.WordName,ReadTrainingData()) ## finds the data from the file that matches the word
    # the user typed in 
    ## word file is the list of all the types of word that this word could be according to the database 
    if(WordFile==None):
      UserOpinion=UserWordTypeOpinion(TheWord)
      #PrintTest(UserOpinion)
    elif(len(WordFile)>1):
      for term in WordFile:
        print(str(WordFile.index(term)+1)+". "+term+"\n")
      print(TheWord.WordName)
      print("Which type of word is this word? (input the number)")
      UserOpinion=input()
      UserOpinion=WordToValueTranslator[WordFile[int(UserOpinion)-1].lower()]
    else:
      UserOpinion=WordToValueTranslator[WordFile[0].lower()]
  TheWord.UpdateType(UserOpinion,WordPosition) # This tells the system what type of word a word is and also where it appears in a sentence
  SentanceAnalyst.UpdateStructure(UserOpinion,WordPosition)# this function updates the sentence data types general structure values 
  ## tells the word which type it is 
  ## this subprogram should also tell the sentance analyzing data structure 
  ## How often the data type Shown shows up 
  os.system("clear")

# a subprogram that goes through every word in a sentance
# and accurately stores it in its own little cell 

def AnalyzeSentance(FuncInput):
  ## takes in a sentence and analyzes the types of words that are used and where they are used
  WordPosition=0
  Sentance=FuncInput.split(" ")
  for CurrentWord in Sentance:
    WordPosition+=1
    if(SearchKnown(CurrentWord)==True):      ## ie the AI already knows this word
      ## The AI will let the node know that it has been seen before
      KnownWords[CurrentWord].AddInstance()
      ## The System will also need ot let this node revaluate which Graphs it is in and also 
      ## Update its position in the Grand Graph of the world 
    else:
      ## i.e. the Ai has never seen this word before 
      ## The system will create a new node in the system at the default position 
      KnownWords[CurrentWord]=Word(CurrentWord,None)
    ## a data pointer to the current word object the system is editing
    CurrentWordObject=KnownWords[CurrentWord]
    ## The Ai Will then ask the user what type of word it is looking at
    ## or make a prediction based on the data that it already has 
    CheckCapitalization(CurrentWordObject)
    WordType=DetermineWordType(CurrentWordObject,WordPosition)
    ## when it has decided which type of word it is looking at 


# maybe make two systems one that like super precise and the other one that 
## has like a good general idea of what is going on in the sentence

## The next section of this code is going to be creating a way for the Ai to test itself with supervised learning 
## it will go through its database and see if it has any matches to the word it is looking at 
## if there are multiple word types for that word it will ask the user which one it is 
## it will then go through the rest of the code as notmal

def ProcessWordsIntoTrainingData():
  RawData=GetData()
  ProcessedData=AddDataTypes(RawData) # also sends data back to the process data file 

def GetData():
  ## gets the training data from Training_Data.txt
  f=open("Training_data.txt","r")
  AllOfTheData=f.readlines()
  f.close()
  NewList=[]
  i=0
  for term in AllOfTheData:
    NewList.append(AllOfTheData[i].rstrip())
    i+=1
  f=open("Memories.txt","r")
  NewData=f.readlines()
  f.close()
  ImportSentenceData(NewData)

  # with open("Memory.pkl","rb") as file:
  #   SentanceAnalyst.WordTypeDict=pickle.load("Memory.pkl")
  #   SentanceAnalyst.WordTypeFrequencyDict=pickle.load("Memory.pkl")
    
  return(NewList)
  
def ImportSentenceData(data):
  # This function will correctly import the data from a csv back into a 
  # codeable class
  SplitDicts=data.split("\n")[:len(SplitDicts)-1]
  print(SplitDicts)
  
def AddWordToTrainingDataFile(Word):
  ## adds a given word to the training data 
  print(Word)
  print("What type of word is this?")
  UserInput=input()
  while(UserInput.upper()!="N"):
    Word=Word+","+UserInput.lower()
    print("Any other word types?")
    UserInput=input()
  os.system("clear")
  print("Word Added")
  f=open("Processed_Datarinos.txt","a")
  f.write(Word+"\n")
  f.close()
  input()
  os.system("clear")

def AddDataTypes(RawDatarinos):
  for Word in RawDatarinos:
    AddWordToTrainingDataFile(Word)
  
def ReadTrainingData():
  ## reads the file that has the words with their data types stored in it 
  ## turns that data into something i can use to train the AI 
  f=open("Processed_Datarinos.txt","r")
  AllOfTheData=f.readlines()
  f.close()
  TrainingReadyData={}
  for Term in AllOfTheData:
    if(len(Term)>1):
      ListView=Term.rstrip()
      ListView=ListView.split(",")
      Key=ListView[0].lower()
      Data=[]
      for i in range(0,len(ListView)-1):
        Data.append(ListView[i+1])
      if(ListView[0].lower() not in TrainingReadyData):
        TrainingReadyData[Key]=Data
  return(TrainingReadyData)
 
def FindMatchesInFile(SearchTerm):
  # should successfully process the list of finished words into a dictionary 
  # then should find if the Search term is in this dictionary
  f=open("Processed_Datarinos.txt","r")
  TheList=f.readlines()
  NewList=[]
  Database={}
  f.close()
  for Term in TheList:
    NewList.append(Term.rstrip().split(","))
  for Term in NewList:
    WordData=[]
    for i in range(0,len(Term)-1):
      WordData.append(Term[i+1])
    Database[Term[0].lower()]=WordData
  return(FindMatches(SearchTerm,Database)) # returns the data associated with a word
    
  
def FindMatches(SearchTerm,TrainingData):
  ## takes a dictionary as an input and returns the resulting data from the file 
  if(str(SearchTerm.lower()) not in TrainingData):
    print("not found")
    return(None)
  else:
    print("Found")
    ReturnVariable=TrainingData[SearchTerm.lower()]
    print(ReturnVariable) 
    return(ReturnVariable)




for i in range(1):
  UserInput=input("Please input a sentance of some type of description")
  AnalyzeSentance(UserInput)

SentanceAnalyst.RelayData()
SentanceAnalyst.StoreSentenceInMemory()
## next stage is to store all of the Data in a new file This File will
## Store the sentences that the user inputs and the system analyzes
## for now ill use a csv to store the percentage of times a word type shows up in a dict

## what im actually gonna do is implement a dictionary system to store word types and percentages
## first number is position in sentence
## second word = type of word 
## third number = times it has been seen in this position






