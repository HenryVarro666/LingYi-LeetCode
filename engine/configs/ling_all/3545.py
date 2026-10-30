CONFIG = dict(
    num=3545, title='不同字符数量最多为 K 时的最少删除数', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='保留次数最大的 k 个字母',
    tags=['贪心与思维', '从最小/最大开始贪心', '难度分 1211'],
    code='''
class Solution:
    def minDeletion(self, s: str, k: int) -> int:
        cnt = sorted(Counter(s).values())
        return sum(cnt[:-k])  # 保留出现次数最大的 k 个字母
''',
    call='Solution().minDeletion("aabcbbd", 2)',
    expect=2,
    views=[
        dict(type='string', var='s', label='s', h=170),
        dict(type='array', var='cnt', label='cnt：各字母出现次数（从小到大）', h=260,
             color=lambda S, i, v: ('green' if 'cnt' in S and i >= len(S['cnt']) - S['k'] else 'red'),
             dim=lambda S, i, v: False),
        dict(type='text', size=32, h=120,
             fn=lambda S: (f"保留最大的 `{S['k']}` 个：{sum(S['cnt'][-S['k']:])}，删掉其余：==`{sum(S['cnt'][:-S['k']])}`==" if 'cnt' in S else '')),
    ],
    watch=[('k', 'k', 'blue'), ('cnt', 'cnt', 'cyan')],
    captions={
        'cnt = sorted': '统计每个字母的出现次数并排序：`cnt = {cnt}`，有 `{len(cnt)}` 种字母',
        'return sum': '字母种类要降到 `{k}` 种：==删掉最少的 `{len(cnt)-k}` 种==，即 `cnt[:-{k}] = {cnt[:-k]}`，求和 =={ret}==',
    },
    cards=dict(
        one_liner='先扔出现次数最少的字母，保留次数最大的 k 个',
        complexity='时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
        problem=['删除一些字符，让剩下的不同字符数 `<= k`，求最少删几个',
                 '删一个字母就得删光它的所有出现',
                 '本视频：`s="aabcbbd"`，`k=2` → `2`'],
        quote='优先去掉出现次数少的字母，也就是去掉出现次数前 26-k 小的字母。或者说，保留出现次数最大的 k 个字母。',
        quote_src='—— 灵茶山艾府题解',
        idea=['删字母要整种删，所以按「种」来看，每种代价是它的出现次数',
              '要删掉若干种、总代价最小 → 删次数最少的那些',
              '排序后 `cnt[:-k]` 就是要删的，求和即答案'],
        after=[dict(heading='另一种写法：长 26 的数组', lines=['`cnt = [0] * 26`，逐个字符 `cnt[ord(b) - ord(\'a\')] += 1`', '`cnt.sort()` 后 `sum(cnt[:-k])`', '出现次数为 0 的字母排在最前，正好被「删掉」，不影响答案'])],
        summary=['时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
                 '`cnt[:-k]`：种类数不超过 k 时切片为空，和为 0，不需要特判',
                 '`Counter` 里没出现的字母不计，等价于原文把次数 0 的也算上',
                 '题解另给了长 26 的数组写法：`cnt` 数组 + 排序，思路相同'],
    ),
)
