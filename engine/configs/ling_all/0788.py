_D = (0, 0, 1, -1, -1, 1, 1, -1, 0, 1)


def _I(S):
    i = S['_inner'].get('i')
    return i if i is not None and i < len(S['s']) else None


def _info(S):
    i = S['_inner'].get('i')
    if i is None:
        return '`f(i, has_diff, is_limit)`：从第 i 位开始填，有几种方案能凑成好数'
    s = S['s']
    hd = S['_inner'].get('has_diff')
    il = S['_inner'].get('is_limit')
    if i >= len(s):
        return f'填完了：`has_diff = {hd}` → ==' + ('是好数，计 1' if hd else '全是 0/1/8，旋转后不变，计 0') + '=='
    up = int(s[i]) if il else 9
    return f'第 {i} 位：前面{"==已含==" if hd else "还没有"} 2/5/6/9；{"==贴着上界==" if il else "不受上界限制"}，最多填 `{up}`'


CONFIG = dict(
    num=788, title='旋转数字', difficulty='Medium', category='动态规划',
    author='灵茶山艾府', technique='数位 DP（上界模板）',
    tags=['灵神题单', '数位 DP'],
    code='''
DIFFS = (0, 0, 1, -1, -1, 1, 1, -1, 0, 1)

class Solution:
    def rotatedDigits(self, n: int) -> int:
        s = str(n)
        @cache
        def f(i: int, has_diff: bool, is_limit: bool) -> int:
            if i == len(s):
                return has_diff  # 只有包含 2/5/6/9 才算一个好数
            res = 0
            up = int(s[i]) if is_limit else 9
            for d in range(0, up + 1):  # 枚举要填入的数字 d
                if DIFFS[d] != -1:  # d 不是 3/4/7
                    res += f(i + 1, has_diff or DIFFS[d], is_limit and d == up)
            return res
        return f(0, False, True)
''',
    call='Solution().rotatedDigits(25)',
    expect=12,
    views=[
        dict(type='string', var='s', label='s = str(n)（框 = 当前要填的位）', cell=110, h=210,
             pointers={_I: 'blue'}, pointer_labels={_I: 'i'}),
        dict(type='text', fn=_info, size=26, h=70),
        dict(type='calls', h=250),
    ],
    watch=[('i', lambda S: S['_inner'].get('i'), 'blue'), ('d', lambda S: S['_inner'].get('d'), 'pink'),
           ('res', lambda S: S['_inner'].get('res'), 'green')],
    max_steps=110,
    skip=['for d in range', 'res = 0'],
    captions={
        'DIFFS = ': '`DIFFS[d]`：0/1/8 旋转后不变记 `0`；2/5/6/9 变成别的数记 `1`；3/4/7 无效记 `-1`',
        's = str(n)': '把 `n = {n}` 转成字符串 `s = "{s}"`，逐位构造不超过它的数',
        'if i == len(s)': lambda S, B, r: ('填完了 → 看 `has_diff`' if S.i == len(S.s)
                                           else f'第 `{S.i}` 位还没填完，继续枚举'),
        'return has_diff': '填完：`has_diff = {bool(has_diff)}` → ==' + '至少有一位变了才是好数==，返回 `{int(has_diff)}`',
        'up = int': lambda S, B, r: (f'受上界约束：这一位最多填 `s[{S.i}] = {S.up}`' if S.is_limit
                                     else '不受约束：这一位随便填，最多 `9`'),
        'if DIFFS[d] != -1': lambda S, B, r: (f'试填 `{S.d}`：`DIFFS[{S.d}] = -1` → ==3/4/7 旋转后无效==，跳过' if _D[S.d] == -1
                                              else f'试填 `{S.d}`：`DIFFS[{S.d}] = {_D[S.d]}` 合法；已累计 `res = {S.res}`'),
        'res += f(': lambda S, B, r: (f'填 `{B.d}` 后进入下一位：`has_diff = {bool(B.has_diff or _D[B.d])}`，'
                                      f'`is_limit = {B.is_limit and B.d == B.up}`'),
        'return res': '这一层汇总完毕，返回 `{ret}` 种',
        'return f(0': '从最高位出发：`has_diff = False`，`is_limit = True`（受 n 约束）→ 最终答案 ==12==',
    },
    cards=dict(
        one_liner='逐位填数：不含 3/4/7，且至少含一个 2/5/6/9',
        complexity='时间 `O(mD)`，空间 `O(m)`（m 为位数）',
        problem=['一个数每位旋转 180 度后仍是有效数字，且和原数不同，就是好数',
                 '0/1/8 旋转不变，2↔5，6↔9，其余无效',
                 '示例：`N = 10` → `4`（2、5、6、9）；演示用 `N = 25` → `12`'],
        quote='根据题意，好数中不能有 3,4,7，且至少包含 2,5,6,9 中的一个。……由于前导零对答案无影响，isNum 可以省略。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`f(i, has_diff, is_limit)`：构造第 i 位及之后的合法方案数',
              '`has_diff` 记录前面是否出现过 2/5/6/9，`is_limit` 记录是否还贴着 n',
              '`DIFFS[d] == -1` 的数字直接跳过；到末尾只有 `has_diff` 为真才计 1'],
        summary=['时间 `O(mD)`：状态 `O(m)` 个 × 每个枚举 `D = 10` 个数字',
                 '前导零不影响答案，所以 `isNum` 参数可省略',
                 '易错：必须==至少一个== 2/5/6/9，否则像 1、8、10 旋转后不变',
                 '题解还提到：Java/C++/Go 只需记忆化 `(i, has_diff)`，且仅在不受限时缓存'],
    ),
)
