import chardet

# 检测文件编码
with open('output.csv', 'rb') as f:
    result = chardet.detect(f.read())

# 获取检测到的编码
encoding = result['encoding']

# 使用 Pandas 读取文件
df = pd.read_csv('output.csv', encoding=encoding)