# Server
# requsets 라는 라이브러를 활용
# get을 활용해 sever에 요청하는 client 역할


# Python의 Server는
# Flast VS Django
# Django = 보안 정책, 풀 패키지로 구성된 프레임워크
# Flask: 마이크로 웹 프레임워크(굉장히 간단, 기본기능 x)
# Flask를 활용, 나만의 커스텀 웹 서버 구축
# html 문서 로드
# 단, template 폴더에만 있는 html만 바라볼 수 있다.
from flask import Flask
from flask import request, redirect, make_response
from flask import render_template 
from werkzeug.utils import secure_filename
from aws import detect_labels_local_file as label
from aws import compare_faces 
app = Flask(__name__)
# 서버 주소/로 들어오면 
# return의 내용을 html로 전달
@app.route("/")
def index():
    return render_template("home.html")
@app.route("/compare",methods = ["POST"])
def compare():
    try:
        if request.method == "POST":
            f1 = request.files["file1"]
            f2 = request.files["file2"]
            f1_name = secure_filename(f1.filename)
            f2_name = secure_filename(f2.filename)
            f1.save("static/" + f1_name)
            f2.save("static/" + f2_name)
            result = compare_faces("static/"+f1_name, "static/"+f2_name)
            return result
    except:
        return "비교 불가"
    return "얼굴 비교 페이지"
@app.route("/detect", methods = ["POST"])
def detect():
    try:
        if request.method == "POST":
            f = request.files["file"]
            filename = secure_filename(f.filename)
            # 외부에서 온 이미지, 파일등을
            # 마음댈 저장 불가능
            # 서버에 클라이언트가 보낸 이미지 저장
            # 저장 경로를 라벨로 던지기.
            f.save("static/"+filename)
            r = label("static/"+filename)
            return r

    except: 
        return "감지 실패"


   
@app.route("/mbti", methods= ["POST"])
def mbti():
        try:
            if request.method == "POST":
                mbti = request.form["mbti"]
                return f"당신의 MBTI는 {mbti}입니다."

        except:
            return "데이터 수신 실패"
@app.route("/login", methods=["GET"])
def login():
    try:
        if request.method == "GET":
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]
            # return f"{login_id}님 환영합니다."
            if (login_id == "aaa") and (login_pw == "1234"):
                response = make_response(redirect("/login/success"))
                response.set_cookie("user",login_id)    
                return response
            else:
                return redirect("/")
    except:
        return "잘못된 접근입니다."
@app.route("/login/success")
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다."

    
if __name__ == "__main__":
    # 1. host
    # 2. port 
    app.run(host="0.0.0.0")