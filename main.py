
class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password
        self.friends = []
        self.posts = []
        self.messages = []

    def create_post(self, content: str):
        post = Post(self, content)
        self.posts.append(post)
        return post

    def add_friend(self, friend_username):
        self.friends.append(friend_username)
        return (f"{friend_username} was added to your friend list {self.friends}")

    def send_message(self, message, to_user):
        to_user.messages.append(message)
        return f"Message was successfully send"

    def like_post(self, post: 'Post'):
        post.like(self)

    def comment_on_post(self, post: 'Post', content: str):
        post.add_comment(self, content)


class Post:
    pass



