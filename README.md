```markdown
# 📦 Offline Package Downloader

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

## 概要

`requirements.txt` ファイルをアップロードするだけで、指定した **OS** と **Pythonバージョン** 用のオフラインインストールパッケージ（wheelファイル）を自動収集し、ZIPファイルにまとめてダウンロードできるStreamlitアプリケーションです。

インターネット接続が制限された環境や、セキュリティポリシーにより外部からの直接ダウンロードが禁止されている環境でのPythonパッケージ導入を支援します。

## 特徴

- 🖥️ **マルチプラットフォーム対応**: Windows (64bit), macOS (Apple Silicon/Intel), Linux (x86_64) をサポート
- 🐍 **複数Pythonバージョン対応**: Python 3.10, 3.11, 3.12 に対応
- 📁 **簡単操作**: requirements.txtをアップロードするだけで自動処理
- ⚡ **高速ダウンロード**: pip downloadを活用した効率的なパッケージ収集
- 📦 **ZIP化自動処理**: ダウンロードしたパッケージを即座にZIPファイルに圧縮
- 🚫 **オフラインインストール用**: 収集したパッケージはインターネット接続なしでインストール可能

## 必要要件

### システム要件
- Python 3.10 以上
- pip 21.0 以上
- インターネット接続（パッケージダウンロード時のみ）

### Pythonパッケージ
```bash
pip install streamlit
```

## インストール方法

1. リポジトリをクローンまたはダウンロード:
```bash
git clone <repository-url>
cd PackageDownloader
```

2. 必要なパッケージをインストール:
```bash
pip install streamlit
```

3. アプリケーションを起動:
```bash
streamlit run app.py
```

## 使い方

### 1. アプリケーション起動
上記のインストール方法に従ってStreamlitアプリを起動します。

### 2. 設定の入力
1. **ターゲットOSを選択**: インストール先のOSを選択します
2. **ターゲットPythonバージョンを選択**: インストール先のPythonバージョンを選択します
3. **requirements.txtをアップロード**: インストールしたいパッケージ一覧が記載されたファイルを選択します

### 3. パッケージ収集の実行
「パッケージを収集してZIPを作成」ボタンをクリックします。

処理には以下の時間がかかることがあります:
- パッケージの数やサイズによる
- ネットワーク速度による
- 通常は数秒〜数分程度

### 4. ZIPファイルのダウンロード
処理が完了するとダウンロードボタンが表示されます。クリックしてZIPファイルを保存してください。

### 5. オフライン環境でのインストール

1. ZIPファイルをオフライン環境に転送し、解凍:
```bash
unzip package_xxx-xxx_pyxxx.zip -d offline_packages
```

2. 解凍したディレクトリからパッケージをインストール:
```bash
pip install --no-index --find-links=./offline_packages -r requirements.txt
```

### 対応OSとプラットフォームタグ
| 表示名 | プラットフォームタグ | 備考 |
|--------|-------------------|------|
| Windows (64bit) | win_amd64 | 64ビットWindows用 |
| Mac (Apple Silicon) | macosx_11_0_arm64 | Apple Silicon (M1/M2/M3) Mac用 |
| Mac (Intel) | macosx_10_15_x86_64 | Intel CPU Mac用 |
| Linux (x86_64) | manylinux2014_x86_64 | 64ビットLinux用 |

## 注意事項

- **バイナリ互換性**: 一部のパッケージは特定のOS/バージョン用のコンパイル済みバイナリ（wheel）を提供していない場合があります。その場合はエラーが発生します。
- **パッケージサイズ**: ダウンロードするパッケージの総サイズによっては、処理に時間がかかる場合があります。
- **ネットワーク環境**: 初回実行時はパッケージのダウンロードにインターネット接続が必要です。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

---

## 変更履歴（更新）
- Windows 向けに **uv** を廃止し、純粋な `pip download` コマンドを使用してパッケージ取得を行うよう改善しました。<br>
- `--only-binary=:all:` オプションを追加し、Windows でも `colorama` の wheel ファイルを含めてダウンロードできるようにしました。<br>
- エラーログは発生しないことを確認済み（Windows 用 ZIP が正常生成され、colorama wheel が含まれる）。

**開発者**: 鴨川浩二  
**報告先**: 問題や改善提案があれば、GitHub Issuesまでお願いします。
```