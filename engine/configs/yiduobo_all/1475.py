CONFIG = dict(
    num=1475, title='商品折扣后的最终价格', difficulty='Easy', category='单调栈',
    author='yiduobo', technique='单调栈 · 下一个较小元素',
    tags=['单调栈', '基础'],
    code='''
class Solution(object):
    def finalPrices(self, prices):

        stack = [0]
        res = prices[:]
        for index in range(1, len(prices)):
            while stack and prices[stack[-1]] >= prices[index]:
                res[stack[-1]] -= prices[index]
                stack.pop()

            stack.append(index)

        return res
''',
    call='Solution().finalPrices([10,6,8,3,5,4])',
    expect=[4, 3, 5, 3, 1, 4],
    views=[
        dict(type='array', var='prices', label='prices（蓝 = 当前 index，粉 = 栈顶）', cell=90, h=200,
             pointers={'index': 'blue'},
             color=lambda S, i, v: 'blue' if S.get('index') == i else ('pink' if S.get('stack') and S['stack'][-1] == i else None)),
        dict(type='array', var='res', label='res（折扣后的价格，随栈顶弹出而更新）', cell=90, h=200,
             color=lambda S, i, v: 'green' if 'prices' in S and v != S['prices'][i] else None),
        dict(type='stack', var='stack', label='stack（还没找到下一个较小元素的下标，价格单调不减）', fmt=lambda i: f'{i}', h=200),
    ],
    watch=[('index', 'index', 'blue'), 'stack'],
    captions={
        'stack = [0]': '第 0 个元素先入栈，它还没找到下一个较小元素',
        'res = prices[:]': '`res` 是 `prices` 的拷贝，折扣直接扣在 `res` 上',
        'for index in range': '扫描到 `index = {index}`，价格 `{prices[index]}`',
        'while stack and prices[stack[-1]] >= prices[index]': lambda S, B, r: (
            f'栈顶 `prices[{S.stack[-1]}] = {S.prices[S.stack[-1]]}` >= `{S.prices[S.index]}` → 成立：栈顶找到了下一个较小元素'
            if S.stack and S.prices[S.stack[-1]] >= S.prices[S.index] else
            ('栈空了，停止弹栈' if not S.stack else f'栈顶 `{S.prices[S.stack[-1]]}` < `{S.prices[S.index]}` → 不成立，停止弹栈，栈保持单调')),
        'res[stack[-1]] -= prices[index]': '栈顶下标 `{stack[-1]}` 的折扣就是 `prices[{index}] = {prices[index]}`：`res[{stack[-1]}]` → =={res[stack[-1]]}==',
        'stack.pop()': '栈顶已经有答案，弹出，栈变成 `{stack}`',
        'stack.append(index)': '`index = {index}` 入栈：等它的下一个较小元素',
        'return res': '栈里剩下的没有折扣，返回 `{res}`',
    },
    cards=dict(
        one_liner='经典「下一个较小元素」：栈里放还没找到的',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['买第 `i` 件商品可减去其右边第一个 `<=` 它的价格',
                 '没有就不减，返回折扣后的价格数组',
                 '本视频：`[10,6,8,3,5,4]` → `[4,3,5,3,1,4]`'],
        quote='栈中的元素必然是单调不减的，因为若栈中存在两个位置i和j，满足i < j且prices[i] < prices[j]，那么此时i就已经有了下一个较小元素了，不应当存在于栈中。',
        quote_src='—— yiduobo 题解原文',
        idea=['栈维护当前==还没找到下一个较小元素==的位置',
              '新元素 `<=` 栈顶：栈顶找到答案，弹出并扣掉折扣，重复到不满足或栈空',
              '最后把当前下标压栈'],
        summary=['时间 `O(n)`：每个下标入栈、出栈各一次',
                 '`>=` 包含相等：折扣条件是 `<=`',
                 '原文为 Python 2 风格，本文代码无需改动，只去掉了多余的空白',
                 '对比灵神：灵神把折扣直接减在原数组上，yiduobo 用 `res` 拷贝'],
    ),
)
