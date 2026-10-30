CONFIG = dict(
    num=2899, title='上一个遍历的整数', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='模拟 · 倒数第 k 个', tags=[],
    code='''
class Solution:
    def lastVisitedIntegers(self, nums: List[int]) -> List[int]:
        ans = []
        seen = []
        k = 0
        for x in nums:
            if x > 0:
                seen.append(x)
                k = 0
            else:
                k += 1
                ans.append(-1 if k > len(seen) else seen[-k])  # 倒数第 k 个
        return ans
''',
    call='Solution().lastVisitedIntegers([1,-1,2,-1,-1,-1])',
    expect=[1, 2, 1, -1],
    views=[
        dict(type='array', var='nums', h=170, label='nums', pointers={'idx': 'blue'},
             color=lambda S, i, v: ('green' if v > 0 else 'pink') if i <= S.get('idx', -1) else None),
        dict(type='array', var='seen', h=150, label='seen（新的在末尾）', pointers={'len(seen) - k': 'pink'}),
        dict(type='array', var='ans', h=150, label='ans', color=lambda S, i, v: 'yellow' if i == len(S['ans']) - 1 else None),
    ],
    watch=['x', ('k', 'k', 'pink'), ('len(seen)', 'len(seen)')],
    captions={
        5: '`k` 记录当前连续 -1 的个数',
        9: '`k` 清零：下一个 -1 重新从 1 数起',
        'if x > 0': '`x = {x}` → {"正整数" if x > 0 else "是 -1"}',
        'seen.append': '`{x}` 放进 `seen`，==连续 -1 中断== → `k = 0`',
        'k += 1': '又一个连续的 -1：`k = {k}`',
        'ans.append': '`k = {k}`，`len(seen) = {len(seen)}`：{"k 太大，没有这么多数" if k > len(seen) else "取 seen 倒数第 " + str(k) + " 个"} → 答案加入 =={ans[-1]}==',
        'return ans': '遍历结束，返回 `{ret}`',
    },
    cards=dict(
        one_liner='seen 尾部追加，第 k 个 -1 就取倒数第 k 个',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 里是正整数或 `-1`，为每个 `-1` 找「最后访问的整数」',
                 '正整数放进 `seen` 头部；连续第 `k` 个 `-1` 取 `seen` 第 `k` 个，不够则 `-1`',
                 '示例：`[1,2,-1,-1,-1]` → `[2,1,-1]`'],
        quote='按题意模拟即可。',
        quote_src='—— 灵茶山艾府题解（代码注释：倒数第 k 个）',
        idea=['题目说「放头部」，但头部插入慢，改成 ==尾部 append==',
              '于是头部第 `k` 个 = 末尾倒数第 `k` 个 = `seen[-k]`',
              '遇到正数 `k` 清零；遇到 -1 `k` 加一，`k > len(seen)` 就填 -1'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：遇到正整数时 `k` 要清零（连续才算）',
                 '`k > len(seen)` 要先判断，否则 `seen[-k]` 越界',
                 '倒着存的技巧：头部插入改成尾部追加'],
    ),
)
