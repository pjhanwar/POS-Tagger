import sys
from decimal import *
import codecs

tag_set = set()
word_set = set()

def parse_traindata():
    fin = "hmmmodel.txt"
    output_file = "hmmmoutput.txt"
    transition_prob = {}
    emission_prob = {}
    tag_list = []
    tag_count ={}
    global tag_set
    try:
        input_file = codecs.open(fin,mode ='r', encoding="utf-8")
        lines = input_file.readlines()
        flag = False
        for line in lines:
            line = line.strip('\n')
            if line != "Emission Model":
                i = line[::-1]
                key_insert = line[:-i.find(":")-1]
                value_insert = line.split(":")[-1]
                if flag == False:
                    transition_prob[key_insert] = value_insert
                    if (key_insert.split("~tag~")[0] not in tag_list) and (key_insert.split("~tag~")[0] != "start"):
                        tag_list.append(key_insert.split("~tag~")[0])

                else:
                    emission_prob[key_insert] = value_insert
                    key_tag = line[:-i.find(":") - 1]
                    val = key_tag.split("/")[-1]
                    j = key_insert[::-1]
                    word = key_insert[:-j.find("/")-1]
                    #print word
                    word_set.add(word.lower())
                    if val in tag_count:
                        tag_count[val] +=1
                    else:
                        tag_count[val] = 1
                    tag_set.add(val)

            else:
                flag = True
                continue

        input_file.close()
        return tag_list, transition_prob, emission_prob, tag_count, word_set

    except IOError:
        fo = codecs.open(output_file, mode='w',encoding="utf-8")
        fo.write("File not found: {}".format(fin))
        fo.close()
        sys.exit()


def viterbi_algorithm(sentence, tags, transition_prob, emission_prob,tag_count, word_set):
    #print "In Viterbi\n"
    global tag_set
    sentence = sentence.strip("\n")
    word_list = sentence.split(" ")
    current_prob = {}
    for tag in tags:
        tp = Decimal(0)
        em = Decimal(0)
        if "start~tag~"+tag in transition_prob:
            tp = Decimal(transition_prob["start~tag~"+tag])
        if word_list[0].lower() in word_set:
            if (word_list[0].lower()+"/"+tag) in emission_prob:
                em = Decimal(emission_prob[word_list[0].lower()+"/"+tag])
                current_prob[tag] = tp * em
        else:
            em = Decimal(1) /(tag_count[tag] +len(word_set))
            current_prob[tag] = tp

    if len(word_list) == 1:
        max_path = max(current_prob, key=current_prob.get)
        return max_path
    else:
        for i in xrange(1, len(word_list)):
            previous_prob = current_prob
            current_prob = {}
            locals()['dict{}'.format(i)] = {}
            previous_tag = ""
            for tag in tags:
                if word_list[i].lower() in word_set:
                    if word_list[i].lower()+"/"+tag in emission_prob:
                        em = Decimal(emission_prob[word_list[i].lower()+"/"+tag])
                        max_prob, previous_state = max((Decimal(previous_prob[previous_tag]) * Decimal(transition_prob[previous_tag + "~tag~" + tag]) * em, previous_tag) for previous_tag in previous_prob)
                        current_prob[tag] = max_prob
                        locals()['dict{}'.format(i)][previous_state + "~" + tag] = max_prob
                        previous_tag = previous_state
                else:
                    em = Decimal(1) /(tag_count[tag] +len(word_set))
                    max_prob, previous_state = max((Decimal(previous_prob[previous_tag]) * Decimal(transition_prob[previous_tag+"~tag~"+tag]) *em, previous_tag) for previous_tag in previous_prob)
                    current_prob[tag] = max_prob
                    locals()['dict{}'.format(i)][previous_state + "~" + tag] = max_prob
                    previous_tag = previous_state

            if i == len(word_list)-1:
                max_path = ""
                last_tag = max(current_prob, key=current_prob.get)
                max_path = max_path + last_tag + " " + previous_tag
                for j in range(len(word_list)-1,0,-1):
                    for key in locals()['dict{}'.format(j)]:
                        data = key.split("~")
                        if data[-1] == previous_tag:
                            max_path = max_path + " " +data[0]
                            previous_tag = data[0]
                            break
                result = max_path.split()
                result.reverse()
                return " ".join(result)


def main():
    tag_list, transition_model, emission_model, tag_count, word_set = parse_traindata()
    #print tag_count
    #print(word_set)
    fin = sys.argv[1]
    input_file = codecs.open(fin, mode='r', encoding="utf-8")
    fout = codecs.open("hmmoutput.txt",mode='w',encoding="utf-8")
    for sentence in input_file.readlines():
        #print("New Sentence\n")
        path = viterbi_algorithm(sentence, tag_list, transition_model, emission_model,tag_count, word_set)
        sentence = sentence.strip("\n")
        word = sentence.split(" ")
        tag = path.split(" ")
        for j in range(0,len(word)):
            if j == len(word)-1:
                fout.write(word[j] + "/" + tag[j]+u'\n')
            else:
                fout.write(word[j] + "/" + tag[j] + " ")


if __name__ == '__main__':
    main()
