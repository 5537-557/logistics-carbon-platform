import streamlit as st
from modules.deepseek import ask_deepseek
import pandas as pd
from pathlib import Path


from modules.calculator import (
    calculate_transport,
    calculate_packaging,
    calculate_warehouse,
    calculate_total,
    calculate_ratio
)


from modules.recommendation import (
    generate_recommendation
)


from modules.report import (
    generate_report
)



# =========================
# 页面设置
# =========================

st.set_page_config(
    page_title="企业碳足迹测算平台",
    page_icon="🌱",
    layout="wide"
)



# =========================
# 基础路径
# =========================

BASE_DIR = Path(__file__).parent



# =========================
# 加载排放因子
# =========================

FACTOR_FILE = (
    BASE_DIR
    /
    "data"
    /
    "emission_factors.csv"
)


@st.cache_data
def load_factor():

    return pd.read_csv(
        FACTOR_FILE,
        encoding="utf-8-sig"
    )


factors = load_factor()



# 默认电力因子

electric_factor = float(
    factors.iloc[0]["value"]
)



# =========================
# 页面菜单
# =========================

page = st.sidebar.radio(
    "平台功能",
    [
        "🏠 首页",
        "📥 数据导入",
        "📊 碳足迹分析与溯源",
	"♻️ 减碳建议",
        "📄 报告中心",
        "🔋 换电接口"
    ]
)



# =========================
# 首页
# =========================

if page == "🏠 首页":

    st.title(
        "🌱 企业碳足迹测算平台"
    )


    st.write(
        """
        面向城市末端配送企业，
        实现运输、包装、仓储等环节
        碳排放自动测算与分析。
        """
    )


    st.metric(
        "当前电力排放因子",
        f"{electric_factor} kgCO₂/kWh"
    )
# =========================
# 数据导入
# =========================

elif page == "📥 数据导入":

    st.title("📥 企业数据导入中心")

    st.write(
        """
        企业上传运输、包装、仓储数据，
        平台自动完成碳排放核算。
        """
    )


    # ---------------------
    # 运输数据
    # ---------------------

    st.subheader("🚚 运输数据")

    transport_file = st.file_uploader(
        "上传运输数据 Excel",
        type=["xlsx"],
        key="transport"
    )


    if transport_file:

        transport_df = pd.read_excel(
            transport_file
        )


        st.dataframe(
            transport_df,
            use_container_width=True
        )


        transport_df["碳排放(kgCO₂e)"] = (
            transport_df["耗电量(kWh)"]
            .apply(
                lambda x:
                calculate_transport(
                    x,
                    electric_factor
                )
            )
        )


        transport_total = (
            transport_df[
                "碳排放(kgCO₂e)"
            ].sum()
        )


        st.success(
            f"运输排放：{transport_total:.2f} kgCO₂e"
        )


        st.session_state[
            "transport_total"
        ] = transport_total



    # ---------------------
    # 包装数据
    # ---------------------

    st.divider()

    st.subheader("📦 包装数据")


    packaging_file = st.file_uploader(
        "上传包装数据 Excel",
        type=["xlsx"],
        key="packaging"
    )


    if packaging_file:


        packaging_df = pd.read_excel(
            packaging_file
        )


        st.dataframe(
            packaging_df,
            use_container_width=True
        )


        packaging_df["碳排放(kgCO₂e)"] = (
            packaging_df.apply(
                lambda row:
                calculate_packaging(
                    row["重量(kg)"],
                    row["排放因子"]
                ),
                axis=1
            )
        )


        packaging_total = (
            packaging_df[
                "碳排放(kgCO₂e)"
            ].sum()
        )


        st.success(
            f"包装排放：{packaging_total:.2f} kgCO₂e"
        )


        st.session_state[
            "packaging_total"
        ] = packaging_total



    # ---------------------
    # 仓储数据
    # ---------------------

    st.divider()

    st.subheader("🏭 仓储数据")


    warehouse_file = st.file_uploader(
        "上传仓储数据 Excel",
        type=["xlsx"],
        key="warehouse"
    )


    if warehouse_file:


        warehouse_df = pd.read_excel(
            warehouse_file
        )


        st.dataframe(
            warehouse_df,
            use_container_width=True
        )


        warehouse_df["碳排放(kgCO₂e)"] = (
            warehouse_df["用电量(kWh)"]
            .apply(
                lambda x:
                calculate_warehouse(
                    x,
                    electric_factor
                )
            )
        )


        warehouse_total = (
            warehouse_df[
                "碳排放(kgCO₂e)"
            ].sum()
        )


        st.success(
            f"仓储排放：{warehouse_total:.2f} kgCO₂e"
        )


        st.session_state[
            "warehouse_total"
        ] = warehouse_total
# =========================
# 排放溯源
# =========================

elif page == "📊 碳足迹分析与溯源":
    st.title("📊 碳足迹分析与排放溯源")


    transport = st.session_state.get(
        "transport_total",
        0
    )

    packaging = st.session_state.get(
        "packaging_total",
        0
    )

    warehouse = st.session_state.get(
        "warehouse_total",
        0
    )


    total = calculate_total(
        transport,
        packaging,
        warehouse
    )


    if total == 0:

        st.warning(
            "请先完成数据导入和测算"
        )

    else:


        st.success(
            "排放分析完成"
        )


        col1,col2,col3,col4 = st.columns(4)


        col1.metric(
            "总排放",
            f"{total:.2f} kgCO₂e"
        )


        col2.metric(
            "运输",
            f"{transport:.2f}"
        )


        col3.metric(
            "包装",
            f"{packaging:.2f}"
        )


        col4.metric(
            "仓储",
            f"{warehouse:.2f}"
        )


        result = pd.DataFrame(
            {
                "环节":
                [
                    "运输",
                    "包装",
                    "仓储"
                ],

                "排放量":
                [
                    transport,
                    packaging,
                    warehouse
                ]
            }
        )


        st.subheader(
            "排放贡献分析"
        )


        st.dataframe(
            result,
            use_container_width=True
        )


        st.bar_chart(
            result.set_index(
                "环节"
            )
        )


        # 保存占比

        st.session_state[
            "ratios"
        ] = {

            "transport":
            calculate_ratio(
                transport,
                total
            ),

            "packaging":
            calculate_ratio(
                packaging,
                total
            ),

            "warehouse":
            calculate_ratio(
                warehouse,
                total
            )

        }



# =========================
# 减碳建议
# =========================
elif page == "♻️ 减碳建议":

    st.title(
        "♻️ 智能减碳建议"
    )


    ratios = st.session_state.get(
        "ratios",
        None
    )


    transport = st.session_state.get(
        "transport_total",
        0
    )

    packaging = st.session_state.get(
        "packaging_total",
        0
    )

    warehouse = st.session_state.get(
        "warehouse_total",
        0
    )


    if ratios is None:

        st.warning(
            "请先完成排放测算"
        )


    else:

        suggestions = generate_recommendation(

            ratios["transport"],

            ratios["packaging"],

            ratios["warehouse"]

        )


        st.subheader(
            "📌 系统分析建议"
        )


        for item in suggestions:

            st.subheader(
                item["环节"]
            )


            st.write(
                item["问题"]
            )


            st.write(
                "优化建议："
            )


            for s in item["建议"]:

                st.write(
                    "✅ " + s
                )



        st.divider()


        st.subheader(
            "🤖 AI减碳分析"
        )


        if st.button(
            "生成AI优化方案"
        ):


            prompt = f"""
你是一名物流碳管理专家。

请根据以下企业碳排放结果，
分析主要排放来源，并提出可执行的减碳建议。

运输排放：
{transport} kgCO₂e

包装排放：
{packaging} kgCO₂e

仓储排放：
{warehouse} kgCO₂e


要求：

1. 分析主要排放问题
2. 给出3条优化措施
3. 使用物流行业语言
"""


            answer = ask_deepseek(
                prompt,
                st.secrets["DEEPSEEK_API_KEY"]
            )


            st.write(
                answer
            )
# =========================
# 报告中心
# =========================

elif page == "📄 报告中心":

    st.title(
        "📄 企业碳足迹报告"
    )

    transport = st.session_state.get(
        "transport_total",
        0
    )

    packaging = st.session_state.get(
        "packaging_total",
        0
    )

    warehouse = st.session_state.get(
        "warehouse_total",
        0
    )

    ratios = st.session_state.get(
        "ratios",
        {}
    )


    if transport + packaging + warehouse == 0:

        st.warning(
            "暂无测算结果，请先完成数据导入"
        )


    else:

        recommendations = generate_recommendation(

            ratios.get("transport", 0),

            ratios.get("packaging", 0),

            ratios.get("warehouse", 0)

        )


        report = generate_report(

            "示例物流企业",

            "2026年9月",

            transport,

            packaging,

            warehouse,

            recommendations

        )


        st.subheader(
            "📄 企业碳足迹分析报告"
        )


        st.write(
            f"""
## 一、基本信息

企业名称：
{report["基本信息"]["企业名称"]}

核算周期：
{report["基本信息"]["核算周期"]}


## 二、碳排放结果

运输配送：
{report["碳排放结果"]["运输配送"]}

包装材料：
{report["碳排放结果"]["包装材料"]}

仓储网点：
{report["碳排放结果"]["仓储网点"]}

企业总排放：
{report["碳排放结果"]["企业总排放"]}


## 三、减碳优化建议
"""
        )


        for item in recommendations:

            st.markdown(
                f"""
### {item["环节"]}

问题：
{item["问题"]}
"""
            )


            st.write(
                "建议："
            )


            for s in item["建议"]:

                st.write(
                    "✅ " + s
                )# =========================
# 换电接口
# =========================

elif page == "🔋 换电接口":


    st.title(
        "🔋 新能源车辆换电数据接口"
    )


    st.info(
        """
        换电数据不作为独立排放源，
        而作为新能源车辆能源数据输入运输模型。
        """
    )


    st.code(
        """
{
    vehicle_id:"京A001",
    swap_times:120,
    electricity:1800,
    unit:"kWh"
}
        """
    )


    st.success(
        "换电接口模块 Demo 已完成"
    )