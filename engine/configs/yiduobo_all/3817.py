def _col(S, i, v):
    if 'index' in S and 'length' in S and S['index'] - S['length'] + 1 <= i <= S['index']:
        return 'yellow'
    if i in S.get('res', []):
        return 'green'
    return None

CONFIG = dict(
    num=3817, title='数字字符串中的好索引', difficulty='Medium', category='字符串',
    author='yiduobo', technique='枚举下标 + 截取子串', tags=[],
    code='''
class Solution(object):
    def goodIndices(self, s):
        
        res = []
        for index in range(len(s)):
            length = len(str(index))
            if int(s[index - length + 1: index + 1]) == index:
                res.append(index)
        
        return res
''',
    call='Solution().goodIndices("021345678100")',
    expect=[0, 3, 4, 5, 6, 7, 8, 10],
    views=[
        dict(type='string', var='s', color=_col, pointers={'index': 'blue'}, cell=70, h=260),
        dict(type='text', fn=lambda S: (f"index = {S['index']}，截取 `s[{S['index']-S['length']+1}:{S['index']+1}]` = `{S['s'][S['index']-S['length']+1:S['index']+1]}`，要等于 =={S['index']}==" if 'length' in S else ''), h=100),
        dict(type='text', fn=lambda S: f"好索引 res = {S['res']}" if 'res' in S else '', h=100),
    ],
    watch=['index', 'length', ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 收集所有好索引',
        'for index': '枚举每个下标 `index = {index}`',
        'length = len': '`index` 的十进制有 `{length}` 位 → 只需要看以它结尾的 `{length}` 个字符（最多 5 位）',
        'if int(': lambda S, B, r: (f'`int(s[{S.index-S.length+1}:{S.index+1}])` = {int(S.s[S.index-S.length+1:S.index+1])}，和 `index = {S.index}` ' + ('==相等== → 好索引' if int(S.s[S.index-S.length+1:S.index+1]) == S.index else '不相等 → 不是')),
        'res.append': '`{index}` 是好索引，加入 `res`',
        'return res': '全部枚举完，好索引为 =={res}==',
    },
    cards=dict(
        one_liner='下标最多 5 位，截取末尾几位比较即可',
        complexity='时间 `O(n·L)`，`L ≤ 5`，约 `O(n)`；空间 `O(1)`（不计答案）',
        problem=['给一个数字字符串 `s`（长度 ≤ 10^5）', '若存在以 `index` 结尾的子串，数值等于 `index` 的十进制表示，则 `index` 为好索引',
                 '按升序返回所有好索引；本视频：`"021345678100"`'],
        quote='对于任意一个索引index，最多只需要截取从index开始向前的5个字符，转化为数字后与index进行比较就行了。',
        quote_src='—— yiduobo 题解原文',
        idea=['`s` 长 ≤ 10^5，最大下标 99999，最多 5 位', '子串长度必须等于 `index` 的位数，截取 `s[index-length+1 : index+1]`', '转成整数后和 `index` 比，相等就收进答案'],
        summary=['时间约 `O(n)`，每次截取只有 1~5 个字符', '截取长度 = `len(str(index))`，不是固定 5',
                 '原文为 Python 2 风格，本题代码在 Python 3 下无需修改', '本题题面库中缺失，题意按 yiduobo 原文整理'],
    ),
)
