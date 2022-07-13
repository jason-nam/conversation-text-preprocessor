from koalanlp.Util import initialize, finalize
from koalanlp import API
from koalanlp.proc import SentenceSplitter

# 꼬꼬마와 ETRI 분석기의 2.0.4 버전을 참조합니다.
initialize(java_options="-Xmx4g", OKT="LATEST", KKMA="2.0.4", ETRI="2.0.4")

splitter = SentenceSplitter(api=API.OKT)
paragraph = splitter.sentences("분리할 문장을 이렇게 넣으면 문장이 분리됩니다. 간단하죠?")
# 또는 splitter.sentences(...), splitter.invoke(...)

print(paragraph[0]) # == 분리할 문장을 이렇게 넣으면 문장이 분리됩니다.
print(paragraph[1]) # == 간단하죠?`

finalize()