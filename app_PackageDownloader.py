import streamlit as st
import subprocess
import tempfile
import shutil
import os
import sys

# --- UIの設定 ---
st.set_page_config(page_title="Offline Package Downloader", page_icon="📦")
st.title("📦 Offline Package Downloader")
st.write("`requirements.txt`をアップロードすると、指定したOS・Pythonバージョン用のオフラインインストール用パッケージ（wheel）を収集し、ZIP化してダウンロードできます。")
st.markdown("---")
st.write("【ZIPファイルの解凍】")
st.write("`unzip package_xxx-xxx_pyxxx.zip -d offline_packages`")
st.write("【ライプライリのインポート】")
st.write("`pip install --no-index --find-links=./offline_packages -r requirements.txt`")
st.markdown("---")

# --- 設定パラメータの入力 ---
col1, col2 = st.columns(2)
with col1:
    target_os = st.selectbox(
        "ターゲットOSを選択",
        ["Windows (64bit)", "Mac (Apple Silicon)", "Mac (Intel)", "Linux (x86_64)"]
    )
with col2:
    target_py_version = st.selectbox(
        "ターゲットのPythonバージョン",
        ["3.10", "3.11", "3.12"]
    )

uploaded_file = st.file_uploader("requirements.txt をアップロードしてください", type=["txt"])

# OSごとのプラットフォームタグの定義
platform_map = {
    "Windows (64bit)": ("win", "win_amd64"),
    "Mac (Apple Silicon)": ("mac-arm", "macosx_11_0_arm64"),
    "Mac (Intel)": ("mac-intel", "macosx_10_15_x86_64"),
    "Linux (x86_64)": ("linux", "manylinux2014_x86_64")
}

if uploaded_file is not None:
    # ファイルの中身を表示（確認用）
    with st.expander("アップロードされた requirements.txt の内容を確認"):
        st.code(uploaded_file.getvalue().decode("utf-8"))

    if st.button("パッケージを収集してZIPを作成"):
        # requirements.txt のサイズ制限チェック（5MB）
        if len(uploaded_file.getvalue()) > 5 * 1024 * 1024:
            st.error("requirements.txt は 5MB を超えています。")
            # 処理を中断
            st.stop()
            # 処理を中断
        else:
            # 処理状態を表示するプレースホルダー
            status_text = st.empty()
            progress_bar = st.progress(0)

            os_prefix, platform_tag = platform_map[target_os]
            py_ver_short = target_py_version.replace(".", "")  # "3.10" -> "310"

        status_text.info("一時ディレクトリを準備中...")
        progress_bar.progress(10)

        # 一時ディレクトリの作成（ブロックを抜けると自動削除されます）
        with tempfile.TemporaryDirectory() as temp_dir:
            req_file_path = os.path.join(temp_dir, "requirements.txt")
            download_dir = os.path.join(temp_dir, "offline_packages")
            os.makedirs(download_dir, exist_ok=True)

            # アップロードされたファイルを一時ディレクトリに保存
            with open(req_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            status_text.info(f"{target_os} (Python {target_py_version}) 用のパッケージをダウンロードしています...\n\n※パッケージの数やサイズによっては数分かかる場合があります。")
            progress_bar.progress(30)

            # pip download コマンドの構築
            # すべて Windows とそれ以外で同じ pip download コマンドを使用
            cmd = [
                "pip", "download", "-r", req_file_path,
                "-d", download_dir,
                "--python-version", py_ver_short,
                "--implementation", "cp",
                "--platform", platform_tag,
                "--only-binary=:all:"
            ]

            # サブプロセスでコマンドを実行
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
            except FileNotFoundError as e:
                progress_bar.empty()
                status_text.error("❌ pip が見つかりません。Python の環境を確認してください。")
                st.exception(e)
                st.stop()
            except Exception as e:
                progress_bar.empty()
                status_text.error("❌ パッケージダウンロード中に予期せぬエラーが発生しました。")
                st.exception(e)
                st.stop()

            if result.returncode != 0:
                progress_bar.empty()
                status_text.error("❌ パッケージのダウンロード中にエラーが発生しました。")
                st.warning("**よくある原因:** 指定したOS・Pythonバージョン用の\"コンパイル済みバイナリ(wheel)\"が提供されていないライブラリが含まれています。")
                with st.expander("詳細なエラーログを見る"):
                    st.code(result.stderr)
            else:
                progress_bar.progress(80)
                status_text.info("ダウンロード完了。ZIP圧縮を行っています...")

                # ZIPファイルの作成
                zip_base_name = os.path.join(temp_dir, f"packages_{os_prefix}_py{py_ver_short}")
                shutil.make_archive(zip_base_name, 'zip', download_dir)
                zip_file_path = f"{zip_base_name}.zip"

                progress_bar.progress(100)
                status_text.success("✅ ZIPファイルの作成が完了しました！下のボタンからダウンロードしてください。")

                # ZIPファイルをメモリに読み込んでダウンロードボタンを生成
                # (Streamlitの仕様上、temp_dirが消える前にデータを保持しておく必要があるため)
                with open(zip_file_path, "rb") as fp:
                    zip_data = fp.read()

                st.download_button(
                    label="📦 ZIPファイルをダウンロード",
                    data=zip_data,
                    file_name=f"packages_{os_prefix}_py{py_ver_short}.zip",
                    mime="application/zip",
                                    )