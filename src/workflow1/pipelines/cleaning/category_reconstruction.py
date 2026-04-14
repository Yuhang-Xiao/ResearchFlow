"""Goal-driven product category reconstruction for Sichuan 2023 raw data."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import pandas as pd


RAW_PATH = Path("data/01_raw/FINAL_SiChuan_2023_ALL_DATA.xlsx")
DATASET_STEM = "FINAL_SiChuan_2023_ALL_DATA"

OUTPUT_DATASET = Path("data/03_primary/FINAL_SiChuan_2023_ALL_DATA__category_cleaned.csv")
MAPPING_TABLE = Path("reports/tables/category_mapping_FINAL_SiChuan_2023_ALL_DATA.csv")
TAXONOMY_TABLE = Path("reports/tables/category_taxonomy_FINAL_SiChuan_2023_ALL_DATA.csv")
MASTER_REPORT = Path("reports/category_reconstruction_summary_FINAL_SiChuan_2023_ALL_DATA.md")
CATEGORY_REPORT_DIR = Path("reports/category_reports/FINAL_SiChuan_2023_ALL_DATA")


@dataclass(frozen=True)
class CategoryDecision:
    level1: str
    level2: str
    level3: str
    basis: str
    confidence: float
    review: bool
    rule_id: str
    trigger: str


def has_any(text: str, words: tuple[str, ...]) -> bool:
    return any(word in text for word in words)


def split_raw_category(raw_category: str) -> tuple[str, str]:
    parts = [part.strip() for part in str(raw_category).split("-->") if part.strip()]
    if not parts:
        return "缺失", "缺失"
    if len(parts) == 1:
        return parts[0], "未细分"
    return parts[0], parts[1]


def vegetable_group(raw_sub: str, name: str) -> tuple[str, str, str, float, bool]:
    text = f"{raw_sub} {name}"
    groups: list[tuple[str, str, tuple[str, ...]]] = [
        ("蔬菜制品", "酱腌菜/腌渍蔬菜", ("酱腌菜", "泡菜", "咸菜", "榨菜", "酸菜", "腌", "雪菜", "萝卜干")),
        ("蔬菜制品", "干制/脱水蔬菜", ("干燥蔬菜", "干制", "脱水", "笋干", "梅干菜", "干菜", "黄花菜")),
        ("食用菌", "食用菌及其制品", ("食用菌", "香菇", "蘑菇", "平菇", "金针菇", "木耳", "银耳", "菌", "杏鲍菇")),
        ("鲜食蔬菜", "叶菜类", ("菠菜", "油麦菜", "生菜", "芹菜", "韭菜", "苋菜", "空心菜", "茼蒿", "菜心", "油菜", "青菜", "小白菜", "白菜", "甘蓝", "包菜", "卷心菜")),
        ("鲜食蔬菜", "根茎/薯芋/葱蒜类", ("土豆", "马铃薯", "红薯", "山药", "芋", "莲藕", "藕", "萝卜", "胡萝卜", "姜", "莴笋", "竹笋", "芦笋", "蒜", "葱", "洋葱", "蒜薹")),
        ("鲜食蔬菜", "瓜类蔬菜", ("黄瓜", "苦瓜", "丝瓜", "南瓜", "冬瓜", "西葫芦", "瓠瓜")),
        ("鲜食蔬菜", "茄果类蔬菜", ("辣椒", "甜椒", "番茄", "西红柿", "茄子")),
        ("鲜食蔬菜", "豆类蔬菜", ("豇豆", "四季豆", "豆角", "扁豆", "豌豆", "毛豆", "菜豆")),
        ("鲜食蔬菜", "芽苗类蔬菜", ("豆芽", "芽苗")),
    ]
    for level2, level3, keywords in groups:
        if has_any(text, keywords):
            trigger = next(word for word in keywords if word in text)
            return level2, level3, trigger, 0.93, False
    return "鲜食蔬菜", raw_sub if raw_sub and raw_sub != "未细分" else "其他蔬菜", "原始蔬菜分类", 0.72, True


def fruit_group(raw_sub: str, name: str) -> tuple[str, str, str, float, bool]:
    text = f"{raw_sub} {name}"
    if has_any(text, ("蜜饯", "果脯", "果干", "干制", "水果制品")):
        return "水果制品", "蜜饯/果干/加工水果", "加工水果词", 0.9, False
    fruit_groups = [
        ("鲜食水果", "仁果类", ("苹果", "梨")),
        ("鲜食水果", "柑橘类", ("柑", "橘", "橙", "柚", "柠檬")),
        ("鲜食水果", "热带/亚热带水果", ("香蕉", "芒果", "菠萝", "火龙果", "荔枝", "龙眼", "椰")),
        ("鲜食水果", "浆果/葡萄类", ("葡萄", "草莓", "蓝莓", "桑葚")),
        ("鲜食水果", "瓜果类", ("西瓜", "甜瓜", "哈密瓜")),
        ("鲜食水果", "核果类", ("桃", "李", "杏", "樱桃", "枣")),
    ]
    for level2, level3, keywords in fruit_groups:
        if has_any(text, keywords):
            trigger = next(word for word in keywords if word in text)
            return level2, level3, trigger, 0.88, False
    return "鲜食水果", raw_sub if raw_sub and raw_sub != "未细分" else "其他水果", "原始水果分类", 0.72, True


def grain_group(raw_sub: str, name: str, is_catering: bool = False) -> CategoryDecision:
    text = f"{raw_sub} {name}"
    if is_catering:
        return CategoryDecision(
            "餐饮食品",
            "餐饮主食",
            "米面熟制品",
            "原始分类为餐饮场景，且产品为米面及其制品；保留餐饮加工/使用语境，不与原粮大米合并。",
            0.88,
            False,
            "CAT_CATERING_STAPLE",
            "餐饮-->米面及其制品",
        )
    if has_any(text, ("大米制品", "米粉", "米线", "河粉", "年糕", "粽", "汤圆")):
        return CategoryDecision("粮食及粮食制品", "米制品", "大米加工制品", "产品名称/原始分类指向大米加工制品。", 0.9, False, "CAT_GRAIN_RICE_PRODUCT", "米制品")
    if has_any(text, ("大米", "籼米", "粳米", "糯米", "香米")):
        return CategoryDecision("粮食及粮食制品", "谷物原粮及初加工", "大米", "产品名称/原始分类指向大米原粮或初加工品。", 0.94, False, "CAT_GRAIN_RICE", "大米")
    if has_any(text, ("小麦粉", "面粉")):
        return CategoryDecision("粮食及粮食制品", "谷物粉类", "小麦粉", "产品名称/原始分类指向小麦粉。", 0.94, False, "CAT_GRAIN_FLOUR", "小麦粉")
    if has_any(text, ("挂面", "面条", "面制品", "馒头", "包子", "饺子皮")):
        return CategoryDecision("粮食及粮食制品", "面制品", raw_sub, "产品名称/原始分类指向面制品。", 0.86, False, "CAT_GRAIN_WHEAT_PRODUCT", "面制品")
    return CategoryDecision("粮食及粮食制品", raw_sub, "其他粮食及其制品", "保留原始粮食分类语义。", 0.76, True, "CAT_GRAIN_OTHER", "原始粮食分类")


def classify(raw_category: str, product_name: str) -> CategoryDecision:
    raw_main, raw_sub = split_raw_category(raw_category)
    name = "" if pd.isna(product_name) else str(product_name)
    text = f"{raw_category} {name}"

    if raw_main == "餐饮":
        if raw_sub == "餐饮具":
            return CategoryDecision("餐饮相关", "餐饮具/食品接触类", "餐饮具", "原始分类明确为餐饮具，不作为普通食品重分类。", 0.98, False, "CAT_CATERING_WARE", "餐饮具")
        if raw_sub == "米面及其制品":
            return grain_group(raw_sub, name, is_catering=True)
        if raw_sub == "蔬菜":
            level2, level3, trigger, conf, review = vegetable_group(raw_sub, name)
            return CategoryDecision("蔬菜及蔬菜制品", level2, f"{level3}（餐饮场景）", f"原始分类为餐饮-->蔬菜；产品名称支持蔬菜细分，保留餐饮场景 traceability。触发词：{trigger}。", conf - 0.04, review, "CAT_CATERING_VEG", trigger)
        if raw_sub in {"复合调味料", "调味料"}:
            return CategoryDecision("调味品", "复合调味料", "餐饮用复合调味料", "原始分类为餐饮场景，但产品语义为调味料。", 0.84, False, "CAT_CATERING_SEASONING", raw_sub)
        if raw_sub == "餐饮用油":
            return CategoryDecision("食用油、油脂及其制品", "食用植物油", "餐饮用油", "原始分类为餐饮用油；按食品语义归入食用油并保留餐饮场景。", 0.86, False, "CAT_CATERING_OIL", raw_sub)
        if raw_sub == "饮品":
            return CategoryDecision("饮料", "餐饮现制饮品", "餐饮饮品", "原始分类为餐饮饮品；按饮料语义归并并保留餐饮场景。", 0.82, False, "CAT_CATERING_DRINK", raw_sub)
        if raw_sub == "肉及肉制品":
            return CategoryDecision("肉及肉制品", "餐饮肉制品", "餐饮场景肉制品", "原始分类为餐饮场景，但产品语义为肉及肉制品。", 0.8, False, "CAT_CATERING_MEAT", raw_sub)
        return CategoryDecision("餐饮食品", raw_sub, "其他餐饮食品", "原始分类为餐饮；产品名称未提供足够证据脱离餐饮场景。", 0.66, True, "CAT_CATERING_OTHER", raw_sub)

    if raw_main == "蔬菜及其制品" or has_any(text, ("蔬菜", "食用菌", "酱腌菜", "辣椒", "白菜", "土豆", "黄瓜", "番茄", "茄子", "豇豆", "芹菜", "韭菜")):
        level2, level3, trigger, conf, review = vegetable_group(raw_sub, name)
        return CategoryDecision("蔬菜及蔬菜制品", level2, level3, f"结合原始产品分类与产品名称进行蔬菜细分；触发词：{trigger}。", conf, review, "CAT_VEG", trigger)

    if raw_main == "水果及其制品":
        level2, level3, trigger, conf, review = fruit_group(raw_sub, name)
        return CategoryDecision("水果及水果制品", level2, level3, f"结合原始产品分类与产品名称进行水果细分；触发词：{trigger}。", conf, review, "CAT_FRUIT", trigger)

    if raw_main == "粮食及其制品":
        return grain_group(raw_sub, name)

    direct_map = {
        "油脂及其制品": ("食用油、油脂及其制品", "食用油脂", raw_sub, "原始分类指向食用油脂。", 0.9, "CAT_OIL"),
        "水产及其制品": ("水产及水产制品", raw_sub, "按原始水产细类", "原始分类指向水产及其制品。", 0.88, "CAT_AQUATIC"),
        "肉及肉制品": ("肉及肉制品", raw_sub, "按原始肉类细类", "原始分类指向肉及肉制品。", 0.88, "CAT_MEAT"),
        "蛋及蛋制品": ("蛋及蛋制品", raw_sub, "按原始蛋类细类", "原始分类指向蛋及蛋制品。", 0.9, "CAT_EGG"),
        "乳及乳制品": ("乳及乳制品", raw_sub, "按原始乳品细类", "原始分类指向乳及乳制品。", 0.9, "CAT_DAIRY"),
        "调味品": ("调味品", raw_sub, "按原始调味品细类", "原始分类指向调味品。", 0.88, "CAT_SEASONING"),
        "酒类": ("酒类", raw_sub, "按原始酒类细类", "原始分类指向酒类。", 0.9, "CAT_ALCOHOL"),
        "饮料": ("饮料", raw_sub, "按原始饮料细类", "原始分类指向饮料。", 0.88, "CAT_BEVERAGE"),
        "茶叶及相关制品": ("茶叶及相关制品", raw_sub, "按原始茶叶细类", "原始分类指向茶叶及相关制品。", 0.88, "CAT_TEA"),
        "焙烤食品": ("焙烤食品", raw_sub, "按原始焙烤细类", "原始分类指向焙烤食品。", 0.88, "CAT_BAKERY"),
        "豆及豆制品": ("豆及豆制品", raw_sub, "按原始豆制品细类", "原始分类指向豆及豆制品。", 0.88, "CAT_BEAN"),
        "淀粉及淀粉制品": ("淀粉及淀粉制品", raw_sub, "按原始淀粉细类", "原始分类指向淀粉及淀粉制品。", 0.88, "CAT_STARCH"),
        "坚果和籽类": ("坚果和籽类", raw_sub, "按原始坚果籽类细类", "原始分类指向坚果和籽类。", 0.88, "CAT_NUT_SEED"),
        "薯类及膨化食品": ("薯类及膨化食品", raw_sub, "按原始薯类/膨化细类", "原始分类指向薯类及膨化食品。", 0.86, "CAT_PUFFED"),
        "方便食品": ("方便食品", raw_sub, "按原始方便食品细类", "原始分类指向方便食品。", 0.86, "CAT_CONVENIENCE"),
        "速冻面米与调制食品": ("速冻食品", raw_sub, "按原始速冻细类", "原始分类指向速冻面米与调制食品。", 0.86, "CAT_FROZEN"),
        "糖果和巧克力、可可及其制品": ("糖果巧克力及果冻", raw_sub, "按原始糖果细类", "原始分类指向糖果、巧克力、可可或果冻。", 0.88, "CAT_CANDY"),
        "保健食品": ("保健食品", raw_sub, "按原始剂型", "原始分类指向保健食品。", 0.9, "CAT_HEALTH"),
        "特殊膳食食品": ("特殊膳食食品", raw_sub, "按原始特殊膳食细类", "原始分类指向特殊膳食食品。", 0.9, "CAT_SPECIAL_DIET"),
        "蜂产品": ("蜂产品", raw_sub, "按原始蜂产品细类", "原始分类指向蜂产品。", 0.88, "CAT_HONEY"),
        "食糖": ("食糖", raw_sub, "按原始食糖细类", "原始分类指向食糖。", 0.88, "CAT_SUGAR"),
    }
    if raw_main in direct_map:
        level1, level2, level3, basis, conf, rule_id = direct_map[raw_main]
        return CategoryDecision(level1, level2, level3, basis, conf, False, rule_id, raw_main)

    return CategoryDecision("其他/待复核", raw_main, raw_sub, "未匹配到明确的食品语义规则，保留原始分类并建议人工复核。", 0.45, True, "CAT_REVIEW_OTHER", raw_main)


def safe_filename(value: str) -> str:
    return re.sub(r"[\\/:*?\"<>|\\s]+", "_", value).strip("_")[:80]


def main() -> None:
    for path in [OUTPUT_DATASET.parent, MAPPING_TABLE.parent, TAXONOMY_TABLE.parent, CATEGORY_REPORT_DIR]:
        path.mkdir(parents=True, exist_ok=True)

    df = pd.read_excel(RAW_PATH, sheet_name="Sheet1")
    required = {"产品分类", "产品名称"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    decisions = [classify(row["产品分类"], row["产品名称"]) for _, row in df.iterrows()]
    df.insert(df.columns.get_loc("产品分类") + 1, "原始产品分类", df["产品分类"])
    df["新一级类"] = [d.level1 for d in decisions]
    df["新二级类"] = [d.level2 for d in decisions]
    df["新三级类"] = [d.level3 for d in decisions]
    df["分类依据"] = [d.basis for d in decisions]
    df["分类置信度"] = [d.confidence for d in decisions]
    df["是否建议人工复核"] = ["是" if d.review else "否" for d in decisions]
    df["分类规则ID"] = [d.rule_id for d in decisions]
    df["分类触发词"] = [d.trigger for d in decisions]

    df.to_csv(OUTPUT_DATASET, index=False, encoding="utf-8-sig")

    mapping = (
        df.groupby(["原始产品分类", "分类规则ID", "分类触发词", "新一级类", "新二级类", "新三级类", "分类依据", "是否建议人工复核"], dropna=False)
        .agg(记录数=("产品名称", "size"), 示例产品名称=("产品名称", lambda s: "；".join(map(str, s.dropna().astype(str).drop_duplicates().head(8)))))
        .reset_index()
        .sort_values(["记录数", "原始产品分类"], ascending=[False, True])
    )
    mapping.to_csv(MAPPING_TABLE, index=False, encoding="utf-8-sig")

    taxonomy = (
        df.groupby(["新一级类", "新二级类", "新三级类"], dropna=False)
        .agg(
            记录数=("产品名称", "size"),
            原始产品分类数=("原始产品分类", "nunique"),
            示例原始产品分类=("原始产品分类", lambda s: "；".join(map(str, s.dropna().astype(str).drop_duplicates().head(8)))),
            示例产品名称=("产品名称", lambda s: "；".join(map(str, s.dropna().astype(str).drop_duplicates().head(8)))),
            建议复核数=("是否建议人工复核", lambda s: int((s == "是").sum())),
        )
        .reset_index()
        .sort_values(["新一级类", "记录数"], ascending=[True, False])
    )
    taxonomy.to_csv(TAXONOMY_TABLE, index=False, encoding="utf-8-sig")

    major = (
        df.groupby("新一级类", dropna=False)
        .agg(
            记录数=("产品名称", "size"),
            原始产品分类数=("原始产品分类", "nunique"),
            新二级类数=("新二级类", "nunique"),
            建议复核数=("是否建议人工复核", lambda s: int((s == "是").sum())),
            平均置信度=("分类置信度", "mean"),
        )
        .reset_index()
        .sort_values("记录数", ascending=False)
    )

    for _, row in major.iterrows():
        level1 = row["新一级类"]
        sub = df[df["新一级类"] == level1]
        top_l2 = sub["新二级类"].value_counts().head(20)
        top_raw = sub["原始产品分类"].value_counts().head(20)
        examples = sub["产品名称"].dropna().astype(str).drop_duplicates().head(30)
        review_examples = sub[sub["是否建议人工复核"] == "是"][["原始产品分类", "产品名称", "新二级类", "新三级类", "分类依据"]].head(30)

        report = [
            f"# 分类报告：{level1}",
            "",
            f"- 记录数：{int(row['记录数']):,}",
            f"- 原始产品分类数：{int(row['原始产品分类数']):,}",
            f"- 新二级类数：{int(row['新二级类数']):,}",
            f"- 建议人工复核数：{int(row['建议复核数']):,}",
            f"- 平均分类置信度：{row['平均置信度']:.3f}",
            "",
            "## Top 新二级类",
            "",
            *[f"- `{idx}`：{cnt:,}" for idx, cnt in top_l2.items()],
            "",
            "## Top 原始产品分类",
            "",
            *[f"- `{idx}`：{cnt:,}" for idx, cnt in top_raw.items()],
            "",
            "## 示例产品名称",
            "",
            *[f"- `{item}`" for item in examples],
            "",
            "## 建议人工复核示例",
            "",
        ]
        if review_examples.empty:
            report.append("- 无。")
        else:
            for _, ex in review_examples.iterrows():
                report.append(f"- 原始产品分类 `{ex['原始产品分类']}`；产品名称 `{ex['产品名称']}`；新分类 `{ex['新二级类']} / {ex['新三级类']}`；依据：{ex['分类依据']}")
        (CATEGORY_REPORT_DIR / f"{safe_filename(level1)}.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    review_count = int((df["是否建议人工复核"] == "是").sum())
    master = f"""# 产品分类体系重构与清洗总报告：{DATASET_STEM}

## 任务目标

基于 active raw dataset 的 `产品分类` 与 `产品名称`，重构一个更实用的层级化食品分类体系。该任务不是简单 exact-string grouping，而是结合原始分类、产品名称语义、食品监管/抽检分类逻辑，以及可从名称推断的加工或使用场景进行分类。

## 输入与输出

- 输入数据：`{RAW_PATH}`
- 清洗后分类数据集：`{OUTPUT_DATASET}`
- 旧分类/名称规则到新分类的 mapping table：`{MAPPING_TABLE}`
- 可复用 taxonomy table：`{TAXONOMY_TABLE}`
- 分大类报告目录：`{CATEGORY_REPORT_DIR}`

## 分类原则

- 保留原始中文字段名，并新增 `原始产品分类` 作为 traceability field。
- 新增 `新一级类`、`新二级类`、`新三级类`、`分类依据`、`分类置信度`、`是否建议人工复核`。
- 不把包含同一字的产品简单合并。例如含“米”的产品会结合 `产品分类` 与加工/使用语境区分为 `粮食及粮食制品 / 谷物原粮及初加工 / 大米`、`粮食及粮食制品 / 米制品 / 大米加工制品` 或 `餐饮食品 / 餐饮主食 / 米面熟制品`。
- 蔬菜按名称与原始分类进一步细分为叶菜类、根茎/薯芋/葱蒜类、瓜类、茄果类、豆类、芽苗类、食用菌、酱腌菜/腌渍蔬菜、干制/脱水蔬菜等。
- 餐饮类产品不一律保留在宽泛 `餐饮` 下；当产品语义明确时，重分类到更有解释力的食品大类，同时在 `分类依据` 中保留餐饮场景说明。

## 外部/通用分类依据

- 参考了市场监管食品安全抽检覆盖“蔬菜、水果、畜禽肉、米、面、油、餐饮食品”等多类食品的通用监管语境。
- 对蔬菜细分时参考了 GB 2763 食品类别中常见的叶菜类、茄果类、豆类蔬菜、根茎类和薯芋类蔬菜、食用菌等分类口径。
- 这些参考仅用于构建 practical taxonomy，不替代任何正式监管判定。

## 总体结果

- 总记录数：{len(df):,}
- 新一级类数量：{df['新一级类'].nunique():,}
- 新二级类数量：{df['新二级类'].nunique():,}
- 新三级类数量：{df['新三级类'].nunique():,}
- 建议人工复核记录数：{review_count:,}
- 建议人工复核比例：{review_count / len(df):.2%}

## 新一级类分布

| 新一级类 | 记录数 | 原始产品分类数 | 新二级类数 | 建议复核数 | 平均置信度 |
|---|---:|---:|---:|---:|---:|
"""
    for _, row in major.iterrows():
        master += f"| `{row['新一级类']}` | {int(row['记录数']):,} | {int(row['原始产品分类数']):,} | {int(row['新二级类数']):,} | {int(row['建议复核数']):,} | {row['平均置信度']:.3f} |\n"

    master += """
## 困难与模糊情况

- 原始 `餐饮` 分类中存在加工/使用场景与食品语义交叉的问题；本次尽量将语义明确的产品重分类到对应食品大类，并在 `分类依据` 中保留餐饮场景。
- `其他餐饮环节产品`、`其他粮食及其制品` 等宽泛原始分类在产品名称不足以判断时被标记为建议人工复核。
- 高度稀疏或名称泛化的产品仍可能需要人工抽样复核，以便进一步扩充规则词表。
- 本次 taxonomy 是 practical cleaning taxonomy，不等同于正式监管目录、生产许可目录或法定限量适用目录。
"""
    MASTER_REPORT.write_text(master, encoding="utf-8")

    print(f"wrote {OUTPUT_DATASET}")
    print(f"wrote {MAPPING_TABLE}")
    print(f"wrote {TAXONOMY_TABLE}")
    print(f"wrote {MASTER_REPORT}")
    print(f"wrote category reports: {CATEGORY_REPORT_DIR}")


if __name__ == "__main__":
    main()
