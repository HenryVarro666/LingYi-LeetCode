CONFIG = dict(
    num=3228, title='将 1 移动到末尾的最大操作次数', difficulty='Medium', category='贪心算法',
    author='yiduobo', technique='从头遍历 + 末尾补 1',
    tags=['灵神题单', '贪心与思维', '难度分 1593'],
    code='''
class Solution(object):
    def maxOperations(self, s):

        cnt = 0
        res = 0
        s += '1'
        for index in range(len(s)):
            if s[index] == '1' and index > 0 and s[index - 1] == '0':
                res += cnt
            if s[index] == '1':
                cnt += 1
            
        return res
''',
    call='Solution().maxOperations("1001101")',
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"当前位置左侧有 `{S['cnt']}` 个 1；累计 =={S['res']}==" if 'cnt' in S and 'res' in S else '')),
        dict(type='string', var='s', pointers={'index': 'blue'}, h=230,
             color=lambda S, i, v: ('yellow' if (i == len(S['s']) - 1 and 'index' in S) else 'green' if v == '1' else None) if 'index' in S and i <= S['index'] else None,
             dim=lambda S, i, v: 'index' in S and i > S['index']),
    ],
    watch=['index', ('cnt', 'cnt', 'cyan'), ('res', 'res', 'green')],
    captions={
        'cnt = 0': '`cnt`：当前位置左侧 1 的个数',
        'res = 0': '`res`：累计操作次数',
        "s += '1'": '末尾补一个 `1`（黄色）：这样“最后一个 0 把所有 1 移到末尾”也能被一组 `01` 统计到；原本末尾是 1 时补一个也不影响',
        "s[index] == '1' and index > 0": lambda S, B, r: (f'`s[{S.index}] = 1` 且左边是 `0`：可把左侧 `{S.cnt}` 个 1 都挪过来 → `res += {S.cnt}`' if S.index > 0 and S.s[S.index] == '1' and S.s[S.index-1] == '0' else '不是“0 后接 1”，这里不新增操作'),
        'res += cnt': '`res = {B.res} + {cnt}` = =={res}==',
        "if s[index] == '1':": lambda S, B, r: ('是 1：左侧 1 的个数要加一' if S.s[S.index] == '1' else '是 0：`cnt` 不变'),
        'cnt += 1': '`cnt` → {cnt}',
        'return res': '最多操作 `{ret}` 次',
    },
    cards=dict(
        one_liner='先动靠前的 1 才能多操作：每遇到 0→1，累加左侧 1 的个数',
        complexity='时间 `O(n)`，空间 `O(1)`（补 1 的字符串拷贝为 `O(n)`）',
        problem=['二进制串，选 `s[i]=1`、`s[i+1]=0` 的 1 向右移到下一个 1 的左边（或末尾）',
                 '求最多操作次数',
                 '示例：`"1001101"` → `4`'],
        quote='题目要求执行操作的次数最多，也就是说应该尽量避免一步到位的操作。换言之，在这里应该先执行字符串头部的操作而不是尾部的操作。',
        quote_src='—— yiduobo 题解原文',
        idea=['从 DP 角度：当前 1 与右侧 1 不相邻时，它的次数 = 右侧的次数 + 1',
              '所以应从头到尾移动：遇到“0 后接 1”，左侧每个 1 都能移一次',
              '末尾补 `1`，让最后一段 0 也能形成 `01` 被统计'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：不补 1 会漏掉“末尾是 0”时把所有 1 移到末尾的那一批',
                 '`cnt` 要在统计 `res` 之后再加：当前这个 1 不算左侧的车',
                 '原文为 Python 2 写法，代码无需改动',
                 '对比灵神：灵神在 0 的位置累加，这里在 1 的位置累加并补哨兵'],
    ),
)
