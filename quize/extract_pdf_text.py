from pathlib import Path

from pypdf import PdfReader


FILES = [
    ("/Users/gongpengxiang/Downloads/1_1_MH6827_intro.pdf", "1_1_MH6827_intro.txt"),
    ("/Users/gongpengxiang/Downloads/1_2_DB_OLTP_Relational_model.pdf", "1_2_DB_OLTP_Relational_model.txt"),
    ("/Users/gongpengxiang/Downloads/1_3_ERD_database_design.pdf", "1_3_ERD_database_design.txt"),
    ("/Users/gongpengxiang/Downloads/1_4_database_normalization.pdf", "1_4_database_normalization.txt"),
    ("/Users/gongpengxiang/Downloads/2_1_SQL_basics.pdf", "2_1_SQL_basics.txt"),
    ("/Users/gongpengxiang/Downloads/2_2_SQL_join.pdf", "2_2_SQL_join.txt"),
    ("/Users/gongpengxiang/Downloads/2_2_SQL_join_examples.pdf", "2_2_SQL_join_examples.txt"),
    ("/Users/gongpengxiang/Downloads/2_3_SQL_aggregation.pdf", "2_3_SQL_aggregation.txt"),
    ("/Users/gongpengxiang/Downloads/2_4_1_SQL_more_sql.pdf", "2_4_1_SQL_more_sql.txt"),
    ("/Users/gongpengxiang/Downloads/2_4_2_SQL_Subqueries_and_CTEs.pdf", "2_4_2_SQL_Subqueries_and_CTEs.txt"),
    ("/Users/gongpengxiang/Downloads/3_1_dw-intro.pdf", "3_1_dw-intro.txt"),
    ("/Users/gongpengxiang/Downloads/3_2_dw-dimensional_model.pdf", "3_2_dw-dimensional_model.txt"),
    ("/Users/gongpengxiang/Downloads/3_3_dw_dimensions_tables.pdf", "3_3_dw_dimensions_tables.txt"),
    ("/Users/gongpengxiang/Downloads/4_1_ETL.pdf", "4_1_ETL.txt"),
    ("/Users/gongpengxiang/Downloads/4_2_ETL_example.pdf", "4_2_ETL_example.txt"),
    (
        "/Users/gongpengxiang/Library/Containers/com.tencent.xinWeChat/Data/Library/Caches/com.tencent.xinWeChat/2.0b4.0.9/618a2f3756fe2c12652985df36eb6576/SaveTemp/33c64755e931d644f1c5b12a7d74b0d8/sample_questions.pdf",
        "sample_questions.txt",
    ),
]


def main() -> None:
    out_dir = Path(__file__).with_name("extracted_text")
    out_dir.mkdir(parents=True, exist_ok=True)

    for src, name in FILES:
        reader = PdfReader(src)
        parts = []
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            parts.append(f"--- PAGE {page_num} ---\n{text}")
        (out_dir / name).write_text("\n\n".join(parts), encoding="utf-8")
        print(f"{name}: {len(reader.pages)} pages, {sum(len(p) for p in parts)} chars")


if __name__ == "__main__":
    main()
