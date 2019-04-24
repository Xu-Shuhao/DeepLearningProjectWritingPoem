# coding: UTF-8

from config import *

class POEMS:
    "poem class"
    def __init__(self, filename, isEvaluate=False):
        #__ 开头表示 是私有的，不能被类的外部使用或者访问
        """pretreatment"""#预处理
        poems = []
        file = open(filename, "r", encoding="utf-8")
        for line in file:  #every line is a poem
            title, author, poem = line.strip().split("::")  #get title and poem
            poem = poem.replace(' ','')#poem is type of []，把原有的空格 消去
            if len(poem) < 10 or len(poem) > 512:  #filter poem len = 汉字+ punctuation
                continue
            if '_' in poem or '《' in poem or '[' in poem or '(' in poem or '（' in poem:
                continue# 去除没有干净的字符处理
            poem = '[' + poem + ']' #add start and end signs
            poems.append(poem)
            #print(title, author, poem)

        #counting words
        wordFreq = collections.Counter()
        for poem in poems:
            wordFreq.update(poem)# 自动统计字数出现的次数，按照大小排序，逗号
        # print(wordFreq)

        # erase words which are not common
        #--------------------bug-------------------------
        # word num less than original num, which causes nan value in loss function
        # erase = []
        # for key in wordFreq:
        #     if wordFreq[key] < 2:
        #         erase.append(key)
        # for key in erase:
        #     del wordFreq[key]

        wordFreq[" "] = -1
        #把出来的空格给排序为1
        #出现的数据就是 词的数量
        wordPairs = sorted(wordFreq.items(), key = lambda x: -x[1])
        self.words, freq = zip(*wordPairs)
        self.wordNum = len(self.words)
        #统计所有词和词频
        self.wordToID = dict(zip(self.words, range(self.wordNum))) #word to ID zip() 函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表。
        poemsVector = [([self.wordToID[word] for word in poem]) for poem in poems] # poem to vector
        #上述还是在进行数据处理，把字转变为向量
        if isEvaluate: #evaluating need divide dataset into test set and train set，需不需要拆分成 训练和测试
            self.trainVector = poemsVector[:int(len(poemsVector) * trainRatio)]
            self.testVector = poemsVector[int(len(poemsVector) * trainRatio):]
        else:
            self.trainVector = poemsVector
            self.testVector = []
        print("训练样本总数： %d" % len(self.trainVector))
        print("测试样本总数： %d" % len(self.testVector))


    def generateBatch(self, isTrain=True):
        #padding length to batchMaxLength
        if isTrain:
            poemsVector = self.trainVector
        else:
            poemsVector = self.testVector

        random.shuffle(poemsVector)
        batchNum = (len(poemsVector) - 1) // batchSize
        X = []
        Y = []
        #create batch
        for i in range(batchNum):
            batch = poemsVector[i * batchSize: (i + 1) * batchSize]
            maxLength = max([len(vector) for vector in batch])
            temp = np.full((batchSize, maxLength), self.wordToID[" "], np.int32) # padding space
            for j in range(batchSize):
                temp[j, :len(batch[j])] = batch[j]
            X.append(temp)
            temp2 = np.copy(temp) #copy!!!!!!
            temp2[:, :-1] = temp[:, 1:]
            Y.append(temp2)
        return X, Y

