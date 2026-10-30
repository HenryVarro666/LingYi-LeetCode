NUMS = [10, 3, 8, 9, 4]
SHORT = {'Gold Medal': '金牌', 'Silver Medal': '银牌', 'Bronze Medal': '铜牌'}


def _cur(S):
    """第二个循环里当前 num 的下标（示例分数互不相同）"""
    if S.get('_line', 0) < 8 or 'num' not in S:
        return None
    return S['nums'].index(S['num'])


def _for1(S, B, ret):
    if B.get('index') != S.get('index') or 'index' not in B:
        return f'从高到低第 `{S.index + 1}` 名是 `{S.score}` 分'
    return '名次表建好了'


def _for2(S, B, ret):
    if B.get('num') != S.get('num') or 'num' not in B:
        return f'按原顺序取 `num = {S.num}`，查表：第 `{S.score_dict[S.num]}` 名'
    return '每个人的名次都输出了'


def _rank_if(k, word):
    def f(S, B, ret):
        r = S.score_dict[S.num]
        if r == k:
            return f'第 {k} 名 → =={word}=='
        return f'名次 `{r}` ≠ {k}'
    return f


CONFIG = dict(
    num=506, title='相对名次', difficulty='Easy', category='哈希',
    author='yiduobo', technique='排序 + 分数→名次字典',
    tags=['字节30天'],
    code='''
class Solution(object):
    def findRelativeRanks(self, nums):
        score_dict = {}
        for index, score in enumerate(sorted(nums, reverse=True)):
            score_dict[score] = index + 1

        res = []
        for num in nums:
            if score_dict[num] == 1:
                res.append('Gold Medal')
            elif score_dict[num] == 2:
                res.append('Silver Medal')
            elif score_dict[num] == 3:
                res.append('Bronze Medal')
            else:
                res.append(str(score_dict[num]))

        return res
''',
    call=f'Solution().findRelativeRanks({NUMS})',
    expect=['Gold Medal', '5', 'Bronze Medal', 'Silver Medal', '4'],
    views=[
        dict(type='array', var=lambda S: sorted(S['nums'], reverse=True) if 'score_dict' in S else None,
             label='sorted(nums, reverse=True)（从高到低；蓝 = 当前 index，绿 = 已记名次）', cell=96,
             color=lambda S, i, v: 'blue' if S.get('_line') in (4, 5) and i == S.get('index') and v not in S.get('score_dict', {})
             else ('green' if v in S.get('score_dict', {}) else None)),
        dict(type='map', var='score_dict', label='score_dict（分数 → 名次）', h=120, fmt=lambda k, v: f'{k} → 第{v}名'),
        dict(type='array', var='nums', label='nums（原顺序）', cell=96,
             pointers={'nums.index(num) if _line >= 8 else None': 'pink'},
             pointer_labels={'nums.index(num) if _line >= 8 else None': 'num'},
             color=lambda S, i, v: ('green' if _cur(S) is not None and i < len(S.get('res', [])) else None)),
        dict(type='array', var=lambda S: [SHORT.get(x, x) for x in S['res']] if 'res' in S else None,
             label='res（前三名的奖牌简写为 金牌 / 银牌 / 铜牌）', cell=96, min_slots=5,
             color=lambda S, i, v: {'金牌': 'yellow', '银牌': 'cyan', '铜牌': 'orange'}.get(v)),
    ],
    watch=[('index', lambda S: S.get('index') if S.get('_line') in (4, 5) else None, 'blue'),
           ('score', lambda S: S.get('score') if S.get('_line') in (4, 5) else None), ('num', 'num', 'pink'),
           ('score_dict[num]', lambda S: S['score_dict'][S['num']] if 'num' in S else None, 'green')],
    captions={
        'score_dict = {}': '`score_dict` 记录每个分数对应的名次',
        'for index, score in': _for1,
        'score_dict[score] = index + 1': '下标从 0 开始，名次从 1 开始：`score_dict[{score}] = {index} + 1 = {index + 1}`',
        'res = []': '再按==原顺序==遍历，查表得到每个人的名次',
        'for num in nums': _for2,
        'if score_dict[num] == 1': _rank_if(1, '金牌 Gold Medal'),
        "res.append('Gold Medal')": '`{num}` 分第一名：`Gold Medal`',
        'elif score_dict[num] == 2': _rank_if(2, '银牌 Silver Medal'),
        "res.append('Silver Medal')": '`{num}` 分第二名：`Silver Medal`',
        'elif score_dict[num] == 3': _rank_if(3, '铜牌 Bronze Medal'),
        "res.append('Bronze Medal')": '`{num}` 分第三名：`Bronze Medal`',
        'res.append(str(': '第 4 名及以后输出名次的==字符串==：`"{score_dict[num]}"`',
        'return res': '返回 `res`',
    },
    cards=dict(
        one_liner='排序得到名次，用字典记下“分数 → 名次”，再按原顺序查表',
        complexity='时间 `O(n log n)`，空间 `O(n)`',
        problem=['`score[i]` 是第 `i` 位运动员的得分，==所有得分互不相同==',
                 '前三名分别输出 `"Gold Medal"`、`"Silver Medal"`、`"Bronze Medal"`',
                 '其余输出名次的字符串，按原顺序返回',
                 '示例：`[10,3,8,9,4]` → `["Gold Medal","5","Bronze Medal","Silver Medal","4"]`'],
        quote='比较基础的题目，按照分数从大到小排序后输出即可。',
        quote_src='—— yiduobo 知乎题解',
        idea=['`sorted(nums, reverse=True)`：下标 `index` 的分数排第 `index + 1` 名',
              '分数互不相同 → 可以用分数当 key 建 `score_dict`',
              '再按原顺序遍历 `nums`，前三名换成奖牌，其余转成字符串'],
        summary=['时间 `O(n log n)`（排序），空间 `O(n)`（字典 + 结果）',
                 '易错：名次从 1 开始，`index + 1`；第 4 名起要 `str()` 转成字符串',
                 '能用分数当 key，是因为题目保证==得分互不相同==',
                 '原文为 Python 2 风格，只删去了类型说明文档字符串'],
    ),
)
