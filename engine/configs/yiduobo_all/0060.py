def _cand(S):
    pos = S.get('pos')
    if pos is None:
        return '`candidate_list` = 还没选的数字，从小到大排好'
    off = S.get('offset')
    if off is None or S['_line'] in (9, 10):
        return f'`pos = {pos}`：现在要定第 {len(S["res"]) + 1} 位，后面还剩 `{pos}` 位，每个开头对应 `{S["factor_list"][pos]}` 种排列'
    return f'`offset = {off}`：当前位取剩余数字里 ==第 {off + 1} 小== 的，即 `{S["candidate_list"][off]}`'


CONFIG = dict(
    num=60, title='第k个排列', difficulty='Hard', category='数学算法',
    author='yiduobo', technique='康托展开 · 逐位定数',
    tags=['常用数据结构'],
    code='''
class Solution(object):
    def getPermutation(self, n, k):

        factor_list = [1, 1, 2, 6, 24, 120, 720, 5040, 40320]
        candidate_list = [str(index) for index in range(1, n+1)]
        res = []
        
        k -= 1
        for pos in range(n - 1, 0, -1):
            offset = k // factor_list[pos]
            k %= factor_list[pos]
            res.append(str(candidate_list[offset]))
            for index in range(offset, pos):
                candidate_list[index] = candidate_list[index + 1]

        res.append(candidate_list[0])

        return ''.join(res)
''',
    call='Solution().getPermutation(4, 9)',
    expect='2314',
    views=[
        dict(type='array', var='factor_list', label='factor_list（阶乘表：pos! 种排列）', pointers={'pos': 'blue'}, cell=84, h=190),
        dict(type='array', var='candidate_list', label='candidate_list（剩余数字，灰 = 空位）', pointers={'offset': 'pink'}, cell=90,
             dim=lambda S, i, v: S.get('pos') is not None and i > S['pos'], h=190),
        dict(type='array', var='res', label='res（已确定的前几位）', cell=90, h=150),
        dict(type='text', fn=_cand, size=28, h=90),
    ],
    watch=[('k', 'k', 'yellow'), ('pos', 'pos', 'blue'), ('offset', 'offset', 'pink'), ('res', "''.join(res)", 'green')],
    captions={
        'factor_list = ': '`factor_list[i] = i!`：后面还剩 `i` 位时，每个开头对应 `i!` 种排列',
        'candidate_list = ': '`candidate_list = {candidate_list}`：还没用过的数字，从小到大',
        'k -= 1': '第 k 个改成从 0 开始数：`k = {k}`，这样 `k // 阶乘` 才刚好是下标',
        'for pos in': lambda S, B, r: ('`pos` 已经是 1：只剩一个数字，循环结束' if B.get('pos') == S['pos'] else f'`pos = {S["pos"]}`：定下一位，后面还剩 `{S["pos"]}` 位'),
        'offset = k': '`{B.k} // {factor_list[pos]}` = =={offset}==：商不是数字本身，而是它在剩余数字里排第几小（下标）',
        'k %= factor_list': '余数留给后面的位：`k = {B.k} % {factor_list[pos]} = {k}`',
        'res.append(str(': '取出 `candidate_list[{offset}]` = ==`{candidate_list[offset]}`==，作为这一位',
        'for index in range': '`range({offset}, {pos})`：把下标 `{offset}` 之后的数字左移一格，补上刚用掉的空位',
        'candidate_list[index] =': '`candidate_list[{index}] = candidate_list[{index + 1}]` → `{candidate_list[index]}`',
        'res.append(candidate_list[0])': '只剩最后一个数字了，直接接在末尾：`{candidate_list[0]}`',
        'return': '拼起来：==`{ret}`==',
    },
    cards=dict(
        one_liner='用阶乘定每一位：k 除以 (n−1)! 的商，就是它在剩余数字里排第几小',
        complexity='时间 `O(n²)`（每位要左移剩余数字），空间 `O(n)`',
        problem=['数字 `1..n` 的全排列按字典序排好，求第 `k` 个排列',
                 '示例：`n = 3, k = 3` → `"213"`',
                 '本视频：`n = 4, k = 9` → `"2314"`'],
        quote='这里得到的商代表的并不是当前这一位应该是多少，而是当前这一位在剩余数字中是第几小的。',
        quote_src='—— yiduobo 题解原文',
        idea=['以 1 开头的排列有 `(n-1)!` 个，以 2 开头的也一样 → 用 k 除以 `(n-1)!` 定第一位',
              '余数 `k % (n-1)!` 就是剩下 `n-1` 个数里的名次，如法炮制往后找',
              '用「剩余数字」数组 + 左移删除，模拟从小到大第几个'],
        summary=['时间 `O(n²)`，空间 `O(n)`；题目 `n ≤ 9`，阶乘表只开到 `8!`',
                 '易错：先 `k -= 1` 变成 0 起点，否则整除后下标会错位',
                 '易错：商是「剩余数字里第几小」，不是数字本身',
                 '原文为 Python 2 写法，整数除法 `/` 已改为 `//`',
                 '最后一位不用算：循环到 `pos = 1` 停，剩下的唯一数字直接接上'],
    ),
)
