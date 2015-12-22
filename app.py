# project/__init__.py

from flask import Flask, request, jsonify, session, render_template
from flask.ext.mysql import MySQL
import time



# config

app = Flask(__name__)
mysql = MySQL()
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "apple"
app.config["MYSQL_DATABASE_DB"] = "vigu"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_POST"] = "3306"
mysql.init_app(app)


def getuserid(uname):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select userid from users where username = '"+uname+"'")
    row = cursor.fetchone()
    print row[0]
    return row[0]
# routes

@app.route("/")
def load():
    return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
	req = request.json
	_uname = req["username"]
	_pass = req["password"]
	status = False
	if _uname and _pass :
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ("select username from users where username = %s and password = %s")
		cursor.execute(query,(_uname,_pass))

		for(user_name) in cursor:
			if user_name :
				status = True
				return jsonify({"message":"Login Successfull","code":"200","result": status, "user": req})
		else :
			status = True
			return jsonify({"message":"User not registered or Invalid Username/Password","code":"201","result": status})


@app.route("/api/logout")
def logout():
    return jsonify({"result": "success"})

@app.route("/api/register", methods=["POST"])
def register():
	return jsonify({"message":"Username not available","code":"201","result": True})

@app.route("/api/blockreq/<uname>")
def post(uname):
	userid = getuserid(uname)
	print userid
	status = False
	result = {}
	visibility = 0
	output = {}
	if userid :
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ("Select p.postid, p.subject , p.content , p.datetime  from post p, userdetails u where p.author = u.userid and p.visibility = %s and u.blockid = (select blockid from userdetails where userid = %s) order by p.datetime desc")
		cursor.execute(query,(visibility,userid))
		posts= {}
		posts['items'] = [dict(postid=row[0], subject=row[1], content =row[2], datetime =row[3]) for row in cursor.fetchall()]
		v = posts.get('items')
		if v is None:
			posts['status'] = "Fail"
			posts['message'] = "Content not available"
		else:
			posts['status'] = "Success"
			posts['message'] = "Coontent available"
		conn.close()
		return jsonify(posts)



@app.route("/api/profile/<uname>")
def profile(uname):
	_username = uname
	status = False
	print _username
	conn = mysql.connect()
	cursor = conn.cursor()
	query = ("Select interest from userdetails where userid = (select userid from Users where username = %s)")
	cursor.execute(query,(_username))
	return jsonify({"message":"need to update","code":"201","result": True})

@app.route('/api/search/<uname>/<text>',methods=['GET'])
def search(uname,text):
	userid = getuserid(uname)
	conn = mysql.connect()
	cursor = conn.cursor()
	v_block = 0
	v_hood = 1
	v_all_f = 2
	v_pvt = 3
	v_neigh = 4
	search = '%'+text+'%'
	status = 1
	queryt = "Select p.postid, p.subject, p.content, p.datetime from post p, userdetails u, comments c where p.author = u.userid and c.postid = p.postid and p.visibility = %s and u.userid = %s and (p.subject like %s or p.content like %s or c.comment like %s )"+"union select p.postid, P.subject, p.content, p.datetime from userdetails u,post p, comments c where p.author= u.userid and c.postid = p.postid and p.visibility = %s and u.blockid in (select blockid from blocks where hoodid = (select b.hoodid from blocks b, userdetails u where b.blockid = u.blockid and u.userid = %s)) and ( p.subject like %s or p.content like %s or c.comment like %s )"+"union select p.postid, p.subject, p.content, p.datetime from post p, comments c where  p.visibility = %s and c.postid = p.postid and p.author in (Select userone from frndrequest where (usertwo = %s) and status = %s union  Select usertwo from frndrequest where (userone = %s) and status = %s ) and ( p.subject like %s or p.content like %s or c.comment like %s )"+"union select p.postid, p.subject, p.content, p.datetime from post p, comments c where p.author = %s and  c.postid = p.postid and p.visibility= %s and (p.subject like %s or p.content like %s or c.comment like %s)"
	query = (queryt)
	cursor.execute(query,(v_block,userid,search,search,search,v_hood,userid,search,search,search,v_all_f,userid,status,userid,status,search,search,search,userid,v_all_f,search,search,search))
	posts={}
	posts['items'] = [dict(postid=row[0], subject=row[1], content =row[2], datetime =row[3]) for row in cursor.fetchall()]
	v = posts.get('items')
	print v
	if v is None:
		posts['status'] = "Fail"
		posts['message'] = "Content not available"
	else:
		posts['status'] = "Success"
		posts['message'] = "Coontent available"
	conn.close()
	return jsonify(posts)

@app.route("/api/hoodreq/<uname>")
def hoodpost(uname):
	userid = getuserid(uname)
	print userid
	status = False
	result = {}
	visibility = 1
	output = {}
	if userid :
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ("Select p.postid, p.subject , p.content , p.datetime  from post p, userdetails u where p.author = u.userid and p.visibility = %s and u.blockid = (select blockid from userdetails where userid = %s) order by p.datetime desc")
		cursor.execute(query,(visibility,userid))
		posts= {}
		posts['items'] = [dict(postid=row[0], subject=row[1], content =row[2], datetime =row[3]) for row in cursor.fetchall()]
		v = posts.get('items')
		if bool(v):
			posts['status'] = "Success"
			posts['message'] = "Coontent available"
		else:
			posts['status'] = "Fail"
			posts['message'] = "Content not available"
		conn.close()
		return jsonify(posts)

@app.route("/api/neigbhorreq/<uname>")
def neigbhorpost(uname):
	userid = getuserid(uname)
	status = False
	result = {}
	visibility = 4
	output = {}
	if userid :
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ("select * from (Select p.postid, p.subject , p.content , p.datetime  from post p where p.author in (Select fromid from neighbours where toid = %s) and p.visibility = %s union select p.postid, p.subject , p.content , p.datetime from post p where p.author = %s and p.visibility = %s)a order By a.datetime desc")
		print query
		cursor.execute(query,(userid,visibility,userid,visibility))
		posts= {}
		posts['items'] = [dict(postid=row[0], subject=row[1], content =row[2], datetime =row[3]) for row in cursor.fetchall()]
		print posts
		v = posts.get('items')
		if bool(v):
			posts['status'] = "Success"
			posts['message'] = "Coontent available"
		else:
			posts['status'] = "Fail"
			posts['message'] = "Content not available"
		conn.close()
		return jsonify(posts)

@app.route("/api/friendreq/<uname>")
def allfriendpost(uname):
	userid = getuserid(uname)
	status = False
	result = {}
	visibility = 2
	status = 1
	output = {}
	if userid :
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ("select * from (Select p.postid, p.subject , p.content , p.datetime  from post p where p.author in (Select userone from frndrequest where (usertwo = %s) and status = %s union select usertwo from frndrequest where (userone = %s)and status = %s) and p.visibility = %s union select p.postid, p.subject , p.content , p.datetime from post p where p.author = %s and p.visibility = %s)a order By a.datetime desc")
		print query
		cursor.execute(query,(userid, status,userid, status, visibility,userid,visibility))
		posts= {}
		posts['items'] = [dict(postid=row[0], subject=row[1], content =row[2], datetime =row[3]) for row in cursor.fetchall()]
		print posts
		v = posts.get('items')
		if bool(v):
			posts['status'] = "Success"
			posts['message'] = "Coontent available"
		else:
			posts['status'] = "Fail"
			posts['message'] = "Content not available"
		conn.close()
		return jsonify(posts)

@app.route("/api/private/<uname>")
def pvtmsg(uname):
	userid = getuserid(uname)
	status = False
	visibility = 3
	if userid :
		conn = mysql.connect()
		cursor = conn.cursor()
		query = ("select * from (select p.postid,p.subject,p.content,p.datetime,concat (u.first_name,' ',u.last_name) from post p,privatemsg m,users u where p.postid = m.postid and m.userid = %s and p.author = u.userid  union select p.postid,p.subject,p.content,p.datetime,concat(u.first_name,' ',u.last_name) from post p, users u where p.author = %s  and p.visibility = %s and u.userid = %s)a order By a.datetime desc")
		cursor.execute(query,(userid,userid, visibility,userid))
		posts= {}
		posts['items'] = [dict(postid=row[0], subject=row[1], content =row[2], datetime =row[3], uname = row[4]) for row in cursor.fetchall()]
		print posts
		v = posts.get('items')
		if bool(v):
			posts['status'] = "Success"
			posts['message'] = "Coontent available"
		else:
			posts['status'] = "Fail"
			posts['message'] = "Content not available"
		conn.close()
		return jsonify(posts)

@app.route('/api/pvtmembers/<username>/<pid>/',methods=['GET'])
def getpvtmembers(pid,username):
    conn = mysql.connect()
    cursor = conn.cursor()
    posts = {}
    uid = getuserid(username)
    query = ("select userid , concat(first_name,' ',last_name) from users where userid in (select userid from privatemsg where postid = %s and userid != %s)")
    cursor.execute(query,(pid,uid))
    posts={}
    posts['items'] = [dict(userid=row[0], name=row[1] ) for row in cursor.fetchall()]
    v = posts.get('items')
    if bool(v):
        posts['status'] = "Success"
        posts['message'] = "Content available"
    else:
        posts['status'] = "Fail"
        posts['message'] = "Content not available"
    conn.close()
    return jsonify(posts)

@app.route('/api/comments/<pid>/',methods=['GET'])
def getcomments(pid):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select c.comment,c.datetime,c.author, concat(u.first_name,' ',u.last_name)  from comments c, users u where u.userid = c.author and c.postid = '"+pid+"'")
    posts={}
    posts['items'] = [dict(comment=row[0], datetime=row[1], author =row[2],username = row[3]) for row in cursor.fetchall()]
    cursor.execute("select p.subject, p.content, p.datetime, concat(u.first_name,' ',u.last_name) from post p, Users u where postid = '"+pid+"' and userid = author")
    posts['post'] = [dict(subject=row[0], content=row[1], datetime =row[2], uname =row[3]) for row in cursor.fetchall()]
    v = posts.get('items')
    if bool(v):
        posts['status'] = "Success"
        posts['message'] = "Content available"
    else:
        posts['status'] = "Fail"
        posts['message'] = "Content not available"
    conn.close()
    return jsonify(posts)


@app.route('/api/pending/<username>',methods = ['GET'])
def pending(username):
	conn = mysql.connect()
	cursor = conn.cursor()
	uid = getuserid(username)
	print uid
	posts ={}
	status = 0
	print "testsssss"
	query1 = ("select userid , concat (first_name,' ',last_name) from users where userid in (select userone  from frndrequest where usertwo = %s and status = %s and fromid != %s union select usertwo from FrndRequest where userone = %s and status = %s and fromid != %s) ") 
	cursor.execute(query1,(uid,status,uid,uid,status,uid))
	posts['pending'] = [dict(userid=row[0], name=row[1]) for row in cursor.fetchall()]
	query2 = ("select userid , concat (first_name,' ',last_name) from users where userid in (select userone  from frndrequest where usertwo = %s and status = %s and fromid = %s union select usertwo from FrndRequest where userone = %s and status = %s and fromid = %s)") 
	cursor.execute(query2,(uid,status,uid,uid,status,uid))
	posts['requested'] = [dict(userid=row[0], name=row[1]) for row in cursor.fetchall()]
	query3 = ("select userid,concat(first_name ,last_name) from users where userid NOT IN (select userone from frndrequest where usertwo = %s union select usertwo from frndrequest where userone = %s) and userid!= %s")
	cursor.execute(query3,(uid,uid,uid))
	posts['tobesent'] = [dict(userid=row[0], name=row[1]) for row in cursor.fetchall()]
	b = posts.get('tobesent')
	s = posts.get('pending') 
	v = posts.get('requested')
	if bool(s) or bool(v) or bool(b):
		posts['status'] = "Success"
		posts['message'] = "Content available"
	else:
		posts['status'] = "Fail"
		posts['message'] = "Content not available or no requests pending"
	conn.close()
	return jsonify(posts)

@app.route('/api/friendrequest/<user_id>/<frnd_id>',methods = ['POST'])
def frndrequest(user_id,frnd_id):
	print user_id
	print frnd_id
	print " received req"
	fromid = user_id
	toid = frnd_id
	conn = mysql.connect()
	cursor = conn.cursor()
	status = 0
	posts ={}
	t = time.strftime('%Y-%m-%d %H:%M:%S')
	print t
	query = ("Insert into FrndRequest (userone, usertwo, status, fromid) values (%s,%s,%s,%s)")
	print "query"
	if (fromid > toid):
		print "if"
		cursor.execute(query,(toid,fromid,status,fromid))
	else:
		print "else"
		cursor.execute(query,(fromid,toid,status,fromid))
	fid = cursor.lastrowid
	print fid
	if fid:
		print "success query"
		posts['status'] = "Success"
		posts['message'] = "Content available"
	else:
		print "failed query"
		posts['status'] = "Fail"
		posts['message'] = "Content not available"
	conn.close()
	return jsonify(posts)

@app.route('/api/fq/<id1>/<id2>',methods = ['POST'])
def frndreq(id1,id2):
	print "received req 123"
	print id1
	print "___"
	print id2
	return jsonify(result={"status": 350})

@app.route('/api/getapi/<username>',methods = ['GET'])
def getapi(username):
	print "get api"
	

@app.route('/api/oldfriends/<username>',methods = ['GET'])
def getnewfriends(username):
    conn = mysql.connect()
    cursor = conn.cursor()
    uid = getuserid(username)
    status = 1
    posts = {}
    query = ("select a.userone, concat(u.first_name, ' ',u.last_name) from(select userone from frndrequest where (usertwo = %s) and status = %s union \
    	select usertwo from frndrequest where (userone = %s) and status = %s )a,users u where u.userid = a.userone")
    cursor.execute(query,(uid,status,uid,status))
    posts['items'] = [dict(id= row[0],name=row[1]) for row in cursor.fetchall()]
    conn.close()
    return jsonify(posts)

@app.route('/api/viewprofile/<pid>/',methods=['GET'])
def vprofile(pid):
    conn = mysql.connect()
    cursor = conn.cursor()
    posts={}
    cursor.execute("select concat(u.first_name, ' ', u.last_name), ud.description, ud.interest, ud.dob from userdetails ud, users u where ud.userid = '"+pid+"' and u.userid = '"+pid+"'")
    posts['post'] = [dict(subject=row[0], content=row[1], datetime =row[2], uname =row[3]) for row in cursor.fetchall()]
    v = posts.get('post')
    if bool(v):
        posts['status'] = "Success"
        posts['message'] = "Content available"
    else:
        posts['status'] = "Fail"
        posts['message'] = "Content not available"
    conn.close()
    return jsonify(posts)


if __name__ == "__main__":
   app.run()