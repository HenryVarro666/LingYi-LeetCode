CONFIG = dict(
    num=2866, title='美丽塔 II', difficulty='Medium', category='动态规划',
    author='yiduobo', technique='枚举山峰 · 预处理前后缀 · 单调栈',
    tags=['灵神题单·单调栈', '灵神题单·动态规划', '难度分 2072'],
    code='''
class Solution(object):
    def maximumSumOfHeights(self, maxHeights):

        n = len(maxHeights)

        prefix = [maxHeights[0]]
        stack = [0]
        s = maxHeights[0]
        for index in range(1, n):
            while stack and maxHeights[stack[-1]] > maxHeights[index]:
                right = stack.pop()
                if stack:
                    left = stack[-1]
                else:
                    left = -1
                
                s -= maxHeights[right] * (right - left)
            
            if stack:
                left = stack[-1]
            else:
                left = -1
            
            s += (index - left) * maxHeights[index]
            stack.append(index)
            prefix.append(s)
        
        suffix = [maxHeights[n - 1]]
        stack = [n - 1]
        s = maxHeights[n - 1]
        for index in range(n - 2, -1, -1):
            while stack and maxHeights[stack[-1]] > maxHeights[index]:
                left = stack.pop()
                if stack:
                    right = stack[-1]
                else:
                    right = n
                
                s -= maxHeights[left] * (right - left)

            if stack:
                right = stack[-1]
            else:
                right = n

            s += (right - index) * maxHeights[index]
            stack.append(index)
            suffix.append(s)
        
        suffix.reverse()

        res = 0
        for index in range(n):
            res = max(res, prefix[index] + suffix[index] - maxHeights[index])
        
        return res
''',
    call='Solution().maximumSumOfHeights([5,3,4,1,1])',
    expect=13,
    views=[
        dict(type='bars', var='maxHeights', pointers={'index': 'blue'}, h=200, label='maxHeights',
             color=lambda S, i, v: 'blue' if i == S.get('index', -99) else None),
        dict(type='stack', var='stack', h=100, fmt=lambda j: f'下标{j}'),
        dict(type='array', var='prefix', h=130, label='prefix：以 index 结尾的递增段最大和'),
        dict(type='array', var='suffix', h=130, label='suffix：以 index 开头的递减段最大和'),
        dict(type='text', fn=lambda S: f"当前这一侧的和 `s = {S['s']}`" if 's' in S else ''),
    ],
    watch=[('index', 'index', 'blue'), ('s', 's', 'yellow'), ('res', 'res', 'green')],
    captions={
        'prefix = [maxHeights[0]]': '`prefix[i]`：以 `i` 结尾、单调不减的前缀，高度和最大是多少',
        's = maxHeights[0]': '`s` = 当前前缀的总和 = `{s}`；栈里存==没被压低过==的下标',
        10: lambda S, B, r: (
            f'栈顶高度 `{S.maxHeights[S.stack[-1]]}` > 当前 `{S.maxHeights[S.index]}`：栈顶那段要被压低到 `{S.maxHeights[S.index]}`' if S.stack and S.maxHeights[S.stack[-1]] > S.maxHeights[S.index]
            else ('栈空了：前面全被压低过，停止' if not S.stack else f'栈顶高度 `{S.maxHeights[S.stack[-1]]}` <= 当前 `{S.maxHeights[S.index]}`：不用再压')),
        11: '弹出下标 `{right}`，它管着左边一段，先找这段的左边界',
        13: '`left = {left}`：被压的这一段是 `({left}, {right}]`',
        15: '栈空，`left = -1`：这一段从数组开头算起',
        17: '撤销旧高度：`s -= {maxHeights[right]} × ({right} − {left})` → `s = {s}`',
        20: '`left = {left}`：新塔负责 `({left}, {index}]`',
        22: '栈空，`left = -1`',
        24: '`({left}, {index}]` 共 `{index - left}` 座塔都取 `{maxHeights[index]}`：`s = {s}`',
        26: '`prefix[{index}] = {s}`',
        28: '对称地算 `suffix`：从右往左，`suffix[i]` 是以 `i` 开头的递减段最大和',
        32: lambda S, B, r: (
            f'栈顶高度 `{S.maxHeights[S.stack[-1]]}` > 当前 `{S.maxHeights[S.index]}`：栈顶那段要被压低到 `{S.maxHeights[S.index]}`' if S.stack and S.maxHeights[S.stack[-1]] > S.maxHeights[S.index]
            else ('栈空了：右边全被压低过，停止' if not S.stack else f'栈顶高度 `{S.maxHeights[S.stack[-1]]}` <= 当前 `{S.maxHeights[S.index]}`：不用再压')),
        33: '弹出下标 `{left}`，先找这段的右边界',
        35: '`right = {right}`：被压的这一段是 `[{left}, {right})`',
        37: '栈空，`right = n`：这一段一直到数组末尾',
        39: '撤销旧高度：`s -= {maxHeights[left]} × ({right} − {left})` → `s = {s}`',
        42: '`right = {right}`：新塔负责 `[{index}, {right})`',
        44: '栈空，`right = n`',
        46: '`[{index}, {right})` 共 `{right - index}` 座塔都取 `{maxHeights[index]}`：`s = {s}`',
        48: '`suffix` 追加 `{s}`（这是 `suffix[{index}]`，列表从右往左存）',
        50: '`suffix` 是从右往左存的，翻转后下标就对上了',
        53: lambda S, B, r: (f'枚举山峰位置 `index = {S.index}`' if not (B.get('index') == S.index == len(S.maxHeights) - 1) else '枚举完毕'),
        54: '山峰在 `{index}`：`prefix {prefix[index]} + suffix {suffix[index]} − 峰高 {maxHeights[index]}`（峰高算了两次）→ `res = {res}`',
        56: '最大高度和 `{res}`',
    },
    skip=['if stack:', 'stack.append(index)', 'n = len(maxHeights)', 'stack = [0]', 'stack = [n - 1]', 's = maxHeights[n - 1]', 'res = 0'],
    max_steps=130,
    cards=dict(
        one_liner='山峰左右两侧分别预处理，栈里只保留没被压低的下标',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`maxHeights[i]` 是第 `i` 座塔的高度上限，塔高 >= 1',
                 '塔高要形成山脉（先不降后不增），求高度和的最大值',
                 '本视频示例：`[5,3,4,1,1]` → `13`'],
        quote='注意到这些被弹出的位置的最终高度值都将等于maxHeight[index]，那么在这里就可以将单调栈记录的内容从每个位置的最终高度调整为所有从未修改过高度的位置的下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['`prefix[i]` / `suffix[i]` 表示以 `i` 结尾 / 开头的最大和',
              '山峰选 `i` 时总和 = `prefix[i] + suffix[i] − maxHeights[i]`',
              '栈里存下标：相邻两个下标之间的塔，高度都等于右边那个下标的高度'],
        summary=['时间 `O(n)`，每个下标进出栈最多一次；空间 `O(n)`',
                 '峰顶 `maxHeights[i]` 在 `prefix` 和 `suffix` 里各算了一次，要减掉一次',
                 '比较用 `>`：栈里保持高度不减，相等的不弹',
                 '对比灵神：灵神把 `suf` 存成 `n+1` 长并用哨兵，yiduobo 用 `if stack` 处理空栈'],
    ),
)
