# cg
bezierとC2 interpolatingを実装しています。  
main関数のmodeという引数を変更することで切り替えることができます。  
初期はC2になっています。  
pygame, modengl, numpyのインストールが必要です。  

pythonでopenglを書くにあたって次のyoutube動画を参考にしています  
Let's code 3D Engine in Python. OpenGL Pygame Tutorial

# C2 interpolatingについて
b_i,1を求めることはできているっぽい  
線の混ぜ合わせが正しいのかわからない  
bezierにおいて0<t<1であるが、必要なのは0<theta<piであるような曲線であり、そのように変数変換する方法が与えられていないように思う。今回はF_iはtから1を線形変換、F_i+1は0からtを線形変換することで与えた。これで良いのかわからない。
