CONFIG = dict(
    num=3746, title='等量移除后的字符串最小长度', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='一趟遍历计 a 与 b 之差',
    tags=['贪心与思维', '脑筋急转弯', '难度分 1327'],
    code='''
class Solution(object):
    def minLengthAfterRemovals(self, s):
        
        res = 0
        for c in s:
            if c == 'a':
                res += 1
            else:
                res -= 1
        
        return abs(res)
''',
    call="Solution().minLengthAfterRemovals('aabbaab')",
    expect=1,
    views=[
        dict(type='string', var='s', label='s（蓝 = a 加 1，粉 = b 减 1）', h=240,
             color=lambda S, i, v: 'blue' if v == 'a' else 'pink'),
        dict(type='text', fn=lambda S: f"当前 `res = {S['res']}`：a 比 b 多 =={S['res']}== 个" if 'res' in S and S['res'] >= 0 else (f"当前 `res = {S['res']}`：b 比 a 多 =={-S['res']}== 个" if 'res' in S else ''), size=30),
    ],
    watch=[('c', 'c', 'yellow'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 记录 a 与 b 数量之差，一开始为 0',
        "if c == 'a'": '`c = {c}`：是 a 吗？→ {"是，a 多一个" if c == "a" else "不是，b 多一个"}',
        'res += 1': '遇到 a：`res` {B.res} → =={res}==',
        'res -= 1': '遇到 b：`res` {B.res} → =={res}==',
        'return abs(res)': '最终差为 `{res}`，两种字母配对消掉后剩 `abs({res})` = =={ret}==',
    },
    skip=['for c in s'],
    cards=dict(
        one_liner='能配对的 a、b 全消掉，剩下的就是数量之差',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `s` 仅由 `a`、`b` 组成，可反复移除 a、b 数量相同的子串',
                 '求剩余字符串的最小长度',
                 '本视频：`"aabbaab"` → `1`'],
        quote='当字符串中还存在两种字符时，必然存在至少一组相邻字符是由a和b组成的，于是可以不断移除掉这一组相邻的字符，直到字符串中仅剩a或者仅剩b为止。',
        quote_src='—— yiduobo 题解原文',
        idea=['还有两种字符 → 一定有相邻的 a、b，删掉它们',
              '一直删到只剩一种字符为止',
              '所以答案就是 a 与 b 数量之差的绝对值，一趟遍历统计即可'],
        after=[dict(heading='遍历怎么统计', lines=['遇到 a：`res += 1`；遇到 b：`res -= 1`', '遍历完 `res` 就是 a 的个数减 b 的个数', '返回 `abs(res)`，不用关心谁多'])],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：要取绝对值，b 多时 `res` 为负',
                 '原文为 Python 2 风格，代码无需改动',
                 '对比灵神：灵神用 `count` 直接算 `|2k - n|`，yiduobo 手写遍历累加 +1/-1'],
    ),
)
