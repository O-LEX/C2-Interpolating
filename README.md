Cem YukselのA Class of C2 Interpolating Splinesの追実装です。
C2 Interpolating CurvesとはC2連続な曲線を表しており、任意の点列を繋ぐ滑らかな曲線を生成します。
この論文の素晴らしいところは自然な曲線を生成することができるだけでなく、点列に対し新しい点を追加した際に全体を再構成する必要がなく、最も新しい曲線のみを変更することでC2連続な曲線を生成できることです。また実装もシンプルです。


https://github.com/user-attachments/assets/d5e0613d-10fb-4c6f-bb66-b852d0051c47



https://github.com/user-attachments/assets/133bab40-40b6-4965-8123-e98ae4d38575


# 実装について
bezierとC2 interpolatingを実装しています。  
main関数のmodeという引数を変更することで切り替えることができます。  
初期はC2になっています。  
pygame, modengl, numpyのインストールが必要です。  

# C2 interpolatingについて
b_i,1を求めることはできているっぽい  
線の混ぜ合わせが正しいのかわからない  
bezierにおいて0<t<1であるが、必要なのは0<theta<piであるような曲線であり、そのように変数変換する方法が与えられていないように思う。今回はF_iはtから1を線形変換、F_i+1は0からtを線形変換することで与えた。これで良いのかはわからない。

# 引用及びGPT等
次のyoutube動画を参考にしています  
Let's code 3D Engine in Python. OpenGL Pygame Tutorial  
参考:A Class of C2 Interpolating Splines
copilotを利用しています  
