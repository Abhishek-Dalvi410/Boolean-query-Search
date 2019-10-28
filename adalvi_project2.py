import sys
with open(sys.argv[1], 'r') as f:
    contents = f.read()


document_list=contents.splitlines()
term_list=[]
document_term_number={}

same_term_flag=False
doc_flag=False
for document in document_list:
    #print(document)
    document_tokenized=document.split() 
    for token in range(len(document_tokenized)):
        same_term_flag=False
        if(token==0):
            docid=document_tokenized[token]
            document_term_number[docid]=len(document_tokenized)-1
            continue
        for x in term_list:
            doc_flag=False
            if(x[0]==document_tokenized[token]):
                same_term_flag=True
                k=0
                for y in x:
                    if(k==0):
                        k=k+1
                        continue
                    if(y[0]==docid):
                        y[1]=y[1]+1
                        doc_flag=True
                        break
                if(doc_flag==False):
                    x.append([docid,1])
                    break
        if(same_term_flag==False):
            llist=[docid,1]
            term_list.append([document_tokenized[token],llist])
    #break

def get_postings_list(query_term):
    global f
    doclist=[]
    for term in term_list:
        #print(term)
        if(term[0]==query_term):
            print(term[0], file=f)
            print("Postings list:", end='', file=f)
            for x in range(1,len(term)):
                print("",term[x][0], end = '', file=f)
                doclist.append(term[x][0])
            print("", file=f)
    return doclist

and_comparisons=0
def DAAT_and(docid_lists):
    global and_comparisons
    if(len(docid_lists)>2):
        li=DAAT_and(docid_lists[:2])
        #print(li)
        reserve_doc=docid_lists[2:]
        #print("Reserve_doc",reserve_doc)
        reserve_doc.append(li)
        reserve_doc=Sorting(reserve_doc)
        #print(reserve_doc)
        return DAAT_and(reserve_doc)
    else:
        i=0
        j=0
        and_list=[]
        while(i<len(docid_lists[0]) and j<len(docid_lists[1])):
            if(docid_lists[0][i]==docid_lists[1][j]):
                and_list.append(docid_lists[0][i])
                #print(docid_lists[0][i],"=",docid_lists[1][j])
                i=i+1
                j=j+1
                and_comparisons=and_comparisons+1
            elif(docid_lists[0][i]>docid_lists[1][j]):
                #print(docid_lists[0][i],">",docid_lists[1][j])
                j=j+1
                and_comparisons=and_comparisons+1
            else:
                #print(docid_lists[0][i],"<",docid_lists[1][j])
                i=i+1
                and_comparisons=and_comparisons+1
        return and_list

or_comparisons=0
def DAAT_or(docid_lists):
    global or_comparisons
    
    #print(docid_lists)
    
    if(len(docid_lists)>2):
        li=DAAT_or(docid_lists[:2])
        #print(li)
        reserve_doc=docid_lists[2:]
        #print("Reserve_doc",reserve_doc)
        reserve_doc.append(li)
        reserve_doc=Sorting(reserve_doc)
        #print(reserve_doc)
        return DAAT_or(reserve_doc)
    else:
        i=0
        j=0
        or_list=[]
        while(i<len(docid_lists[0]) and j<len(docid_lists[1])):
            if(docid_lists[0][i]==docid_lists[1][j]):
                or_list.append(docid_lists[0][i])
                #print(docid_lists[0][i],"=",docid_lists[1][j])
                i=i+1
                j=j+1
                or_comparisons=or_comparisons+1
            elif(docid_lists[0][i]>docid_lists[1][j]):
                #print(docid_lists[0][i],">",docid_lists[1][j])
                or_list.append(docid_lists[1][j])
                j=j+1
                or_comparisons=or_comparisons+1
            else:
                #print(docid_lists[0][i],"<",docid_lists[1][j])
                or_list.append(docid_lists[0][i])
                i=i+1
                or_comparisons=or_comparisons+1
                
        while(j<len(docid_lists[1])):
            or_list.append(docid_lists[1][j])
            j=j+1
            
        while(i<len(docid_lists[0])):
            or_list.append(docid_lists[0][i])
            i=i+1
            
    return or_list

def no_times_term_in_doc(word,doc):
    k=True
    global term_list
    for term in term_list:
        if(term[0]==word):
            #print(term[1])
            for x in range(1,len(term)):
                #print(term[x][0])
                if(term[x][0]==doc):
                    #print(doc)
                    k=False
                    return term[x][1]
    if(k==True):
        return 0

def no_docs_with_term(word):
    global term_list
    for term in term_list:
        if(term[0]==word):
            count=0
            for counting in range(len(term)):
                count=count+1
            return count-1

def tf_idf(doc_list,words):
    global document_term_number
    global term_list
    
    #print(doc_list)
    #print(words)
    doc_scores=[]
    for x in doc_list:
        #print("Scoring for document start")
        #print(x)
        doc_score=0
        for word in words:
            #print(word)
            #print("no_times_term_in_doc ",doc,"is",no_times_term_in_doc(word,x))
            tf=float(no_times_term_in_doc(word,x))/float(document_term_number[x])
            #print("TF:- ",no_times_term_in_doc(word,x),"/",document_term_number[x])
            
            idf=float(len(document_term_number))/float(no_docs_with_term(word))
            #print("IDF:-",len(document_term_number),"/",(no_docs_with_term(word)),"=",idf)
            #print("***************")
            score=tf*idf
            doc_score=doc_score+score
        doc_scores.append(doc_score)
        #print(x," score ", doc_score)
        #print("Scoring for document end \n \n")
    
    return doc_scores
    

def rank2(doc_list,doc_scores):
    n = len(doc_scores)
    #print("inside function rank2")
    #print(doc_scores)
    
    # Traverse through all array elements 
    for i in range(n): 
  
        # Last i elements are already in place 
        for j in range(0, n-i-1):
            #print(doc_scores[j])
  
            # traverse the array from 0 to n-i-1 
            # Swap if the element found is greater 
            # than the next element 
            if doc_scores[j] < doc_scores[j+1] :
                #print(doc_scores[j],"<",doc_scores[j+1])
                t=doc_scores[j+1]
                doc_scores[j+1]=doc_scores[j]
                doc_scores[j]=t
                
                t=doc_list[j+1]
                doc_list[j+1]=doc_list[j]
                doc_list[j]=t
                
    #print("rank2 end")
    return doc_list

#print(sys.argv[3])

with open(sys.argv[3], 'r') as f:
    q = f.read()

query_list=q.splitlines()

def Sorting(lst): 
    lst2 = sorted(lst, key=len) 
    return lst2 


f = open(sys.argv[2], "w")
for query in query_list:
    query_words=query.split()
    doc_list_for_query_words=[]
    for query_term in query_words:
        print("GetPostings", file=f)
        l=get_postings_list(query_term)
        doc_list_for_query_words.append(l)
        doc_list_for_query_words=Sorting(doc_list_for_query_words)
        
    ###########################################
    print("DaatAnd", file=f)
    print(query, file=f)
    and_list=DAAT_and(doc_list_for_query_words)
    print("Results: ", end='', file=f)
    no_result_counter=True
    for doc in and_list:
        no_result_counter=False
        print(doc,"", end='', file=f)
    if(no_result_counter==True):
        print("empty", end='', file=f)
    print(file=f)
    print("Number of documents in results:",len(and_list), file=f)
    print("Number of comparisons:",and_comparisons, file=f)
    and_comparisons=0
    print("TF-IDF", file=f)
    print("Results: ", end='', file=f)
    doc_scores=tf_idf(and_list,query_words)
    ranked_and_list=rank2(and_list,doc_scores)
    #print(ranked_and_list)
    if(no_result_counter==False):
        for doc in ranked_and_list:
            print(doc,"", end='', file=f)
    if(no_result_counter==True):
        print("empty", end='', file=f)
    print("", file=f)
    
    
    
    #############################################
    print("DaatOr", file=f)
    print(query, file=f)
    or_list=DAAT_or(doc_list_for_query_words)
    print("Results: ", end='', file=f)
    no_result_counter_1=True
    for doc in or_list:
        no_result_counter_1=False
        print(doc,"", end='', file=f)
    if(no_result_counter_1==True):
        print("empty", end='', file=f)
    print(file=f)
    print("Number of documents in results:",len(or_list), file=f)
    print("Number of comparisons:",or_comparisons, file=f)
    or_comparisons=0
    print("TF-IDF", file=f)
    print("Results: ", end='', file=f)
    
    #print(or_list)
    #print("//////////////// \n")
    
    doc_scores2=tf_idf(or_list,query_words)
    
    
    ranked_or_list=rank2(or_list,doc_scores2)
    
    if(no_result_counter_1==False):
        for doc in ranked_or_list:
            print(doc,"", end='', file=f)
    
    if(no_result_counter_1==True):
        print("empty", end='', file=f)
        
    #if(no_result_counter==False):
        #tf_idf(and_list,query_words)
    #break
    print("\n", file=f)
f.close()   