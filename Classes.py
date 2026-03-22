class SentanceDataPoint():
  def __init__(self):
    self.WordTypeFrequencyDict={} # a dict storing how many times the program 
    # has seen words in a position 
    self.WordTypeDict={} # a dict storing word types and frequencies due to position 
  def UpdateStructure(self,Value,WordPosition):
    ## word position meaning the position of the word in the sentance
    ## Value meaning the word type value as defined by the ReadMe
    if(WordPosition not in self.WordTypeDict):
      ## if no words have been seen in this position before 
      ## then add a new dict to record the position stuff here 
      NewDict={}
      NewDict[Value]=1
      ## primary key= position of the word in the sentence
      # secondary key = the type fo word it is 
      # data = the number of times this word has been seen here
      self.WordTypeDict[WordPosition]=NewDict
    else:
      print(Value)
      print(self.WordTypeDict[WordPosition])
      input()
      if(Value not in self.WordTypeDict[WordPosition]):
        ## if a word type has never been seen in a certain position in
        ## a sentence before 
        self.WordTypeDict[WordPosition][Value]=1
      else:
        ## if a word type has been seen again appearing at a certain position
        ## in a sentence 
        self.WordTypeDict[WordPosition][Value]+=1
    if(WordPosition not in self.WordTypeFrequencyDict):
      ### omg ive never seen a word in that position in a sentance before im gonna add it in 
      self.WordTypeFrequencyDict[WordPosition]=1
    else:
      ### omg another one of those word things in that position lemme mark that one down
      self.WordTypeFrequencyDict[WordPosition]+=1
  def RelayData(self):
    ## a function that allows this class to tell the user teh data that it has 
    ## currently gathered on word types being in a position in a sentence
    TypeToWordTranslator={0:"Noun",1:"Verb",2:"Adjective",3:"Adverb",4:"Pronoun",5:"Preposition",6:"Conjunction",7:"Article"}
    for key in self.WordTypeFrequencyDict:
      #i.e. for every position you have seen a word appear in a sentence
      ## print the percentages of times different word types have appeared
      ## in each position
      for term in self.WordTypeDict[key]:
        print("the word type {} has appeared at position {} in the sentence {} % of the time".format(TypeToWordTranslator[term],key,(100*self.WordTypeDict[key][term]/self.WordTypeFrequencyDict[key])))

        
  

class Punctuation():
  def __init__(self,PuncName,PuncPos):
    ## a data type storing any instancces of punctuation
    self.PuncName=PuncName # the literal punctuation value being stored
    self.PuncPosition=PuncPos # the position this punctuation mark appears in a sentance with probabilities 
    self.InstancesFound=0
  def AddInstance(self):
    self.InstancesFound+=1
    
    

class Word():
  def __init__(self,WordName,Capitalized):
    ## WordName is the word itself
    
    ## WordType is a dictionary of Values that decide what a word is 
    ## The meaning of teh values stored in WordType is shown in the readme
    ## the magnitude of the value stored at the wordtype posiiton 
    ## Shows how many times it has been seen in that context 
    ## The position of the Value stored in the WordType List represents
    ## Which context that word has been seen in before 
    
    ## Instances Recorded is going to be the amount of times that this 
    ## word has appeared in previous sentances 
    
    ## Capitalized is a boolean that represents whether a word is 
    ## capitalized or not 
    self.WordName=WordName
    self.WordType={}
    self.Capitalized=Capitalized
    self.InstancesRecorded=0
    self.WordPosition={} # a dictionary containing the positions the word is found in a sentance and their probabilities 
  def AddInstance(self):
    self.InstancesRecorded+=1
  def SetCapital(self,Value):
    ## sets the Capitalized variable to its correct value 
    self.Capitalized=Value
  def UpdateType(self,UpdateValue,UpdatePosition):
    # update value updates the words position in its type graph 
    # Update Position updates the words position in its position Graph
    #adds one to the value in the list that represents the word type 
    self.InstancesRecorded+=1
    if(UpdateValue not in self.WordType):
      self.WordType[UpdateValue]=1
    else:
      self.WordType[UpdateValue]+=1
    if(UpdatePosition not in self.WordPosition):
      self.WordPosition[UpdatePosition]=1
    else:
      self.WordPosition[UpdatePosition]+=1
  def __str__(self):
    return(self.WordName)
