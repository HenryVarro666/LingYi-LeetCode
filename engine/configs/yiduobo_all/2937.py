def _col(S, i, v):
    return 'green' if i < S.get('p', 0) else None


CONFIG = dict(
    num=2937, title='使三个字符串相等', difficulty='Easy', category='字符串',
    author='yiduobo', technique='从头找最大相同前缀 p',
    code='''
class Solution(object):
    def findMinimumOperations(self, s1, s2, s3):

        p = 0
        while p < len(s1) and p < len(s2) and p < len(s3) and s1[p] == s2[p] == s3[p]:
            p += 1
        
        if p == 0:
            return -1
        else:
            return len(s1) + len(s2) + len(s3) - p * 3
''',
    call='Solution().findMinimumOperations("abcd", "abce", "abd")',
    expect=5,
    views=[
        dict(type='string', var='s1', label='s1', pointers={'p': 'blue'}, color=_col, h=150),
        dict(type='string', var='s2', label='s2', color=_col, h=130),
        dict(type='string', var='s3', label='s3', color=_col, h=130),
        dict(type='text', fn=lambda S: f"保留前缀长度 `p` = =={S['p']}==" if 'p' in S else '', h=70),
    ],
    watch=[('p', 'p', 'blue')],
    captions={
        'p = 0': '`p` 是三个字符串长度为 p 的前缀相同时的最大 p，从 0 开始试',
        'while p < len(s1)': lambda S, B, r: (f"`p = {S.p}` 没越界，且三个串第 {S.p} 位都是 `{S.s1[S.p]}` → ==继续=="
                                              if (S.p < len(S.s1) and S.p < len(S.s2) and S.p < len(S.s3) and S.s1[S.p] == S.s2[S.p] == S.s3[S.p])
                                              else f"`p = {S.p}`：越界或第 {S.p} 位不全相同 → 前缀到头了，退出循环"),
        'p += 1': '这一位三个串相同，前缀可以再长一位：`p` = =={p}==',
        'if p == 0': lambda S, B, r: ('`p = 0`：首字母就不同 → 无论删多少都不可能相等' if S.p == 0 else f'`p = {S.p} > 0`：可以删到长度 p'),
        'return -1': '返回 ==-1==',
        'return len': '每个串都要删到长度 p：`{len(s1)} + {len(s2)} + {len(s3)} − {p} × 3` = =={ret}==',
    },
    cards=dict(
        one_liner='删除只能从后往前 → 留下的必是前缀',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次可以删掉长度 ≥ 2 的字符串的最右字符，求让三个字符串相等的最少操作数',
                 '示例：`"dac" "bac" "cac"` → `-1`（首字母不同）',
                 '本视频：`"abcd" "abce" "abd"` → `5`'],
        quote='题目中的删除操作只能从后向前进行，那么保留下来的字符串一定是原字符串的前缀。换言之，题目就是要找到最大的p，使得三个字符串长度为p的前缀相同。',
        quote_src='—— yiduobo 题解原文',
        idea=['删除只能删最右边，所以剩下的必然是前缀', '问题变成：找最大的 `p`，三串前 `p` 位都一样',
              '`p = 0` 返回 `-1`；否则每个串删到长度 `p`，共删 `总长 − 3p`'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`while` 条件先判断三个长度再比字符，避免下标越界',
                 '`p = 0` 单独返回 `-1`',
                 '原文已是 Python 3 可运行写法，未作修改'],
    ),
)
