"""
碳足迹报告模块

生成企业碳排放报告内容
"""


from datetime import datetime



def generate_report(
    company_name,
    period,
    transport,
    packaging,
    warehouse,
    recommendations
):
    """
    生成碳足迹报告

    参数：

    company_name:
        企业名称

    period:
        核算周期

    transport:
        运输排放

    packaging:
        包装排放

    warehouse:
        仓储排放

    recommendations:
        减碳建议

    返回：
        字典格式报告
    """


    total = (
        transport
        +
        packaging
        +
        warehouse
    )


    report = {

        "基本信息":
        {
            "企业名称":
                company_name,

            "核算周期":
                period,

            "生成时间":
                datetime.now()
                .strftime(
                    "%Y-%m-%d"
                )
        },


        "碳排放结果":
        {
            "运输配送":
                f"{transport:.2f} kgCO₂e",

            "包装材料":
                f"{packaging:.2f} kgCO₂e",

            "仓储网点":
                f"{warehouse:.2f} kgCO₂e",

            "企业总排放":
                f"{total:.2f} kgCO₂e"
        },


        "减碳建议":
            recommendations

    }


    return report