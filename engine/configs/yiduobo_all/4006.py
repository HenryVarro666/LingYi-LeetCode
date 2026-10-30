CONFIG = dict(
    num=4006, title='统计有效前缀数目', difficulty='Easy', category='字符串',
    author='yiduobo', technique='维护 0/1 数量差',
    tags=[],
    code='''
class Solution(object):
    def countValidPrefixes(self, s):
        
        diff = 0
        res = 0
        for c in s:
            if c == '1':
                diff += 1
            else:
                diff -= 1
            
            if abs(diff) <= 1:
                res += 1
        
        return res
''',
    call='Solution().countValidPrefixes("0010110")',
    expect=5,
    views=[
        dict(type='string', var='s', label='s（粉色箭头 = 当前读到的字符）', cell=70, h=170,
             ),
        dict(type='text', size=36, h=130, fn=lambda S: (f"`diff` = 1 的个数 − 0 的个数 = =={S['diff']}==，`|diff|` = {abs(S['diff'])}" if 'diff' in S else '')),
    ],
    watch=['c', ('diff', 'diff', 'blue'), ('res', 'res', 'green')],
    captions={
        "if c == '1'": '读到 `{c}`：是 1 则 `diff` +1，是 0 则 `diff` −1',
        'diff += 1': '1 比 0 多一个：`diff` → {diff}',
        'diff -= 1': '0 比 1 多一个：`diff` → {diff}',
        'if abs(diff)': '`|diff| = {abs(diff)}`：{"不超过 1，这个前缀能重排成交替串" if abs(diff) <= 1 else "超过 1，重排后必有相邻相同"}',
        'res += 1': '有效前缀 +1 → `res = {res}`',
        'return res': '共 `{res}` 个有效前缀',
    },
    cards=dict(
        one_liner='只看 0 和 1 的数量差，绝对值不超过 1 就有效',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['二进制字符串 `s`，前缀的字符能重排成交替串则有效',
                 '问有效前缀的数目',
                 '示例：`"00101"` → `3`；本视频用 `"0010110"` → `5`'],
        quote='若其中0的数量与1的数量之差diff的绝对值不超过1，那么这个前缀就是有效的。',
        quote_src='—— yiduobo 题解原文',
        idea=['重排后只能是 `1010…` 或 `0101…`',
              '前者 1 的个数等于或比 0 多 1，后者反过来',
              '一趟遍历维护 `diff`（1 加、0 减），`|diff| ≤ 1` 就计数'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '只用一个变量 `diff`，不必分别存 0、1 的个数',
                 '原文可直接在 Python 3 运行，未做修改',
                 '对比灵神：灵神用 `cnt[0]`、`cnt[1]` 两个计数，yiduobo 合并成一个差值'],
    ),
)
