def _wcol(S, i, v):
    if S.get('_line', 0) >= 45 and 'left' in S and 'right' in S and 'mid' in S and S['left'] <= i <= S['right']:
        return 'yellow' if i == S['mid'] else 'blue'
    return None


def _txt(S):
    ln = S.get('_line', 0)
    if 'prefix_s' not in S:
        if 'three' in S:
            f = lambda b: '有' if b else '无'
            return f'三连 1：{f(S["three"])}；两连 1：{f(S["two"])}；有 1：{f(S["one"])}'
        return '先扫一遍：收集 1 的位置，并看看有没有连续的 1'
    if 'left' not in S or ln < 45:
        return f'特殊操作先全用上，还要用常规操作拾 `k = {S["k"]}` 个 1：枚举 `pos_list` 中连续 `k` 个'
    if 'cost' not in S:
        return f'窗口 `[{S["left"]}, {S["right"]}]`，中位数 `pos_list[{S["mid"]}] = {S["pos_list"][S["mid"]]}`'
    return (f'窗口 `[{S["left"]}, {S["right"]}]` 到中位数的距离和 + `maxChanges×2` = =={S["cost"]}==，最小 `res` = ' + (f'=={S["res"]}==' if S.get('res') is not None else '无'))


CONFIG = dict(
    num=3086, title='拾起 K 个 1 需要的最少行动次数', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='特判 + 滑窗中位数',
    tags=['前缀和', '中位数贪心', '难度分 2673'],
    code='''
class Solution(object):
    def minimumMoves(self, nums, k, maxChanges):

        n = len(nums)
        pos_list = []
        three = two = one = False
        for index in range(n):
            if nums[index] == 1:
                pos_list.append(index)
                one = True
                if index > 0 and nums[index - 1] == 1:
                    two = True
                    if index > 1 and nums[index - 2] == 1:
                        three = True

        if k >= 3 and k - maxChanges <= 3 and three:
            return 2 + (k - 3) * 2
        elif k >= 2 and k - maxChanges <= 2 and two:
            return 1 + (k - 2) * 2
        elif k - maxChanges <= 1 and one:
            return (k - 1) * 2
        elif k <= maxChanges:
            return k * 2

    
        k -= maxChanges
        
        prefix_s = [0]
        for v in pos_list:
            prefix_s.append(prefix_s[-1] + v)
        
        res = None
        print(pos_list, k)
        for left in range(len(pos_list) - k + 1):
            right = left + k - 1
            mid = (left + right) // 2

            if k % 2 == 0:
                cost = prefix_s[right + 1] - prefix_s[mid + 1] - (prefix_s[mid + 1] - prefix_s[left])
            else:
                cost = prefix_s[right + 1] - prefix_s[mid + 1] - (prefix_s[mid] - prefix_s[left])

            cost += maxChanges * 2

            if res is None or res > cost:
                res = cost
        
        return res
''',
    call='Solution().minimumMoves([1,1,0,0,1,0,1], 4, 1)',
    expect=6,
    views=[
        dict(type='array', var='nums', label='nums（蓝 = 正在扫描的位置）', h=170, pointers={'_none': 'blue'},
             color=lambda S, i, v: 'blue' if 'prefix_s' not in S and S.get('index') == i else None),
        dict(type='array', var='pos_list', label='pos_list：1 的位置（蓝 = 窗口，黄 = 中位数）', h=190,
             color=_wcol),
        dict(type='array', var='prefix_s', label='prefix_s：前缀和', h=150, pointers={'_none': 'blue'}),
        dict(type='text', fn=_txt, h=70),
    ],
    skip=['n = len(nums)', 'pos_list = []'],
    watch=['k', 'three', 'two', 'one', 'left', 'right', 'mid', ('cost', 'cost', 'orange'), ('res', 'res', 'green')],
    captions={
        'three = two = one': '三个标记：有没有三连 1（`three`）、两连 1（`two`）、单个 1（`one`）',
        'pos_list.append(index)': '位置 `{index}` 是 1，记入 `pos_list = {pos_list}`',
        'one = True': '出现 1：`one = True`',
        'two = True': '`nums[{index - 1}]` 和 `nums[{index}]` 都是 1：`two = True`',
        'three = True': '连续三个 1：`three = True`',
        'if k >= 3 and': lambda S, B, r: (f'三连 1 的特判：`k={S.k} ≥ 3`，`k − maxChanges = {S.k - S.maxChanges} ≤ 3`，`three = {S.three}` → 不满足'
                                          if not (S.k >= 3 and S.k - S.maxChanges <= 3 and S.three) else '站在三连 1 的中间：2 次拾三个，其余都用特殊操作'),
        'elif k >= 2 and': lambda S, B, r: (f'两连 1 的特判：`k − maxChanges = {S.k - S.maxChanges}`，要 `≤ 2` 才行 → 不满足'
                                            if not (S.k >= 2 and S.k - S.maxChanges <= 2 and S.two) else '站在两连 1：1 次拾两个，其余用特殊操作'),
        'elif k - maxChanges <= 1': '单个 1 的特判：`k − maxChanges = {k - maxChanges}`，要 `≤ 1` → 不满足',
        'elif k <= maxChanges': '`k = {k} ≤ maxChanges = {maxChanges}`？特殊操作不够全用 → 不满足',
        'k -= maxChanges': '特殊操作用满 `maxChanges = {maxChanges}` 次（各 2 步），剩下要常规拾取的 `k = {k}` 个',
        'prefix_s = [0]': '准备前缀和：`prefix_s[0] = 0`',
        'prefix_s.append': '`v = {v}`：`prefix_s` → {prefix_s}',
        'res = None': '`res` 记最小代价，先设为空',
        'print(pos_list, k)': '（原文调试输出）`pos_list = {pos_list}`，`k = {k}`',
        'for left in range': lambda S, B, r: ('窗口枚举完了' if 'left' in B and B.left == S.left
                                              else f'窗口左端 `left = {S.left}`：取 `pos_list` 中连续 {S.k} 个 1'),
        'right = left + k - 1': '窗口 `[{left}, {right}]`，共 `k = {k}` 个',
        'mid = ': '中位数下标 `mid = {mid}`：位置 `pos_list[{mid}] = {pos_list[mid]}`',
        'cost = prefix_s[right + 1] - prefix_s[mid + 1] - (prefix_s[mid + 1]': '`k` 偶数：右半和 − 左半和 = =={cost}==',
        'cost = prefix_s[right + 1] - prefix_s[mid + 1] - (prefix_s[mid]': '`k` 奇数：右边（不含中位数）和 − 左边和 = `{prefix_s[right + 1] - prefix_s[mid + 1]} − {prefix_s[mid] - prefix_s[left]}` = =={cost}==',
        'cost += maxChanges * 2': '加上特殊操作的 `maxChanges × 2 = {maxChanges * 2}`，窗口总代价 =={cost}==',
        'res = cost': lambda S, B, r: f'更小，`res` 更新为 =={S.cost}==',
        'if res is None or res > cost': lambda S, B, r: ('第一个窗口，直接作为 `res`' if S.res is None else f'`res = {S.res}` 与 `cost = {S.cost}` 比较' + ('：新的更小' if S.res > S.cost else '：不更小，保留')),
        'return res': '最少行动 `{res}`',
    },
    cards=dict(
        one_liner='特殊操作 2 步一个，常规拾取走窗口取中位数',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`nums` 是 0/1 数组，Alice 站在某处拾起 `k` 个 1',
                 '动作：最多 `maxChanges` 次把 0 变成 1；或交换相邻的 1 和 0',
                 '示例：`[1,1,0,0,0,1,1,0,0,1]`，`k=3`，`maxChanges=1` → `3`',
                 '视频用 `[1,1,0,0,1,0,1]`，`k=4`，`maxChanges=1` → `6`'],
        quote='特殊操作就相当于通过两次操作拾取了一个1。……此时拾取的k个1一定处于一个连续的区间内，也就是说在这里可以使用一个边长的滑动窗口从左向右滑动。',
        quote_src='—— yiduobo 题解原文',
        idea=['特殊操作：把相邻的 0 变成 1 再换过去，==2 步拾一个==',
              '站在三连 1 / 两连 1 / 单个 1 上，前几个 1 只要 0～2 步，先特判',
              '特判不成立，特殊操作用满，剩下 `k − maxChanges` 个 1 用窗口 + 中位数：距离和 = 右边和 − 左边和'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '奇偶不同：奇数时中位数自己不计入左右两边，偶数时左右各一半',
                 '原文为 Python 2 写法，`print pos_list, k` 已改为 `print(pos_list, k)`，`//` 本身已是整数除法',
                 '对比灵神：灵神把特判统一成 `c`（长度≤3 的最长连续 1），yiduobo 分三种情况逐一判断'],
    ),
)
