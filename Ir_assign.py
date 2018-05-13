import nltk
import math
from os import walk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer,WordNetLemmatizer
from nltk.corpus import stopwords
import os

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()
extras = "~ ` ! @ # $ % ^ & * ( ) - _ = + { [ } ] | \ : ; ' < , > . ? /"
extras_list = extras.split(" ")
dict = {}
query_dict = {}
q_tf = {}
q_idf = {}
cosine_dict = {}
cosine_list = []
document = []
#-------------------------------------------------------
from tkinter import *

def show_entry_fields():
    #------------------------------------------------------------
  #add to dictionary
  def addtodict(list,k):
      for i in list:
       if i in dict:
           if k in dict[i][-1]:
               #print(k)
               dict[i][-1][1]=dict[i][-1][1]+1
           else:
              dict[i] = dict[i]+[[k,1]]
       else:
          dict[i]=[[k,1]]
          

  # ------------------------------------------------
  #tokenize query
  def tokenize_query(s):
      global extras_list
      query1 = word_tokenize(s)
      query = [lemmatizer.lemmatize(w.lower()) for w in query1 if not w in extras_list]
      #print(query)
      return query

  #---------------------------------------------------------

  def find_intersection(lower_list,query):
        intersection=[]
        for i in lower_list:
            #print(i)
            if i in query:
                if i in intersection:
                    continue
                else:
                    intersection.append(i)          
            else:
                continue
        #print(intersection)      
        return intersection 

   #-------------------------------------------------------------
  def document_tfidf(document,intersection,k):
          weight=[]
          for i in intersection:
              x=len(dict[i])
              for j in range(0,x):
                  if(dict[i][j][0]==k):
                      weight.append(1+math.log10(dict[i][j][1]))
          
          for i in document:
              if i in intersection:
                  continue
              else:
                  x=len(dict[i])
                  for j in range(0,x):
                      if(dict[i][j][0]==k):
                          weight.append(1+math.log10(dict[i][j][1]))
          #weighted values before normalization
          #print(weight)
          
          n_value = normalise(weight)
          n=0
          for k in weight:
              weight[n]=k/n_value
              n=n+1                      
          return weight

   #--------------------------------------------------------------
  def minimize_doc(document):
      listed = []
      for i in document:
          if i in listed:
              continue
          else:
              listed.append(i)
      return listed    

   #------------------------------------------------------------

  def normalise(normal):
      sum = 0
      for k in normal:
          sum = sum + (k*k)
      value = math.sqrt(sum)
      return float(value)


  #--------------------------------------------------
  # for a query


  def add_query(query):
      for i in query:
          if i in query_dict:
              query_dict[i]=query_dict[i]+1
          else:
              query_dict[i]=1

  #---------------------------------------------------------------                                     
  #---------------------------------------------------------------


  def query_tf(query_listed):
      for i in query_listed:
          q_tf[i] = 1+math.log10(query_dict[i])
          

  #---------------------------------------------------------------

  def query_idf(query_listed):
      for i in query_listed:
          if i not in dict:
              q_idf[i] = 0
          else:
              q_idf[i] = math.log10((doc_count/len(dict[i])))

  #---------------------------------------------------------------


  #heap sort
  def heapify(arr, n, i):
      largest = i 
      l = 2 * i + 1    
      r = 2 * i + 2     

      if l < n and arr[i] < arr[l]:
          largest = l
          
      if r < n and arr[largest] < arr[r]:
          largest = r
   
      if largest != i:
          arr[i],arr[largest] = arr[largest],arr[i]
          heapify(arr, n, largest)

  def heapSort(arr):
      n = len(arr)
      for i in range(n, -1, -1):
          heapify(arr, n, i)
   
      for i in range(n-1,-1, -1):
          arr[i], arr[0] = arr[0], arr[i]  
          heapify(arr, i, 0)
    

  #---------------------------------------------------------------

  f=[]
  #print(query_listed)
  #print(query_dict)
  #print("tf of query") 

  #-----------------------------------------------------

  for (dirpath,dirnames,filenames) in walk('G:/Users/avina/Desktop/lol'):
      f.extend(filenames)
      
      doc_count = len(f)
  for k in f:
         print(k) 
         fo = open(k,"r+",encoding="utf8")
          
         data = fo.read()

         list = word_tokenize(data)
         lower_list = [lemmatizer.lemmatize(w.lower()) for w in list if not w in extras_list]  
         
         addtodict(lower_list,k)
         fo.close()

  #-------------------------------------------------------------------------------
  s = e1.get() # INPUT HERE<-------------------------------S-------------------------------------->     
  query = tokenize_query(s)   
  add_query(query)
  query_listed = minimize_doc(query)
  query_tf(query_listed)

  #-------------------------------------------------------------------------------
  query_idf(query_listed)
  #idf of query
  #print(q_idf)
 

  tf_idf = {}

  for i in q_tf:
      
      tf_idf[i] = (q_tf[i]*q_idf[i])

  #tf idf value before normalization    
  #print(tf_idf)
  

  sum = 0
  for i in tf_idf:
      sum = sum+tf_idf[i]*tf_idf[i]

  #normalized value   
  value = math.sqrt(sum)
  #print(value)
  

  for i in tf_idf:
        if value==0:
          print("No documents found")
        else:  
           tf_idf[i]=tf_idf[i]/value
        

  #----------------------------------------------
  #normalized tf idf value
  #print(tf_idf)
  
  # tf_idf dictionary contains the tf_idf values of query
  #------------------------------------------------------------
  #-------------------------------------------------------------

  for i in query_listed:   
      if i in dict:
          local_len = len(dict[i])
          for j in range(0,local_len):
              file_name = dict[i][j][0]
              if file_name in document:
                  continue
              else:
                  document.append(dict[i][j][0])
      else:
          continue

  #print(document)    
  #-------------------------------------------------------------

  for k in document:
         fo = open(k,"r+",encoding="utf8")
        # print(k)
         data = fo.read()

         list = word_tokenize(data)
         lower_list = [lemmatizer.lemmatize(w.lower()) for w in list if not w in extras_list]  
      
         fo.close()
    
         listed = minimize_doc(lower_list)
         intersection = find_intersection(lower_list,query)
  #  print("intersection values")
  # print(intersection)
 

         
         weight = document_tfidf(listed,intersection,k)
  #       print("weighted values of document after normalization")
  #       print(weight)
 

         total = [] 
         ins_len = len(intersection)
         l=0
         cosine = 0
         for i in intersection:
             total.append(weight[l]*tf_idf[i])
             cosine = cosine+total[l]
             l = l+1
   #      tf idf of common values between document and query    
   #      print(total)
   
   #      total cosine value
   #      print(cosine)
         cosine_list.append(cosine)
         cosine_dict[cosine] = k

  #print(cosine_dict)       

  n = len(cosine_list)
  heapSort(cosine_list)
  #print(cosine_list)
  count=0
  # print("First Name: %s\nLast Name: %s" % (e1.get(), e2.get()))
  ll = []
  for i in range(n-1,-1,-1):
     if count>10:
         break
     else:  
      f1=cosine_list[i]
      ll.append(cosine_dict[f1])
      count = count+1
  b1=Label(root, text=ll[0],bg='lightblue',font='10',height=2,width=15).grid(row=5)   
  b2=Label(root, text=ll[1],bg='lightblue',font='10',height=2,width=15).grid(row=6)
  b3=Label(root, text=ll[2],bg='lightblue',font='10',height=2,width=15).grid(row=7)
  b4=Label(root, text=ll[3],bg='lightblue',font='10',height=2,width=15).grid(row=8)
  b5=Label(root, text=ll[4],bg='lightblue',font='10',height=2,width=15).grid(row=9)
  b6=Label(root, text=ll[5],bg='lightblue',font='10',height=2,width=15).grid(row=10)
  b7=Label(root, text=ll[6],bg='lightblue',font='10',height=2,width=15).grid(row=11)
  b8=Label(root, text=ll[7],bg='lightblue',font='10',height=2,width=15).grid(row=12)
  b9=Label(root, text=ll[8],bg='lightblue',font='10',height=2,width=15).grid(row=13)
  b10=Label(root, text=ll[9],bg='lightblue',font='10',height=2,width=15).grid(row=14)
    

root = Tk()
root.title('getit')
root.configure(background='lightblue')
root.geometry("300x300")

Label1=Label(root, text="getit",bg='lightblue',font='150').grid(row=3,column=3)
Label(root, text="search here",bg='lightblue',font='10').grid(row=4)

e1 = Entry(root)

e1.grid(row=4,column=3)


button2=Button(root, text='Search', command=show_entry_fields)
button2.grid(row=4,column=5)

root.mainloop( )




#<-------------------------------------------------------------------------------OUTPUT HERE-------------------------------------------------------------->
    
