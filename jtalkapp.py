import streamlit as st
import glob, os, tempfile, subprocess

import datetime

param_info = [
    ("α",      0.0,  1.0, 0.5, 0.01, "-a",  "オールパス値、位相だけをバラつかせることで音が自然になる"),
    ("β",     0.0,  1.0, 0.0, 0.01, "-b",  "ポストフィルタ値、統計モデルによる平滑化による音質劣化を緩和する" ),
    ("速度",    0.0,  2.0, 1.0, 0.01, "-r",  "話す速さ"),
    ("ﾊｰﾌﾄｰﾝ", -10.0, 10.0, 0.0, 0.1,  "-fm", "追加ハーフトーン"),
    ("境界",   0.0,  1.0, 0.5, 0.01, "-u",  "有声/無声境界値"),
    ("GV0",   0.0,  5.0, 1.0, 0.01, "-jm", "スペクトラム系列内変動の重み、統計モデルによる平滑化で失われる特徴量を考慮した音声合成をする時の重み"),
    ("GV1",  0.0,  5.0, 1.0, 0.01, "-jf", "F0(基本周波数）系列内変動の重み、F0に対して特徴量を考慮して音声合成する時の重み"),
    ("音量", 0.0, 20.0, 1.0, 0.1,  "-g",  "音量"),
]

param=[0] * 8

voice_info = [
    ("mei","mei/mei_normal.htsvoice")
]

OPENJTALK = "open_jtalk"
DIC_DIR = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
VOICE_DIR = "/usr/share/hts-voice/"
OUTPUT_DIR = "/tmp/"

def run_command(args):
    """Run command, transfer stdout/stderr back into Streamlit and manage error"""
    st.info(f"Running '{' '.join(args)}'")
    result = subprocess.run(args, capture_output=True, text=True)
    try:
        result.check_returncode()
        st.info(result.stdout)
    except subprocess.CalledProcessError as e:
        st.error(result.stderr)
        raise e


st.title('openJtalk Web FrontEnd')
st.write("音声モデル：mei_normal(モデル変更機能実装予定）")
st.write("音声モデルライセンス（奥付等に確実に記載ください）：CC-CY 3.0 Copyright 2009- Nagoya Institute of Technology (MMDAgent Accessory “NIT Menu”)")
for i, p in enumerate(param_info):
    param[i] = st.slider(p[0], min_value=p[1], max_value=p[2], value=p[3], step=p[4], format="%f",help=p[6])

text = st.text_area("入力テキスト", value='', max_chars=None, key=None,  help=None)


if st.button('音声ファイル生成'):
    pass
    #st.write('param 1 is ' + str(param_info[1][3]))
    dt_now = datetime.datetime.now()
    index = 0
    filename = dt_now.strftime('%Y%m%d%H%M%S_') + '{:03d}'.format(index) + ".wav"
    path = os.path.join(OUTPUT_DIR,filename)

    while os.path.exists(path):
        index = index + 1
        filename = dt_now.strftime('%Y%m%d%H%M%S_') + '{:03d}'.format(index) + ".wav"
        path = os.path.join(OUTPUT_DIR,filename)

    st.write("output file name is " + filename)

    cmd = [OPENJTALK,
       "-x", DIC_DIR,
       "-m", os.path.join(VOICE_DIR, voice_info[0][1]),
       "-ow", os.path.join(OUTPUT_DIR,filename)]

#    st.write(cmd)
    for i,p in enumerate(param_info):
        cmd.append(p[5])
        cmd.append(str(param[i]))

    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(text.encode())
    c.stdin.close()
    c.wait()

    st.audio(path, format='audio/wav', start_time=0)


else:
    pass

