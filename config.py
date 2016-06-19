MOCO_GET_MESSAGES = "/servlet/api/chat/getMessages.do?roomId=$ID&limit=1&page=1"
MOCO_SEND_MESSAGE = "/servlet/api/chat/sendMessage.do"
# this I assume just takes the id
MOCO_LEAVE_ROOM = "/servlet/api/chat/leaveRoom.do"
MOCO_SET_COLOR = "/servlet/api/chat/setColor.do"  # set color
# takes the user's uid and a comment
MOCO_REPORT_USER = "/servlet/api/chat/reportChatUser.do"
MOCO_IGNORE_USER = "/servlet/api/chat/ignoreUser.do"  # takes the uid of the user
# takes uid of the ignored user
MOCO_UNIGNORE_USER = "/servlet/api/chat/unignoreUser.do"
MOCO_USERS_IN_ROOM="/servlet/api/chat/getUsersInChatRoom.do?roomId=$ID&fields=[%22name%22,%20%22firstName%22,%20%22uid%22]&limit=500&page=1"
MOCO_GET_USER_COUNT = "/servlet/api/chat/getUsersCountInRoom.do?roomId=$ID"
MOCO_LOGIN = "https://www.mocospace.com/html/login.jsp"
MOCO_HEADERS = {
    # this I got from wireshark, because I couldn't get the POST to work
    # correctely. This is basically your auth.
    "Cookie": "",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",  # need to spoof the agent

}
botowner="" # enter your user or name
