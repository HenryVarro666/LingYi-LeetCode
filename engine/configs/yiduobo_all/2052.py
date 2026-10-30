SENT = 'i love leetcode'


def _words(S):
    ws = SENT.split(' ')
    return '单词：' + '  '.join(f'`{w}`={len(w)}' for w in ws)


def _v_color(S, k, v):
    if 'i' not in S:
        return None
    i = S['i']
    if 'j' in S and S.get('_line', 0) >= 12 and S['j'] < S['i'] and S['j'] <= k <= i:
        return 'yellow' if k in (S['j'], i) else 'blue'
    if k == i:
        return 'yellow'
    return None


def _f_color(S, k, v):
    i = S.get('i')
    if i is not None and k == len(S['f']) - 1 and S.get('_line', 0) in (11, 12, 15, 16):
        return 'yellow'
    return None


CONFIG = dict(
    num=2052, title='将句子分隔成行的最低成本', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='划分型 DP · 后缀和枚举上一行',
    tags=['灵神题单·动态规划'],
    code='''
class Solution(object):
    def minimumCost(self, sentence, k):

        v = [len(word) for word in sentence.split(' ')]
        f = [0]
        n = len(v)
        for i in range(n - 1):
            f.append(f[-1] + (k - v[i]) ** 2)
            now = v[i]
            for j in range(i - 1, -1, -1):
                now += v[j] + 1
                if now > k:
                    break
                f[-1] = min(f[-1], f[j] + (k - now) ** 2)
        
        res = f[-1]
        now = v[-1]
        for i in range(n - 2, -1, -1):
            now += v[i] + 1
            if now > k:
                break
            res = min(res, f[i])

        return res
''',
    call=f'Solution().minimumCost({SENT!r}, 12)',
    expect=36,
    max_steps=60,
    views=[
        dict(type='text', fn=_words, size=26, h=60),
        dict(type='array', var='v', label='v：每个单词的长度（黄 = 当前单词 / 这一行的首尾，蓝 = 行内）', h=240, cell=100,
             pointers={'j': 'pink', 'i': 'blue'}, color=_v_color),
        dict(type='array', var='f', label='f[t]：把前 t 个单词排好（含最后一行的成本）的最少成本', h=190, cell=100,
             color=_f_color),
        dict(type='text', fn=lambda S: (f"当前这一行：`now` = =={S['now']}== ≤ k = {S['k']}，成本 `({S['k']} − {S['now']})^2` = =={(S['k'] - S['now']) ** 2}==" if 'now' in S and S.get('_line', 0) in (11, 12, 13, 14) else ''), size=26, h=60),
    ],
    watch=[('k', 'k'), ('i', 'i', 'blue'), ('j', 'j', 'pink'), ('now', 'now', 'cyan'), ('res', 'res', 'green')],
    captions={
        'v = [len': '只关心单词长度：`v = {v}`',
        'f = [0]': '`f[0] = 0`：一个单词都没排，成本 0',
        'n = len': '`n = {n}` 个单词',
        'for i in range(n - 1)': lambda S, B, ret: (f'算前 `{S.i + 1}` 个单词的 `f`（最后一个单词留到最后单独处理）' if S.get('i') != B.get('i') or 'i' not in B else '前 n−1 个单词都算完'),
        'f.append': '先让单词 `{i}` ==单独成一行==：`f` 追加 `f[-2] + ({k} − {v[i]})^2` = =={f[-1]}==',
        'now = v[i]': '`now` = 当前这一行的宽度，目前只有单词 `{i}`：`{now}`',
        'for j in range(i - 1': lambda S, B, ret: (f'尝试把单词 `{S.j}` 也并进这一行（从后往前扩）' if S.get('j') != B.get('j') and S.get('j', 99) < S.i else '前面没有更多单词可以并入了'),
        'now += v[j] + 1': '并入单词 `{j}`：`now += {v[j]} + 1`（加一个空格）→ `{now}`',
        'if now > k': lambda S, B, ret: (f'`now = {S.now} > k = {S.k}`：==放不下了==，再往前更长，直接 break' if S.now > S.k else f'`now = {S.now} ≤ k = {S.k}`：这一行放得下'),
        'f[-1] = min(': lambda S, B, ret: f'这一行是单词 `{S.j}..{S.i}`，成本 `({S.k} − {S.now})^2` = {(S.k - S.now) ** 2}，加上 `f[{S.j}]` = {S.f[S.j]}：`f[-1]` = =={S.f[-1]}==',
        'res = f[-1]': '最后一行==不计成本==。先假设最后一个单词独占一行：`res = f[-1]` = =={res}==',
        'now = v[-1]': '从最后一个单词开始，向前看最后一行最多能装多少：`now = {now}`',
        'for i in range(n - 2': lambda S, B, ret: (f'最后一行能不能再并入单词 `{S.i}`？' if S.now == S.v[-1] or S.i != B.get('i') else '遍历结束'),
        'now += v[i] + 1': '最后一行加入单词 `{i}`：`now` → `{now}`',
        'res = min': '最后一行放得下，前面成本是 `f[{i}]` = {f[i]} → `res` = =={res}==',
        'return res': '最低成本 =={ret}==',
    },
    cards=dict(
        one_liner='成本只和单词长度有关：枚举上一行从哪个单词开始',
        complexity='时间 `O(n·k)`，空间 `O(n)`',
        problem=['句子拆成单词，按顺序排成若干行，每行总长（含空格）不超过 `k`',
                 '除最后一行外，每行成本 = `(k − 行长)^2`；最后一行不计成本',
                 '示例：`"i love leetcode"`，`k = 12` → `36`'],
        quote='题目中求解的问题与句子的内容无关，而是与分割单词的长度有关，因此可以先将字符串分割成单词，并将单词的长度收集起来得到长度数组v。',
        quote_src='—— yiduobo 题解原文',
        idea=['`f` 存“前面若干单词排好”的最小成本，新单词要么独占一行，要么与前面几个并成一行',
              '从 `i − 1` 往前枚举 `j`，用 `now` 累加行宽，超过 `k` 就停',
              '最后一行不计成本：再从后往前找最后一行的起点，取对应 `f` 的最小值'],
        result='`"i love"` 一行成本 36，`"leetcode"` 最后一行免费 → 36 ✓',
        summary=['时间 `O(n·k)`（每行至多并入 `k` 个单词），空间 `O(n)`',
                 '易错：最后一行不计成本，所以主循环只算到 `n − 2`',
                 '行宽 = 单词长度和 + 单词间空格数，所以每并入一个词要 `+ 1`',
                 '原文本身可在 Python 3 运行，未修改'],
    ),
)
