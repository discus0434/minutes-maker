# Minutes Maker

<h1 align="center">
  <img src="../assets/sample.gif" width=100%>
</h1>

**Minutes Makerは、会議や講義の逐次書き起こしと要約を自動生成するウェブアプリです。**

## Overview

主な機能:

- [faster-whisper](https://github.com/guillaumekln/faster-whisper)を使用して、**ほぼ全ての音声/ビデオファイルを書き起こす**
- [OpenAI LLMs](https://openai.com/blog/openai-api/)を使用して**トランスクリプトを要約**
- **使いやすいウェブインターフェース**
- **英語と日本語**に対応
- **CPUとGPUの両方**に対応

## Installation

#### 1. 環境変数を`.env`ファイルに設定します

以下の環境変数を設定する必要があります。

- `OPENAI_API_KEY`は要約のためのAPIキーで、[こちら](https://platform.openai.com/account/api-keys)で見つけることができます。

- `REACT_APP_PUBLIC_IP`は、アプリケーションを実行するマシンの公開IPアドレスです。
  - アプリをローカルマシンでデプロイする場合は、`'0.0.0.0'`になります。
  - アプリをリモートサーバーでデプロイする場合は、サーバーの公開IPアドレスになります。

以下のコマンドを実行することで、環境変数を`.env`ファイルに設定できます：

```bash
cd minutes-maker
echo "OPENAI_API_KEY='sk-XXX'" >> .env
echo "REACT_APP_PUBLIC_IP='XXX.XXX.XXX.XXX'" >> .env
```

#### 2. Dockerイメージをビルドする

マシンがNVIDIA GPUを持っているかどうかは自動的に検出され、適切なDockerイメージがビルドされます。

```bash
make build
```

#### 3. アプリケーションを実行する

```bash
make up
```

#### 4. アプリケーションにアクセスする

ブラウザで`http://<PUBLIC_IP or 0.0.0.0>:10356`を開きます。

## Usage

<p align="center">
  <img src="../assets/sample.png" width=50%>
</p>

_フォームに入力してSubmitボタンをクリックするだけです！_

**フォームの簡単な説明は以下の通りです:**

1. 音声/ビデオファイルのアップロード

    書き起こしと要約を行いたい音声/ビデオファイルを選択します。ほぼ全ての音声/ビデオファイルが使用でき、ファイルサイズに制限はありません。

2. `target language`の選択

    _どの言語で要約したいか_の言語を選択します。
    現在、英語と日本語がサポートされています。

3. カテゴリーの選択

    音声/ビデオファイルのカテゴリー、`meeting`または`lecture`を選択します。このパラメータを適切に設定すると、要約の品質が向上します。

4. `meeting`/`lecture`内容の入力

    `meeting`や`lecture`の内容、例えばテーマ（例："新製品の開発"）を入力します。
    内容を適切に設定すると、書き起こしの品質が向上します。

## Requirements

x86-64アーキテクチャのコンピュータ
Docker

## License

このリポジトリはCC BY-NC-SA 4.0ライセンスの下でライセンスされています。詳細は[LICENSE](./LICENSE)をご覧ください。
