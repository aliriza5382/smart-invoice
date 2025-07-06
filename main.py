import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder
import io

# Şüpheli açıklama anahtar kelimeleri
suspect_keywords = [
    "unknown", "misc", "various", "test", "sample", "no description", "dummy", "undefined",
    "hizmet bedeli", "genel gider", "diğer", "vs", "çeşitli", "lost", "missing"
]

st.title("SmartInvoice – Akıllı Fatura Denetleyici")

uploaded_file = st.file_uploader(
    "Fatura Excel/CSV Dosyasını Yükle (.xlsx, .csv)", type=['xlsx', 'csv']
)
if uploaded_file:
    # Dosya okuma (ilk 5000 satır hızlıca)
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, nrows=5000)
    st.write("Yüklenen Faturalar (ilk 20 satır):")
    st.dataframe(df.head(20))

    # 1. Tutar Bazlı Anomaly Detection (Isolation Forest)
    st.subheader("Anomali Tespiti (Tutar Bazlı)")
    anomali_df = pd.DataFrame()
    if "Price" in df.columns:
        try:
            df_amount = df[df["Price"] > 0].copy()
            amounts = df_amount[["Price"]].values

            clf = IsolationForest(contamination=0.05, random_state=42)
            preds = clf.fit_predict(amounts)
            df_amount["Anomaly"] = preds
            anomali_df = df_amount[df_amount["Anomaly"] == -1]

            st.success(f"Bulunan anomali fatura sayısı: {anomali_df.shape[0]}")
            st.dataframe(anomali_df)
        except Exception as e:
            st.error(f"Anomali tespiti sırasında hata: {e}")
    else:
        st.info("Price (Tutar) sütunu bulunamadı. Anomali tespiti atlandı.")

    # 2. NLP: Şüpheli Açıklama Analizi
    st.subheader("Şüpheli Açıklama Analizi (NLP)")
    suspicious = pd.DataFrame()
    if "Description" in df.columns:
        def is_suspect(desc):
            if isinstance(desc, str):
                desc = desc.lower()
                for keyword in suspect_keywords:
                    if keyword in desc:
                        return True
                if len(desc.strip()) < 5:
                    return True
            return False

        df["SuspectDescription"] = df["Description"].apply(is_suspect)
        suspicious = df[df["SuspectDescription"]]
        st.warning(f"Şüpheli açıklama içeren fatura sayısı: {suspicious.shape[0]}")
        st.dataframe(
            suspicious[["Invoice", "Description", "Price"]] if "Price" in df.columns
            else suspicious[["Invoice", "Description"]]
        )
    else:
        st.info("Description (Açıklama) sütunu bulunamadı. NLP analizi için açıklama alanı gereklidir.")

    # 3. Tekrarlayan Açıklama & Tutar Analizi
    st.subheader("Tekrarlayan Açıklama ve Tutar Analizi")
    merged = pd.DataFrame()
    if "Description" in df.columns and "Price" in df.columns:
        df["Price_rounded"] = np.round(df["Price"], 2)
        repeated = df.groupby(["Description", "Price_rounded"]).size().reset_index(name='RepeatCount')
        repeated = repeated[repeated["RepeatCount"] >= 2]
        merged = df.merge(repeated, on=["Description", "Price_rounded"])
        merged = merged.sort_values(["Description", "Price_rounded", "Invoice"])
        st.info(f"Tekrarlayan açıklama ve benzer tutara sahip fatura sayısı: {merged.shape[0]}")
        st.dataframe(merged[["Invoice", "Description", "Price", "RepeatCount"]])
    else:
        st.info("Description veya Price alanı bulunamadı. Tekrarlayan analiz yapılamadı.")

    # 4. Gelişmiş Anomaly Detection: Çoklu Özellik
    st.subheader("Gelişmiş Anomali Tespiti (Çoklu Özellik)")
    advanced_anom = pd.DataFrame()
    if all(x in df.columns for x in ["Price", "Quantity", "Customer ID", "Description"]):
        df["DescLength"] = df["Description"].apply(lambda x: len(str(x)) if pd.notnull(x) else 0)
        le = LabelEncoder()
        df["CustomerID_Label"] = le.fit_transform(df["Customer ID"].astype(str))
        X = df[["Price", "Quantity", "DescLength", "CustomerID_Label"]].values

        clf2 = IsolationForest(contamination=0.05, random_state=42)
        preds2 = clf2.fit_predict(X)
        df["AdvancedAnomaly"] = preds2
        advanced_anom = df[df["AdvancedAnomaly"] == -1]

        st.success(f"Gelişmiş anomaly detection ile bulunan anomali fatura sayısı: {advanced_anom.shape[0]}")
        st.dataframe(
            advanced_anom[["Invoice", "Customer ID", "Description", "Price", "Quantity", "DescLength"]]
        )
    else:
        st.info("Price, Quantity, Customer ID ve Description alanları olmadan gelişmiş anomaly detection yapılamaz.")

    # 5. Müşteri/Firma Bazında Lokal Anomali Tespiti
    st.subheader("Müşteri/Firma Bazında Lokal Anomali Tespiti")
    result = pd.DataFrame()
    if "Price" in df.columns and "Customer ID" in df.columns:
        anomalies_firma = []
        for cid, group in df.groupby("Customer ID"):
            prices = group["Price"]
            mean = prices.mean()
            std = prices.std()
            if pd.notnull(std) and std > 0:
                anomalous = group[(prices > mean + 2*std) | (prices < mean - 2*std)]
                anomalies_firma.append(anomalous)
        if anomalies_firma:
            result = pd.concat(anomalies_firma)
            st.success(f"Müşteri/Firma bazında bulunan anomaly sayısı: {result.shape[0]}")
            st.dataframe(result[["Invoice", "Customer ID", "Description", "Price"]])
        else:
            st.info("Müşteri bazında istatistiksel anomaly bulunamadı.")
    else:
        st.info("Customer ID ve Price alanı olmadan müşteri bazlı anomaly detection yapılamaz.")

    # ---- PROFESYONEL EXCEL RAPOR BUTONU ----
    def export_excel_report(dfs_dict):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for sheet_name, df_out in dfs_dict.items():
                # Boşsa sadece başlık yazılır, sorun olmaz
                df_out.to_excel(writer, index=False, sheet_name=sheet_name)
                worksheet = writer.sheets[sheet_name]
                for i, col in enumerate(df_out.columns):
                    max_len = max(df_out[col].astype(str).map(len).max(), len(col))
                    worksheet.set_column(i, i, max_len + 2)
            # Giriş sekmesi ekle
            pd.DataFrame({
                "Rapor": ["Bu dosya SmartInvoice tarafından otomatik oluşturulmuştur."],
                "Açıklama": [
                    "Her analiz sonucu ayrı bir sekmede, başlıkları ve otomatik kolon genişliğiyle sunulmuştur."
                ]
            }).to_excel(writer, sheet_name="Rapor Hakkında", index=False)
        return output.getvalue()

    excel_report = export_excel_report({
        "Tutar Bazlı Anomali": anomali_df,
        "Şüpheli Açıklamalar": suspicious,
        "Tekrarlayan Faturalar": merged,
        "Gelişmiş Anomali": advanced_anom,
        "Müşteri Bazlı Anomali": result
    })

    st.download_button(
        label="Tüm Analizleri Düzenli Excel Raporu Olarak İndir",
        data=excel_report,
        file_name="SmartInvoice_Rapor.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
