KEY = 'TTFTF'
K = 1


def _live(S):
    return 'char' in S and 'l' in S and 'r' in S


def _color(S, i, v):
    if not _live(S):
        return None
    if S['l'] <= i <= S['r']:
        return 'green' if v == S['char'] else 'orange'
    return None


def _dim(S, i, v):
    return _live(S) and not (S['l'] <= i <= S['r'])


def _top(S):
    if not _live(S):
        return '分别求「全变 T」和「全变 F」的最长区间，取较大值'
    c = S['char']
    return (f"目标字符 char = =={c}==：区间 `[{S['l']}, {S['r']}]` 里不是 {c} 的有 `cnt = {S['cnt']}` 个"
            f"（最多 `k = {K}`）")


def _if_cnt(S, B, ret):
    if S.cnt > S.k:
        return f'`cnt = {S.cnt} > k = {S.k}`：改不过来了，要把==一个非 {S.char} 字符==踢出区间'
    return f'`cnt = {S.cnt} ≤ {S.k}`：把它改成 {S.char} 就行，l 不动'


def _skip(S, B, ret):
    l = S.l
    if l <= S.r and S.answerKey[l] == S.char:
        return f'`answerKey[{l}] = {S.char}` 和 char 一致，踢掉它没用 → l 继续右移'
    return f'`answerKey[{l}] = {S.answerKey[l]}` 不是 {S.char}：踢掉==这一个==就够了'


CONFIG = dict(
    num=2024, title='考试的最大困扰度', difficulty='Medium', category='滑动窗口与双指针',
    author='yiduobo', technique='分别枚举目标字符 + 双指针',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def maxConsecutiveAnswers(self, answerKey, k):

        n = len(answerKey)

        def check(char):
            l = 0
            r = -1
            cnt = 0
            res = 0
            while r + 1 < n:
                r += 1
                if answerKey[r] != char:
                    cnt += 1
                    if cnt > k:
                        while l <= r and answerKey[l] == char:
                            l += 1
                        cnt -= 1
                        l += 1

                res = max(res, r - l + 1)

            return res

        return max(check('T'), check('F'))
''',
    call=f'Solution().maxConsecutiveAnswers({KEY!r}, {K})',
    expect=4,
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='answerKey', label='answerKey（框 = 区间 [l, r]；绿 = 等于 char，橙 = 要修改的）',
             pointers={'l': 'blue', 'r': 'pink'}, window=('l', 'r'), color=_color, dim=_dim, cell=110, h=300),
        dict(type='calls', h=120),
    ],
    watch=[('char', 'char', 'purple'), ('l', 'l', 'blue'), ('r', 'r', 'pink'), ('cnt', 'cnt', 'orange'), ('res', 'res', 'green')],
    captions={
        'n = len': '`n = {n}`',
        'def check': '`check(char)`：把区间都变成 char 时，最长能有多长',
        'l = 0': '开始求 char = =={char}== 的答案：`l = 0, r = -1`（空区间），`cnt` 记区间里==不是 char== 的个数',
        'r = -1': '`r = -1`：区间先为空',
        'cnt = 0': '`cnt`：区间里==不是 char== 的字符数',
        'res = 0': '`res = 0`',
        'while r + 1 < n': lambda S, B, ret: (f'r 右移一位，`answerKey[{S.r + 1}] = {S.answerKey[S.r + 1]}` 加入区间' if S.r + 1 < S.n else f'扫描完毕，char = {S.char} 时最长 `{S.res}`'),
        'r += 1': '`answerKey[{r}] = {answerKey[r]}` 加入区间',
        'if answerKey[r] != char': lambda S, B, ret: (f'`{S.answerKey[S.r]} ≠ {S.char}`：需要修改，计入 cnt' if S.answerKey[S.r] != S.char
                                                    else f'`{S.answerKey[S.r]} == {S.char}`：情况 1，l 不需要变动'),
        'cnt += 1': '`cnt` → {cnt}',
        'if cnt > k': _if_cnt,
        'while l <= r and': _skip,
        'l += 1': '`l` → {l}',
        'cnt -= 1': '踢掉一个非 {char} 字符：`cnt` → {cnt}',
        'res = max': '区间 `[{l}, {r}]` 长 `{r - l + 1}`：`res = max({B.res}, {r - l + 1})` = =={res}==',
        'return res': '`check({char!r})` 返回 =={ret}==',
        'return max(check': lambda S, B, ret: ('分别调用 `check(\'T\')`、`check(\'F\')`，取较大值' if ret is None
                                               else f'`max(check(\'T\'), check(\'F\'))` = =={ret}=='),
    },
    skip=['r = -1', 'cnt = 0', 'res = 0', 'r += 1'],
    max_steps=80,
    cards=dict(
        one_liner='先定下要连成 T 还是 F，再用双指针找最长区间',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字符串 `answerKey` 只含 T/F，最多修改 `k` 次',
                 '求修改后==最长的连续相同字符==个数',
                 '示例：`"TFFT", k = 1` → `3`；本视频 `"TTFTF", k = 1` → `4`'],
        quote='若新加入的字符与char不一致，且此时区间l到r之间不是char的字符已经达到了k + 1个，此时就需要==不断将l向右移动==，直到……有某个不是char的字符因为l的向右移动被排除出了区间',
        quote_src='—— yiduobo 题解原文',
        idea=['固定目标字符 char，区间里非 char 的个数 `cnt` 不能超过 k',
              '超了就让 l 跳过所有 char，==恰好踢出一个==非 char 字符',
              '`check(\'T\')` 和 `check(\'F\')` 取较大值'],
        summary=['时间 `O(n)`：两趟扫描，l、r 都只右移',
                 'r 从 -1 开始，每轮先 `r += 1` 再处理新字符',
                 '内层 while 停在非 char 字符上，之后还要再 `l += 1` 把它踢出',
                 '原文为 Python 2 风格（`class Solution(object)`），代码未改动',
                 '对比灵神：灵神一趟同时统计 T、F；这里拆成两次 check 更直观'],
    ),
)
