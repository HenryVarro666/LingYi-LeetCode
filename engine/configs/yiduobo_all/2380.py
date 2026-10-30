CONFIG = dict(
    num=2380, title='二进制字符串重新安排顺序需要的时间', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='每个 1 归位时间 · 一趟遍历',
    tags=[],
    code='''
class Solution(object):
    def secondsToRemoveOccurrences(self, s):

        res = 0
        cnt = 0
        for char in s:
            if char == '0':
                cnt += 1
            elif cnt > 0:
                res = max(res + 1, cnt)
        
        return res
''',
    call='Solution().secondsToRemoveOccurrences("0110101")',
    expect=4,
    views=[
        dict(type='string', var='s', label='s（最终所有 1 在左、0 在右）', h=200),
        dict(type='text', h=110, size=34, fn=lambda S: f"已遇到 `{S['cnt']}` 个 0，最后一个 1 归位用 =={S['res']}== 秒" if 'cnt' in S else ''),
    ],
    watch=[('char', 'char', 'blue'), ('cnt', 'cnt', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res`：目前最后一个 1 归位所需的时间',
        'cnt = 0': '`cnt`：目前遇到 0 的数目',
        'for char in s': '看下一个字符 `{char}`',
        "if char == '0'": lambda S, B, r: ("是 `0`：计数 `cnt` 加 1" if S.char == '0' else "是 `1`：算它归位需要多久"),
        'cnt += 1': '`cnt = {cnt}`',
        'elif cnt > 0': lambda S, B, r: (f'`cnt = {B.cnt} > 0`：左边有 0，这个 1 需要移动' if B.cnt > 0 else '`cnt = 0`：左边没有 0，这个 1 已经归位'),
        'res = max': '理想情况 `cnt = {cnt}` 秒；被前一个 1 卡住则是前一个 1 的时间 +1 = `{B.res} + 1`。取大：`res = {res}`',
        'return res': '最后一个 1 归位时间就是答案 `{res}`',
    },
    cards=dict(
        one_liner='右边的 1 归位时间 = max(左边 1 的时间 + 1, 它左侧 0 的个数)',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每一秒所有 `"01"` 同时变成 `"10"`，直到没有 `"01"`',
                 '求需要的秒数；进阶要求 `O(n)`',
                 '示例：`"0110101"` → `4`'],
        quote='右侧1归位的时间恰好就等于左侧1归位的时间再加上1。',
        quote_src='—— yiduobo 题解原文',
        idea=['最终所有 1 在左、0 在右，考虑每个 1 归位的时间',
              '最左边的 1：时间 = 它左侧 0 的数目',
              '两个相邻的 1 若挤在一起，右边的会被卡住，比左边晚 1 秒；否则就是左侧 0 的数目'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错：只有 `cnt > 0` 时才更新 `res`',
                 '规模小时也可以直接模拟，但题目进阶要求 `O(n)`',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串，代码未改'],
    ),
)
