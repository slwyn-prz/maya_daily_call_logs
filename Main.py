import streamlit as st
import polars as pl
from io import BytesIO

st.title("MAYA Daily Call Logs")

remark_report_file = st.file_uploader("Upload Daily Remark Report", type="xlsx")

if remark_report_file is not None:
    remark_report = pl.read_excel(remark_report_file)

    filter_status = ["ABORT", "BULK SMS SENT", "NEW", "REACTIVE", "SMS SENT"]

    filtered_remark_report = remark_report.filter(~(pl.col("Status").is_in(filter_status))).sort("Time")
    filtered_remark_report = filtered_remark_report.with_columns(
        pl.arange(1, filtered_remark_report.height + 1).alias("S.No")
    )

    export = BytesIO()

    filename = f"maya_call_logs_{filtered_remark_report["Date"].max()}.xlsx"

    filtered_remark_report.write_excel(
        export,
        dtype_formats={
            pl.Datetime: "mm/dd/yyyy hh:mm:ss",
            pl.Date: "mm/dd/yyyy",
            pl.Int64: "0",
            pl.Float64: "#,##0.00"
        },
        autofit=True
    )

    export.seek(0)

    st.download_button(
        label="Download Daily Call Logs",
        data=export.getvalue(),
        file_name=filename,mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )