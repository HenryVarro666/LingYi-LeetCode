TRACK = '''
class KList(list):
    pass

class TList(list):  # 只用于动画：记录 for 循环当前遍历到的下标 k
    def __iter__(self):
        for k in range(len(self)):
            self.k = k
            yield list.__getitem__(self, k)
        self.k = None

    def __deepcopy__(self, memo):
        c = KList(list.copy(self))
        c.k = getattr(self, 'k', -1)
        return c
'''


def _k(S):
    if 'index' in S:
        return S['index']
    k = getattr(S.get('nums'), 'k', None)
    return k if isinstance(k, int) and k >= 0 else None


def _color(S, i, v):
    if 'x' in S and v == S['x'] and 'tot' in S:
        return 'green'
    return None


def _txt(S):
    if 'tot' not in S:
        if 'cnt' in S:
            return f'摩尔投票：候选 `x` = =={S["x"]}==，票数 `cnt` = =={S["cnt"]}=='
        return '先找支配元素，再枚举左半的右边界'
    if 'index' not in S:
        return f'支配元素 `x` = {S["x"]}，已数出 `tot` = =={S["tot"]}== 个'
    i, n, c, t = S['index'], len(S['nums']), S['cnt'], S['tot']
    return f'左 `{c}×2` vs `{i + 1}`　｜　右 `{t - c}×2` vs `{n - i - 1}`'


CONFIG = dict(
    num=2780, title='合法分割的最小下标', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='摩尔投票找支配元素 · 枚举左半右边界',
    tags=['动态规划', '数学算法', '难度分 1550'],
    code='''
class Solution(object):
    def minimumIndex(self, nums):

        x = nums[0]
        cnt = 1
        for v in nums[1:]:
            if v == x:
                cnt += 1
            elif cnt > 0:
                cnt -= 1
            else:
                x = v
                cnt = 1
        
        tot = 0
        for v in nums:
            if v == x:
                tot += 1
        
        cnt = 0
        for index, v in enumerate(nums):
            if v == x:
                cnt += 1
            
            if cnt * 2 > index + 1 and (tot - cnt) * 2 > len(nums) - index - 1:
                return index
        
        return -1
''',
    setup=TRACK,
    call='Solution().minimumIndex(TList([2,1,3,1,1,1,7,1,2,1]))',
    expect=4,
    max_steps=100,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='array', var='nums', pointers={_k: 'yellow'}, pointer_labels={_k: 'v'}, color=_color,
             window=(lambda S: 0 if 'index' in S else None, 'index'), h=300,
             label='nums（绿 = 支配元素，黄框 = 左半）'),
    ],
    watch=[('x', 'x', 'green'), 'cnt', ('tot', 'tot', 'purple'), 'index', ('v', 'v', 'yellow')],
    captions={
        'x = nums[0]': '摩尔投票：先把 `nums[0]` = =={x}== 当候选 `x`',
        'if v == x': lambda S, B, r: (
            ('相同' if S.v == S.x else '不同') + f'：`v = {S.v}`，`x = {S.x}`'),
        'cnt += 1': '同伙，票数 +1 → `cnt` = =={cnt}==',
        'elif cnt > 0': lambda S, B, r: (f'不同，且票数 `{S.cnt}` > 0 → 互相抵消一票' if S.cnt > 0
                                         else '不同，但票数已经是 0 → 换候选'),
        'cnt -= 1': '一票抵消 → `cnt` = =={cnt}==',
        'x = v': '票数为 0，候选换成 `v` → `x` = =={x}==',
        'cnt = 1': lambda S, B, r: ('候选 `nums[0]` 先有 1 票：`cnt = 1`' if S['_line'] == 5 else '新候选先有 1 票：`cnt = 1`'),
        'tot = 0': '支配元素一定存在，候选 `x` = =={x}==；再扫一遍数它的个数 `tot`',
        'tot += 1': '`v = {x}` → `tot` = =={tot}==',
        'cnt = 0': '`tot` = =={tot}==。再用 `cnt` 数左半里 `x` 的个数',
        'for index, v in enumerate': '枚举左半 `nums[0..{index}]`，长度 {index + 1}',
        'if v == x': lambda S, B, r: (
            ('相同' if S.v == S.x else '不同') + f'：`v = {S.v}`，`x = {S.x}`'),
        'if cnt * 2': lambda S, B, r: (
            f'左：`{S.cnt}×2 = {S.cnt * 2}` {">" if S.cnt * 2 > S.index + 1 else "≤"} `{S.index + 1}`；'
            f'右：`{S.tot - S.cnt}×2 = {(S.tot - S.cnt) * 2}` {">" if (S.tot - S.cnt) * 2 > len(S.nums) - S.index - 1 else "≤"} `{len(S.nums) - S.index - 1}`'
            + ('　==两边都过半==' if S.cnt * 2 > S.index + 1 and (S.tot - S.cnt) * 2 > len(S.nums) - S.index - 1
               else '　还不行')),
        'return index': '两边的支配元素都是 `x` → 最小下标 =={index}==',
        'return -1': '都不满足 → `-1`',
    },
    cards=dict(
        one_liner='两半的支配元素必须是整体的支配元素，枚举边界数个数',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['支配元素：出现次数超过数组长度一半',
                 '在 `i` 处切开，两段的支配元素都与整体相同才合法，求最小 `i`',
                 '示例：`[2,1,3,1,1,1,7,1,2,1]` → `4`'],
        quote='对于两个子数组而言，若这两个子数组的支配元素相同，那么其必然是整个数组的支配元素',
        quote_src='—— yiduobo 题解原文',
        idea=['支配元素必唯一，且两半的支配元素就是整体的 `x`',
              '一趟投票找出 `x`，再数出总个数 `tot`',
              '枚举左半右边界，累计 `cnt`，两边都满足 `×2 >` 长度就返回'],
        summary=['时间 `O(n)`，空间 `O(1)`：用投票代替哈希表',
                 '易错：左半长度 `index + 1`，右半长度 `n − index − 1`',
                 '投票结果是「候选」，题目保证存在支配元素才可直接用',
                 '原文本身是 Python 3 可运行的，没有改动',
                 '对比灵神：灵神用 Counter 找众数，空间 `O(n)`；这里一开始就用投票'],
    ),
)
