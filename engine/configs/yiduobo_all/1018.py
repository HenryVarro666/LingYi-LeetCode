def _txt(S):
    if 'num' not in S or 'now' not in S:
        return ''
    return f"`now = (上一个余数 × 2 + {S['num']}) % 5` → 余数 =={S['now']}=="


def _cur(S):
    if 'res' not in S:
        return None
    k = len(S['res']) - (1 if S['_line'] == 9 else 0)
    return k if 0 <= k < len(S['A']) else None


CONFIG = dict(
    num=1018, title='可被 5 整除的二进制前缀', difficulty='Easy', category='数学算法',
    author='yiduobo', technique='递推 N_i = 2·N_{i-1} + A[i]，只传余数',
    tags=['数学算法', '难度分 1376'],
    code='''
class Solution(object):
    def prefixesDivBy5(self, A):

        res = []
        now = 0

        for num in A:
            now = (now * 2 + num) % 5
            res.append(now == 0)
        
        return res
''',
    call='Solution().prefixesDivBy5([0, 1, 1, 0, 1, 0, 1, 1])',
    expect=[True, False, False, False, False, False, False, False],
    views=[
        dict(type='array', var='A', label='A（二进制位）', h=170, pointers={_cur: 'blue'}, pointer_labels={_cur: 'num'},
             color=lambda S, i, v: 'blue' if i == _cur(S) else None),
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='res', label='res（True = 余数为 0）', h=170,
             color=lambda S, i, v: 'green' if v is True else None),
    ],
    watch=[('num', 'num', 'blue'), ('now', 'now', 'yellow')],
    captions={
        'for num in A': lambda S, B, r: ('`A` 扫完了' if len(S.res) == len(S.A) else f'取下一位：`num = {S.num}`'),
        'res = []': '`res` 收集每个前缀的判断结果',
        'now = 0': '`now` 是当前前缀对 5 的余数，空前缀为 0',
        'now = (now * 2': '`N_i = 2·N_(i-1) + A[i]`，只关心余数：`({B.now} × 2 + {num}) % 5` = =={now}==',
        'res.append': '`now = {now}`，{"为 0 → 追加 ==True==" if now == 0 else "不为 0 → 追加 False"}',
        'return res': '遍历结束，返回 `res`',
    },
    cards=dict(
        one_liner='N_i = 2·N_{i-1} + A[i]，余数也能这样递推',
        complexity='时间 `O(n)`，空间 `O(1)`（不计结果）',
        problem=['`A` 是 0/1 数组，`N_i` 是前缀 `A[0..i]` 对应的二进制数',
                 '`N_i` 能被 5 整除则 `answer[i]` 为 true',
                 '示例：`[0,1,1]` → `[true,false,false]`；本视频用 `[0,1,1,0,1,0,1,1]`'],
        quote='可以从头到尾遍历A，然后每次使用当前的A[i]以及N_i-1 % k的结果来求出N_i % k，并使用这个余数来更新答案。',
        quote_src='—— yiduobo 题解原文',
        idea=['新前缀就是旧前缀乘 2 再加 `A[i]`：`N_i = 2·N_(i-1) + A[i]`',
              '两边同时对 5 取模，右边只需要旧余数和 `A[i]`',
              '所以只带一个余数 `now` 往后扫，余数为 0 就是答案 true'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：不要先算出完整的大数再取模，每步都要 `% 5`',
                 '余数只会是 0~4，所以 `now` 永远很小',
                 '对比灵神：灵神用 `x << 1 | bit` 写法，yiduobo 用 `now * 2 + num`，本质相同',
                 '原文签名参数名为 `A`，代码未改动'],
    ),
)
