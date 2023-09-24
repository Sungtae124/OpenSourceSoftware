def read_data(filename):                                                        #CSV 파일 불러와서 데이터를 2차원 리스트로 저장하기
    # TODO) Read `filename` as a list of integer numbers
    data = []
    with open(filename, 'r') as fi:                                             # with - as 로 파일 열기
        for line in fi.readlines():                                             # 한 줄 씩 파일 읽기
           if not line.lstrip().startswith(("#")):                              # without line which start with Header('#') 
               values = [int(word) for word in line.split(',')]                 # ','를 기준으로 쪼개기
               #print(values)
               data.append(values)                                              # 구한 값을 data list에 저장하기
    #print(data)           
    return data


def calc_weighted_average(data_2d, weight):                                     #가중치 평균 구하기
    # TODO) Calculate the weighted averages of each row of `data_2d`
    average = []
    for midScore, finScore in data_2d:                                          #2차원 리스트로 저장된 값들을 average 리스트에 가중치 계산을 하여 소숫점 3자리로 끊어서 저장하기
        average.append(round(midScore * weight[0] + finScore * weight[1] , 3))
    #print(average)
    return average

def analyze_data(data_1d):                                                      # 중간, 기말, 평균에 대한 평균, 분산, 중간값 구하기
    # TODO) Derive summary of the given `data_1d`
    # Note) Please don't use NumPy and other libraries. Do it yourself.
    mean = round(sum(data_1d) / len(data_1d),3)                                 # 평균 구한 뒤 소숫점 3자리로 끊어서 저장
    #print(sum(data_1d), len(data_1d), mean)
    
    
    diff = []                                                                   # 편차 배열 선언
    poweredDiff = []                                                            # 편차 제곱 배열 선언
    for idx in range(len(data_1d)):                                             # 인덱스로 for문 돌기
        diff.append(data_1d[idx] - mean)                                        # 편차 배열에 구한 편차 저장해두기
        poweredDiff.append(diff[idx] * diff[idx])                               # 편차 제곱 배열에 저장
    var = round(sum(poweredDiff) / len (diff) , 3)                              # 분산 구해서 소숫점 3자리로 끊어서 저장
    #print(var)
    
    sortedAvg = sorted(data_1d)                                                 # 실제 데이터 순서는 바뀌지 않도록 sorted 사용하여 정렬
    median = round(sortedAvg[(int)(len(data_1d) / 2)], 3)                       # median에 정렬된 순서를 이용하여 리스트 길이의 절반에서 중간값을 찾아 저장
    
    #print(mean, var, median)
    return mean, var, median, min(data_1d), max(data_1d)


if __name__ == '__main__':
    data = read_data('data/class_score_en.csv')
    if data and len(data[0]) == 2: # Check 'data' is valid
        average = calc_weighted_average(data, [40/125, 60/100])
        #analyze_data(average)

        # Write the analysis report as a markdown file
        with open('class_score_analysis.md', 'w') as report:
            report.write('### Individual Score\n\n')
            report.write('| Midterm | Final | Total |\n')
            report.write('| ------- | ----- | ----- |\n')
            for ((m_score, f_score), a_score) in zip(data, average):
                report.write(f'| {m_score} | {f_score} | {a_score:.3f} |\n')
            report.write('\n\n\n')


            report.write('### Examination Analysis\n')
            data_columns = {
                'Midterm': [m_score for m_score, _ in data],
                'Final'  : [f_score for _, f_score in data],
                'Average': average }
            
            for name, column in data_columns.items():
                mean, var, median, min_, max_ = analyze_data(column)
                report.write(f'* {name}\n')
                report.write(f'  * Mean: **{mean:.3f}**\n')
                report.write(f'  * Variance: {var:.3f}\n')
                report.write(f'  * Median: **{median:.3f}**\n')
                report.write(f'  * Min/Max: ({min_:.3f}, {max_:.3f})\n')
