# Nconnect
A Social Networking platform for neighborhoods. 
It primarily enables people to connect to with others living in their neighborhoods and blocks they belong to. People will have access to posts and comments from neighborhoods and blocks. 

They can add friends and open private chat threads with any member regardless of their neighborhood. People can post local events, newsletters and even alerts during emergencies. 

Designed RESTful API’s using flask micro framework. Developed this website as a SPA(single page application) using AngularJS.

Requirements
=======
* Angularjs
* Flask
* passlib
* Werkzeug

API Documentation
=======
1) Request to change block
```bash
/api/blockchange/ 
```

2) List of pending block request
```bash
/api/pendingbrequest/<username>/
```

2) List of neighborhood
```bash
/api/listofneighbors/<username>/
```

3) Add a new neighbors
```bash
/api/addednb/<username>/
```

4) Display profile
```bash
/api/displayprofile/<username>/
```

5) Accept block request
```bash
/api/acceptbrequest/<username>/<brid>
```

6) Block request
```bash
/api/blockreq/<uname> 
```

7) Neighbor request
```bash
/api/neigbhorreq/<uname>
```

8) Hood request
```bash
/api/hoodreq/<uname>
```

9) Friend request
```bash
/api/friendreq/<uname>
```

10) To send personal message
```bash
/api/private/<uname>
```

11) List of personal messages
```bash
/api/pvtmembers/<username>/<pid>/
```

12) View User profile
```bash
/api/profile/<uname> 
```

13) Keyword Search
```bash
/api/search/<uname>/<text> 
```

14) List of Friends
```bash
/api/oldfriends/<username>
```

15) Friend request status 
```bash
/api/pending/<username>
```

16) Send friend request
```bash
/api/friendrequest/
```

17) Post on Wall
```bash
/api/post/ 
```

18) Get Comments
```bash
/api/comments/<pid>/
```

19) Update Address
```bash
/api/registeraddress/
```

20) Register
```bash
/api/register/
```

21) Approve Friend Request
```bash
/api/approvefriend/<username>/<toid>
```

22) Reject Friend Request
```bash
/api/rejectfriend/<username>/<toid>
```
