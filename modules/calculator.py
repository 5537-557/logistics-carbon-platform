"""
企业碳足迹测算模型层

功能：
1. 运输排放计算
2. 包装排放计算
3. 仓储排放计算
4. 总碳排放汇总
"""


# =========================
# 通用计算公式
# =========================

def calculate_emission(
    activity,
    factor
):
    """
    碳排放通用公式

    排放量 = 活动数据 × 排放因子

    activity:
        活动数据
        例如：
        kWh
        kg
        L

    factor:
        排放因子

    返回：
        kgCO2e
    """

    return activity * factor



# =========================
# 运输模块
# =========================

def calculate_transport(
    electricity,
    electricity_factor
):
    """
    新能源车辆运输排放

    输入：
    electricity:
        车辆耗电量 kWh

    electricity_factor:
        电力排放因子

    输出：
        kgCO2e
    """

    return calculate_emission(
        electricity,
        electricity_factor
    )



# =========================
# 包装模块
# =========================

def calculate_packaging(
    weight,
    material_factor
):
    """
    包装材料排放

    输入：
    weight:
        包装重量 kg

    material_factor:
        包装材料排放因子

    输出：
        kgCO2e
    """

    return calculate_emission(
        weight,
        material_factor
    )



# =========================
# 仓储模块
# =========================

def calculate_warehouse(
    electricity,
    electricity_factor
):
    """
    仓储用电排放
    """

    return calculate_emission(
        electricity,
        electricity_factor
    )



# =========================
# 换电数据转换
# =========================

def calculate_battery_energy(
    battery_kwh,
    electricity_factor
):
    """
    换电数据

    注意：
    换电不是独立排放源，
    转换为车辆能源消耗，
    进入运输模型。

    输入：
    battery_kwh:
        换电补充电量

    输出：
        kgCO2e
    """

    return calculate_transport(
        battery_kwh,
        electricity_factor
    )



# =========================
# 汇总
# =========================

def calculate_total(
    transport,
    packaging,
    warehouse
):
    """
    企业总碳足迹

    总排放 =
    运输
    +
    包装
    +
    仓储
    """

    return (
        transport
        +
        packaging
        +
        warehouse
    )



# =========================
# 排放占比
# =========================

def calculate_ratio(
    value,
    total
):
    """
    计算贡献比例
    """

    if total == 0:
        return 0

    return value / total * 100