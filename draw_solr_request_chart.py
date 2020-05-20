import re
import sys
import os
import xlsxwriter

def file_read(filename, phase, attr, rate):
    time_arr = []
    count_arr = []
    with open(filename) as f:
        for line in f:
            if not line.strip(' \t\n\r,'):
                continue
            else:
                if re.match('\d{4}-\d{2}-\d{2}\s{1}\d{2}:\d{2}:\d{2}', line):
                    time_arr.append(line)
                if phase in line:
                    line = next(f).strip(' \t\n\r,')
                    while attr not in line: 
                        line = next(f).strip(' \t\n\r,')
                    count_arr.append(float((line.split(': ', 1)[1])))

    if attr == "Count":
        if rate == "rate":
            count_rate_arr = get_rate(count_arr)
            return time_arr, count_rate_arr
    
    return time_arr, count_arr


def get_rate(input_array):
    prev = 0
    return_arr = []
    for current in input_array:
        rate = int(current) - int(prev)
        prev = current
        if rate < 0:
            rate = 0
        return_arr.append(rate)
    return return_arr



def draw_chart(data, nodes, output, attr):
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    print nodes
    itr = 0
    while itr < len(nodes):
       index = 2 * itr 
       print nodes[itr]
       worksheet.write(0,index, nodes[itr])
       worksheet.write(0, (index+1), nodes[itr])
       itr += 1

    i = 0
    while i < len(data):
        worksheet.write_column(1,i, data[i])
        i += 1

    chart1 = workbook.add_chart({'type': 'line'})
    
    max_row = len(data[0])
    print max_row
    print range(len(nodes))
    for j in range(len(nodes)):
        col = 2*j + 1 
        chart1.add_series({
            'name': ['Sheet1', 0, col],
            'categories': ['Sheet1', 1, 2*j, max_row, 0],
            'values': ['Sheet1', 1, col, max_row, col],
            })
        j += 1

    chart1.set_x_axis({'name': 'Timestamp'})
    chart1.set_y_axis({'name': attr, 'major_gridlines': {'visible': False}})

    worksheet.insert_chart('G2', chart1)

    workbook.close()


def main():
    if len(sys.argv) < 5:
        print "Usage: python draw_solr_request_chart.py <xlsx output file> [RETRIEVE|COORDINATE|EXECUTE] <Attribute of the phase, for example, Count or 99thPercentile> [rate|false] <file path1> <file path2> ..."
        sys.exit()

    output = sys.argv[1]
    if os.path.splitext(output)[1] != '.xlsx':
        print "The output file needs to have ext .xlsx"
        sys.exit()

    phase = sys.argv[2].strip()
    attr = sys.argv[3].strip()
    rate = sys.argv[4].strip()
    x_axis = attr + " of phase " + phase 
    print phase, attr
    i = 5
    data = []
    nodes = []
    while i < len(sys.argv):
        fp = sys.argv[i]
        if not os.path.isfile(fp):
            print("File path {} does not exist. Exiting...".format(fp))
            sys.exit()
        
        x,y = file_read(fp, phase, attr, rate)

        node = os.path.splitext(str(fp))[0].split('/')[-1].split('-')[0]
        nodes.append(node)

        data.append(x)
        data.append(y)

        i += 1


    draw_chart(data, nodes, output, x_axis)



if __name__== "__main__":
  main()
