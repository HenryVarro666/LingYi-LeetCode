CONFIG = dict(
    num=937, title='重新排列日志文件', difficulty='Medium', category='字符串',
    author='yiduobo', technique='按首个空格拆分 · 字母日志排序',
    tags=[],
    code='''
class Solution(object):
    def reorderLogFiles(self, logs):

        letters = []
        digits = []
        for log in logs:
            tmp = log.split(' ', 1)
            if tmp[1][0] >= '0' and tmp[1][0] <= '9':
                digits.append(log)
            else:
                letters.append([tmp[0], tmp[1]])
        
        return [x[0] + ' ' + x[1] for x in sorted(letters, key=lambda d:(d[1], d[0]))] + digits
''',
    call="Solution().reorderLogFiles(['a1 9 2 3', 'g1 act car', 'z1 8 1', 'a8 act zoo', 'ab1 off key dog'])",
    expect=['g1 act car', 'a8 act zoo', 'ab1 off key dog', 'a1 9 2 3', 'z1 8 1'],
    views=[
        dict(type='queue', var='logs', h=200, fmt=lambda x: x),
        dict(type='text', fn=lambda S: f"标识符 `{S['tmp'][0]}`　内容 `{S['tmp'][1]}`　内容首字符 `{S['tmp'][1][0]}`" if 'tmp' in S else ''),
        dict(type='stack', var='letters', h=200, fmt=lambda x: f'{x[0]} | {x[1]}'),
        dict(type='stack', var='digits', h=150, fmt=lambda x: str(x)),
    ],
    watch=['log', 'tmp'],
    captions={
        'letters = []': '`letters` 放字母日志（拆成 [标识符, 内容]），`digits` 放数字日志',
        'for log in logs': '处理日志 `{log}`',
        "split(' ', 1)": '只按第一个空格切：标识符 `{tmp[0]}`，内容 `{tmp[1]}`',
        "tmp[1][0] >= '0'": '内容首字符 `{tmp[1][0]}`：{"是数字 → 数字日志" if "0" <= tmp[1][0] <= "9" else "是字母 → 字母日志"}',
        'digits.append': '数字日志原样放入 `digits`，保持原来的相对顺序',
        'letters.append': '字母日志拆成 `[标识符, 内容]` 放入 `letters`',
        'return': lambda S, B, ret: '字母日志先按内容、内容相同再按标识符排序，然后接上数字日志：`' + str(ret) + '`',
    },
    cards=dict(
        one_liner='字母日志按内容排序，数字日志保持原序放最后',
        complexity='时间 `O(n log n)`（比较按日志长度计），空间 `O(n)`',
        problem=['每条日志是「标识符 + 空格 + 内容」；内容全是数字的叫数字日志，否则叫字母日志',
                 '字母日志排在数字日志前，字母日志按内容字典序排，内容相同按标识符排；数字日志保持原相对顺序',
                 '本视频：5 条日志 → `[g1 act car, a8 act zoo, ab1 off key dog, a1 9 2 3, z1 8 1]`'],
        quote='只需要将log通过第一个空格进行分割，然后判断分割出来的第二部分的首字符是数字还是字母，然后将其加入到字符list或者数字list的末尾。',
        quote_src='—— yiduobo 题解原文',
        idea=['`split(\' \', 1)` 只切第一个空格，后面内容保持完整',
              '看内容第一个字符就能判断类型；数字日志直接收进 `digits`',
              '字母日志用 key `(内容, 标识符)` 排序，最后拼上数字日志'],
        summary=['时间 `O(n log n)`，空间 `O(n)`',
                 '`split(\' \', 1)` 必须限制切一次，否则内容会被拆碎',
                 '排序 key 是 `(内容, 标识符)`，先内容后标识符，顺序不能反',
                 '原文为 Python 2 写法，仅删去了类型说明文档字符串'],
    ),
)
