C0 = 'a12b1a3c2'


def _pq(S):
    return S.get('p'), S.get('q')


def _color(S, i, v):
    p, q = _pq(S)
    if p is None or p >= len(S['compressed']):
        return None
    if i == p:
        return 'blue'
    if q is not None and p < i < q:
        return 'green'
    return None


def _dim(S, i, v):
    p = S.get('p')
    return p is not None and i < p


def _top(S):
    c = S['compressed']
    p, q = _pq(S)
    if p is None:
        return '格式：字符 + 频率，要把相同字符的频率加起来，再按字典序输出'
    if p >= len(c):
        return '整串都拆完了 → 按字典序拼出答案'
    if q is None or 'char' not in S:
        return f"新的一段从 `p = {p}` 开始：`compressed[p] = '{c[p]}'` 一定是字符"
    return f"字符 `'{c[p]}'`，频率 `compressed[{p+1}:{q}] = '{c[p+1:q]}'`"


CONFIG = dict(
    num=3167, title='字符串的更好压缩', difficulty='Medium', category='字符串',
    author='yiduobo', technique='双指针分段 + 哈希表累加',
    tags=[],
    code='''
class Solution(object):
    def betterCompression(self, compressed):
        freq = Counter()
        p = 0
        while p < len(compressed):
            char = compressed[p]
            q = p + 1
            while q < len(compressed) and '0' <= compressed[q] <= '9':
                q += 1

            freq[char] += int(compressed[p + 1 : q])
            p = q

        return ''.join([char + str(freq[char]) for char in sorted(freq.keys())])
''',
    call=f'Solution().betterCompression({C0!r})',
    expect='a15b1c2',
    views=[
        dict(type='text', fn=_top, size=28, h=80),
        dict(type='string', var='compressed', label='compressed（蓝 = p 处字符，绿 = 它的频率数字）', cell=84, h=210,
             pointers={'p': 'blue', 'q': 'pink'},
             dim=_dim, color=_color),
        dict(type='map', var='freq', label='freq（每种字符累计出现次数）', fmt=lambda k, v: f"'{k}': {v}", h=170, font=34),
    ],
    watch=[('p', 'p', 'blue'), ('q', 'q', 'pink'), ('char', 'char', 'cyan')],
    captions={
        'freq = Counter()': '`freq` 统计每种字符在原串里出现的总次数',
        'p = 0': '`p` 是当前一段的起点，`compressed[p]` 一定是那个字符',
        'while p < len(compressed)': lambda S, B, ret: (f'`p = {S.p} < {len(S.compressed)}`：还有一段没拆' if S.p < len(S.compressed)
                                                        else f'`p = {S.p}` 到达末尾：所有段都累加完了'),
        'char = compressed[p]': "这一段的字符：`compressed[{p}]` = =={char!r}==",
        'q = p + 1': '`q` 从字符后一位出发，向后找频率数字的结尾',
        'while q < len(compressed) and': lambda S, B, ret: (
            f"`compressed[{S.q}] = {S.compressed[S.q]!r}` 是数字 → 频率还没结束" if S.q < len(S.compressed) and S.compressed[S.q].isdigit()
            else (f"`q = {S.q}` 已到末尾 → 频率到此为止" if S.q >= len(S.compressed)
                  else f"`compressed[{S.q}] = {S.compressed[S.q]!r}` 不是数字 → 下一段的字符，频率结束")),
        'q += 1': '数字继续，`q` → {q}',
        'freq[char] +=': '频率是 `compressed[{p+1}:{q}] = {compressed[p+1:q]!r}`（可能多位）→ `freq[{char!r}]` 累加到 =={freq[char]}==',
        'p = q': '下一段从 `q` 开始：`p` → {p}',
        'return': '按字典序（`sorted(freq.keys())`）把字符和次数拼起来 = =={ret!r}==',
    },
    cards=dict(
        one_liner='拆出每段（字符，频率），哈希表累加，再按字典序拼接',
        complexity='时间 `O(n + k log k)`，空间 `O(k)`，`k` 为字符种数',
        problem=['`compressed` 由“字符 + 频率”依次拼成，如 `"a3b1a1c2"` 表示 `"aaabacc"`',
                 '重新压缩：每种字符只出现一次（频率为总次数），并按字典序排好',
                 '示例：`"a3b1a1c2"` → `"a4b1c2"`',
                 '本视频：`"a12b1a3c2"` → `"a15b1c2"`'],
        quote='利用双指针一趟遍历，将每一组(字符，频率)都分离出来，然后使用哈希表将每种字符的频率累加起来，得到原字符串中每种字符出现的次数。',
        quote_src='—— yiduobo 题解原文',
        idea=['段起点 `p`：`compressed[p]` 一定是字符；`q` 从 `p + 1` 向后跳过所有数字',
              '`compressed[p + 1 : q]` 就是频率，`int()` 后累加进 `freq`，然后 `p = q`',
              '得到 `freq` 后，按字典序遍历，字符接上次数即为答案'],
        result='a 共 12 + 3 = 15 次，b 1 次，c 2 次 → `"a15b1c2"` ✓',
        summary=['时间 `O(n + k log k)`，空间 `O(k)`',
                 '易错：频率可能是==多位数==（如 `12`），所以要用 `q` 一路往后找，不能只取一位',
                 '易错：同一字符可能出现多段，要累加，不能覆盖',
                 '原文为 Python 2 风格，只删去 def 后的空行，代码无需其他修改'],
    ),
)
