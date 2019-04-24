# coding: UTF-8
from config import *
import data
import model

def defineArgs():
    """define args"""
    parser = argparse.ArgumentParser(description = "Chinese_poem_generator.")
    parser.add_argument("--mode",help = "select mode by 'train' or test or head",
                        choices = ["train", "test", "head"], default = "train")
   #choices: 这个参数用来检查输入参数的范围。如：choices=[1,3,5]
    return parser.parse_args()

if __name__ == "__main__":
    args = defineArgs()
    trainData = data.POEMS(trainPoems)#train data是一个对象
    MCPangHu = model.MODEL(trainData)
    if args.mode == "train":
        MCPangHu.train()
    else:
        if args.mode == "test":
            poems = MCPangHu.test()
        else:
                characters = input("please input chinese character:")
                poems = MCPangHu.testHead(characters)