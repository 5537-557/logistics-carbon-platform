"""
减碳建议模块

根据不同环节排放占比
自动生成优化建议
"""


def generate_recommendation(
    transport_ratio,
    packaging_ratio,
    warehouse_ratio
):
    """
    输入：
        三个环节排放占比(%)

    输出：
        建议列表
    """


    recommendations = []


    # =====================
    # 运输建议
    # =====================

    if transport_ratio >= 50:

        recommendations.append(
            {
                "环节": "运输配送",
                "问题": "运输环节贡献较高",
                "建议": [
                    "优化配送路径，减少无效里程",
                    "提升车辆装载率",
                    "增加新能源配送车辆比例",
                    "利用智能调度降低空驶率"
                ]
            }
        )


    # =====================
    # 包装建议
    # =====================

    if packaging_ratio >= 30:

        recommendations.append(
            {
                "环节": "包装材料",
                "问题": "包装产生较高碳排放",
                "建议": [
                    "推广循环包装",
                    "减少一次性包装材料",
                    "优化包装尺寸",
                    "提高包装材料回收利用率"
                ]
            }
        )


    # =====================
    # 仓储建议
    # =====================

    if warehouse_ratio >= 20:

        recommendations.append(
            {
                "环节": "仓储/配送网点",
                "问题": "仓储能源消耗较高",
                "建议": [
                    "使用绿色电力",
                    "优化照明和设备能耗",
                    "建设智能能源管理系统"
                ]
            }
        )


    # 如果没有明显高排放

    if not recommendations:

        recommendations.append(
            {
                "环节": "整体",
                "问题": "各环节排放较均衡",
                "建议": [
                    "持续监测碳排放变化",
                    "建立长期减排计划"
                ]
            }
        )


    return recommendations