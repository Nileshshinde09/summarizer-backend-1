import nltk
from nltk import sent_tokenize,word_tokenize
from nltk.stem.porter import PorterStemmer
import math
from nltk.stem import WordNetLemmatizer
sentence_length=10
stopwords={'those', 'on', 'own', '’ve', 'yourselves', 'around', 'between', 'four', 'been', 'alone', 'off', 'am', 'then', 'other', 'can', 'regarding', 'hereafter', 'front', 'too', 'used', 'wherein', '‘ll', 'doing', 'everything', 'up', 'onto', 'never', 'either', 'how', 'before', 'anyway', 'since', 'through', 'amount', 'now', 'he', 'was', 'have', 'into', 'because', 'not', 'therefore', 'they', 'n’t', 'even', 'whom', 'it', 'see', 'somewhere', 'thereupon', 'nothing', 'whereas', 'much', 'whenever', 'seem', 'until', 'whereby', 'at', 'also', 'some', 'last', 'than', 'get', 'already', 'our', 'once', 'will', 'noone', "'m", 'that', 'what', 'thus', 'no', 'myself', 'out', 'next', 'whatever', 'although', 'though', 'which', 'would', 'therein', 'nor', 'somehow', 'whereupon', 'besides', 'whoever', 'ourselves', 'few', 'did', 'without', 'third', 'anything', 'twelve', 'against', 'while', 'twenty', 'if', 'however', 'herself', 'when', 'may', 'ours', 'six', 'done', 'seems', 'else', 'call', 'perhaps', 'had', 'nevertheless', 'where', 'otherwise', 'still', 'within', 'its', 'for', 'together', 'elsewhere', 'throughout', 'of', 'others', 'show', '’s', 'anywhere', 'anyhow', 'as', 'are', 'the', 'hence', 'something', 'hereby', 'nowhere', 'latterly', 'say', 'does', 'neither', 'his', 'go', 'forty', 'put', 'their', 'by', 'namely', 'could', 'five', 'unless', 'itself', 'is', 'nine', 'whereafter', 'down', 'bottom', 'thereby', 'such', 'both', 'she', 'become', 'whole', 'who', 'yourself', 'every', 'thru', 'except', 'very', 'several', 'among', 'being', 'be', 'mine', 'further', 'n‘t', 'here', 'during', 'why', 'with', 'just', "'s", 'becomes', '’ll', 'about', 'a', 'using', 'seeming', "'d", "'ll", "'re", 'due', 'wherever', 'beforehand', 'fifty', 'becoming', 'might', 'amongst', 'my', 'empty', 'thence', 'thereafter', 'almost', 'least', 'someone', 'often', 'from', 'keep', 'him', 'or', '‘m', 'top', 'her', 'nobody', 'sometime', 'across', '‘s', '’re', 'hundred', 'only', 'via', 'name', 'eight', 'three', 'back', 'to', 'all', 'became', 'move', 'me', 'we', 'formerly', 'so', 'i', 'whence', 'under', 'always', 'himself', 'in', 'herein', 'more', 'after', 'themselves', 'you', 'above', 'sixty', 'them', 'your', 'made', 'indeed', 'most', 'everywhere', 'fifteen', 'but', 'must', 'along', 'beside', 'hers', 'side', 'former', 'anyone', 'full', 'has', 'yours', 'whose', 'behind', 'please', 'ten', 'seemed', 'sometimes', 'should', 'over', 'take', 'each', 'same', 'rather', 'really', 'latter', 'and', 'ca', 'hereupon', 'part', 'per', 'eleven', 'ever', '‘re', 'enough', "n't", 'again', '‘d', 'us', 'yet', 'moreover', 'mostly', 'one', 'meanwhile', 'whither', 'there', 'toward', '’m', "'ve", '’d', 'give', 'do', 'an', 'quite', 'these', 'everyone', 'towards', 'this', 'cannot', 'afterwards', 'beyond', 'make', 'were', 'whether', 'well', 'another', 'below', 'first', 'upon', 'any', 'none', 'many', 'serious', 'various', 're', 'two', 'less', '‘ve'}
total_documents=0
def frequency_matrix(text):
    frequency_matrix={}
    ps=PorterStemmer()
    for sent in text:
        frequency_table={}
        new_sent=word_tokenize(sent)
        for word in new_sent:
            if word in stopwords:
                continue
            if word in frequency_table:
                frequency_table[word]+=1
            else:
                frequency_table[word]=1
        frequency_matrix[sent[:sentence_length]] = frequency_table
    return frequency_matrix
    
def Tf(frequency_matrix):
    tf_matrix={}
    for word, freq_table in frequency_matrix.items():
        tf_table={}
        count_of_word=len(freq_table)
        for sent,num in freq_table.items():
            tf_table[sent]=num/count_of_word
        tf_matrix[word]=tf_table
    return tf_matrix

def documents_per_words(frequency_matrix):
    word_per_doc={}
    for sent, frequency_table in frequency_matrix.items():
        for word,num_of_counts in frequency_table.items():
            if word in word_per_doc:
                word_per_doc[word]+=1
            else:
                word_per_doc[word] =1
    return word_per_doc




def tf_idf_matrix(tf,idf):
    create_tf_idf_matrix={}
    for (sent1,freq_table1),(sent2,freq_table2) in zip(tf.items(),idf.items()):
        tf_idf_table={}
        for (word1,num1),(word2,num2) in zip(freq_table1.items(),freq_table2.items()):
            tf_idf_table[word1]=float(num1*num2)
        create_tf_idf_matrix[sent1]=tf_idf_table
    return create_tf_idf_matrix

def score_for_sent(tf_idf_mat):
    score_value={}
    for sent,tf_idf_table in tf_idf_mat.items():
        val_count=0
        for word,val in tf_idf_table.items():
            val_count+=val
        score_value[sent]=val_count/len(tf_idf_table)
    return score_value

def avg_score_for_threshold(sent_score_value):
    value_sum=0
    for i in sent_score_value.keys():
        value_sum +=sent_score_value[i]
    print(value_sum/len(sent_score_value))
    return (value_sum/len(sent_score_value))

def summary_of_text(text,sentvalue,threshold):
    sentcount=0
    summary=''
    for sent in text:
        if sent[:sentence_length] in sentvalue and sentvalue[sent[:sentence_length]]>=threshold:
            summary+=" "+sent
            sentcount+=1
    return summary.strip()

def Idf(total_no_of_doc,frequency_matrix,total_documents):
    idf_matrix={}
    for sent,freq_table in frequency_matrix.items():
        idf_table={}
        for word in freq_table.keys():
            idf_table[word]=math.log10(total_documents/total_no_of_doc[word])
        idf_matrix[sent]=idf_table
    return idf_matrix

def summerize(text):
    text=sent_tokenize(text)
    total_documents=len(text)
    
    idf=Idf(documents_per_words(frequency_matrix(text)),frequency_matrix(text),total_documents)
    tf=Tf(frequency_matrix(text))
    
    summary=summary_of_text(text,score_for_sent(tf_idf_matrix(tf,idf)),avg_score_for_threshold(score_for_sent(tf_idf_matrix(tf,idf))))
    lemmatizer = WordNetLemmatizer()
    # Tokenize the sentence into words
    words = word_tokenize(summary)
    # Lemmatize each word in the sentence
    lemmatized_sentence = [lemmatizer.lemmatize(word, pos="a") for word in words]
    # Join the lemmatized words back into a sentence
    lemmatized_sentence = " ".join(lemmatized_sentence)
    return lemmatized_sentence

    #Demonstration
# threeidiots="""
#         In their first year of college, students Farhan Qureshi and Raju Rastogi join the prestigious Imperial College of Engineering (ICE) in Delhi and meet Ranchhoddas Shamaldas Chanchad ("Rancho"), their roommate. Rancho is passionate about experimenting and consequently tops the class. Rancho's playful attitude to engineering puts him at odds with the rigid approach of the college's director, Dr. Viru Sahastrabuddhe (nicknamed "Virus" by the students).

#         When a student named Joy Lobo commits suicide after failing to meet a project deadline, Rancho confronts Virus about the extreme pressure placed on ICE students, but is rudely rebuffed.

#         One night, the trio gatecrashes a wedding party, not knowing that it is for Virus's daughter Mona. Mona's younger sister, Pia, is initially upset by Rancho’s behavior, but then attracted to him after he pranks her materialistic boyfriend Suhas to demonstrate his obsession with money and status. Pia breaks up with Suhas after he scolds her for wearing a cheap watch, which belonged to her mother. An infuriated Virus warns Farhan and Raju about the effects of them being friends with Rancho by pointing out the modest financial situations of their families, scaring Raju into bunking with Chatur "Silencer" Ramalingam, a competitive, arrogant Tamil student who believes in learning by rote memorization but is not fluent in Hindi. To teach Chatur a lesson about memorization, Rancho and Farhan secretly make obscene modifications to the all-Hindi Teachers Day speech that Chatur is to deliver in honor of a visit by the Minister of Education. Humiliated and furious, Chatur challenges Rancho to meet in ten years and see who is more successful.

#         The night before their final exams, Raju's paralyzed father experiences a heart attack. With Pia's help, Rancho rushes Raju's father to the hospital on Pia's scooter. Raju is initially furious at Rancho, but upon realizing that Rancho saved his father's life, Raju reconciles with him. At the end of the year, Rancho comes first in the class, while Farhan and Raju are last and second to last, respectively. During the yearly class photo, Rancho makes a bet with Virus that if either Raju or Farhan gets a job from on-campus interviews, Virus will shave his mustache.

#         One night in their fourth year of college, Rancho tells his friends why they consistently place last: Farhan's passion is photography, not engineering, and Raju lacks self-confidence. After Farhan and Raju promise to confront their problems if Rancho confesses his feelings for Pia, the three of them drunkenly break into Virus' house, and while exfiltrating, Farhan and Raju drunkenly urinate on his letterbox. Virus spots them during their escape, recognizing Raju, and the next day gives Raju an ultimatum: to incriminate his friends or be expelled himself. Distraught, Raju attempts suicide but survives, leading to Virus revoking the expulsion. Raju recovers, thanks to the support and care of his friends and family. Raju is successful in a job interview, while Farhan convinces his father to let him become a photographer.

#         Virus then tries to destroy Raju's chances of success by setting an unfairly difficult exam. With Pia's help, Rancho and Farhan break into Virus' office and steal the exam paper. Upon being given the paper, Raju refuses to cheat and throws it away, but the three of them are caught and expelled. Pia confronts her father over her brother's suicide, which was prompted by similar pressure placed on him by Virus. That night, during a heavy rainstorm, Mona, who is pregnant, goes into labor. Unable to drive to a hospital, Rancho modifies a vacuum cleaner into a ventouse and delivers the baby with the help of Pia, Farhan, and Raju. A grateful Virus acknowledges Rancho by giving him a valuable space pen, which he promised to give only to his most distinguished student, and revokes the trio's expulsions. On graduation day, Rancho suddenly disappears.

#         Ten years later, Chatur, now the prosperous vice president of a reputable company in California, calls Farhan and Raju to remind them of the bet he made with Rancho about who would be more successful. Farhan, who is on a flight at the time, feigns a medical emergency in order to meet up with Chatur and Raju. The three of them set out to find Rancho. Upon reaching Shimla, where Chatur has located Rancho's house, they come across a different man named Ranchhoddas Shyamaldas Chanchad, whose face is pasted over Rancho's in their graduation portrait. The man is reluctant to reveal anything at first and threatens the trio at gunpoint, only relenting after Farhan and Raju threaten to flush his late father's ashes down a toilet. He explains that the "Rancho" at ICE was his family's gardener's son "Chhote", who was incredibly intelligent and gifted. Ranchhoddas' father paid for Chhote to attend ICE, on condition that he use his son's name and, after graduating, cut all contact with anyone at ICE. Chhote, who was more interested in learning than in getting a degree, agreed, but afterward warned that two idiots would come looking for him one day. Ranchoddas tells the trio that he is grateful for what Chhote did, and gives them Chhote/Rancho's address in Ladakh.

#         On the way there, Farhan and Raju gatecrash Pia's wedding to Suhas in Manali and convince her to come with them to find Rancho. At the address in Ladakh, the group is astonished to find a thriving school. They meet "Millimetre", formerly an errand boy whom they met at ICE, now Rancho's assistant, who tells them that Rancho has keenly followed their careers. They reunite with Rancho on a sandbar. Rancho admits he is still in love with Pia and the two share a kiss. Chatur assumes that Rancho is a mere schoolteacher and mocks him, but Rancho reveals himself to be Phunsukh Wangdu, a successful entrepreneur with 400 patents, whom Chatur's company is courting. A shocked Chatur accepts defeat as the others run away from him laughing.
#         """

# summer=summerize(threeidiots)