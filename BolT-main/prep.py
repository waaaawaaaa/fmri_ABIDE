# TO GET DATA READY FOR THE TESTER


import argparse   #导入argparse模块，用于解析命令行参数。

parser = argparse.ArgumentParser()      #创建一个ArgumentParser对象，用于解析命令行参数。

parser.add_argument("-d", "--dataset", type=str, choices=["abide1", "hcpRest", "hcpTask"], default="abide1")
# parser.add_argument("-a", "--atlas", type=str, choices=["schaefer7_400", 'AAL_116'], default="schaefer7_400")
parser.add_argument("-a", "--atlas", type=str, choices=["schaefer7_400", 'AAL_116'], default="AAL_116")
# 添加两个参数，分别为-d或--dataset和-a或--atlas。这些参数可以通过命令行输入，并限定了参数的类型和可选值。默认值为"abide1"和"schaefer7_400"。
argv = parser.parse_args()  #解析命令行参数，并将结果存储在argv变量中。


from Dataset.Prep.prep_abide import prep_abide


if(argv.dataset == "abide1"):
    prep = prep_abide


prep(argv.atlas)    #解析命令行参数，并将结果存储在argv变量中。


