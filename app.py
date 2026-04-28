# import streamlit as st
# from openpyxl import load_workbook
# from openpyxl.utils import get_column_letter
# import io

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(page_title="Add Price Columns", page_icon="💎", layout="centered")

# st.title("💎 Add Updated Price & Difference")

# st.write("Upload your Excel file → Download updated file with formula")

# # ---------------- FILE UPLOAD ----------------
# file = st.file_uploader("Upload Excel File", type=["xlsx"])

# # ---------------- FUNCTION ----------------
# def process_file(file):
#     wb = load_workbook(file)
#     ws = wb.active

#     # Detect Cost / Cts column
#     headers = [cell.value for cell in ws[1]]
#     cost_col = None

#     for i, h in enumerate(headers):
#         if h and "cost" in str(h).lower() and "cts" in str(h).lower():
#             cost_col = i + 1
#             break

#     if cost_col is None:
#         raise Exception("❌ 'Cost / Cts.' column not found")

#     # Add new columns
#     last_col = ws.max_column
#     upd_col = last_col + 1
#     diff_col = last_col + 2

#     ws.cell(1, upd_col).value = "Updated Price"
#     ws.cell(1, diff_col).value = "Difference"

#     # Column letters
#     cost_letter = get_column_letter(cost_col)
#     upd_letter = get_column_letter(upd_col)

#     # Apply formula
#     for row in range(2, ws.max_row + 1):
#         formula = f"=-ROUND(({cost_letter}{row}-{upd_letter}{row})/{cost_letter}{row}*100,2)"
#         ws.cell(row, diff_col).value = formula

#     # Save file
#     output = io.BytesIO()
#     wb.save(output)
#     output.seek(0)

#     return output

# # ---------------- PROCESS ----------------
# if file:
#     try:
#         output = process_file(file)

#         st.success("✅ Columns added successfully!")

#         st.download_button(
#             label="📥 Download Updated File",
#             data=output,
#             file_name="updated_price_file.xlsx"
#         )

#     except Exception as e:
#         st.error(str(e))












# import streamlit as st
# from openpyxl import load_workbook
# from openpyxl.utils import get_column_letter
# import io

# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(page_title="Diamond Smart Repricing", page_icon="💎", layout="centered")

# st.title("💎 Diamond Smart Repricing Tool")
# st.write("Upload file → Select multiple shapes → Process → Download")

# # ---------------- FILE UPLOAD ----------------
# file = st.file_uploader("Upload Excel File", type=["xlsx"])


# # ---------------------------------------------------
# # GET SHAPES FROM FILE
# # ---------------------------------------------------
# def get_shapes(uploaded_file):
#     wb = load_workbook(uploaded_file, data_only=True)
#     ws = wb.active

#     headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

#     shape_col = None

#     for i, h in enumerate(headers):
#         if h.lower() == "shape":
#             shape_col = i + 1
#             break

#     if shape_col is None:
#         return []

#     shapes = set()

#     for row in range(2, ws.max_row + 1):
#         val = ws.cell(row, shape_col).value
#         if val:
#             shapes.add(str(val).strip().upper())

#     return sorted(list(shapes))


# # ---------------------------------------------------
# # UI AFTER FILE UPLOAD
# # ---------------------------------------------------
# if file:

#     shape_list = get_shapes(file)

#     st.subheader("Answer Questions")

#     selected_shapes = st.multiselect(
#         "1️⃣ Select Shape(s) you want to work / reprice",
#         shape_list,
#         default=shape_list
#     )

#     fancy_option = st.radio(
#         "2️⃣ Do you want to work with Fancy Colors?",
#         ["Yes", "No"]
#     )

#     lot_option = st.radio(
#         "3️⃣ Remove stones starts with VJ / VP OR ends with A / B / U ?",
#         ["Yes", "No"]
#     )

#     six_cts_option = st.radio(
#         "4️⃣ Do You want 6.00 <= Stone ?",
#         ["Yes", "No"]
#     )

#     run_btn = st.button("🚀 Process File")


# # ---------------------------------------------------
# # PROCESS FILE
# # ---------------------------------------------------
#     if run_btn:

#         try:
#             wb = load_workbook(file)
#             ws = wb.active

#             headers = [str(c.value).strip() if c.value else "" for c in ws[1]]

#             cost_col = None
#             color_col = None
#             shape_col = None
#             lot_col = None

#             for i, h in enumerate(headers):
#                 h_low = h.lower()

#                 if "cost" in h_low and "cts" in h_low:
#                     cost_col = i + 1

#                 elif h_low == "color":
#                     color_col = i + 1

#                 elif h_low == "shape":
#                     shape_col = i + 1

#                 elif h_low == "lot #":
#                     lot_col = i + 1

#             if cost_col is None:
#                 st.error("❌ Cost / Cts column not found")
#                 st.stop()

#             rows_to_delete = []

#             # --------------------------------
#             # FILTER ROWS
#             # --------------------------------
#             for row in range(2, ws.max_row + 1):

#                 delete_row = False

#                 # 1 MULTIPLE SHAPE FILTER
#                 if shape_col and selected_shapes:
#                     shp = ws.cell(row, shape_col).value
#                     shp = str(shp).strip().upper() if shp else ""

#                     if shp not in selected_shapes:
#                         delete_row = True

#                 # 2 FANCY COLOR FILTER
#                 if not delete_row and fancy_option == "No" and color_col:
#                     clr = ws.cell(row, color_col).value
#                     clr = str(clr).strip().upper() if clr else ""

#                     if clr not in ["D", "E", "F", "G", "H", "I"]:
#                         delete_row = True

#                 # 3 LOT FILTER
#                 if not delete_row and lot_option == "Yes" and lot_col:
#                     lot = ws.cell(row, lot_col).value
#                     lot = str(lot).strip().upper() if lot else ""

#                     if (
#                         lot.startswith("VJ")
#                         or lot.startswith("VP")
#                         or lot.endswith("A")
#                         or lot.endswith("B")
#                         or lot.endswith("U")
#                     ):
#                         delete_row = True

#                 # 4 REMOVE 6.00+ STONES
#                 if not delete_row and six_cts_option == "No":
#                     val = ws.cell(row, cost_col).value

#                     try:
#                         num = float(val)
#                         if num >= 6.00:
#                             delete_row = True
#                     except:
#                         pass

#                 if delete_row:
#                     rows_to_delete.append(row)

#             # DELETE ROWS REVERSE
#             for r in reversed(rows_to_delete):
#                 ws.delete_rows(r)

#             # --------------------------------
#             # ADD UPDATED PRICE + DIFFERENCE
#             # --------------------------------
#             last_col = ws.max_column
#             upd_col = last_col + 1
#             diff_col = last_col + 2

#             ws.cell(1, upd_col).value = "Updated Price"
#             ws.cell(1, diff_col).value = "Difference"

#             cost_letter = get_column_letter(cost_col)
#             upd_letter = get_column_letter(upd_col)

#             for row in range(2, ws.max_row + 1):
#                 formula = f"=-ROUND(({cost_letter}{row}-{upd_letter}{row})/{cost_letter}{row}*100,2)"
#                 ws.cell(row, diff_col).value = formula

#             # --------------------------------
#             # SAVE FILE
#             # --------------------------------
#             output = io.BytesIO()
#             wb.save(output)
#             output.seek(0)

#             st.success("✅ File Processed Successfully!")

#             st.download_button(
#                 label="📥 Download Final File",
#                 data=output,
#                 file_name="diamond_final_output.xlsx"
#             )

#         except Exception as e:
#             st.error(str(e))



# import streamlit as st
# import pandas as pd
# import io
# import zipfile
# from openpyxl import load_workbook
# from openpyxl.utils import get_column_letter

# # -------------------------------------------------
# # PAGE CONFIG
# # -------------------------------------------------
# st.set_page_config(page_title="Diamond Smart Repricing PRO", page_icon="💎", layout="wide")

# st.title("💎 Diamond Smart Repricing PRO")
# st.write("⚡ Fast Version | Upload → Filter → Formula → Download")

# # -------------------------------------------------
# # FILE UPLOAD
# # -------------------------------------------------
# file = st.file_uploader("Upload Excel File", type=["xlsx"])


# # -------------------------------------------------
# # TEAM SHAPE MATCHING
# # -------------------------------------------------
# def get_team(shape):
#     s = str(shape).upper()

#     if any(x in s for x in ["RBC", "ROUND", "ASSCHER", "PRINCESS"]):
#         return "Love"

#     elif any(x in s for x in ["CUSHION MODIFIED", "CUSHION BRILLIANT", "HEART"]):
#         return "Harshali"

#     elif any(x in s for x in ["OVAL", "EMERALD"]):
#         return "Gautam"

#     elif any(x in s for x in ["PEAR", "RADIANT"]):
#         return "Milan"

#     return "Others"


# # -------------------------------------------------
# # ADD EXCEL FORMULA
# # -------------------------------------------------
# def add_formula_excel(df, cost_col_name):

#     output = io.BytesIO()

#     # Save pandas first
#     with pd.ExcelWriter(output, engine="openpyxl") as writer:
#         df.to_excel(writer, index=False, sheet_name="Sheet1")

#     output.seek(0)

#     # Load with openpyxl
#     wb = load_workbook(output)
#     ws = wb.active

#     headers = [cell.value for cell in ws[1]]

#     cost_col = headers.index(cost_col_name) + 1
#     upd_col = len(headers) + 1
#     diff_col = len(headers) + 2

#     ws.cell(1, upd_col).value = "Updated Price"
#     ws.cell(1, diff_col).value = "Difference"

#     cost_letter = get_column_letter(cost_col)
#     upd_letter = get_column_letter(upd_col)

#     for row in range(2, ws.max_row + 1):
#         ws.cell(row, diff_col).value = f"=-ROUND(({cost_letter}{row}-{upd_letter}{row})/{cost_letter}{row}*100,2)"

#     final = io.BytesIO()
#     wb.save(final)
#     final.seek(0)

#     return final


# # -------------------------------------------------
# # MAIN APP
# # -------------------------------------------------
# if file:

#     with st.spinner("⚡ Reading File..."):
#         df = pd.read_excel(file)

#     df.columns = df.columns.str.strip()

#     # Detect columns
#     shape_col = "Shape"
#     color_col = "Color"
#     lot_col = "Lot #"

#     cost_col = None
#     for c in df.columns:
#         if "cost" in c.lower() and "cts" in c.lower():
#             cost_col = c
#             break

#     if cost_col is None:
#         st.error("❌ Cost / Cts column not found")
#         st.stop()

#     # -------------------------------------------------
#     # QUESTIONS
#     # -------------------------------------------------
#     shapes = sorted(df[shape_col].dropna().astype(str).str.upper().unique())

#     selected_shapes = st.multiselect(
#         "1️⃣ Select Shape(s)",
#         shapes,
#         default=shapes
#     )

#     fancy_option = st.radio(
#         "2️⃣ Fancy Colors?",
#         ["Yes", "No"]
#     )

#     lot_option = st.radio(
#         "3️⃣ Remove VP/VJ Starts or Ends A/B ?",
#         ["Yes", "No"]
#     )

#     six_option = st.radio(
#         "4️⃣ Keep Only 6.00+ Stones?",
#         ["Yes", "No"]
#     )

#     col1, col2 = st.columns(2)

#     process_btn = col1.button("🚀 Process File")
#     team_btn = col2.button("👥 Create Team Files")


# # -------------------------------------------------
# # PROCESS FILE
# # -------------------------------------------------
#     if process_btn:

#         with st.spinner("⚡ Processing..."):

#             data = df.copy()

#             # Shape Filter
#             data = data[data[shape_col].astype(str).str.upper().isin(selected_shapes)]

#             # Fancy Color Filter
#             if fancy_option == "No":
#                 data = data[data[color_col].astype(str).str.upper().isin(["D","E","F","G","H","I"])]

#             # Lot Filter
#             if lot_option == "Yes":
#                 lot = data[lot_col].astype(str).str.upper()

#                 data = data[
#                     ~(
#                         lot.str.startswith("VP") |
#                         lot.str.startswith("VJ") |
#                         lot.str.endswith("A") |
#                         lot.str.endswith("B")
#                     )
#                 ]

#             # 6.00+
#             if six_option == "Yes":
#                 data = data[pd.to_numeric(data[cost_col], errors="coerce") >= 6.00]

#             final_file = add_formula_excel(data, cost_col)

#         st.success("✅ Ready!")

#         st.download_button(
#             "📥 Download Final File",
#             data=final_file,
#             file_name="diamond_output.xlsx"
#         )


# # -------------------------------------------------
# # TEAM FILES
# # -------------------------------------------------
#     if team_btn:

#         with st.spinner("⚡ Creating Team Files..."):

#             data = df.copy()

#             data["Team"] = data[shape_col].apply(get_team)

#             zip_buffer = io.BytesIO()

#             with zipfile.ZipFile(zip_buffer, "w") as zf:

#                 for team in ["Love", "Harshali", "Gautam", "Milan"]:

#                     team_df = data[data["Team"] == team].drop(columns=["Team"])

#                     if len(team_df) > 0:

#                         file_data = add_formula_excel(team_df, cost_col)
#                         zf.writestr(f"{team}.xlsx", file_data.read())

#             zip_buffer.seek(0)

#         st.success("✅ Team Files Ready!")

#         st.download_button(
#             "📦 Download Team ZIP",
#             data=zip_buffer,
#             file_name="Repricing_Team_Files.zip"
#         )

        


# import streamlit as st
# import pandas as pd
# import io
# import zipfile
# from openpyxl import load_workbook
# from openpyxl.utils import get_column_letter

# # -------------------------------------------------
# # PAGE CONFIG
# # -------------------------------------------------
# st.set_page_config(page_title="Diamond Smart Repricing PRO", page_icon="💎", layout="wide")

# st.title("💎 Diamond Smart Repricing PRO")
# st.write("⚡ Fast Version | Upload → Filter → Formula → Download")

# # -------------------------------------------------
# # FILE UPLOAD
# # -------------------------------------------------
# file = st.file_uploader("Upload Excel File", type=["xlsx"])

# # -------------------------------------------------
# # TEAM SHAPE MATCHING
# # -------------------------------------------------
# TEAM_SHAPES = {
#     "Love": ["RBC", "ROUND", "ASSCHER", "PRINCESS"],
#     "Harshali": ["CUSHION MODIFIED", "CUSHION BRILLIANT", "HEART"],
#     "Gautam": ["OVAL", "EMERALD"],
#     "Milan": ["PEAR", "RADIANT"]
# }

# def get_team(shape):
#     s = str(shape).upper()

#     for team, shape_list in TEAM_SHAPES.items():
#         if any(x in s for x in shape_list):
#             return team

#     return "Others"

# # -------------------------------------------------
# # ADD EXCEL FORMULA
# # -------------------------------------------------
# def add_formula_excel(df, cost_col_name):

#     output = io.BytesIO()

#     with pd.ExcelWriter(output, engine="openpyxl") as writer:
#         df.to_excel(writer, index=False, sheet_name="Sheet1")

#     output.seek(0)

#     wb = load_workbook(output)
#     ws = wb.active

#     headers = [cell.value for cell in ws[1]]

#     cost_col = headers.index(cost_col_name) + 1
#     upd_col = len(headers) + 1
#     diff_col = len(headers) + 2

#     ws.cell(1, upd_col).value = "Updated Price"
#     ws.cell(1, diff_col).value = "Difference"

#     cost_letter = get_column_letter(cost_col)
#     upd_letter = get_column_letter(upd_col)

#     for row in range(2, ws.max_row + 1):
#         ws.cell(row, diff_col).value = f"=-ROUND(({cost_letter}{row}-{upd_letter}{row})/{cost_letter}{row}*100,2)"

#     final = io.BytesIO()
#     wb.save(final)
#     final.seek(0)

#     return final

# # -------------------------------------------------
# # FILTER FUNCTION
# # -------------------------------------------------
# def apply_filters(data, shapes_selected, fancy_option, lot_option, six_option):

#     data = data[data[shape_col].astype(str).str.upper().isin(shapes_selected)]

#     if fancy_option == "No":
#         data = data[data[color_col].astype(str).str.upper().isin(["D", "E", "F", "G", "H", "I"])]

#     if lot_option == "Yes":
#         lot = data[lot_col].astype(str).str.upper()

#         data = data[
#             ~(
#                 lot.str.startswith("VP") |
#                 lot.str.startswith("VJ") |
#                 lot.str.endswith("A") |
#                 lot.str.endswith("B")
#             )
#         ]

#     if six_option == "Yes":
#         data = data[pd.to_numeric(data[cost_col], errors="coerce") >= 6.00]

#     return data

# # -------------------------------------------------
# # MAIN APP
# # -------------------------------------------------
# if file:

#     df = pd.read_excel(file)
#     df.columns = df.columns.str.strip()

#     shape_col = "Shape"
#     color_col = "Color"
#     lot_col = "Lot #"

#     cost_col = None
#     for c in df.columns:
#         if "cost" in c.lower() and "cts" in c.lower():
#             cost_col = c
#             break

#     if cost_col is None:
#         st.error("Cost/Cts column not found")
#         st.stop()

#     all_shapes = sorted(df[shape_col].dropna().astype(str).str.upper().unique())

#     # -------------------------------------------------
#     # FIRST QUESTION
#     # -------------------------------------------------
#     team_mode = st.radio(
#         "1️⃣ Do you want to create file for Repricing Team?",
#         ["Yes", "No"]
#     )

#     # -------------------------------------------------
#     # SHAPE SELECTION
#     # -------------------------------------------------
#     if team_mode == "No":
#         selected_shapes = st.multiselect(
#             "2️⃣ Select Shape(s)",
#             all_shapes,
#             default=all_shapes
#         )
#     else:
#         selected_shapes = all_shapes

#     # -------------------------------------------------
#     # OTHER QUESTIONS
#     # -------------------------------------------------
#     fancy_option = st.radio("3️⃣ Fancy Colors?", ["Yes", "No"])
#     lot_option = st.radio("4️⃣ Remove VP/VJ Starts or Ends A/B ?", ["Yes", "No"])
#     six_option = st.radio("5️⃣ Keep Only 6.00+ Stones?", ["Yes", "No"])

#     if st.button("🚀 Process & Download"):

#         # -------------------------------------------------
#         # TEAM MODE
#         # -------------------------------------------------
#         if team_mode == "Yes":

#             zip_buffer = io.BytesIO()

#             with zipfile.ZipFile(zip_buffer, "w") as zf:

#                 for team, team_shapes in TEAM_SHAPES.items():

#                     team_df = df.copy()

#                     # shapes assigned automatically
#                     shapes_for_team = [
#                         s for s in all_shapes
#                         if any(x in s for x in team_shapes)
#                     ]

#                     team_df = apply_filters(
#                         team_df,
#                         shapes_for_team,
#                         fancy_option,
#                         lot_option,
#                         six_option
#                     )

#                     if len(team_df) > 0:
#                         file_data = add_formula_excel(team_df, cost_col)
#                         zf.writestr(f"{team}.xlsx", file_data.read())

#             zip_buffer.seek(0)

#             st.download_button(
#                 "📦 Download Team ZIP",
#                 data=zip_buffer,
#                 file_name="Repricing_Team_Files.zip"
#             )

#         # -------------------------------------------------
#         # MANUAL MODE
#         # -------------------------------------------------
#         else:

#             data = df.copy()

#             data = apply_filters(
#                 data,
#                 selected_shapes,
#                 fancy_option,
#                 lot_option,
#                 six_option
#             )

#             final_file = add_formula_excel(data, cost_col)

#             st.download_button(
#                 "📥 Download Final File",
#                 data=final_file,
#                 file_name="diamond_output.xlsx"
#             )


import streamlit as st
import pandas as pd
import io
import zipfile
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Diamond Smart Repricing PRO", page_icon="💎", layout="wide")

st.title("💎 Diamond Smart Repricing PRO")
st.write("⚡ Fast Version | Upload → Filter → Formula → Download")

# -------------------------------------------------
# FILE UPLOAD
# -------------------------------------------------
file = st.file_uploader("Upload Excel File", type=["xlsx"])

# -------------------------------------------------
# TEAM SHAPE MATCHING
# -------------------------------------------------
TEAM_SHAPES = {
    "Love": ["RBC", "ROUND", "ASSCHER", "PRINCESS"],
    "Harshali": ["CUSHION MODIFIED", "CUSHION BRILLIANT", "HEART"],
    "Gautam": ["OVAL", "EMERALD"],
    "Milan": ["PEAR", "RADIANT"]
}

def get_team(shape):
    s = str(shape).upper()

    for team, shape_list in TEAM_SHAPES.items():
        if any(x in s for x in shape_list):
            return team

    return "Others"

# -------------------------------------------------
# ADD EXCEL FORMULA
# -------------------------------------------------
def add_formula_excel(df, cost_col_name):

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")

    output.seek(0)

    wb = load_workbook(output)
    ws = wb.active

    headers = [cell.value for cell in ws[1]]

    cost_col = headers.index(cost_col_name) + 1
    upd_col = len(headers) + 1
    diff_col = len(headers) + 2

    ws.cell(1, upd_col).value = "Updated Price"
    ws.cell(1, diff_col).value = "Difference"

    cost_letter = get_column_letter(cost_col)
    upd_letter = get_column_letter(upd_col)

    for row in range(2, ws.max_row + 1):
        ws.cell(row, diff_col).value = f"=-ROUND(({cost_letter}{row}-{upd_letter}{row})/{cost_letter}{row}*100,2)"

    final = io.BytesIO()
    wb.save(final)
    final.seek(0)

    return final

# -------------------------------------------------
# FILTER FUNCTION
# -------------------------------------------------
def apply_filters(data, shapes_selected, fancy_option, lot_option, six_option):

    data = data[data[shape_col].astype(str).str.upper().isin(shapes_selected)]

    if fancy_option == "No":
        data = data[data[color_col].astype(str).str.upper().isin(["D", "E", "F", "G", "H", "I"])]

    if lot_option == "Yes":
        lot = data[lot_col].astype(str).str.upper()

        data = data[
            ~(
                lot.str.startswith("VP") |
                lot.str.startswith("VJ") |
                lot.str.endswith("A") |
                lot.str.endswith("B")
            )
        ]

    if six_option == "Yes":
        data = data[pd.to_numeric(data[cost_col], errors="coerce") >= 6.00]

    return data

# -------------------------------------------------
# MAIN APP
# -------------------------------------------------
if file:

    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()

    shape_col = "Shape"
    color_col = "Color"
    lot_col = "Lot #"

    cost_col = None
    for c in df.columns:
        if "cost" in c.lower() and "cts" in c.lower():
            cost_col = c
            break

    if cost_col is None:
        st.error("Cost/Cts column not found")
        st.stop()

    all_shapes = sorted(df[shape_col].dropna().astype(str).str.upper().unique())

    # -------------------------------------------------
    # FIRST QUESTION
    # -------------------------------------------------
    team_mode = st.radio(
        "1️⃣ Do you want to create file for Repricing Team?",
        ["Yes", "No"]
    )

    # -------------------------------------------------
    # SHAPE SELECTION
    # -------------------------------------------------
    if team_mode == "No":
        selected_shapes = st.multiselect(
            "2️⃣ Select Shape(s)",
            all_shapes,
            default=all_shapes
        )
    else:
        selected_shapes = all_shapes

    # -------------------------------------------------
    # OTHER QUESTIONS
    # -------------------------------------------------
    fancy_option = st.radio("3️⃣ Fancy Colors?", ["Yes", "No"])
    lot_option = st.radio("4️⃣ Remove VP/VJ Starts or Ends A/B ?", ["Yes", "No"])
    six_option = st.radio("5️⃣ Keep Only 6.00+ Stones?", ["Yes", "No"])

    if st.button("🚀 Process & Download"):

        # -------------------------------------------------
        # TEAM MODE
        # -------------------------------------------------
        if team_mode == "Yes":

            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, "w") as zf:

                for team, team_shapes in TEAM_SHAPES.items():

                    team_df = df.copy()

                    # shapes assigned automatically
                    shapes_for_team = [
                        s for s in all_shapes
                        if any(x in s for x in team_shapes)
                    ]

                    team_df = apply_filters(
                        team_df,
                        shapes_for_team,
                        fancy_option,
                        lot_option,
                        six_option
                    )

                    if len(team_df) > 0:
                        file_data = add_formula_excel(team_df, cost_col)
                        zf.writestr(f"{team}.xlsx", file_data.read())

            zip_buffer.seek(0)

            st.download_button(
                "📦 Download Team ZIP",
                data=zip_buffer,
                file_name="Repricing_Team_Files.zip"
            )

        # -------------------------------------------------
        # MANUAL MODE
        # -------------------------------------------------
        else:

            data = df.copy()

            data = apply_filters(
                data,
                selected_shapes,
                fancy_option,
                lot_option,
                six_option
            )

            final_file = add_formula_excel(data, cost_col)

            st.download_button(
                "📥 Download Final File",
                data=final_file,
                file_name="diamond_output.xlsx"
            )