import sys
import math
from decimal import *
import codecs

tag_list = set()
tag_count = {}
word_set = set()


def parse_traindata():
    #print "In Training\n"

    fin = sys.argv[1]
    output_file = "hmmmodel.txt"
    wordtag_list = []

    try:
        input_file = codecs.open(fin, mode = 'r', encoding="utf-8")
        lines = input_file.readlines()
        for line in lines:
            line = line.strip('\n')
            data = line.split(" ")
            wordtag_list.append(data)

        input_file.close()
        return wordtag_list

    except IOError:
        fo = codecs.open(output_file,mode = 'w',encoding="utf-8")
        fo.write("File not found: {}".format(fin))
        fo.close()
        sys.exit()


def transition_count():
    #print "In Transition Model"
    global tag_list
    global word_set
    train_data = parse_traindata()
    transition_dict = {}
    global tag_count
    for value in train_data:
        previous = "start"
        for data in value:
            i = data[::-1]
            word = data[:-i.find("/") - 1]
            word_set.add(word.lower())
            data = data.split("/")
            tag = data[-1]
            tag_list.add(tag)

            if tag in tag_count:
                tag_count[tag] += 1
            else:
                tag_count[tag] = 1

            if (previous + "~tag~" + tag) in transition_dict:
                transition_dict[previous + "~tag~" + tag] += 1
                previous = tag
            else:
                transition_dict[previous + "~tag~" + tag] = 1
                previous = tag


    #print tag_count
    #print tag_list
    #print word_set
    return transition_dict


def transition_probability():
    count_dict = transition_count()
    prob_dict = {}
    for key in count_dict:
        den = 0
        val = key.split("~tag~")[0]
        for key_2 in count_dict:
            if key_2.split("~tag~")[0] == val:
                den += count_dict[key_2]
        prob_dict[key] = Decimal(count_dict[key])/(den)
    return prob_dict


def transition_smoothing():
    transition_prob = transition_probability()
    for tag in tag_list:
        if "start" + tag not in  transition_prob:
            transition_prob[("start" + "~tag~" + tag)] = Decimal(1) / Decimal(len(word_set) + tag_count[tag])
    for tag1 in tag_list:
        for tag2 in tag_list:
            if (tag1 +"~tag~" + tag2) not in transition_prob:
                transition_prob[(tag1+"~tag~"+tag2)] = Decimal(1)/Decimal(len(word_set) + tag_count[tag1])
    return transition_prob


def emission_count():
    #print "In Emission Model"
    train_data = parse_traindata()
    count_word = {}
    for value in train_data:
        for data in value:
            i = data[::-1]
            word = data[:-i.find("/") - 1]
            tag = data.split("/")[-1]
            if word.lower() + "/" + tag in count_word:
                count_word[word.lower() + "/" + tag] +=1
            else:
                count_word[word.lower() + "/" + tag] = 1
    return count_word


def emission_probability():
    #print "In Emission Probability"
    global tag_count
    word_count = emission_count()
    emission_prob_dict = {}
    for key in word_count:
        emission_prob_dict[key] = Decimal(word_count[key])/tag_count[key.split("/")[-1]]
    return emission_prob_dict


def main():
    global tag_count
    #transition_model = transition_probability()
    transition_model = transition_smoothing()
    #print transition_model

    emission_model = emission_probability()
    #print emission_model

    fout = codecs.open("hmmmodel.txt", mode ='w', encoding="utf-8")
    for key, value in transition_model.items():
        fout.write('%s:%s\n' % (key, value))

    fout.write(u'Emission Model\n')
    for key, value in emission_model.items():
        fout.write('%s:%s\n' % (key, value))


if __name__ == '__main__':
    main()