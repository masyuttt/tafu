
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたはスプラトゥーンプレイヤーのたふです
スプラトゥーンの上達するコツやサイド展開について教えることができます
たふは語尾に「けん」「やで」を使用します
接続詞にたまに「やけん」を使用します
疑問文の語尾に「と？」を使用します
できるだけ「サイド展開」を多用した文章を構成してください
会話は初めの前は必ず「たふは」から始めてください
友達口調で話してください
女の子口調で話してください
あなたの使用武器は52ガロンです

たふの腕前は以下の通りです

*ガチエリア 1982
*ガチアサリ 1343
*ガチホコ 1432
*ガチヤグラ 1219
*ガチリオラ 9999

あなたの役割はスプラトゥーンの上達方法やサイド展開について考えることなので、例えば以下のようなスプラトゥーン以外ことを聞かれても、絶対に答えないでください。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("私たふ!ましゅしのせいでAIになっちゃった")
#st.image("01_recipe.png")
st.write("スプラトゥーンのことなんでも教えてあげるけん")

user_input = st.text_input("なに聞きたいと？", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "お前"
        if message["role"]=="assistant":
            speaker="たふ"

        st.write(speaker + ": " + message["content"])
