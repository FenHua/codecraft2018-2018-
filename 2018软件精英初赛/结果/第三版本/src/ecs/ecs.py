# coding=utf-8
import sys
import os
import utils
import predictor

def main():
    
    print 'main function begin.'
    if len(sys.argv) != 4:
        print 'parameter is incorrect!'
        print 'Usage: python esc.py ecsDataPath inputFilePath resultFilePath'
        exit(1)
    # Read the input files
    inputFilePath = sys.argv[1]
    ecsDataPath = sys.argv[2]
    resultFilePath = sys.argv[3]
    '''
    # read the path of file
    ecsDataPath = "Data/input_5flavors_cpu_7days.txt"
    inputFilePath ="Data/TestData_2015.2.20_2015.2.27.txt"
    resultFilePath = "Data/results.txt"
    '''
    #read the file
    ecs_infor_array = read_lines(ecsDataPath)
    

    input_file_array = read_lines(inputFilePath)
    
    
    # implementation the function predictVm
    predic_result = predictor.predict_vm(ecs_infor_array, input_file_array)

    print predic_result
    
    # write the result to output file
    if len(predic_result) != 0:
        write_result(predic_result, resultFilePath)
    else:
        predic_result.append("NA")
        write_result(predic_result, resultFilePath)
    print 'main function end.'


def write_result(array, outpuFilePath):
    with open(outpuFilePath, 'w') as output_file:
        for item in array:
            output_file.write("%s\n" % item)


def read_lines(file_path):
    if os.path.exists(file_path):
        array = []
        with open(file_path, 'r') as lines:
            for line in lines:
                array.append(line)
        return array
    else:
        print 'file not exist: ' + file_path
        return None


if __name__ == "__main__":
    main()
